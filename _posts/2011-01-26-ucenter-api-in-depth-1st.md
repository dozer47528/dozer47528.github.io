---
title: 深入研究 UCenter API 之 开篇
author: Dozer
layout: post
permalink: /2011/01/ucenter-api-in-depth-1st.html
categories:
  - 编程技术
tags:
  - AspDotNet
---
> **目录：**
> 
> 1.  <a href="/2011/01/ucenter-api-in-depth-1st.html" target="_blank"><strong>开篇</strong></a>
> 2.  <a href="/2011/01/ucenter-api-in-depth-2nd.html" target="_blank"><strong>通讯原理：UCenter API 与子站之间的通讯原理和单点登陆原理</strong></a>
> 3.  <a href="/2011/01/ucenter-api-in-depth-3rd.html" target="_blank"><strong>加密与解密：AuthCode详解 & AuthCode函数翻译过程中的注意点</strong></a>
> 4.  **<a href="/2011/02/ucenter-api-in-depth-4th.html" target="_blank">网站搭建： 康盛旗下网站 & Asp.net 网站搭建</a>**
> 5.  **<a href="/2011/04/ucenter-api-in-depth-5th.html" target="_blank">MVC 网站下的用法：在 MVC 下的使用方法</a>**
> 6.  **<a href="/2011/05/ucenter-api-for-net-on-codeplex.html" target="_blank">下载地址：UCenter API For .Net 在 CodePlex 上发布啦！</a>**

&nbsp;

**  
**

既然说是开篇，那就先说点别的吧~

&nbsp;

Discuz 的强大的大家有目共睹的，现在又被腾讯收购，不知道以后会不会发展地更强大！

Discuz 算是很开放的吧（对php程序员而言）

因为它的核心产品 UCenter（用户中心）对外的 API 很强大，可以很方便地实现例如同步登陆，短信息，等功能，而且还有一份非常详细的文档和源码！

<!--more-->

可惜，这份源码和文档只有 php 程序员能享用了，Asp.net 怎么办？

既然它的源码已经公开，那就一定能翻译成 Asp.net 版本！

&nbsp;

在有一段时间，我就研究过这个，后来发现了一个残缺的DLL（不知道怎么用，有BUG，并且并没有实现全部的 API）

反编译之（原作者再原文中说可以反编译，但找不到他了），后经过修改，BUG 是没了，基本功能也可以用了，所以写了一篇<a style="font-weight: bold;" href="http://www.cnblogs.com/dozer/archive/2010/09/21/ucenter-api_with_asp-net.html" target="_blank">文章</a>，并且还把这个应用到了**<a href="http://online.cumt.edu.cn" target="_blank">学生在线</a>**的网站上

[<img alt="ucenter" class="alignnone size-full wp-image-191" title="ucenter" src="/uploads/2011/01/ucenter.png" width="632" height="437" />][1]

&nbsp;

但是，它终究还是残缺的，所以决定在寒假继续深入研究，完成地重写一份，并提供完整的使用方法！

目前的进度：所有原理和过程全部清楚了，需要的只是时间~

期望得到大家的支持和关注！有需要这个的朋友也可以所示向我求助，一起探讨！

 [1]: /uploads/2011/01/ucenter.png
