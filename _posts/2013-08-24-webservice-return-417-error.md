---
title: 调用 WebService 返回 417 错误
author: Dozer
layout: post
permalink: /2013/08/webservice-return-417-error/
posturl_add_url:
  - yes
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
categories:
  - 编程技术
tags:
  - Asp.net
  - IIS
  - IIS6
---

### <span id="i">错误现象</span>

现象很简单，调用某个 WebService 的时候返回了如下的错误信息：

<span style="color: #ff0000;">The request failed with HTTP status 417: Expectation failed.</span>

实在是搞不懂这个错误是什么原因啊！解决办法很简单，按照如下文章在 web.config 中加入一段配置即可。

注意，不是在服务提供方那边加（加了也没用），而是在服务调用方那边加上。

解决方法：<a href="http://www.codeproject.com/Articles/94235/The-request-failed-with-HTTP-status-417-Expectatio" target="_blank"><strong>http://www.codeproject.com/Articles/94235/The-request-failed-with-HTTP-status-417-Expectatio</strong></a>

<!--more-->

&nbsp;

### <span id="i-2">为什么会出错？</span>

看了上面的解决方案，总感觉这是一种兼容，而不是真正地解决问题。

既然是服务提供商无法识别，那为什么不能让服务提供商正确识别呢？

搜索了相关资料后才发现，这貌似是微软 IIS 的一个 bug。

<a href="http://support.microsoft.com/kb/898708" target="_blank">http://support.microsoft.com/kb/898708</a>

<a href="http://support.microsoft.com/kb/956594" target="_blank">http://support.microsoft.com/kb/956594</a>

你可以在你的服务器上下载相关补丁看看是否可以解决。

&nbsp;

### <span id="100_Continue_Status">100 (Continue) Status</span>

另外，这个问题中反复出现一个词：100 (Continue) Status

这是 HTTP1.1 中的一个标准：<a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3" target="_blank">http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3</a>

上面出错的原因就是因为调用方向服务提供者发送了一个特殊的请求，并在 headers 中加上了 100-continue 这个特殊的标记。

而服务商没有正确识别，最终导致了如上的错误，原因也说了，貌似是 IIS 的一个 bug。

&nbsp;

可是这个特殊请求和那个 header 到底有什么用呢？

看了下 w3c 的介绍，大致的作用是这样的：

1.  client 像服务端发送 post 请求的时候，先发送一部分（不包括 request body），一般就是发送了 headers，并且要在 headers 中加上 100-continue 标记
2.  server 端识别到了这是 100-continue 的请求，然后根据 heards 里的信息来判断是否有权限，如果没有的话返回 401 错误，如果有的话让 client 端继续发送 request body

这么做的好处也很明显了，就是可以在特殊场景下（没有权限）节约一点流量。

那上面的错误就是因为 server 端没能正确识别，它觉得，你明明是 post 请求，但是为什么没有 request body 呢？

&nbsp;

这时候反过来再看看，如果你不幸出现了这种情况，直接在 web.config 里加上配置是可以解决问题的。

而且也不会出现什么问题，如果你没有用 headers 里的参数进行权限验证的化，也不会有太大的性能影响。

&nbsp;

另外，一个猜测，这种特殊的请求只有当身份验证实在 IIS 中进行的时候才有效，而我们一般都是在网站中验证的。

一个 request 既然都已经到了网站了，那肯定是包含了完整的信息了。

所以得出的结论是，这个功能更加没用了，当然这只是一个猜测，有机会可以验证一下。
