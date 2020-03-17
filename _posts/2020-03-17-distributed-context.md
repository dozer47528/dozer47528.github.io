---
title: Service Mesh 实践（八）：分布式上下文
author: Dozer
layout: post
permalink: /2020/03/distributed-context.html
categories:
  - 系统架构
tags:
  - Kubernetes
  - Service Mesh
---

### 什么是分布式上下文

产品经理突然来了个需求，希望在一些事件打点的地方记录一下用户的各种信息：IP，User Agent，Accept Language 等。

但数据打点是分散在各个地方的，而且需求变化非常快，我们怎么样才可以随时随地拿到这些信息呢？

一种笨办法就是在所有函数调用的地方把相关信息一层层往下传，但你应该没见过这样的代码，实在是太麻烦了。

另外一种方式就是直接从一个静态方法里拿到当前的 Request 对象，并从中拿到各种信息。例如 C# 中是这样的：`HttpContext.Current.Request`，Python Flask 中是这样的：`from flask import request`。如果进去看看源码的话就会发现一般它们都是通过 Thread Local 来实现的。大部分的 HTTP Server 都是一个 Request 只由一个线程处理，所以这么做没什么问题。

而 Golang 的并发模型不一样，所以 Golang 无法这么做，Golang 需要显示地传播 Context。同样，用 Netty 做 HTTP Server 的话，并发模型也是完全不一样的，同样无法直接使用 Thread Local，只能显示传播 Context。还有基于 RxJava 实现的也无法这么做。 

上下文本质上是一种隐式传播的信息，简化工作量。上面提到的这些都是程序内部的上下文，如果把这个隐式的信息传播扩展到微服务之间，那么它就变成分布式上下文了。

<!--more-->

&nbsp;

### RPC 框架中的分布式上下文

大部分 RPC 框架都会自动传播上下文，用户也可以手动添加一下信息，让它自动传播。

