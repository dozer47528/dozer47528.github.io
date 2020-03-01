---
title: Service Mesh 实践（三）：数据库中间件
author: Dozer
layout: post
permalink: /2020/02/database-middleware.html
categories:
  - 系统架构
tags:
  - 数据库
  - MySQL
  - Service Mesh
---

### 为什么要用数据库中间件

严格的来说，数据库中间件的选择和 Servic Mesh 无关，一般公司很早就应该上数据库中间件了。

数据库中间件一般有两个方案：SDK 模式或者 Proxy 模式。SDK 模式性能更好，Proxy 模式兼容性更好。

既然我们都在往 Service Mesh 方向走了，就是不想在业务代码去接 SDK 了，所以 Proxy 模式是我们优先选择的方案。虽然延迟会高一点，但还是那句话，不要只盯着单次调用的延时。

那数据库中间件到底解决了哪些问题？一般来说，利用数据库中间件可以实现如下功能：

1. 读写分离
2. 分库分表
3. 故障转移
4. 动态配置
5. 统计分析
6. SQL 防火墙
7. 查询缓存

之前在大众点评做 [Zebra](https://github.com/Meituan-Dianping/Zebra) 的时候，主要的技术方案就是 SDK 模式，因为整个大众点评是 Java 技术栈，没有多语言的问题，所以用 SDK 模式可以尽量提高性能。

<!--more-->

&nbsp;

### 从 MySQL 到 Aurora

上面说了，数据库中间件在做 Service Mesh 之前就有这个需求了，但我们之前并没有做这块。原因就是 [Amazon Aurora](https://aws.amazon.com/rds/aurora/) 太好用了。

以前在大众点评花了大量的时间做故障转移，但是 Aurora 直接全部帮你搞定了。

Aurora 是 AWS 基于 MySQL 魔改出来的，这篇文章可以一窥 Aurora 的架构设计：[Amazon Aurora 是如何设计原生云关系型数据库的？](https://www.infoq.cn/article/kW4a9VbywO_XLiTizzB1)

而读写分离和分库分表，我们因为只有一个单体程序，所以都是通过手写来实现的。并不是自动读写分离，自动分库分表。

&nbsp;

### 新的挑战

虽然 Aurora 帮我们解决了故障转移这个最棘手的问题，但是别的还是要自己来做。微服务化后，很多轻量级的服务出现，它们只需要基本的读写分离功能，并不希望为了这个再去整合什么 SDK；另外我们涉及到的开发语言也不少。

能否用 Proxy 模式来解决这个问题？Proxy 模式的数据库中间件也是一个非常常见的技术方案。另外这两个方案也并不冲突，完全可以根据不同的业务类型来使用不同的技术方案。

而我们现在是快速迭代试错的阶段，所以找到一个满足我们需求的 Proxy 是第一位的。

&nbsp;

### MyCAT 与 ShardingSphere

因为之前是 Java 技术栈，那么自然先找到了两个 Java 开发的两大中间件了。

MyCAT 成名早，ShardingSphere 是后起之秀，知乎上有一篇两者的对比文章特别有意思：[mycat和sharding-jdbc哪个比较好？各有什么优缺点？
](https://www.zhihu.com/question/64709787)

说真的，的确受不了 MyCAT 的土味气息。而 ShardingSphere 就靠谱多了，首先是在京东有大规模实践，代码完全开源并归属于开源社区，开源运作方式也很标准。

最最重要的就是知乎上提到的，ShardingSphere 的官网和文档好太多了。

然而使用 ShardingSphere 的过程也没那么顺利。一开始就遇到了两个问题，我也给官方提了 issue。

[The result of `getBytes` is wrong.](https://github.com/apache/incubator-shardingsphere/issues/1533)

[Does sharding-proxy support hint?](https://github.com/apache/incubator-shardingsphere/issues/1506)

例如第一个问题，因为 JDBC 规范也挺熟悉了，所以尝试自己去修复一下，但看到他们代码内的`Binary`相关的 MySQL 字段都是处理错误的，心凉了半截。讲真代码还是有点乱的，他们`Binary`这块的逻辑并没有理得很清楚。

当时他们刚开源不久，也还没有加入 Apache 基金会，虽然现在上面两个问题都已经解决，但基于当时的情况，还是不敢用的。另外 Java 在容器化下的慢启动和高内存问题也是我不太敢用 Java 中间件的原因。

&nbsp;

### ProxySQL

后来继续搜寻相关中间件的时候偶然发现了 [ProxySQL](https://www.proxysql.com/)，于是决定尝试一下。

它可以解决上面提到了所有数据库中间件需要解决的问题。

然而，万万没想到，刚开始试用就遇上了 Bug：[ProxySQL hangs after run `set names 'binary'`](https://github.com/sysown/proxysql/issues/1860)

如果不设置这个，MySQL 会认为`'a' = 'ä'`，因为我们是面向全球用户的 APP，很多用户的用户名会用这些字符，这个参数是否设置对结果影响很大，可以看 MySQL 的官方文档：

- [The binary Collation Compared to _bin Collations](https://dev.mysql.com/doc/refman/5.7/en/charset-binary-collations.html)
- [The Binary Character Set](https://dev.mysql.com/doc/refman/5.7/en/charset-binary-set.html)

我给作者提了 Issue，作者响应也非常快，一天内就给我反馈了。他问了我一些细节，也让我帮他抓包看看。

最后大概一个月过后，他把这个 Bug 修复了，并发布了新版本。

而在他修复 Bug 期间，我们其实已经用起来了，因为当时迁移的业务不包含这样子的特殊文本比较，所以不会命中这个 Bug。

整体的使用过程中是非常可靠的，因为 ProxySQL 是 C++ 写的，而且作为 Proxy 主要功能也只是做一些转发，所以 CPU 和内存消耗非常小，启动也非常快。

&nbsp;

### ProxySQL 配置

我们目前通过 ProxySQL 实现了读写分离，强制主库 Hint 和非法 SQL 拦截。这里可以给配置作为参考：

```
mysql_servers =
(
    {
        address = "[change to your mysql master server]" # no default, required
        port = 3306                                      # no default, required
        hostgroup = 0                                    # no default, required
        status = "ONLINE"                                # default: ONLINE
        weight = 1                                       # default: 1
        compression = 0                                  # default: 0
    },
    {
        address = "[change to your mysql slave server]"  # no default, required
        port = 3306                                      # no default, required
        hostgroup = 1                                    # no default, required
        status = "ONLINE"                                # default: ONLINE
        weight = 1                                       # default: 1
        compression = 0                                  # default: 0
    }
)

#defines MySQL Query Rules
mysql_query_rules:
(
    {
        rule_id=0
        active=1
        match_pattern="^\s*UPDATE (?!.[\s\S]*(where))"
        destination_hostgroup=1
        apply=0
        flagOUT=403
    },
    {
        rule_id=1
        active=1
        match_pattern="^\s*DELETE (?!.[\s\S]*(where))"
        destination_hostgroup=1
        apply=0
        flagOUT=403
    },
    {
        rule_id=2
        active=1
        match_pattern="^\s*/\*master\*/"
        destination_hostgroup=0
        apply=1
    },
    {
        rule_id=3
        active=1
        match_pattern="^\s*SELECT [\s\S]* FOR UPDATE$"
        destination_hostgroup=0
        apply=1
    },
    {
        rule_id=4
        ctive=1
        match_pattern="^\s*SELECT"
        destination_hostgroup=1
        apply=1
    },
    {
        rule_id=1001
        active=1
        apply=1
        flagIN=403
        error_msg="Query not allowed"
    }
)
```

前面两条规则是禁止使用没有`WHERE`的`UPDATE`和`DELETE`，这个是血泪史，有同事在线上出过事。还好当时那张表太大，没有执行完就赶紧终止掉了。不然就真是的从删库到跑路了。

第三条是支持强制走写库，因为 ProxySQL 实现了自动读写分离，业务不需要整合任何框架。但是有时候业务就是需要`SELECT`语句强制走写库，那么这时候只要在 SQL 语句前面加上注释就行了。

用法：`/*master*/SELECT * FROM users LIMIT 1`。

第四条支持`SELECT * FROM user FOR UPDATE`强制走写库。这条 SQL 语句是在同一个事务中为了后续更新数据，读取数据并加锁的操作。

第五条规则就是默认所有`SELECT`走从库了。

最后一个是一个通用行为，第一条和第二条规则会跳转到这里。

&nbsp;

### ProxySQL 基准测试与性能调优

如果把它作为长久的方案，那跑一下符合我们环境的基准测试还是必须的。需要了解一下在有 Proxy 和没 Proxy 下的性能区别，各个版本 ProxySQL 的性能区别，还有不同负载下的性能区别。

这里我也做了个基于 Sysbench 的工具可以方便地做 ProxySQL 基准测试，对不同版本，不同参数的对比很有参考意义。

[https://github.com/dozer47528/proxysql-benchmark](https://github.com/dozer47528/proxysql-benchmark)

&nbsp;

#### 极限压力测试

首先测试一下不限制 Sysbench 的 rate，用尽全力去压测。

- MySQL: CPU 2, Memory 4Gi, Max Connection 2048
- ProxySQL: CPU 1, Memory 256Mi, Max Connection 2048
- Sysbench: CPU 1, Memory 1Gi

| Threads | MySQL Min | ProxySQL Min | MySQL Avg | ProxySQL Avg | MySQL Max  | ProxySQL Max | MySQL P95 | ProxySQL P95 |
|---------|-----------|--------------|-----------|--------------|------------|--------------|-----------|--------------|
| 10      | 1.38 ms   | 5.65 ms      | 8.40 ms   | 8.63 ms      | 72.90 ms   | 215.26 ms    | 38.94 ms  | 13.22 ms     |
| 50      | 1.39 ms   | 5.60 ms      | 42.66 ms  | 44.50 ms     | 280.67 ms  | 224.27 ms    | 92.42 ms  | 82.96 ms     |
| 100     | 1.47 ms   | 5.54 ms      | 87.65 ms  | 87.22 ms     | 605.22 ms  | 504.15 ms    | 189.93 ms | 155.80 ms    |
| 500     | 4.32 ms   | 13.20 ms     | 569.17 ms | 436.58 ms    | 2751.15 ms | 3829.34 ms   | 893.56 ms | 831.46 ms    |

![Full](/uploads/2020/02/mysql-proxysql-full.png)

从结果可以看出来并发量增加后最后的瓶颈都是 MySQL 了，并且随着并发量的增加，ProxySQL 的性能损耗基本是常数级别的，Avg 这一栏在并发数是 10,50 的时候都是慢 2ms 左右。

因为 ProxySQL 不会做额外的计算，所以不会因为 MySQL 压力大而影响自身性能。

但这个种把 MySQL 往死里压的场景其实很少，只有 MySQL 故障的时候才会出现。

&nbsp;

#### 限制 Sysbench rate

平日里，MySQL 一般都不会是满负载运行，一般来说连接会很多，但大部分连接都不会一直在请求。所以我在这里尝试把 Sysbench 每秒请求速率控制一下，保证不把 MySQL 压垮。

- MySQL: CPU 2, Memory 4Gi, Max Connection 2048
- ProxySQL: CPU 1, Memory 256Mi, Max Connection 2048
- Sysbench: CPU 1, Memory 1Gi, Rate 256/s

| Threads | MySQL Min | ProxySQL Min | MySQL Avg | ProxySQL Avg | MySQL Max | ProxySQL Max | MySQL P95 | ProxySQL P95 |
|---------|-----------|--------------|-----------|--------------|-----------|--------------|-----------|--------------|
| 10      | 3.24 ms   | 4.37 ms      | 3.82 ms   | 4.95 ms      | 33.06 ms  | 15.21 ms     | 4.33 ms   | 5.37 ms      |
| 50      | 3.23 ms   | 4.52 ms      | 3.84 ms   | 5.10 ms      | 12.34 ms  | 14.20 ms     | 4.33 ms   | 5.57 ms      |
| 100     | 3.24 ms   | 4.55 ms      | 3.82 ms   | 5.21 ms      | 11.91 ms  | 13.97 ms     | 4.41 ms   | 5.77 ms      |
| 500     | 3.25 ms   | 5.04 ms      | 3.87 ms   | 6.05 ms      | 12.26 ms  | 17.71 ms     | 4.49 ms   | 6.91 ms      |
| 1000    | 3.23 ms   | 5.73 ms      | 3.84 ms   | 7.56 ms      | 14.47 ms  | 17.80 ms     | 4.41 ms   | 8.90 ms      |
| 2000    | 3.21 ms   | 7.99 ms      | 3.84 ms   | 11.15 ms     | 48.86 ms  | 45.65 ms     | 4.41 ms   | 17.63 ms     |

![Rate](/uploads/2020/02/mysql-proxysql-rate.png)

在这样的压力下，MySQL 非常稳，而 ProxySQL 的性能却随着连接数的增加而变差了。ProxySQL 默认 4 个线程，Sysbench 并发高的话 4 个线程可能会过小，尝试修改这个参数。

&nbsp;

### 提升 ProxySQL 线程数

- MySQL: CPU 2, Memory 4Gi, Max Connection 2048
- ProxySQL: CPU 1, Memory 256Mi, Max Connection 2048, Threads 8
- Sysbench: CPU 1, Memory 1Gi, Rate 256/s

| Sysbench Threads | ProxySQL Threads | Min     | Avg      | Max      | P95      |
|------------------|------------------|---------|----------|----------|----------|
| 1000             | 4                | 5.73 ms | 7.56 ms  | 17.80 ms | 8.90 ms  |
| 1000             | 8                | 4.97 ms | 6.01 ms  | 50.00 ms | 6.91 ms  |
| 2000             | 4                | 7.99 ms | 11.15 ms | 45.65 ms | 17.63 ms |
| 2000             | 8                | 5.68 ms | 7.54 ms  | 58.87 ms | 9.91 ms  |

这里就出现了一个很有意思的现象了，除了 Max 外比的都降低了。

如果它并发做得好，在线程数大于 CPU 数的前提下，线程数越少越好。

官方的一个 Issue 也很好地解释了应该如何配置线程数：[How can i find the correct number of mysql-threads](https://github.com/sysown/proxysql/issues/1166)

但为什么我配置的 CPU `limits` 是 1，加大了线程数却有效果呢？因为 Kubernetes `limits` 里配置的 1 不是给你一个核，而是指相当于 1 个核的 CPU 时间。

这篇文章讲解的很好：[Kubernetes Container Resource Requirements — Part 2: CPU](https://medium.com/expedia-group-tech/kubernetes-container-resource-requirements-part-2-cpu-83ca227a18b1)

我的电脑是 8 核的 CPU，所以配置成 8 个线程后整体延迟下降了。但是，虽然 8 个核都可以用到，但都是残血的。所以有些线程跑到一半资源又被别的线程抢过去了，导致 Max 增加。

所以在容器化下跑这些东西还是要压测一下才能比较靠谱。

因为我们目前只是轻量级使用 ProxySQL，所以暂时还没做更深入的性能优化。

后面还要继续调优的话，可以看看官方文档，还有这里有些博客，也有很多介绍：[MySQL-中间件：ProxySQL]https://www.junmajinlong.com/mysql/index/#3-2-MySQL-%E4%B8%AD%E9%97%B4%E4%BB%B6%EF%BC%9AProxySQL

&nbsp;

### 后续

后面我们要重度使用的话，不仅仅要做一下性能调优，还有很多工具需要做一下。

ProxySQL 本身把所有配置写入了自己内置的一个数据库中，启动的时候可以读一份配置，运行的时候也可以直接修改。后面数据库实例多了，做一些管理工具是必须的。

另外 ProxySQL 自身监控数据也已经非常多了，但还是需要做一些整合，例如配合 Prometheus 和 Grafana，把它们呈现出来。