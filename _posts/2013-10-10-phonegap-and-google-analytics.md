---
title: PhoneGap 与 Google Analytics
author: Dozer
layout: post
permalink: /2013/10/phonegap-and-google-analytics/
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  -
categories:
  - 编程技术
tags:
  - Google
  - Google Analytics
  - PhoneGap
---

### 怎么整合 GA

PhoneGap 整合 <a href="http://www.google.com/analytics" target="_blank"><strong>GA</strong></a> 的时候会遇到这几个问题：

1.  如果用的是 file 协议，不支持 cookies，ga 一定要启用 cookies
2.  就算不是 file 协议，用网页版的 ga 无法跟踪详细的用户设备信息
3.  PhoneGap 做的话很多都是单页面应用程序，这样的页面很难用 ga 跟踪

所以用以前的网页版 GA 是很难统计好数据的。

<!--more-->

&nbsp;

### 移动应用分析

其实，Google 早就发布了移动版的 GA SDK，只要下载 SDK，就可以在页面中进行统计分析了。

帮助页面：<a href="https://support.google.com/analytics/answer/2587086" target="_blank">https://support.google.com/analytics/answer/2587086</a>

但是和网页版不同的是，它并不能自动捕捉各种事件，你必须手动在各个地方打点。

例如打开了一个页面，需要调用一下；各种事件统计，也需要自己用计时变量来统计。

[<img class="alignnone size-medium wp-image-1379" alt="ga" src="/uploads/2013/10/ga-300x112.png" width="300" height="112" />][1]

&nbsp;

### 和 PhoneGap 整合

既然有了 native 版本的 GA，那为 PhoneGap 写一个插件，把所有的方法包装成 js 不就行了？

github 上没有成本，只有一个半成品(<a href="https://github.com/phonegap-build/GAPlugin" target="_blank">https://github.com/phonegap-build/GAPlugin</a>)，实际用下来各种 BUG。

关键是它在包装 native 方法的时候偏偏还要改名字，很奇葩…

&nbsp;

因为代码其实很简单，所以我们就开发了自己的版本：

<a href="https://github.com/dozer47528/phonegap-gaplugin" target="_blank">https://github.com/dozer47528/phonegap-gaplugin</a>

用法很简单，js 包装的方法名和参数和 native 的是一模一样的，看一下 js 文件就知道有哪些方法了。

官方文档：<a href="https://developers.google.com/analytics/devguides/collection/" target="_blank">https://developers.google.com/analytics/devguides/collection/</a>

&nbsp;

iOS 下的方法定义

    - (void)initGA:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)exitGA:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)sendEvent:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)sendView:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)setCustomDimension:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)setCustomMetric:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)sendTiming:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;
    - (void)sendException:(NSMutableArray *)arguments withDict:(NSMutableDictionary *)options;

&nbsp;

### 自定义维度

GA 官方有很多维度，例如：版本号、地区、操作系统 等等…

但是总有一些自定义维度需要定义：环境(dev, prd)、用户名、用户组、用户城市 等等…

[<img class="alignnone size-full wp-image-1380" alt="weidu" src="/uploads/2013/10/weidu.png" width="362" height="444" />][2]

在 GA 的管理页面，可以找到你应用程序的自定义维度界面。

&nbsp;

接下来在每次启动 App 的时候都读取一下相关信息，然后调用 ga-plugin 中的方法设置维度的方法即可。

维护主要是用来筛选数据的，例如最常用的“环境”，你肯定要把开发环境和测试先上环境的 GA 区分开，所以维度是非常重要的！

&nbsp;

更多高级的用法可以单独写一篇文章了，大家可以先自行搜索相关文档。

 [1]: /uploads/2013/10/ga.png
 [2]: /uploads/2013/10/weidu.png
