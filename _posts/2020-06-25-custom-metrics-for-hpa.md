---
title: Service Mesh 实践（十）：HorizontalPodAutoscaler 支持自定义 Metrics
author: Dozer
layout: post
permalink: /2020/06/custom-metrics-for-hpa.html
categories:
  - 系统架构
tags:
  - Kubernetes
  - Service Mesh
---

### HorizontalPodAutoscaler + Cluster Autoscaler

Kubernetes 内置`HorizontalPodAutoscaler`可以很方便地根据 CPU 和内存做水平扩容缩容。

Kubernetes 在启动`Pod`和销毁`Pod`的时候对生命周期的控制也做的非常好，并不会对一个服务有太大的影响。只要把优雅启动和优雅关闭做好，并且把 Requests 和 Limits 配置到合适的数值，这一切会变得非常便捷。

另外再配合 Kubernetes Cluster Autoscaler，还可以实现整个集群机器的自动扩容缩容。

Cluster Autoscaler 可不是简单地根据机器剩余多少资源来判断是否要扩容缩容的。一般的机器自动扩容缩容都只是判断一下 CPU 用了多少，内存用了多少，如果剩余很多就尝试缩减机器。但 Cluster Autoscaler 的判断逻辑没这么简单，它还会和 Kubernetes 污点，污点容忍性，`Pod`亲和性，Node 亲和性相结合。例如你有一台机器有特殊的 Label，上面有一个`Pod`只能跑在有这个 Label 的机器上，占用的资源非常少。如果是别的程序，看到这台机器占用资源少，就直接把它干掉了，但实际上它不能去掉，因为上面的这个`Pod`只能在这台机器上跑。

<!--more-->

&nbsp;

### IO 密集型应用

本来一切都跑的很好，直到我们集群里出现了 IO 密集型的 Worker 程序。

业务场景很简单，这个 Worker 会不断消费队列里的消息，并调用别的服务来处理这些消息。

这种场景下`Pod`占用的 CPU 会很少，而且也不太稳定，所以根据 CPU 来做自动扩容缩容就很困难了。

我最根本的需求是希望用尽量少的 Pod，尽量让队列一直保持空的状态。所以`Pod`的数量应该是根据队列堆积任务的数量来决定。

&nbsp;

### Prometheus to Custom Metrics

