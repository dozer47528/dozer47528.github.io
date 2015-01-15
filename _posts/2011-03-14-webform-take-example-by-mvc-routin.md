---
title: 那些 WebForm 可以从 MVC 借鉴的东西 —— Routing
author: Dozer
layout: post
permalink: /2011/03/webform-take-example-by-mvc-routin/
categories:
  - 编程技术
tags:
  - AspDotNet
  - MVC
  - WebForm
---

### 前言

最近 MVC 一直很火，我在做项目的时候也一直想用 MVC 做，但是考虑到传承问题（不是所有人都回去学 MVC 的），最后还是没有使用 MVC。

但是虽然不用 MVC，MVC 中很多好的思想还是可以借鉴的！

所以给大家介绍一些可以从 MVC 借鉴的东西。

&nbsp;

### Routing

Routing，MVC 中的路由功能，和 Url 重写类似，但是更高层一点~

&nbsp;

**Routing 的好处：**

1.  方便地进行 Url 重写
2.  方便地获取页面的真实地址（防止网站挂在应用程序下后的地址错误）

<!--more-->

### 在 WebForm 中使用 Routing 功能

1、引用 System.Web.Routing

2、在 Application_Start 中编写 Routing 规则

    void Application_Start(object sender, EventArgs e)
    {
        //注册 Routing ，实现 Url 重写
        Utility.RouteRegister.RegisterRoutes(RouteTable.Routes);
    }

    using System.Web.Routing;

    namespace Utility
    {
        public static class RouteRegister
        {
            public static void RegisterRoutes(RouteCollection routes)
            {
                //根目录
                routes.MapPageRoute(
                    "Root",
                    "",
                    "~/Views/Home_Index.aspx"
                    );

                //后台管理
                routes.MapPageRoute(
                    "Admin",
                    "Admin/{Controller}/{Action}/{Id}",
                    "~/Views/Admin/{Controller}_{Action}.aspx",
                    true,
                    new RouteValueDictionary(new { Controller = "Home", Action = "Index", Id = "" })
                    );

                //默认页面
                routes.MapPageRoute(
                    "Default",
                    "{Controller}/{Action}/{Id}",
                    "~/Views/{Controller}_{Action}.aspx",
                    true,
                    new RouteValueDictionary(new { Controller = "Home", Action = "Index", Id = "" })
                    );
            }
        }
    }

好了，就是这么简单！~

从上面的 Routing 规则可以看到，我全部映射到了 Views 文件夹中 的 aspx 文件中

打开浏览器看看吧~

[<img class="alignnone size-medium wp-image-249" title="routing" alt="routing" src="/uploads/2011/03/routing-300x105.png" width="300" height="105" />][1]

&nbsp;

&nbsp;

### 根据 Routing 设定生成 Url

MVC 中有了 Controller 和 Action 后生成链接非常方便，其实在 Asp.net 4.0 中也有这样的功能

`&lt;%: GetRouteUrl("Default", new {controller = "home" })%&gt;`

上述代码便可以生成指向 Home_Index 页面的链接

&nbsp;

为什么没有直接传入 Controller 和 Action 的名字便可以得到 Url 的函数？

因为 Controller 和 Action 是 MVC 中的概念，而 Routing 并不是 MVC 的一个部分，是脱离的。

如果想像 MVC 里那样，那就需要自己写几个函数了~

 [1]: /uploads/2011/03/routing.png
