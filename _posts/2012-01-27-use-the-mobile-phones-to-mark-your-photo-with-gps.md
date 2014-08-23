---
title: 利用手机，为你的相机照片加上地理位置标记
author: Dozer
layout: post
permalink: /2012/01/use-the-mobile-phones-to-mark-your-photo-with-gps/
categories:
  - 手机
  - 软件
tags:
  - Android
  - GPS
  - 摄影
---

现在智能手机上的相机都有一个功能：地理位置标记

加上这个标记后，在 <a href="http://picasa.google.com/" target="_blank"><strong>Pisaca</strong></a> ，<a href="http://www.flickr.com/" target="_blank"><strong>Flickr</strong></a> 等软件&相册中，就可以看到图片所在的地理位置了，还可以看到自己的轨迹，体验非常好！

但是谁旅游会拿个手机拍照呢？

可是谁家的数码相机又会有 <a href="http://zh.wikipedia.org/wiki/%E5%85%A8%E7%90%83%E5%AE%9A%E4%BD%8D%E7%B3%BB%E7%BB%9F" target="_blank"><strong>GPS</strong></a> 呢？（别那么早下定论，还真有几款<a href="http://www.enet.com.cn/article/2010/0817/A20100817710466.shtml" target="_blank"><strong>数码相机</strong></a>有 GPS）

&nbsp;

后来，偶然看到一款国内的软件，叫<a href="http://aoyouji.com/" target="_blank"><strong>遨游记</strong></a>，它的核心技术就是：

用手机来记录一组 GPS 位置信息，然后相机拍照；然后在电脑上把这两组数据根据时间匹配。这样每张照片都可以找到一个当时所谓位置的信息了。

非常棒的创意！*（后来发现其实早有人实现了）*

可惜只有 iPhone 版，没有 Android 版本…

&nbsp;

**那 Android 版如何实现呢？**

其实仔细想想，这里就涉及到2个技术：

1.  记录位置信息
2.  把位置信息写入照片

后来我还真把这两个软件找齐了，最终实现了这个功能！

<!--more-->

### Android 上记录位置信息的软件

这类软件很多，大多是一些运动类的软件，可以在你跑步的时候记录你的运动轨迹。

但是它们功能太多，而且不能导出数据，在这里我只想要一款很纯粹的，只用来记录位置信息，并且能导出数据的软件。

&nbsp;

#### <a href="https://market.android.com/details?id=com.miian.android.logger" target="_blank">GeoRecorder</a>

这是一款免费好用的软件，唯一的缺点是界面略丑… 但平时它都运行在后台，要求就放低一点吧。

[<img class="alignnone size-medium wp-image-612" title="20120127_152406" alt="20120127_152406" src="/uploads/2012/01/20120127_152406-180x300.jpg" width="180" height="300" />][1] [<img class="alignnone size-medium wp-image-613" title="20120127_152411" alt="20120127_152411" src="/uploads/2012/01/20120127_152411-180x300.jpg" width="180" height="300" />][2]

打开软件后，应该是当服务在运行中的时候就可以记录了，在设置中也有记录的间隔。

但是实测后发现这时候它并没有在工作，至于为什么我也还没搞懂。但是这不是问题。

&nbsp;

[<img class="alignnone size-medium wp-image-614" title="20120127_152421" alt="20120127_152421" src="/uploads/2012/01/20120127_152421-180x300.jpg" width="180" height="300" />][3] [<img class="alignnone size-medium wp-image-615" title="20120127_152426" alt="20120127_152426" src="/uploads/2012/01/20120127_152426-180x300.jpg" width="180" height="300" />][4] [<img class="alignnone size-medium wp-image-617" title="20120127_152431" alt="20120127_152431" src="/uploads/2012/01/20120127_152431-180x300.jpg" width="180" height="300" />][5]

我们点击手动记录，然后设置一下需要记录的时间，然后再设置一下间隔，接下来它就开始自动记录啦！

&nbsp;

[<img class="alignnone size-medium wp-image-618" title="20120127_152453" alt="20120127_152453" src="/uploads/2012/01/20120127_152453-180x300.jpg" width="180" height="300" />][6] [<img class="alignnone size-medium wp-image-619" title="20120127_152457" alt="20120127_152457" src="/uploads/2012/01/20120127_152457-180x300.jpg" width="180" height="300" />][7] [<img class="alignnone size-medium wp-image-620" title="20120127_152504" alt="20120127_152504" src="/uploads/2012/01/20120127_152504-180x300.jpg" width="180" height="300" />][8]

下面再来看看历史记录，它还支持回放哦，可以把你的行程再过一遍。

另外也可以导出数据！具体什么格式到后面再看。我这里用的是 GPX。

&nbsp;

#### <a href="https://market.android.com/details?id=com.google.android.maps.mytracks" target="_blank">My Tracks</a>

后来试用了一下这款软件，整体也很不错！

统计信息更多一点，同样支持导出数据，也很推荐，同样免费。

