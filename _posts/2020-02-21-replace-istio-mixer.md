---
title: Service Mesh 实践（二）：Istio Mixer 模块的性能问题与替代方案
author: Dozer
layout: post
permalink: /2020/02/replace-istio-mixer.html
categories:
  - 系统架构
tags:
  - Istio
  - Prometheus
  - Grafana
  - Fluent Bit
  - Elastic APM
---

### 寄以厚望的 Mixer

[Istio Architecture](https://istio.io/docs/ops/deployment/architecture/)

Istio 的架构设计让人看着非常舒服，分工明确，扩展性强。

<img width="500" src="/uploads/2020/02/istio-arch.svg" alt="The overall architecture of an Istio-based application.">

特别是 Mixer 模块，包含`Telemetry`和`Policy Check`两个模块，数据平面的 Envoy 会把所有请求异步发送给 Mixer 用作遥测，也会定时检查对应规则判断是否可以调用目标服务。

数据平面会把所有的请求上报到 Mixer，如果想要扩展任何功能，只需要扩展 Mixer 就行了。Istio 也把这一层做成了 [CRDs](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)，只需要创建对应的 CRDs 就可以了，而不需要对数据平面做任何改动。

按照 Istio 的理念，遥测和规则检查是属于控制平面的，从解耦的角度看，这样的设计很棒。

<!--more-->

&nbsp;

### 残酷的现实

然而，随着 Istio 1.0 的发布，大家纷纷用上后都发现 Mixer 的性能影响很大。

第一个影响是 Mixer 会导致延迟变高，根据 Istio 官方的 [Benchmark](https://istio.io/docs/ops/deployment/performance-and-scalability/)，文中可以看到 P90 Lantency 在加了 Mixer 以后差了一个数量级。

官方 Benchmark 中有这么一句话：In upcoming Istio releases we are moving istio-policy and istio-telemetry functionality into the proxy as TelemetryV2.

最近，Istio 团队也意识到了这个问题，并已经开始重构。据说即将发布的 Istio 1.5 就会把 Mixer 整合进 Envoy 中。这样减少了额外的远程调用，可以减少延迟降低 CPU 消耗。

其实再去回看蚂蚁金服的 [SOFAMesh](https://www.sofastack.tech/projects/sofa-mesh/overview/) 就会发现，SOFAMesh 在很早就意识到了这个问题，并切着手进行了改造。直接把 Envoy 用自研的模块取代，并把 Mixer 整合进去了。整个改造思路和 Istio 未来的设计是一致的。

&nbsp;

### Mixer 到底有什么用

我们的解决方案非常简单，直接把 Mixer 模块禁用了。这肯定不是一个简单的决定，这肯定是根据我们现状决定的。

首先看看 Mixer 能给我们提供什么。

&nbsp;

#### Policy Check

以我们现在的公司规模，内部是不需要什么服务之间的访问权限控制的，因为内部的“漏洞”太多了，就算你把这里堵住了，真的想搞事的人有大把手段可以绕过这个限制。所以这个功能暂时对我们来说是没什么意义的。

我们很早就把`Policy Check`给禁用了。

如果每个 Istio 版本更新你都看了的话，你会发现很早以前 Istio 是默认开启`Policy Check`的，而当前版本，默认就禁用了`Policy Check`。

可见这个功能对大部分人来说是不需要的。

禁用掉`Policy Check`后，P90 和 P95 好了很多，因为之前它需要定期去检查各种规则。

&nbsp;

#### Telemetry

Istio 里的`Telemetry`主要有这些：

- [Jaeger](https://www.jaegertracing.io/) 或 [Zipkin](https://zipkin.io/) 负责分布式追踪
- Prometheus + Grafana 负责监控和告警
- Access Log 会被统一搜集到 Mixer

先说说分布式追踪，分布式追踪不侵入代码是不可能的。如果你不改任何代码直接在 Istio 里启用分布式追踪，它会有`A -> B`的调用，也会有`B -> C`的调用，但是没有`A -> B -> C`，也就是说不能把它们串起来。

为什么串不起来呢？因为作为 Sidecar 是不侵入代码的，只能观测到所有进出的流量。而对于 Sidecar 来说它观测到的进出请求同时会有很多，如果没有什么特殊的标记，它并不知道它们之间的关系，因此也无法把整个调用链串起来了。

一般 RPC 都会有一个类似`RequestId`的东西，并且会在所有调用中透传，而 HTTP 或 gRPC 现在并没有相关的协议。所以你必须在自己的代码里手工或利用 SDK 来透传。

除此以外，你想做分布式追踪那么代码内部的一些细节你肯定也是想知道的。例如内部调用了几次数据库，分别耗时多少等。光看服务之间的 RPC 调用，颗粒度还是太粗了。

对于分布式追踪来说，侵入代码是必须的，SDK 能帮你尽量少动代码，但无法避免引入对应的 SDK。像 Java 很简单，引一些依赖配合 Spring 就自动处理了，而 Golang 都是需要自己手动改代码的。

所以 Sidecar 模式对分布式追踪来说基本没什么帮助，最后还是要靠自己。

再说 Prometheus + Grafana 来做监控和告警。

Prometheus 本身技术方案是完全不影响业务代码性能的，业务代码把数据放自己内存里暴露一个接口，Prometheus 主动去抓取。一般频率也就一分钟一次，所以对业务是无影响的。然后 Istio 搜集各种指标的时候是先发送给 Mixer 然后再由 Mixer 上报到 Prometheus。

另外 Istio 的 Prometheus 也无法统计自定义的指标，所以整个集群建 Prometheus 是必须的。Istio 的 Prometheus 并没有太大的优势。

最后看 Access Log，首先我觉得在正常情况下内部服务之间的 Access Log 是没必要完全搜集的。微服务化后，服务之间的调用相当于以前代码间的调用。以前你会把所有方法调用的日志记录下来吗？真的没有必要。除非是在做问题排查的时候，应该按需启用。

早期版本的 Istio 默认会启用 Sidecar 的 Access Log 并且全部上报给了 Mixer，对整体性能影响非常大。我们通过配置禁用了。但近期的几个版本 Istio 默认也不搜集 Access Log 了。

另外如果你真的有搜集 Access Log 的需求，完全可以用 Fluent Bit 做成`DaemonSet`直接到宿主机上搜集日志。直接读取日志文件，对业务也完全没有影响。

&nbsp;

### 改造方案

最后，我们的方案就是去掉 Mixer 模块，自己搭建 Jaeger、Prometheus、Grafana 还有 Fluent Bit。

每个模块都以自己性能最佳的方式去得到自己的数据，而不是像 Mixer 一样，先把数据全部汇总，然后再用适配器模式适配成各种需要的数据。

&nbsp;

### Elastic APM

后来，我们又发现了一个好用的东西，那就是 [Elastic APM](https://www.elastic.co/cn/apm)，从名字上可以看出，它的功能高于 Jaeger，不仅仅做了分布式追踪，还做了以前 Istio 内置 Prometheus + Grafana 做的指标功能。

界面和易用性上也完全不是一个水平的。

![Elastic APM UI](/uploads/2020/02/elastic-apm.png)

当然它也不是完美无缺的，我们也对它稍微进行了一些小改动，它本身的功能迭代也非常快，是很好的 Jeager 替代者。

另外，Elastic APM 不遵行 [Opentracing](https://opentracing.io/) 标准，Jeager 遵行 Opentracing 标准，Opentracing 标准里包含一个支持分布式上下文的功能。这个对微服务化来说很重要，之前说过这个功能一般是 RPC 来支持的，但是我们用的是 HTTP 和 gRPC。

关于这个问题，后面还会有详细的介绍，详细介绍了我们的解决方案。

&nbsp;

### 未来

基于上面的分析，除了`Policy Check`以外，遥测相关的功能用 Sidecar 模式并不是一个很好的方案。这些功能对性能要求很高。

`Policy Check`放到 Sidecar 里还是很有用的，期待新版本的 Istio 能把 Mixer 整合到数据平面，大幅度改善这块的性能。

到时候等我们需要`Policy Check`，我们会考虑重新把 Mixer 启用。

其实在实践中我们也慢慢的发现，Sidecar 模式并不是一颗银弹。流量控制这块真的很好用，完全解耦，Sidecar 并不需要业务具体使用什么语言写的。但 Sidecar 模式并不能解决所有问题，很多时候还是应该用更合适的方案去解决问题。