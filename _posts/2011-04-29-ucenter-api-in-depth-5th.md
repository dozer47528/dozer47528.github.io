---
title: 深入研究 UCenter API 之 MVC 网站下的用法
author: Dozer
layout: post
permalink: /2011/04/ucenter-api-in-depth-5th.html
categories:
  - 编程技术
tags:
  - AspDotNet
  - Discuz
  - MVC
  - Ucenter
---
<div>
  <strong><br /> </strong>
</div>

> **目录：**
>
> 1.  <a href="/2011/01/ucenter-api-in-depth-1st.html" target="_blank"><strong>开篇</strong></a>
> 2.  <a href="/2011/01/ucenter-api-in-depth-2nd.html" target="_blank"><strong>通讯原理：UCenter API 与子站之间的通讯原理和单点登陆原理</strong></a>
> 3.  <a href="/2011/01/ucenter-api-in-depth-3rd.html" target="_blank"><strong>加密与解密：AuthCode详解 & AuthCode函数翻译过程中的注意点</strong></a>
> 4.  **<a href="/2011/02/ucenter-api-in-depth-4th.html" target="_blank">网站搭建： 康盛旗下网站 & Asp.net 网站搭建</a>**
> 5.  **<a href="/2011/04/ucenter-api-in-depth-5th.html" target="_blank">MVC 网站下的用法：在 MVC 下的使用方法</a>**
> 6.  **<a href="/2011/05/ucenter-api-for-net-on-codeplex.html" target="_blank">下载地址：UCenter API For .Net 在 CodePlex 上发布啦！</a>**

&nbsp;

### MVC 网站下的用法

前一段时间在 MVC 的网站中使用了自己的 UCenter API

但是出现了一个问题：

MVC 下可以建立静态文件，路由的时候如果存在静态文件则直接访问，包括 aspx, asxh 等文件。

像原来一样，建立了 uc.ashx 文件，但是在使用的时候却出现了一个问题：无法访问 Session

HttpContext 里的 Session 对象是 null

就算继承了 IRequiresSessionStat 接口后还是一样

<!--more-->

那如何解决呢？

本来想从底层想办法，但是发现 Controller 差异太大，所以放弃。

后来发现，其实有个很简单的方法，直接在 Controller 里新建该对象即可。

&nbsp;

    namespace MVC.Controllers
    {
        public class APIController : Controller
        {
            public ActionResult Uc()
            {
                new UcBase().ProcessRequest(System.Web.HttpContext.Current);
                return Content("");
            }

        }
    }
