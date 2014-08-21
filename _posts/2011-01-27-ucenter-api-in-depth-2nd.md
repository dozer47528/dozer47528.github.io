---
title: 深入研究 UCenter API 之 通讯原理
author: Dozer
layout: post
permalink: /2011/01/ucenter-api-in-depth-2nd/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - Asp.net
  - Discuz
  - Ucenter
---

> **目录：**
> 
> 1.  <a href="/2011/01/ucenter-api-in-depth-1st/" target="_blank"><strong>开篇</strong></a>
> 2.  <a href="/2011/01/ucenter-api-in-depth-2nd/" target="_blank"><strong>通讯原理：UCenter API 与子站之间的通讯原理和单点登陆原理</strong></a>
> 3.  <a href="/2011/01/ucenter-api-in-depth-3rd/" target="_blank"><strong>加密与解密：AuthCode详解 & AuthCode函数翻译过程中的注意点</strong></a>
> 4.  **<a href="/2011/02/ucenter-api-in-depth-4th/" target="_blank">网站搭建： 康盛旗下网站 & Asp.net 网站搭建</a>**
> 5.  **<a href="/2011/04/ucenter-api-in-depth-5th/" target="_blank">MVC 网站下的用法：在 MVC 下的使用方法</a>**
> 6.  **<a href="/2011/05/ucenter-api-for-net-on-codeplex/" target="_blank">下载地址：UCenter API For .Net 在 CodePlex 上发布啦！</a>**

&nbsp;

### <span id="UCenter">UCenter 通讯基本原理</span>

UCenter和各个子站的通讯，主要就是通过 POST 的方式调用而已，没有什么技术含量。

[<img class="alignnone size-full wp-image-193" title="ucenterapi" alt="" src="/uploads/2011/01/ucenterapi.png" width="211" height="247" />][1]

表单参数都是经过 **<a href="http://zh.wikipedia.org/zh-cn/Base64" target="_blank">Base64</a>** 算法，加一个通信密钥进行加密和解密的。

返回的数据是单个参数（例如：0或者1），也可能是xml序列化后的数据。

例如一个请求：code=e145fscn314BSKnwxBvqLaQe2yrHJAnKO1M%2B8C4cAKQAtRRQfEqTh8mg665UVJPyrJIrPhDNnEM

解密后：action=test&time=1295631663

返回：1

以上是一个测试是否通讯成功的请求，上面是表单参数，解密的明文如上，返回1代表通讯成功！

<!--more-->

而其中的难点就在于，Discuz 并没有公开所有的 API！而仅仅是提供了一个 php 版的函数库，帮你写好了这些通讯函数。

所以 php 的网站做起来很轻松，而别的网站就痛苦了。

这里的痛苦包括加密和解密函数、序列化和反序列化、还有期中各个参数的名称和格式…

怎么解决？只能翻阅 php 版本的源代码，把它的 API 一条条看过去，然后用自己需要用的语言重写一遍。

&nbsp;

&nbsp;

### <span id="UCenter-2">UCenter 多点登录的原理及过程</span>

通讯原理就这么点，很简单，子站想联系 UCenter，就调用一个地址，传递一些参数就行了，反之亦然。

最难的其实是多点登录的过程。

因为一般的请求，比如在子站请求登录，调用一下，然后返回数据，就完成了；而多点登录没那么简单。

理解原理后才能知道应该怎么用多点登录。

&nbsp;

**先看一下多点登录的过程吧：**

[<img class="alignnone size-full wp-image-130" title="login" alt="" src="/uploads/2011/01/login.png" width="360" height="315" />][2]

子站调用封装好的登录函数（参数：帐号、密码），返回登录信息（包括：uid、用户名、E-mail）

子站调用同步登录函数（参数：uid），返回一段 javascript 代码

在子站前端页面执行这段 javascript 代码

该代码通知其他子站，调用它们的同步登录函数

&nbsp;

**解惑：**

刚看完这个，我也很疑惑，为什么要这样？那我反问下，你想怎么样？

1、子站调用同步登录函数，UCenter 通知子站同步登录？

2、子站调用同步登录函数，得到别的子站的同步登录 API，直接调用？

&nbsp;

为什么上面两个不行？什么叫同步登录？

那就是：用户的电脑需要在每个子站下保存了 **<a href="http://www.google.com/search?q=asp.net+session" target="_blank">Session</a>**，或者在用户电脑上保存了该每个子站的 **<a href="http://www.google.com/search?q=cookie" target="_blank">Cookie</a>**

&nbsp;

**那前面两个方案：**

方案一：在 UCenter 服务器保存了 Cookie，所有子站服务器上的 Session 记录记录的是 UCenter 服务器的，而不是用户的

方案二：同理可得，Cookie 保存在了一台子站的服务器上，Session 记录的是那个子站服务器的

所以，一定要用户的电脑通知各子站才行，那怎么通知呢？通过 javascript

&nbsp;

**关键：**

所以，UCenter 在同步登录的过程中，最关键的就是需要把这个 API 返回的 javascript 代码在前端运行

可以这样写：

<pre class="brush:csharp">using DS.Web.UCenterAPI.UCClient;

var client = new UCClient();
var ucLoginReturn =  client.UC_User_Login("admin", "admin");
if(ucLoginReturn.Success)
{
    var js = client.UC_User_Synlogin(ucLoginReturn.User.Uid);
    Response.Write(js);
}</pre>

&nbsp;

这样就可以实现同步登录了，我们来看一下 UC\_User\_Synlogin 函数返回的 js 代码吧：

[<img class="alignnone size-full wp-image-132" title="login_js" alt="" src="/uploads/2011/01/login_js.png" width="545" height="341" />][3]

&nbsp;

&nbsp;

### <span id="AuthCode">AuthCode函数</span>

这个函数是什么？传说这是康盛公司对 php 发展做出的一个极大的贡献…

该函数可以实现可逆加密，在 php 中广为流传…

这个也是 整个 UCenter API 的重点，下一篇文章将会详解这个函数，和它在翻译成 C# 版时的注意点。

 [1]: /uploads/2011/01/ucenterapi.png
 [2]: /uploads/2011/01/login.png
 [3]: /uploads/2011/01/login_js.png
