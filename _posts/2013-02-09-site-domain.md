---
title: 建站指引 —— 域名
author: Dozer
layout: post
permalink: /2013/02/site-domain.html
categories:
  - 互联网
tags:
  - DNS
  - 域名
---

### 漫漫长路

自己的博客一步步走来其实并不容易，域名、空间、备案等等… 全部折腾完起码也要弄好几个月，还好这几个月主要是等待，不需要你弄什么。

建站第一步当然是买一个域名啦，所以本文会和大家聊聊买域名的各种事。

&nbsp;

### 域名在哪买？

域名购买原则：一定要到国外买，千万不要在国内买！（除了 .cn, .org.cn, .com.cn 等）

首先，一个域名往往归一个国家或一个组织所管理，而同一个域名可以在各个域名供应商那买到，但价格和服务有所不同。

国家域名比较特殊，例如中国的相关域名（.cn, .org.cn, .com.cn 等）就没有开放给国外的域名供应商。因为国家需要对这几个域名做点限制吧。例如前段时间就不允许个人购买 .cn 域名了。

另外，作为一个个人博主，强烈不建议使用 .cn 相关的域名。

相对于国内，无论是价格、服务、稳定性（这个可以解决）等各个方面来看，国外的明显高于国内。国外又好又便宜，干嘛不买国外的呢？

最后，国外貌似只有 <a href="http://www.godaddy.com/" target="_blank"><strong>GoDaddy</strong> </a>支持支付宝，而且它本身也基本上是老外的首先，所以没有道理不用它啦！

购买方式很简单，注册、登陆、选购、支付即可。

<!--more-->

&nbsp;

### 那种域名好？

.com ? .net ? .cc ?

各种域名，有的是为了给各种特殊行业制定的，有的是国家域名。但现在各种限制已经很弱了，所以你可以随意选购。

选择原则：优先选 .com, .net 这两个顶级域名，如果没有的话，就随你喜欢了。

例如 .me ，感觉很适合做博客， .cc 很短也很不错。

另外还可以是一种组合，例如 <a href="https://bu.mp/" target="_blank"><strong>Bump</strong> </a>的域名：bu.mp ，也非常漂亮！

不要 .cn ！！

&nbsp;

### 域名需要多少钱？

个人觉得，对于一个工作了的人来说，域名的钱都可以忽略不计了。

首先，每种域名的价格都不同，10刀到30刀左右，最贵也就人名币200/年啦，完全可以接受。另外第一年买肯定可以优惠，一般60-100就搞定了。

&nbsp;

### 买了域名可以做什么？

域名可以做什么？这还用问吗…

如果自己买了域名，还有个很酷的用处就是：自己独享的邮件域名！

例如我的邮箱可以使 dozer@dozer.cc，也可以是 admin@dozer.cc。整个 @dozer.cc 都是你的，你想怎么玩就怎么玩~

目前免费提供这项服务的有 QQ的域名邮箱（现在升级成企业邮箱），还有 Google Apps（很多公司用的就是这个）。

QQ邮箱可以把你的域名邮箱绑定到你的QQ邮箱上。

我一个QQ邮箱就绑定了好多个帐号…

[<img class="alignnone size-medium wp-image-1051" alt="qq" src="/uploads/2013/02/qq-300x179.png" width="300" height="179" />][1]

而 Google Apps 相当于帮你开了一个新的 Google 帐户，不能和你以前的 Google 帐户绑定。

&nbsp;

### 关于 NameServer

大家都知道域名的核心目的就靠 DNS 服务把人能识别的文本解析成 IP。你每次连接上互联网后，都会被分配到一个或者两个 DNS 服务器。他们会告诉你 dozer.cc 的 IP 是多少。

但是它们怎么知道的呢？它们会问上一级，如果上一级还是不知道呢？继续往上问。

最终会问到各个域名供应商的 NameServer 那里。

每个域名供应商一般都有自己的 NameServer ，你需要在域名供应商的网站上进行配置。告诉它 dozer.cc 需要解析到 IP xxx.xxx.xxx.xxx 上。

&nbsp;

国内的域名域名供应商的 NameServer 不仅功能少，服务差，不稳定！而且还有各种限制！想要更多功能？再付费吧！

相对而言，Godaddy 的 NameServer 的功能就强多了，基本没什么限制，大气！

另外 Godaddy 的 NameServer 解析速度在国外可是飞快的。对… 仅仅在国外！

就是因为 Godaddy 太有名，上面有太多的不和谐内容。所以 Godaddy 的 NameServer 非常不稳定。

那我已经买了 Godaddy 的怎么办？岂不是悲剧了？

&nbsp;

好吧，我真的不是在做广告，我真的是诚心推荐：<a href="https://www.dnspod.cn/" target="_blank"><strong>DNSPOD</strong></a>

你虽然在 Godaddy 买了域名，但你不一定要把域名交给它管理。你也可以告诉 Godaddy ，把这个域名交给 DNSPOD 管理吧！然后 Godaddy 就放手不管了，还会告诉全天下：dozer.cc 这个域名不归我管了，你们找 DNSPOD 去。

DNSPOD 是一个国内的免费 NameServer。个人用户免费且几乎没有任何功能性的限制，仅仅是解析速度慢了一点点而已，我们这种小博主也不用在乎这点速度了。

真的是非常厚道！它只赚大客户的钱。

这里具体的可以看我的另一篇文章：**<a title="利用 DNSPod 解决 Godaddy 域名在国内无法解析的问题" href="/2012/03/using-dnspod-solve-the-problem-of-godaddy-domain-can-not-resolving-in-china.html" target="_blank">利用 DNSPod 解决 Godaddy 域名在国内无法解析的问题</a>**

&nbsp;

还等什么？如果你想建站，那赶快买域名去吧~

 [1]: /uploads/2013/02/qq.png
