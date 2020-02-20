---
title: Amino Service Mesh 实践（一）：从 kops 到 ESK
author: Dozer
layout: post
permalink: /2020/02/migrate-kops-to-eks.html
categories:
  - 系统架构
tags:
  - Kubernetes
  - EKS
---

### kops 问题出在哪？

如果仅从易用性这个角度看，kops 是完胜 EKS 的，下面有一个官方的演示视频。

[<img src="https://asciinema.org/a/97298.png" width="500" />](https://asciinema.org/a/97298)

所有的操作都可以在命令行里完成，包括建集群，改集群。

每次变更都需要如下几个步骤：

1. 编辑 yaml 配置。
2. `kops update cluster`，这一步相当于`dry run`，你可以检查即将产生的变更。
3. `kops update cluster --yes`，这一步才是把配置推到线上。
4. `kops rolling-update cluster`，这里也是`dry run`，上一步虽然把配置推送到线上了，但有些机器的配置需要重建机器。
5. `kops rolling-update cluster --yes`，最后它会按顺序一台台更新机器。

整个集群升级过程非常直观可控，再配合 Kubernetes 的`PodDisruptionBudget`，整个升级过程会变得非常安全。`PodDisruptionBudget`可以控制一个`Deployment`至少存活多少`Pod`，保证服务可用。否则如果一个`Deployment`的两个`Pod`凑巧在一台机器上，没有`PodDisruptionBudget`的话它就直接干掉了。

然而， kops 在 Master 节点的可靠性上出了点问题。

<!--more-->

&nbsp;

### kops 1.11 到 1.12

我们第一个遇到的问题是 kops 升级到 1.12 后的一个架构大改动。当时是 2019 年第二季度左右。

官方介绍：[https://github.com/kubernetes/kops/blob/master/docs/etcd3-migration.md](https://github.com/kubernetes/kops/blob/master/docs/etcd3-migration.md)

Kubernetes is moving from etcd2 to etcd3, which is an upgrade that involves Kubernetes API Server downtime. Technically there is no usable upgrade path from etcd2 to etcd3 that supports HA scenarios, but kops has enabled it using etcd-manager.

可怕，这个升级过程没有可用的高可用方案，必须要有宕机时间。而最可怕的事情就是，Master 节点在整个 Kubernetes 集群中是非常重要的。

首先无法调度就算了，升级期间无法起新的`Pod`也可以接受，一般也在低峰期升级。

我们网络插件是 [Calico](https://www.projectcalico.org/)，Master 节点上的 Kubernetes API Server 长时间宕机会直接导致 Calico 无法获取其他机器的信息从而导致机器之间的网络故障。

除此以外，CoreDNS 也依赖 Kubernetes API Server，长时间的宕机也会产生问题。

但这个升级又不得不进行，长痛不如短痛，趁集群内服务还不是太多的时候，得赶紧想个方案。

最后，因为集群内服务还不多，而且都是无状态的，我们直接新建了一个临时集群，把当时的十几个服务在新集群跑了起来。

然后把流量切到了临时集群后开始升级。

&nbsp;

### kops Kubernetes API Server 配置损坏

可惜升级集群也不是一帆风顺，虽然在测试环境已经演练过了，但是线上竟然一直卡着不动。

而我又做了个很傻的操作，我把 Master 节点重启了。然后就没有然后了…

现在回想起来真想抽自己一个大嘴巴。

不幸中的万幸，我按照 kops 迁移文档对 etcd 的磁盘做了镜像备份。但先要把原因找出来，登陆上 Master 节点查看各种日志，唯一有价值的就是提示 etcd 配置损坏的日志。但是为什么损坏？找了半天还是没找到。

后来发现了一个迁移进度的日志，发现里面并没有什么错误，迁移也没结束。再结合我的重启操作联想一下，猜测应该是迁移并未结束就被我重启了，所以导致配置损坏。

最后只能死马当作活马医了，停掉了 Master 节点，把 etcd 的磁盘从镜像中恢复，再重启 Master 节点。

这次我一直盯着迁移进度，直到它完成。整个迁移过程花了将近半个小时。

因为在测试环境这个过程只有几秒，线上几分钟不动，所以让我以为是卡住了。

但说到底，我直接重启的操作是万万不可取的，以后再遇到类似的问题，第一步一定是去找原因，找到了原因再去重启。否则后果很严重。另外还有一个教训，做这种大的运维操作，记得备份，小心驶得万年船。

&nbsp;

### Kubernetes API Server 高可用

我们用 kops 算是很早的了，当时 kops 并没有 Master 节点高可用方案。Master 是单节点那么意味着 Kubernetes API Server 也是单节点。虽然 Calico 和 CoreDNS 都是强依赖 Kubernetes API Server，但是短暂的宕机并不会有严重的问题。例如 Master 节点升级，几分钟不会有严重的影响。

但在 2019 年年中开始，我们集群会出现大量的 DNS 超时。当时的业务已经不少了，而且公司整个数据平台也是基于 Kubernetes 搭建的，所以整个集群 Kubernetes API Server 的压力是非常大的。

最后研究后发现是 Kubernetes API Server 负载过高，导致 CoreDNS 访问 Kubernetes API Server 超时重启。最后引发了 DNS 超时。整个排查过程也不难，DNS 超时那么肯定先去看 CoreDNS 日志，然后就发现了原因。

新版本的 kops 虽然提供了多 Master 的支持，但是却一直没有完善单节点到多节点的迁移教程。

当时教程是有的，但是却没有故障恢复这个部分。经历过上次的升级问题后，没有故障恢复就很慌，完全不敢操作。

官方在 2019 年 8 月才把故障恢复这部分文档补齐：[Added // restore // guide to single-to-multi-master.md](https://github.com/kubernetes/kops/commit/a27b0f4439a386887d680c79fbe2300ca7c1c9bb#diff-12ee8d2ec7d8967931a5d72ecc62dadf)

在我们等待 kops 官方补齐这部分文档的时候，AWS 中国区的技术专员和我们一起交流了一下我们在 AWS 中使用 Kubernetes 的一些问题。他们向我们推荐了 Amazon EKS，而它和 kops 最大的区别就是：EKS 的 Master 节点是全托管的。Node 节点和 kops 一样是自己管理的。而且 EKS 的一些功能和 AWS 整合地更紧密，虽然这些功能 AWS 都开源做成了标准化 Kubernetes 插件了，但使用便捷性上，亲生的 EKS 还是要更胜一筹。

其中 Master 节点全托管这点非常吸引我们，因为我们出过的问题和面临的问题全部是和 Master 节点相关的。而 AWS 可以保证 Master 节点的稳定可靠和无缝升级，那对我们的运维工作帮助非常大。

我们公司没有运维，没有 DBA。所有相关工作都是我们自己做的，实在是没精力去研究这些了。

&nbsp;

### 调研 EKS

EKS 那么好，那有什么问题吗？这个问题在和 AWS 技术专员交流的时候就问了，其中最大的一个问题就是 EKS 默认用的网络插件是 Amazon VPC CNI：[amazon-vpc-cni-k8s](https://github.com/aws/amazon-vpc-cni-k8s)。

它可以直接给`Pod`分配一个 VPC 内的 IP，就好像是 VPC 内的一台机器一样。这给业务调试带来了极大的便利。

另外从性能角度也在各方面领先 Calico：[Amazon VPC CNI vs Calico CNI vs Weave Net CNI on EKS](https://medium.com/@jwenz723/amazon-vpc-cni-vs-calico-cni-vs-weave-net-cni-on-eks-b0ad8102e849)

但是单台 EC2 IP 总是有限制，目前最多 30 多个，我们看了下我们适合的机器配置和`Pod`运行情况，一般单机也不会超过 30 个`Pod`，所以这个缺点对我们来说问题不大。

另外 EKS 的操作理念和 kops 有些不同。kops 是把线上资源和本地 yaml 配置做对比，然后生成对应的操作。

而 EKS 利用了 [Amazon Cloudformation](https://aws.amazon.com/cloudformation/)，用它来管理资源。

Cloudformation 最麻烦的一点就是，它的理念是一旦提交就不可变，所以 EKS 不能`rolling-update`一组机器。它只能新建一组机器再把老得那组机器销毁，这个过程略嫌麻烦，最后我们通过自己写了点脚本来解决，整体来说也不是什么大问题。

另外 EKS 升级真的是无缝的？这个肯定也要自己试一下，建一个老版本集群集群，压测一下，然后升级。

最后果然是无缝的，据说 EKS 内部 Master 节点魔改了一些东西，可以保证这块的高可用。

&nbsp;

### 迁移到 EKS

托管 Master 的诱惑实在太大，调研结束后我们就准备迁移了。

上次新建临时集群的时候，我们大部分服务都是无状态的，但这次，我们有状态的服务已经不少了。有些服务用了`PersistentVolumeClaim`，所以你得把它们磁盘里的数据迁移过去。

除此以外也并没有什么太大的难度，新集群建好后流量通过负载均衡器慢慢切过去就行了，最后线上整个迁移过程也就用了几天而已。

目前我们已经在 EKS 中运作大半年了，整体非常稳定，没有出现过任何相关的故障。也经历过一次 Kubernetes 版本升级，整个过程是无缝的。

&nbsp;

### AWS Fargate

最近 AWS 推出了 [Fargate](https://docs.aws.amazon.com/eks/latest/userguide/fargate.html)，可以理解为是全托管的 Kubernetes 集群。

但是目前限制非常多，例如`DaemonSet`，`StatefulSet`等特殊的`Pod`都是不支持或者是不提倡使用的。

目前我们这类有状态的应用还是挺多的，所以如果是单集群的话它明显不能满足我们的需求。未来等我们有了多集群方案，这种全托管的 Kubernetes 可以考虑搭配使用。
