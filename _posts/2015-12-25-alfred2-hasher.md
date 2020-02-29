---
title: Alfred2 插件：Hasher
author: Dozer
layout: post
permalink: /2015/12/alfred2-hasher.html
categories:
  - 编程技术
tags:
  - Python
  - Mac
---

### 工具化思维

最近在做的项目，需要频繁地转换 timestamp 到人类可识别的日期时间文本。之前一直在用一个 Chrome 的插件，可以快速转换各种格式，但是每次都要切换到 Chrome 实在是太不方便了，每次都要浪费1-3秒。这对一个懒人来说，是无法接受的。所以决定开始造工具了！

然后最近正好又买了正版的 Alfred2，也学了一点点 Python，那用 Python 给 Alfred2 做一个插件就再合适不过了！

源码和下载地址：[传送门](https://github.com/dozer47528/alfred2-hasher)

<!--more-->

&nbsp;

### 设计思路

所有的使用细节都在项目的 README 里说明了，所以这里主要是想说说设计思路。

这个插件目标有两个：全面 & 易用。

&nbsp;

### 全面

全面很简单，模块化后不断地加模块，设计的时候把模块抽象一下就行了，不难。感兴趣的可以看源码，后面在加功能的过程中可能会有重构。

![Hasher](/uploads/2015/12/hasher-design-1.png)

![Hasher](/uploads/2015/12/hasher-design-2.png)

&nbsp;

### 易用

要做到易用就麻烦了，什么叫易用？那就是输入尽量少的东西，然后尽快地得到正确答案。

所以我根据自己的使用习惯，设想了这样几种场景：

&nbsp;

#### 场景一：常用转换
平时经常用`MD5`，打开 Alfred2，输入`hasher`后直接粘帖需要做`MD5`的文本，可以直接看到结果，也可以按一下回车把结果放到剪贴板。

这个功能已经实现，但是还缺一个根据使用频率自动排序的功能。有了自动排序后，这个场景下用起来就可以非常方便，我觉得方便程度已经是极限了。

![Hasher](/uploads/2015/12/hasher-1.png)

&nbsp;

#### 场景二：找到一种不常用的转换
偶尔要用一下`Datetime`，打开 Alfred2，输入`hasher`。

然后输入`da`，不需要打全，此时下面会出现`Datetime`的提示，按一下`tab`，自动补全完整类型名字`datetime`。

然后粘帖需要转换的内容，结果就出来了，同样可以回车放到剪贴板。

这个交互过程我也想了很久，感觉这样子也是最快的方式了。

![Hasher](/uploads/2015/12/hasher-2.png)

![Hasher](/uploads/2015/12/hasher-3.png)

&nbsp;

### 最后

如果觉得好用的话帮我在 Github 上点个赞吧！

还有很多转换模块没有写完，也可以给我提 Pull request。
