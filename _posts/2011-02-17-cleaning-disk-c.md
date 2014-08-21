---
title: 关闭鸡肋功能，彻底清理C盘
author: Dozer
layout: post
permalink: /2011/02/cleaning-disk-c/
posturl_add_url:
  - yes
categories:
  - 操作系统
tags:
  - Windows
  - Windows7
---

### <span id="i">前言</span>

网上有很多管理清理C盘的教程，但是大多是讲的都是何如清理垃圾，而这些垃圾一般是会再次生成的，作用并不明显。

那就没有别的办法清理C盘了吗？

答案是否定法的，其实 Windows 中存在着大量的鸡肋功能，简单的几步，就可以让你的C盘腾出至少5G的空间（Vista & Windows7 主流配置）

而且一下的几个小技巧数量不多，但各个都是重量级的。

比上面那些弄了半天，才腾出几G的办法有效多了。

而且还不会反弹哦~

&nbsp;

此文仅仅针对 Vista & Windows7 操作系统

<!--more-->

### <span id="i-2">关闭休眠</span>

为什么要在 Vista 和 Windows7 中关闭休眠？

休眠是 XP 时代的功能，在新的操作系统中，已经有睡眠功能取代之（待机功能是完全消失了）

简单的来说，Vista 和 Windows7 中完全不需要休眠功能了，所以可以关闭它。

传送门：**<a href="http://www.google.com/search?q=%E5%BE%85%E6%9C%BA+%E7%9D%A1%E7%9C%A0+%E4%BC%91%E7%9C%A0+%E5%8C%BA%E5%88%AB" target="_blank">待机，睡眠和休眠的区别</a>**

&nbsp;

**关闭休眠后，可以在C盘腾出一块和内存大小一样的空间，也就是说，2G内存的电脑在关闭休眠后C盘可以多出2G**

&nbsp;

**关闭方法：开始菜单——运行——输入“CMD”——输入“powercfg -h off”**

[<img class="alignnone size-full wp-image-241" title="power" alt="" src="/uploads/2011/02/power.jpg" width="677" height="119" />][1]

&nbsp;

&nbsp;

### <span id="i-3">关闭错误转储文件</span>

在默认的设置下，如果系统发生了严重的错误，会转储很多内存中的数据，以便管理人员根据这些数据排除错误。

不过这功能对于我们一般用户确实没有什么用，反而浪费了宝贵的硬盘空间。

因此这项功能完全可以关闭。

&nbsp;

**同样，该功能也可以腾出和内存大小一样的空间**

&nbsp;

**关闭方法：开始菜单——计算机（右击属性）——高级系统设置——高级——启动和故障恢复，设置——系统失败，写入调试信息，选择“无”**

[<img class="alignnone size-medium wp-image-242" title="error" alt="" src="/uploads/2011/02/error-300x195.jpg" width="300" height="195" />][2]

&nbsp;

&nbsp;

笔者电脑内存4G，这两个功能就吃到了我8G的空间，是在是太浪费啦~罪过罪过~

 [1]: /uploads/2011/02/power.jpg
 [2]: /uploads/2011/02/error.jpg
