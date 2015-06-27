---
title: Google Analytics 自定义维度
author: Dozer
layout: post
permalink: /2013/11/google-analytics-dmensions.html
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
categories:
  - 互联网
tags:
  - Google
  - Google Analytics
---

### 什么是自定义维度

Google Analytics 本身有很多维度了，例如：应用版本、设备型号、网络环境 等等…

但是有时候也需要设置一些自定义维度，例如：应用环境（线上、测试）、用户性别、用户注册城市 等等…

<!--more-->

&nbsp;

GA 可以自动识别内置的维度，但是自定义维度需要自己在应用启动的时候去设置一下。

官方解释：<a href="https://support.google.com/analytics/answer/1033861?hl=zh-Hans" target="_blank"><strong>https://support.google.com/analytics/answer/1033861?hl=zh-Hans</strong></a>

&nbsp;

### 维度的坑

自定义维度很好用，但是最近我们的项目发现了一个问题：

[<img class="alignnone size-full wp-image-1398" alt="ga-10" src="/uploads/2013/11/ga-10.png" width="592" height="235" />][1]

&nbsp;

我们为 App 设置了一个叫做“环境”的维度，这个维护会有两种值：prd 和 dev。

理论上，prd + dev = 全部移动应用数据。

但是我们十月份的数据却出现了很大的误差！

这是什么情况？仔细阅读文档后，我们才发现了一个略深的坑。

&nbsp;

### 适用范围和优先级

先解释两个名词：

Hit：告诉GA浏览了一个页面、告诉GA发生了一次事件，每次算一个Hit。

Session：GA 里的 Session 和网站 Session 的概念一样，GA 的 Session 过期时间默认为 30 分钟。

&nbsp;

另外，要理解这个坑，就需要理解维度的适用范围和优先级：

GA 的维度有三种范围，每种范围的优先级也是不一样的。

1.  Hit：在这个配置下，每次配置维度，只对下一次的 Hit 有效。
2.  Session：在这个配置下，每次配置维度，会对本次 Session 有效。 
    *   不一定要在 Session 开始的时候设置维度，任何时候设置都可以；
    *   一次 Session 中如果设置了两次维度，以最后一次为准；
    *   如果 Session 过期，新的 Session 不会有任何自定义维度。
3.  User：在这个配置下，每次配置维度，会对本次 Session 有效，并且会延续到后面的 Session。 
    *   每个设备只要设置一次维度即可，维护会自动延续；
    *   设置新的维度后，本次 Session 会启用新的维度，新的维度会延续下去；
    *   新的维度不会影响之前 Session 的维度。

Google Analitics 官方文档：<a href="https://developers.google.com/analytics/devguides/platform/customdimsmets#processing" target="_blank"><strong>https://developers.google.com/analytics/devguides/platform/customdimsmets#processing</strong></a>

&nbsp;

那我们的问题出在哪了呢？

我们之前设置的范围是 Session，所以发生了如下场景：

*   用户打开 App 后我们的程序会自动设置自定义维度，本次 Session 成功地设置了维度；
*   用户 App 在后台超过了 30 分钟，Session 过期；
*   用户重新打开 App，GA 自动开启了新的 Session，但 App 不算是重新启动，所以本次 Session 没有维度。

最终变看到了如上的数据…

&nbsp;

### 让你的 Session 不再被遗漏

怎么解决？我想了两个办法：

1.  每次启动和后台恢复的时候都设置一下维度。
2.  把维度的范围设置成 User 。

&nbsp;

第一个方法我暂未验证，因为我想先试试看第二种方案。

第二种方案我们试试了一周，prd 和 全部数据越来越接近了，不再会有2-3倍的数据差了。可是理论上应该是百分百吻合啊！？

问题出在哪呢？难道是有一批用户的 App 一直没关闭过？或者他们还在用老版本的 App？一切都有可能…

所以我们还在继续验证中~

 [1]: /uploads/2013/11/ga-10.png
