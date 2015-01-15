---
title: 学生在线更新了什么？
author: Dozer
layout: post
permalink: /2011/04/what-is-new-in-student-online/
categories:
  - 互联网
tags:
  - 学生在线
  - 翔工作室
---

### 新的学生在线

相信大家都发现学生在线悄悄改版了，那么这次改版我们更新了什么呢？

&nbsp;

### IPV6

矿大的 IPV6 部署还是非常给力的，我们也看到了新的机会~

学生在线也拥有了自己的 IPV6 域名： **<a href="http://online.cumt6.edu.cn" target="_blank">http://online.cumt6.edu.cn</a>**

其实这个域名和以前的域名 **<a href="http://online.cumt.edu.cn" target="_blank">http://online.cumt.edu.cn</a>** 指向的是同一个网站

&nbsp;

而 IPV6 和 IPV4 都是属于**<a href="http://baike.baidu.com/view/239600.htm#sub239600" target="_blank">网络层</a>**的，也就是说，它们的更改理论上不会影响网站的访问。

事实上也的确如此，这个就像一个网站绑定个两个域名一样，没有什么影响。

&nbsp;

但唯一的问题是，当用 IPV6 访问的时候，所有的页面链接都要变，而“首页”是个内容聚集的页面，上面的链接大多不是内部链接，都是指向别的网站的链接，所以很多链接都是绝对链接，而不是相对链接。这就导致了在 IPV6 下很多链接会失效（而事实上它们是有 IPV6 地址的）

<!--more-->

**例一：**

首页上方的子站链接：新闻、下载、音乐、跳蚤、博雅、失物、论坛

这些本来设置的都是绝对链接，但因为这几个都是学生在线的子站，所以只要修改成相对链接即可。

<a href="http://online.cumt.edu.cn/discuz">论坛</a> 修改成 <a href="/discuz">论坛</a>

&nbsp;

**例二：**

首页还有很多的外部链接：图书馆，教务系统，就业指导等…

这些是外部链接了，没办法用相对链接来表示，所以唯一的解决办法就是，判断用户是用 IPV4 还是 IPV6 来访问的，然后根据来源，设置对应的链接

&nbsp;

### 布局调整

为了 “迎接“ 百强网站的评选，我们不得不做出了很多让步，放了很多大家并不需要的东西，现在活动结束了，我们也在进行了一定的调查后，对首页的布局进行了调整。

&nbsp;

先来看张图吧

[<img class="alignnone size-medium wp-image-297" title="online" alt="online" src="/uploads/2011/04/online-240x300.png" width="240" height="300" />][1]

&nbsp;

这张图被称为 **<a href="http://baike.baidu.com/view/3668215.html?fromTaglist#sub3668215" target="_blank">热力图</a>**

简单的来说，就是可以反映用户对页面各个部位点击情况的图片，这个是在大家浏览学生在线的时候自动统计出来的，可以直观地反映出大家对页面各个部分的关注程度。

&nbsp;

我们也根据这张图和平时的经验，对页面进行了调整，大家是不是发现学生在线更好用了呢？

&nbsp;

### 手机版

学生在线对手机版的重视程度一直不够，我们也意识到了这个问题，所以在将来改版的时候，会陆续加上手机版。

学生在线首页的手版地址是 **<a href="http://online.cumt.edu.cn/wap" target="_blank">http://online.cumt.edu.cn/wap</a>**

或许现在的手机版和电脑版差距还很大，但是我们会慢慢加强手机版的功能~大家敬请期待！

&nbsp;

### 结束语

最后，感谢大家对学生在线的支持，如果有什么意见或建议，可以到这里来反馈~

<a href="http://online.cumt.edu.cn/FlyingStudio/?page_id=360" target="_blank"><strong>传送门</strong></a>

 [1]: /uploads/2011/04/online.png
