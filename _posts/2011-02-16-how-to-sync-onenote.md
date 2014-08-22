---
title: 如何同步 OneNote ？
author: Dozer
layout: post
permalink: /2011/02/how-to-sync-onenote/
categories:
  - 软件
tags:
  - Office
  - OneNote
---

### <span id="OneNote">OneNote是什么？</span>



&nbsp;

&nbsp;

### <span id="_OneNote">如何同步 OneNote</span>

**同步 OneNote 有两种方法：**

1、直接利用 OneNote 内置的在线同步，把 OneNote 存放在 skydrive 里

2、利用 Dropbox 等同步软件同步本地文件

<!--more-->

**那这两种方法有什么优缺点呢？**

**内置同步功能：**

优点：

1.  无缝结合
2.  可以在网上在线编辑
3.  可以在移动设备上查看（目前支持 Windows Mobile, Windows Phone7, iOs）

&nbsp;

缺点：

1.  速度欠佳（特别是在国内）

&nbsp;

**利用其他同步工具：**

优点：

1.  速度快（国内可以使用 金山快盘，DBank，微盘，Everbox 等）

&nbsp;

缺点：

1.  不能在线编辑
2.  不能再移动设备上查看，只能在两台电脑间共享

&nbsp;

&nbsp;

### <span id="_OneNote-2">利用内置的同步功能同步 OneNote</span>

**如果你还没有笔记本？那么新建 OneNote 笔记本**

[<img class="alignnone size-medium wp-image-232" title="create" alt="create" src="/uploads/2011/02/create-300x258.png" width="300" height="258" />][1]

1.  文件——新建
2.  位置选择 Web
3.  输入一个名字
4.  登陆你的 msn 帐号
5.  选择文件夹
6.  创建笔记本

&nbsp;

**如果你的笔记本在本地？那么把它共享到网上吧**

[<img class="alignnone size-medium wp-image-233" title="share" alt="share" src="/uploads/2011/02/share-300x293.png" width="300" height="293" />][2]

1.  文件——共享
2.  选择一个笔记本
3.  选择位置
4.  登陆 msn 帐号
5.  选择文件夹
6.  共享

&nbsp;

**如果你的笔记本已经在网上了？那我们就用 OneNote 打开它吧**

[<img class="alignnone size-full wp-image-234" title="web" alt="web" src="/uploads/2011/02/web.png" width="533" height="120" />][3]

1.  IE打开 www.skydrive.com(一定要IE）
2.  找到你的 笔记本
3.  点击：在 OneNote 中打开

&nbsp;

&nbsp;

**创建好了如何同步？**

以上三个方法，都可以创建可以同步的 OneNote

创建好以后，你只要修改任何一个地方，它会马上给你同步，基本上是实时的

&nbsp;

&nbsp;

### <span id="i">利用其他同步工具</span>

在本地的 OneNote 默认创建在 我的文档\OneNote 笔记本 中

也就是过，你只要利用其他的公布工具，同步这个文件夹即可

&nbsp;

**但是这里也有一个技巧：**

一般你在用其他同步工具的时候，肯定不会仅仅同步 OneNote ，也会同步别的文件。

一般的工具都会创建一个自己的文件夹：XXX的同步文件夹。

只要把东西放里面就可以同步了，

这时候，你当然可以把需要同步的笔记本直接放在这里面，但是有没有更好的方法？

&nbsp;

答案是肯定的，那就是使用 **<a href="http://www.google.com/search?q=windows+%E9%93%BE%E6%8E%A5" target="_blank">链接</a>** 功能，熟悉 Linux 的人肯定很熟悉这个了，而在 Windows 下这个概念提到的比较少，所以很多人不会用。

这里用到的是 CMD 下的一个命令： **<a href="http://www.google.com/search?q=mklink" target="_blank">mklink</a>**

利用这个命令，把 OneNote 的笔记本文件夹 链接到 同步文件夹下，就可以实现同步了！

&nbsp;

最后，在别的电脑上也安装这个同步工具，并且登陆同一个帐号即可

 [1]: /uploads/2011/02/create.png
 [2]: /uploads/2011/02/share.png
 [3]: /uploads/2011/02/web.png