[<img class="alignnone size-medium wp-image-639" title="mt1" alt="mt1" src="/uploads/2012/01/mt1-179x300.jpg" width="179" height="300" />][9] [<img class="alignnone size-medium wp-image-638" title="mt3" alt="mt3" src="/uploads/2012/01/mt3-168x300.jpg" width="168" height="300" />][10] [<img class="alignnone size-medium wp-image-637" title="mt2" alt="mt2" src="/uploads/2012/01/mt2-168x300.jpg" width="168" height="300" />][11]

使用起来没难度，所以就不多介绍了。

&nbsp;

### 把地理位置信息写入照片中

地理位置记录好了，照片也拍好了，下面就让我们把数据写入照片吧！

&nbsp;

#### <a href="http://www.geosetter.de/en/" target="_blank">GeoSetter</a>

这个软件支持中文，绿色免费！也非常好用，不仅可以自己设置位置，也可以根据数据写入照片！

[<img class="alignnone size-medium wp-image-628" title="20120127152812" alt="20120127152812" src="/uploads/2012/01/20120127152812-254x300.png" width="254" height="300" />][12] [<img class="alignnone size-medium wp-image-629" title="20120127152834" alt="20120127152834" src="/uploads/2012/01/20120127152834-226x300.png" width="226" height="300" />][13]

我们现在这个软件里找到我刚刚拍摄的照片，然后在图像菜单里找到“与GPS数据文件同步…”

&nbsp;

[<img class="alignnone size-medium wp-image-631" title="20120127163416" alt="20120127163416" src="/uploads/2012/01/20120127163416-300x212.png" width="300" height="212" />][14]

[<img class="alignnone size-medium wp-image-630" title="20120127152846" alt="20120127152846" src="/uploads/2012/01/20120127152846-300x229.png" width="300" height="229" />][15]

然后在导入刚才手机上的 GPS 位置记录文件，其实刚才导出的三种格式这个软件都支持。

&nbsp;

[<img class="alignnone size-medium wp-image-626" title="20120127152937" alt="20120127152937" src="/uploads/2012/01/20120127152937-141x300.png" width="141" height="300" />][16]

最后保存一下！大功告成！

&nbsp;

[<img class="alignnone size-medium wp-image-627" title="20120127154633" alt="20120127154633" src="/uploads/2012/01/20120127154633-300x178.png" width="300" height="178" />][17]

当我们再用 Pisaca 打开这几张照片的时候，就可以成功地看到正确的地利位置信息了，误差非常小！

是不是很方便？完全可以批量操作，也非常的简单！

&nbsp;

### 在 <a href="http://www.google.com/earth/index.html" target="_blank">Google Earth</a> 中回味旅途

当图片成功导入照片后，还能有什么用途呢？其实，利用** <a href="http://www.google.com/earth/index.html" target="_blank">Google Earth</a>** 还可以进行旅行回顾哦！

还是在 GeoSetter 软件中，把需要回顾的图片选中，然后点图片菜单。

[<img class="alignnone size-medium wp-image-644" title="20120128163414" alt="20120128163414" src="/uploads/2012/01/20120128163414-300x195.png" width="300" height="195" />][18] [<img class="alignnone size-medium wp-image-642" title="20120128163510" alt="20120128163510" src="/uploads/2012/01/20120128163510-212x300.png" width="212" height="300" />][19]

选择导出到谷歌地图，并设置一下即可。

&nbsp;

然后打开谷歌地图，可以直接把这个文件拖进去。

[<img class="alignnone size-medium wp-image-643" title="20120128163609" alt="20120128163609" src="/uploads/2012/01/20120128163609-300x177.png" width="300" height="177" />][20]

最终效果如下，点击左上角的按钮，还可以模拟轨迹运行一次呢！

 [1]: /uploads/2012/01/20120127_152406.jpg
 [2]: /uploads/2012/01/20120127_152411.jpg
 [3]: /uploads/2012/01/20120127_152421.jpg
 [4]: /uploads/2012/01/20120127_152426.jpg
 [5]: /uploads/2012/01/20120127_152431.jpg
 [6]: /uploads/2012/01/20120127_152453.jpg
 [7]: /uploads/2012/01/20120127_152457.jpg
 [8]: /uploads/2012/01/20120127_152504.jpg
 [9]: /uploads/2012/01/mt1.jpg
 [10]: /uploads/2012/01/mt3.jpg
 [11]: /uploads/2012/01/mt2.jpg
 [12]: /uploads/2012/01/20120127152812.png
 [13]: /uploads/2012/01/20120127152834.png
 [14]: /uploads/2012/01/20120127163416.png
 [15]: /uploads/2012/01/20120127152846.png
 [16]: /uploads/2012/01/20120127152937.png
 [17]: /uploads/2012/01/20120127154633.png
 [18]: /uploads/2012/01/20120128163414.png
 [19]: /uploads/2012/01/20120128163510.png
 [20]: /uploads/2012/01/20120128163609.png
