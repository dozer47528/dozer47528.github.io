---
title: 巧用Windows下的搜索实现快速启动程序
author: Dozer
layout: post
permalink: /2012/01/using-the-windows-search-for-fast-start-program/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103977075196
categories:
  - 操作系统
tags:
  - Windows
  - 搜索
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 怎么快速启动程序？</a>
    </li>
    <li>
      <a href="#Windows_Vista_Windows_7"><span class="toc_number toc_depth_1">2</span> Windows Vista & Windows 7 内置搜索功能</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">3</span> 配置内置搜索功能</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">4</span> 让不是开始菜单中的程序也能搜索到</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">5</span> 用中文首字母来搜索应用程序</a>
    </li>
  </ul>
</div>

### <span id="i">怎么快速启动程序？</span>

有的人喜欢像 MAC 下的启动方式，现在的 Win7 时代呢，完全可以把程序 Pin 在任务栏上，可以达到一样的效果。

但是这种方式有局限性，不能搜索所有的程序，而且也不能搜索文档之类的东西，如果你有大量的文档也想一起搜索怎么办？

&nbsp;

为了解决这个问题，就有了如下两个软件：

首先是 <a href="http://qdesk.qq.com/" target="_blank"><strong>小Q书桌</strong></a>，360等都有类似的软件，大家根据洗好自我选择。

[<img class="alignnone size-full wp-image-592" title="qdesk" alt="" src="/uploads/2012/01/qdesk.png" width="433" height="273" />][1]

<!--more-->

这里有个小软件：**<a href="http://www.launchy.net/" target="_blank">Launchy</a> **它不仅可以搜索程序，还可以搜索文档。

[<img class="alignnone size-full wp-image-591" title="launchy" alt="" src="/uploads/2012/01/launchy.png" width="322" height="249" />][2]

&nbsp;

但是，说实话，他们都有 Windows 下内置好吗？

&nbsp;

### <span id="Windows_Vista_Windows_7">Windows Vista & Windows 7 内置搜索功能</span>

&nbsp;

**一张图就能说明问题，但是也需要来解释一下它的特点：**

<div>
  <a href="/wp-content/uploads/2012/01/search_windows.png"><img class="alignnone size-full wp-image-602" title="search_windows" alt="" src="/uploads/2012/01/search_windows.png" width="410" height="476" /></a>
</div>

1.  根据类型分类，程序排第一（因为大部分情况是为了启动程序）
2.  只需一个按键就可以启动（Win键）
3.  支持搜索文档内部内容，上图“index.html”文件其实并没有出现 “Visual”，但是也被搜索出来了
4.  另外，它还支持直接搜索网络！这招也是刚学来的，博客定位为原创，所以就不贴过来了，详细请看这里：<a href="http://terrychen.info/digging-into-windows7-start-menu-search-box/" target="_blank"><strong>传送门</strong></a>

&nbsp;

**说完了有点，同样也来吐槽一下：**

虽然它可配置搜索哪些目录，但是如果这个程序的快捷方式并不在开始菜单的话，它并不会列于“程序”分类，所以造成了一定的麻烦。每次启动程序需要多按几次，默认选中的第一个往往不是你想要的。

对中文的支持性不好，例如：“有道词典”，你只能输入中文。输入中文… 这还叫快速启动吗？难道不能输入：“ydcd”吗？

&nbsp;

所以，就让我们调教调教它吧~

&nbsp;

### <span id="i-2">配置内置搜索功能</span>

现在开始菜单搜索“索引选项”，我们先来告诉一下 Windows ，它应该去哪里搜索东西。

[<img class="alignnone size-medium wp-image-594" title="index" alt="" src="/uploads/2012/01/index-300x176.png" width="300" height="176" />][3]

一般用默认的就行，除非有特殊需求。

&nbsp;

再次在开始菜单搜索“文件夹选项”，我们现在来配置一些高级选项。

[<img class="alignnone size-medium wp-image-595" title="search" alt="" src="/uploads/2012/01/search-265x300.png" width="265" height="300" />][4]

把这些都够上是为了能让搜索更智能一点，虽然会加大系统负担，但现在的配置不在乎这点了吧？

&nbsp;

OK，初级调教完毕了，这时候，如果你新装了很多软件，并在开始菜单生成了快捷方式，那目前搜索功能已经够你使用了。

这时候先引出第一个进阶攻略，我电脑里很多软件，一重装在开始菜单里就没有了怎么办？

&nbsp;

### <span id="i-3">让不是开始菜单中的程序也能搜索到</span>

其实，如果结合上面的配置，你会发现这个功能非常容易实现。

我会在C盘以外的地方新建一个文件夹，专门存放所有的快捷方式。

这样的优点就是可以让系统重装后，快捷方式不丢失，因为很多软件都是绿色的，完全没必要重装。

然后再按照上面的配置，把这个文件夹配置到搜索的目录中，done!

让我们来看看效果吧。（我假设有一个程序叫“工资”，另外我的文档里也有很多和“工资”有关的文件）

[<img class="alignnone size-full wp-image-597" title="search_temp" alt="" src="/uploads/2012/01/search_temp.png" width="409" height="474" />][5]

纳尼！为什么会这样？程序呢？为什么它跑到了文件里？而且排在了这么后面？！

原来，就算你把别的程序加入了搜索列表，Windows 也不会把它当程序看。**Windows 只认开始菜单下的程序和快捷方式。**

&nbsp;

OK，我们理一下思路：

快捷方式一定要放在开始菜单下，开始菜单在C盘下，重装就会丢。死循环了…

那就没有别的方案了嘛？其实问题的关键就是如何让一些文件包含于开始菜单，又可以在重装的时候不丢呢？

需要解决这个问题就要用到 <a href="http://baike.baidu.com/view/4328569.htm" target="_blank"><strong>mklink</strong></a> 这个工具了。系统内置，直接在 CMD 中输入命令即可。

我们依然把所有的快捷方式放在一个文件夹下，然后在 CMD 中输入一些命令。

<pre class="brush:shell">mklink /j "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Quick" "e:/quickstart"</pre>

其中的 e:/quickstart 替换成你自己的目录就行了。

*请把这里的斜杠替换成反斜杠，Wordpress不知为何打不出反斜杠。*

再试一下？这时候，Windows 已经把这个目录当成开始菜单下的目录了，所以在这个目录下的快捷方式搜出来的就是程序，而且排得很靠前。

&nbsp;

现在，我们把第一个缺点解决了，下面再来一个高级进阶，怎么样才能更好地支持中文呢？

&nbsp;

### <span id="i-4">用中文首字母来搜索应用程序</span>

其实实现合格只是用了一点小技巧，例如 “有道词典”，其实只要改名成 “[ydcd]有道词典” 就行了。

下面看看效果吧。

[<img class="alignnone size-full wp-image-598" title="mtxx" alt="" src="/uploads/2012/01/mtxx.png" width="413" height="475" />][6]

虽然，你每次安装一个程序后都要改一下快捷方式的名字，但是由于会受到重装的影响，所以其实是一劳永逸的。

&nbsp;

 [1]: http://www.dozer.cc/wp-content/uploads/2012/01/qdesk.png
 [2]: http://www.dozer.cc/wp-content/uploads/2012/01/launchy.png
 [3]: http://www.dozer.cc/wp-content/uploads/2012/01/index.png
 [4]: http://www.dozer.cc/wp-content/uploads/2012/01/search.png
 [5]: http://www.dozer.cc/wp-content/uploads/2012/01/search_temp.png
 [6]: http://www.dozer.cc/wp-content/uploads/2012/01/mtxx.png