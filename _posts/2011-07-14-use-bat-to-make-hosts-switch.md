---
title: 利用 bat 文件制作 HOSTS 快速切换器
author: Dozer
layout: post
permalink: /2011/07/use-bat-to-make-hosts-switch/
categories:
  - 操作系统
tags:
  - HOSTS
---

### 切换 HOSTS 文件的困扰

学校里的 IPV6 免费上，而 IPV6 下是不用翻墙的，但是有但是 IPV6 下，有一些网站虽然有 IPV6 的 IP 但是却没有域名… 所以也只能通过修改 HOSTS 文件来访问。

另外在 IPV4 下，Google 的许多服务都需要通过修改 HOSTS 文件后才能正常访问…

所以，在平时每天需要切换好几次 HOSTS 文件。

那有什么办法可以简化这个操作？

<!--more-->

### HOSTS 切换软件

上网搜索了很多软件，但是都不是很好用，甚至都有冲动自己做一个了。

设计的逻辑基本上是这样的：

1、软件保存了很多域名的 IP 地址，并且每个域名拥有一个 IPV4 地址和一个 IPV6 地址（会根据网路情况自动判断）

2、软件可以保存很多方案，每点击一个方案可以执行一系列操作，例如：1、清空 HOSTS；2、增加 XXX，又例如：1、不对当前 HOSTS 进行修改；2、禁用 XXX

&nbsp;

这样子可以非常自由的控制 HOSTS 文件了。

&nbsp;

### 解决方案

有一次突然想到，干嘛要这么麻烦呢？把不同的 HOSTS 文件备份一下，需要哪个就复制过去不就行了？

还是很麻烦？直接写 bat 文件不就行了吗？虽然不能实现上述的高级功能，但是也可以满足日常需要了。

&nbsp;

**1、新建不同的 HOSTS 方案**

[<img class="alignnone size-medium wp-image-400" title="windows" alt="windows" src="/uploads/2011/07/windows-275x300.png" width="275" height="300" />][1]

这里我新建了三个，一个是空的，一个是 IPV4 下的，一个是 IPV6 下的

&nbsp;

**2、开始写 bat 文件**

<pre class="brush:shell">@echo  *****************
@echo  * HOSTS 切换器  *
@echo  * 1--清空       *
@echo  * 2--IPV4       *
@echo  * 3--IPV6       *
@echo  *****************
@choice /c     123

if errorlevel 3 goto IPV6
if errorlevel 2 goto IPV4
if errorlevel 1 goto CLEAR

:CLEAR
copy /y "C:\\Windows\\System32\\drivers\\etc\\hosts.ics" "C:\\Windows\\System32\\drivers\\etc\\HOSTS"
goto END

:IPV4
copy /y "C:\\Windows\\System32\\drivers\\etc\\hosts.ipv4" "C:\\Windows\\System32\\drivers\\etc\\HOSTS"
goto END

:IPV6
copy /y "C:\\Windows\\System32\\drivers\\etc\\hosts.ipv6" "C:\\Windows\\System32\\drivers\\etc\\HOSTS"
goto END

:END</pre>

这里非常容易理解，按照上面写就行了

&nbsp;

**3、遗留问题**

这里还有一个问题，操作 HOSTS 是非常危险的（杀毒软件是这么认为的）

所以不可避免的会弹出警告窗口，没办法，忽略之，并添加到白名单即可

 [1]: /uploads/2011/07/windows.png
