---
title: Windows 下 Php 网站 Temp 文件夹的权限问题
author: Dozer
layout: post
permalink: /2011/04/php-permissions-on-the-temp-folder-in-windows/
categories:
  - 操作系统
tags:
  - IIS
  - Php
  - 服务器
---

### 服务器抽风…

前几天不知为何，服务器抽风严重…

远程连接非常慢，然后论坛 Discuz 程序的进程 CPU 占用率居高不下（IIS7.5 下挂 Php 程序，并且自建了应用程序池）

&nbsp;

### 排查过程

1.  检查网页服务器，病毒，木马？是否被入侵？
2.  检查数据库服务器，CPU，内存，网络一切正常，相应的端口也做了 IP 限制，只允许网页服务器访问，查看日志文件也没有异常情况
3.  检查其余的 .Net 网站，速度正常，没有任何问题
4.  检查其余的 Php 网站，架构方法一样，也没有任何问题（其余的 Php 网站访问量相对于论坛来说小很多）
5.  新建一个应用程序池和网站应用程序，引用的论坛（文件系统相同），单人访问速度没有问题，说明 Discuz 程序没有问题
6.  检查 Php 设置，发现没有异常

<!--more-->

综合以上因素，所以基本可以确定问题主要来源于某个小问题，然后当访问人数过多的时候就会体现出来。

那这个问题是什么呢？

&nbsp;

这时候想到去看一下 Php 日志文件，打开 c:\\windows\\temp 下的 Php 日志文件，突然… Notepad++ 卡死了！

原来这个文件已经达到了 800多 MB，难道是这个问题？

记得以前 IIS 下所有网站都出现了访问缓慢的问题，然后发现 IIS 日志文件达到了几个 G，禁用 IIS 日志后恢复正常。

难道也是这个问题？果断禁用了 Php error log，并删除了这个文件后，略有改善，但是感觉还是没解决…

&nbsp;

正在彷徨时，忽然发现 Temp 文件夹下有大量 sess_ 开头的文件！（之前打开 Temp 文件夹的时候就特别慢）数量竟然达到了 10W 个！总容量虽然只有 300MB ，但是占用空间却达到了 3G

[<img class="alignnone size-medium wp-image-289" title="sess" alt="sess" src="/uploads/2011/04/sess-300x230.png" width="300" height="230" />][1]

&nbsp;

看上去问题就出在这里了！

&nbsp;

关于 NTFS 下的文件数量

NTFS 的优越性就不用说了，也早就是主流了…

NTFS 下的最大文件数是 4,294,967,295个 (2^32 - 1)

但是为什么仅仅 10W 个文件就让系统慢成这样了呢？好吧，都说是理论值了… 不知道有没有人测试过，但 10W 个的确非常多了…

&nbsp;

### 解决方法

删除这些文件是必需的，这个过程很痛苦… 因为系统卡死了…

后借助 CCleaner 后才成功将其删光

&nbsp;

可是光删也不是办法，总有一天它还是会满的…

这些文件其实是 Php 保存 Session 的文件，一个 Session 对应了一个文件，但是 Session 结束的时候不应该删除吗？

&nbsp;

[<img class="alignnone size-medium wp-image-288" title="authorate" alt="authorate" src="/uploads/2011/04/authorate-300x243.png" width="300" height="243" />][2]

其实 Php 是会删除的，但是由于权限的问题，而导致它不能及时的删除了，以上就是 IIS_USERS 组的默认权限。

它并没有删除的权限 ！难怪没办法删除！

&nbsp;

知道这个后就简单了，给 IIS_USERS 加上删除的权限就 OK 了！

&nbsp;

修改好后，Temp 文件夹下的文件数一直维持在一个数量级，而没有明显的变化~

[<img class="alignnone size-medium wp-image-290" title="temp" alt="temp" src="/uploads/2011/04/temp-248x300.png" width="248" height="300" />][3]

 [1]: /uploads/2011/04/sess.png
 [2]: /uploads/2011/04/authorate.png
 [3]: /uploads/2011/04/temp.png
