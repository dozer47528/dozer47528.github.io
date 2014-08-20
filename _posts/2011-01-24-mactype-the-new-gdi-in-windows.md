---
title: MacType！让Windows下的字体渲染效果超越MAC！
author: Dozer
layout: post
permalink: /2011/01/mactype-the-new-gdi-in-windows/
duoshuo_thread_id:
  - 1171159103977075158
posturl_add_url:
  - yes
categories:
  - 软件
tags:
  - ezgdi
  - GDI
  - Mac
  - MacType
  - Windows
  - x64
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#GraphicsDeviceInterface"><span class="toc_number toc_depth_1">1</span> 基础知识：图形设备接口（GraphicsDeviceInterface）</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 效果如下</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">3</span> 相关软件</a>
    </li>
  </ul>
</div>

### <span id="GraphicsDeviceInterface"><strong>基础知识：图形设备接口（GraphicsDeviceInterface）</strong></span>

GDI是Graphics Device Interface的缩写，含义是图形设备接口，它的主要任务是负责系统与绘图程序之间的信息交换，处理所有Windows程序的图形输出。

在Windows操作系统下，绝大多数具备图形界面的应用程序都离不开GDI，我们利用GDI所提供的众多函数就可以方便的在屏幕、打印机及其它输出设备上输出图形，文本等操作。GDI的出现使程序员无需要关心硬件设备及设备驱动，就可以将应用程序的输出转化为硬件设备上的输出，实现了程序开发者与硬件设备的隔离，大大方便了开发工作。

GDI具有如下特点：

1. 不允许程序直接访问物理显示硬件，通过称为“设备环境”的抽象接口间接访问显示硬件；

2. 程序需要与显示硬件(显示器、打印机等) 进行通讯时,必须首先获得与特定窗口相关联的设备环境；

3. 用户无需关心具体的物理设备类型；

4. Windows参考设备环境的数据结构完成数据的输出。

<!--more-->

&nbsp;

### <span id="i"><strong>效果如下</strong></span>

[<img class="alignnone size-medium wp-image-165" title="effect_1" alt="" src="/uploads/2011/01/effect_1-300x141.png" width="300" height="141" />][1]

&nbsp;

[<img class="alignnone size-medium wp-image-166" title="effect_2" alt="" src="/uploads/2011/01/effect_2-300x273.png" width="300" height="273" />][2]

&nbsp;

可以看到 MacType 的效果非常棒！比以前的 GDI++ 好多了～

&nbsp;

&nbsp;

### <span id="i-2"><strong>相关软件</strong></span>

**GDI++：**

最原始的 GDI++ 是个日本的项目，但貌似已经停了好久了

官网：[**http://drwatson.nobody.jp/gdi++/**][3]

&nbsp;

**GDI++ 氦版：**

这是个国人修改的版本，比原始的好用，也已经停了好久了，32位版貌似一直很稳定，没有64位的

官网：[**http://hi.baidu.com/fonlan/home**][4]

&nbsp;

**ezgdi：**

ezgdi项目目的是为64位应用提供类似gdi++的字体渲染功能，以前用过，但是非常不稳定，而且效果不佳，不推荐

官网：[**http://code.google.com/p/ezgdi/**][5]

&nbsp;

**MacType：**

春天来了～这个版本是我用过最稳定，最完美的版本，而且支持 x64 ！别的不多说了～

官网：[**http://mactype.themex.net/**][6]

 [1]: http://www.dozer.cc/uploads/2011/01/effect_1.png
 [2]: http://www.dozer.cc/uploads/2011/01/effect_2.png
 [3]: http://drwatson.nobody.jp/gdi++/
 [4]: http://hi.baidu.com/fonlan/home
 [5]: http://code.google.com/p/ezgdi/
 [6]: http://mactype.themex.net/