Kubernetes 从 1.6 开始支持自定义指标：[https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-custom-metrics](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#support-for-custom-metrics)

在 Kubernetes 中 Prometheus 是常用的组件，那是否可以把 Prometheus 里的指标作为自动扩容缩容的依据呢？

有一个指标专门用来统计队列中还在等待的消息数，这个数字大了就扩容，数字小了就缩容。完美～

这种常见需求自己做一个不难，开源社区也有了现成的东西：[k8s-prometheus-adapter](https://github.com/DirectXMan12/k8s-prometheus-adapter)

&nbsp;

### 安装配置 k8s-prometheus-adapter

安装非常简单，利用`helm`一行命令就可以，但配置就比较麻烦了。原因在于配置太自由，所以你必须要想清楚自己的需求，然后用它特定的语法写转换规则。

第一种配置方法是按需配置，用到什么指标就写一条转换规则，优点是性能更好，不需要的配置就不会拉取。缺点当然就是不灵活，一旦有新的需求就要修改`k8s-prometheus-adapter`的配置。

第二种配置方法的优缺点就正好相反，直接把所有指标都配进来，所有指标随时可用。

对于第二种配置方法还有一个优化的点，就算你集群内本身就有 Prometheus，还是建议单独搭建一个。然后在 Prometheus 里把不需要的指标直接去掉，提高采样率，缩短数据存储时间（这个需求中的指标只要实时的就行）。

最后我们的配置如下：

```yaml
prometheus:
  url: http://prometheus-for-adapter-server.kube-system.svc
  port: 80

replicas: 2

resources:
  requests:
    cpu: 200m
    memory: 2Gi
  limits:
    cpu: 1
    memory: 2Gi

rules:
  default: false
  custom:
  - seriesQuery: '{job="kubernetes-pods",kubernetes_namespace!="",kubernetes_pod_name!=""}'
    resources:
      overrides:
        kubernetes_namespace:
          resource: "namespace"
        kubernetes_pod_name:
          resource: "pod"
    name:
      matches: "(.*)"
      as: "counter_${1}"
    metricsQuery: "sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)"
  - seriesQuery: '{job="kubernetes-nodes-cadvisor",container!="POD",namespace!="",pod!=""}'
    resources:
      overrides:
        namespace:
          resource: "namespace"
        pod:
          resource: "pod"
    name:
      matches: "(.*)"
      as: "counter_${1}"
    metricsQuery: "sum(rate(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)"
  - seriesQuery: '{job="kubernetes-pods",kubernetes_namespace!="",kubernetes_pod_name!=""}'
    resources:
      overrides:
        kubernetes_namespace:
          resource: "namespace"
        kubernetes_pod_name:
          resource: "pod"
    name:
      matches: "(.*)"
      as: "gauge_${1}"
    metricsQuery: "avg(avg_over_time(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)"
  - seriesQuery: '{job="kubernetes-nodes-cadvisor",container!="POD",namespace!="",pod!=""}'
    resources:
      overrides:
        namespace:
          resource: "namespace"
        pod:
          resource: "pod"
    name:
      matches: "(.*)"
      as: "gauge_${1}"
    metricsQuery: "avg(avg_over_time(<<.Series>>{<<.LabelMatchers>>}[2m])) by (<<.GroupBy>>)"
```

配置中核心的点有两个，首先它只会抓取`Pod`自己的指标，这部分都是开发自己暴露的。另外还抓取了 cadvisor 的指标。这里一般都会`Pod`相关的一些运行情况，除了 CPU 和内存外，还会有磁盘，网络等信息，更全面一点。

而像机器相关的指标，在这里其实都是无用的，所以这里不会抓取，Prometheus 里也不会抓取。

&nbsp;

### HorizontalPodAutoscaler 配置

`HorizontalPodAutoscaler`的配置就非常简单了：

```yaml
kind: HorizontalPodAutoscaler
apiVersion: autoscaling/v2beta1
metadata:
    name: example-hpa
    labels:
        app: example
spec:
    scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: example
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Pods
      pods:
        metricName: counter_queue_size
        targetAverageValue: 10
```

这里的配置非常清晰，一方面它依然支持根据 CPU 做扩容缩容，如果 CPU 使用率超过 90% 就扩容。

另一方面，它会根据 counter_queue_size 这个指标做扩容所容，Kubernetes 会保证这个数值保持在 10 附近。如果大了就扩容，如果小了就缩容。

&nbsp;

### 非线性指标带来的问题

本来以为这里配置完就万事大吉了，但实际并非如此。根据上面的配置，在实际运行中会出现问题。

首先，Kubernetes 在做扩容缩容的时候，认为这些指标都是线性的。例如目标 CPU 使用率是 80%，当前 CPU 使用率是 40%，`Pod`数量是 8 个，那么它会认为如果把`Pod`缩减为 4 个就可以应付了。

其次，当队列堆积的消息接近 0 的时候，对它进行采样出来的数字波动会非常大，特别是 QPS 大的系统中，这个数字往往会在 0，10 甚至 100 之间跳动，非常不稳定。就算用平均值抹平这个波动，最后也只能稍微改善一下。

那基于这两个特点会产生什么现象呢？目标队列堆积任务数是 10，当前`Pod`数字刚好够用，队列是接近空的状态，最后取到的指标数值是 5，Kubernetes 一看，这可不行啊，太浪费了，根据计算，只要一半的`Pod`就够了。于是立刻干掉了一半的 Pod。

这下可好，一半的`Pod`没了，任务立刻开始堆积了，10 个，100 个，甚至到了 1000。等到下一次运算的时候，Kubernetes 又慌了，这可不行啊，目标 10个，实际任务堆积 1000，那么要把当前`Pod`扩容 100 倍啊！

就这样，这个 Worker 的`Pod`数在最小`Pod`数和最大`Pod`数之间跳动。

这里的核心问题在哪？核心问题就在于队列堆积任务数这个指标在接近 0 的时候，和`Pod`数量不是线性关系。

&nbsp;

### 找一个更合适的指标

对于一个计算密集型的应用，用 CPU 占用来代表它忙不忙就非常合适。但是对于 IO 密集型的应用用这个指标就不行了。还有什么更合适的指标代表它忙不忙吗？QPS 是否可以？

判断所有`Pod`的 QPS，当业务平稳的时候，它们的 QPS 就可以代表它们忙不忙了。

例如给所有`Pod`分配 1 核的 CPU 资源，根据压测它们的最大队列处理能力是 100 每秒。

我们设定一个 QPS 的指标，取最大处理能力的 80%，也就是 80 每秒。

如果所有`Pod`的平均 QPS 大于 80 了，说明它们有点负荷了，需要再加点 Pod。

如果所有`Pod`的平均 QPS 小于 80 了，说明它们有点闲了，可以尝试去掉几个 Pod。

最终实验下来这个指标运行起来也非常稳定，业务稳定的时候`Pod`数也很稳定，队列也一直不存在堆积的现象。

&nbsp;

### 应对突发流量

这个指标看似完美了，但在另一种场景下又有问题了。

这个队列实际上是用来处理搜索引擎索引变更事件的，平时业务都是平稳的。但是每隔一段时间我们又会用脚本去刷全量数据。这就导致有时候这个队列会严重堆积。会堆积到几千几万。

而基于刚才的设计 QPS 指标，我们取目标 QPS 80，它实际最大处理能力是 100，当队列堆积的时候，Kubernetes 发现数值是 100，比目标 QPS 多了 25%，那么只要扩 25% 的`Pod`就够了。

然而，这里当 QPS 到达它最大处理能力后，它也不再是线性的了，无论任务再怎么堆积，这个数值永远不会增长。虽然它可以扩容，但每次只有扩 25%，要在好几轮后，才可以扩大到理想状态。

既然一个在忙的时候不准，一个在闲的时候不准，那是否可以把它们结合起来呢？

```yaml
kind: HorizontalPodAutoscaler
apiVersion: autoscaling/v2beta1
metadata:
    name: example-hpa
    labels:
        app: example
spec:
    scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: example
    minReplicas: 2
    maxReplicas: 10
    metrics:
    - type: Pods
      pods:
        metricName: counter_qps
        targetAverageValue: 80
    - type: Pods
      pods:
        metricName: counter_queue_size
        targetAverageValue: 1000
```

这是修改完后的`HorizontalPodAutoscaler`，同时`counter_queue_size`这个指标要设置地大一点。平时不堆积的时候，这个条件不会触发。而当遇到突发流量的时候，例如堆积到了 10000 个任务后，因为目标任务是 1000，相差十倍，Kubernetes 会立刻扩出 10 倍的`Pod`来应对这些任务。

而当队列处理完毕的时候，Kubernetes 又会根据所有`Pod`的实际 QPS，把它们缩减到合适的大小。

这样两种场景就都可以应对了。不经可以快速响应需求，`Pod`数也不再会反复跳跃了。