例如 Dubbo 中就有这样的功能：[隐式参数](http://dubbo.apache.org/zh-cn/docs/user/demos/attachment.html)

A 在调用 B 之前调用这个方法：`RpcContext.getContext().setAttachment("user-agent", userAgent);`。

接下来 B 在调用 C，C 在调用 D，每一个下游服务都可以得到这个信息。

但是，我们主要使用的是 gRPC 和 HTTP，它们的协议中并没有设计这块，所以必须要手动处理了。

这也是为什么基于 gRPC 或 HTTP 的微服务要做分布式追踪也只能手动处理，因为分布式追踪能串起来的关键就是要透传类似 Request ID 这样的标记，代表你们是一条链路上的。

&nbsp;

### OpenTracing 中的 Baggage

从底层原理上来看，分布式上下文和分布式追踪有一个共同点，它们都要透传一些信息，这部分代码完全是可以公用的。

这也是为什么 OpenTracing 标准中规范了 Baggage 这个特性：[https://github.com/opentracing/specification/blob/master/specification.md#set-a-baggage-item](https://github.com/opentracing/specification/blob/master/specification.md#set-a-baggage-item)

如果你已经使用了任何符合 OpenTracing 标准的分布式追踪框架，你可以直接读取或者写入各种信息，它会自动帮你透传。

```java
tracer.activeSpan().setBaggageItem("user-agent", userAgent);
```

它的底层也非常简单，例如你远程调用的是 HTTP，那么它会在你调用任何 HTTP 请求的时候注入一个 HTTP Header：`Baggage-User-Agent: userAgent`

下游服务收到请求后，自动提取所有`Baggage-`开头的 HTTP Header 并放到内存中。

&nbsp;

### 倔强的 Elastic APM

之前的文章提到过，我们把分布式追踪的框架改成了 Elastic APM：[Service Mesh 实践（二）：Istio Mixer 模块的性能问题与替代方案](/2020/02/replace-istio-mixer.html)

Elastic APM 并不仅仅做了一个分布式追踪，所以它并没有遵循 OpenTracing 标准。

Elastic APM 应该是 OpenTracing 一个超集，它其实实现了一个 OpenTracing Bridge，想要迁移到 Elastic APM 可以直接把底层的框架替换掉，然后基于 OpenTracing 标准写代码。这并不是 Elastic APM 推荐的长期实现方案，因为这样会缺少部分功能。

除此以外，我们发现这么做以后，OpenTracing 中的 Baggage 功能竟然失效了，看了源码才知道，Elastic APM 直接留了个空函数。

经过询问后，我们才得知它们不想基于 OpenTracing 的标准做这个，以后要实现的话，也会基于 W3C 的标准做。

- [Any plan for support opentracing baggage?](https://discuss.elastic.co/t/any-plan-for-support-opentracing-baggage/182672)
- [Propagation format for distributed trace context: Trace Context headers](https://w3c.github.io/correlation-context/)

毕竟是半个竞争对手，不用对方的标准也可以理解。然而 W3C 的标准还在草案阶段，所以 Elastic APM 暂时并没有实现这个功能。

&nbsp;

### 自研

既然底层的原理都知道，也有两份开源作业摆在我们面前了，Elastic APM 暂时又不想实现，那么只能自己自研了。

其实这块不难，主要就是如何在微服务之间传播，如何在程序内部传播，还有两者的衔接。相关技术细节都可以参考 Elastic APM 和 Jaeger，因为他们也做了类似的事情。

&nbsp;

#### 微服务之间传播

这块参考 OpenTracing 标准和 W3C 草案，他们本质上没有太大的区别，只是 HTTP Header 用的不同而已。

因为我们已经有部分项目在用 OpenTracing 的 Baggage 功能了，所以为了少做改动，我们自研设计的协议也是同样的格式。

最终格式类似这样：

- `Baggage-User-Agent: Mozilla/5.0`
- `Baggage-User-Id: d7af84f8-877c-414d-b008-e9d60a16ac61`
- `Baggage-User-Role: leader`

&nbsp;

#### 内外衔接

作为一个 HTTP Server，怎么拿到这些 Header 并且透传呢？

```go
http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
	userId := request.Header.Get("Baggage-User-Id")

	req, _ := http.NewRequest("GET", "http://127.0.0.1:8888", nil)
	req.Header.Add("Baggage-User-Id", userId)
	resp, _ := http.DefaultClient.Do(req)
})
http.ListenAndServe(":8080", nil)
```

不借助任何中间件的话，直接手写就行了，把上游的 Header 读出来，然后传播到下游。这里的代码只是一个演示，实际还要根据前缀匹配把所有`Baggage-`开头的都透传。

这样的代码很明显不能让人接受。但幸运的是，大部分语言的大部分框架都可以很方便地实现自动透传。

面向对象的语言自己实现一下对应的接口，然后包装一下即可。然后 Python 这样的动态语言直接替换对应的方法就行。

用户用的时候，需要在程序中注册一下，例如 Golang 中 HTTP Server 和 HTTP Client 需要这样注册：

```go
import cphttp "github.com/AminoApps/context-propagation-go/module/context-propagation-http"

http.ListenAndServe(":8080", cphttp.Wrap(myHandler))
client := cphttp.WrapClient(&http.Client{})
```

&nbsp;

#### 程序内部传播

再看上面手写代码的例子：

```go
http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
	userId := request.Header.Get("Baggage-User-Id")

	req, _ := http.NewRequest("GET", "http://127.0.0.1:8888", nil)
	req.Header.Add("Baggage-User-Id", userId)
	resp, _ := http.DefaultClient.Do(req)
})
http.ListenAndServe(":8080", nil)
```

从上游拿到`userId`后，如果马上就要调用下游服务，那么不用特殊的处理。

但是如果调用下游调用别的 HTTP 服务的代码很深，你需要一个个手动往下传播吗？这其实就是最上面提到的问题，不同的语言用不同的处理方式。

Golang 的传播过程就是这样的：

1. HTTP Server 从 Header 中提取 Baggage
2. 存入 Context，后续调用传播 Context
3. 调用下游 HTTP 服务的时候从 Context 中提取出 Baggage
4. 将 Baggage 写入 Header

Java，Python 略有不同，主要区别就是不是通过 Context 传播了，直接放 Thread Local 就行了。

&nbsp;

#### 开源项目

其中，Golang 和 Python 版本我们已经开源。

Golang 版实现地最全面，支持了各种协议和框架：

[Context Propagation Go](https://github.com/AminoApps/context-propagation-go)

- Gin
- Standard Http Server
- Standard Http Client
- gRPC Server
- gRPC Client

&nbsp;

Python 我们内部用的不多，对常用的做了一下支持：

[Context Propagation Python](https://github.com/AminoApps/context-propagation-python)

- flask
- requests

&nbsp;

Java 为什么不支持？

传统的 Java 代码支持起来不难，利用 Thread Local 就行了。但微服务中的 Java HTTP Server 如果使用传统的并发模型，会很吃力。

Java 本身也在做相关转型，Spring Webflux，Vert.x 或者是别的基于 Netty 的框架，并发模型变了以后同一个请求就不一定在同一个线程上处理了。

而它们各自都有一套类似 Context 的解决方案。

所以 Java 想要做的话，需要支持的东西太多了，暂时并没有一个合适的标准。

而且我们内部 Java 不多，以后也不推荐用 Java，所以这项工作就暂缓执行了。

&nbsp;

### 安全性

我们之前把用户认证放到了 API Gateway 中，可以看看这篇文章：

[Service Mesh 实践（四）：从开源 Ingress 到自研 API Gateway](/2020/02/api-gateway.html)

那么下游服务怎么知道这个调用链是哪个用户产生的呢？

这里就需要用到分布式上下文了：

1. API Gateway 对 Session 信息解码
2. API Gateway 将 解码后的 User Id 通过 Baggage 透传
3. 下游业务通过 Baggage 得到 User Id

有了上述中间件以后，只要调用链上的服务都整合了中间件，下游服务可以非常轻松地拿到 User Id 了。

那这里就有两个问题了，如果用户熟悉我们内部系统的一些协议，直接通过外网传播 Baggage 进来怎么办？

内部服务有人作恶，想办法伪造了 Baggage 怎么办？

&nbsp;

#### 防范公网请求

对外防范是非常重要的，不能有一点漏洞。否则会对内部系统造成很大的影响。例如一个用户通过伪造 Baggage，完全可以模拟成另外一个用户。

然而这块的解决方案也非常简单。

对于分布式上下文来说，这本身就是一个内部系统之间的协议，也就是说所有外部请求过来的流量都不应该带有相关协议。

所以我们在 API Gateway 这一层直接抛弃所有的分布式上下文相关信息就行了。这样用户也就无法从公网伪造任何数据了。

&nbsp;

#### 防范内网请求

对内而言，其实如果真要防范是防不慎防的，内部员工有一万种方式攻破你的系统。目前我们服务间调用都没有相关认证，所以这里伪造 Baggage 并不是一个太大的问题。

虽然没有去做，但也要想清楚以后如何去做。

如何验证这个 Baggage 真的是某个人生成的呢？

银行如何知道转账请求真的是你提交的呢？

还记得银行的 U 盾吗？

其实这里也可以用类似的数字签名的机制，API Gateway 不仅返回 Baggage，还要对 Baggage 内容利用私钥进行签名。

使用这个 Baggage 的服务为了认证这个 Baggage 是不是 API Gateway 生成的，那么就需要利用公钥去验证。

大致思路是这样的，但实际却还有很多问题，例如 API Gateway 如何把公钥安全地给别的服务？API Gateway 如何安全地存放私钥？别的服务也要生成 Baggage 并进行签名怎么办？

这里环环相扣，想要完美解决就需要很多东西，并不是一个很容易解决的问题。