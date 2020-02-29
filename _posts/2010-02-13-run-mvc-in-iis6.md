---
title: 在IIS6下运行MVC架构的网站
author: Dozer
layout: post
permalink: /2010/02/run-mvc-in-iis6.html
categories:
  - 编程技术
tags:
  - MVC
---

> 我为什么要写这个教程呢？
>
> 主要是为了解决把网站部署在虚拟主机上的人，因为你根本不能去配置虚拟主机 所以，用下面的方法，可以实现不配置IIS而使老版本IIS运行MVC。

首先，给大家推荐2个MVC的学习好去处：

1、重典MVC视频教程：<a href="http://www.youku.com/playlist_show/id_2416830.html" target="_blank"><strong>http://www.youku.com/playlist_show/id_2416830.html</strong></a>

2、微软官方MVC教程：<a href="http://www.asp.net/mvc/learn" target="_blank"><strong>http://www.asp.net/mvc/learn</strong></a>（英文，但是…我这样没过4级的都可以轻易看懂了…）

看本文的人必须要有MVC基础，所以很多名词我就不解释了

在老版本的IIS中架设MVC有1个条件：必须安装 Framwork 3.5，SP1不是必须的。所以如果你的虚拟主机是2.0的，那就免谈了。现在市面上一般都升级到3.5了

如果你不具备这个最简单的条件，那你的服务器也就根本不能使用MVC架构的网站了

好了，接下来介绍下我们要做的几个步骤

<!--more-->

### 1、复制几个缺失的运行库到bin文件夹

老版本不能运行主要原因当然是因为缺失dll文件啦，其中最重要的是mvc核心库

前三个在C:\Program Files\Microsoft ASP.NET\ASP.NET MVC 2中

System.Web.Mvc.dll

System.Web.Mvc.xml

Microsoft.Web.Mvc.Build.dll

下面2个是 3.5 sp1的动态链接库，去有sp1的电脑上复制下就可以了

System.Web.Routing.dll

System.Web.Abstractions.dll

&nbsp;

### 2、在根目录新建Default.aspx页面，并在后台写入代码

老版本IIS会验证文件是否存在，所以必须新建一个页面，然后在写上代码就可以了

    public partial class _Default : Page
    {
         public void Page_Load(object sender, System.EventArgs e)
         {
             HttpContext.Current.RewritePath(Request.ApplicationPath);
             IHttpHandler httpHandler = new MvcHttpHandler();
             httpHandler.ProcessRequest(HttpContext.Current);
         }
    }

&nbsp;

### 3、设置Route路由表

为了充分利用mvc的新特性，强烈建议你在建设网站的时候全部采用 controller\[/action\]\[/id\].aspx 这样的形式

有方括号代表可省略，但是不能只省略action而不省略id（其实可以实现，但是有限制和注意点，我这里先介绍基本的）

主参数就是id，如果有多个 http参数，就需要用显示GET传送了

controller/action/id.aspx?page=1

下面就是Global.asax文件里的Route设置

&nbsp;

    //默认匹配
    routes.MapRoute("NoAction", "{controller}.aspx", new { controller = "home", action = "index", id = "" });//无Action的匹配
    routes.MapRoute("NoID", "{controller}/{action}.aspx", new { controller = "home", action = "index", id = "" });//无ID的匹配
    routes.MapRoute("Default", "{controller}/{action}/{id}.aspx", new { controller = "home", action = "index", id = "" });//默认匹配
    routes.MapRoute("Root", "", new { controller = "home", action = "index", id = "" });//根目录匹配

&nbsp;

### 4、结束语

这样配置后，别人访问你的网站还是想以前的asp.net一样，全部是以aspx为后缀名。

这样配置后你的虚拟主机也就不会出问题了

OK，3个步骤完成后把你的网站发布到虚拟空间吧！一般不会有问题

本网站就是用MVC架构的，下面给个下载地址，是Default文件和那5个库文件

注意一下，自己更改下Default.aspx和Default.aspx.cs文件里的命名空间，其实不改也不会出问题

> <a style="font-style: normal;" href="http://www.rayfile.com/files/9f2bce21-fbb3-11de-8e46-0014221b798a/" target="_blank"><strong>下载地址(RayFile)</strong></a>
