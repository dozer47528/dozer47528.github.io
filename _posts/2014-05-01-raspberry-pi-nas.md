---
title: 利用树莓派组建支持迅雷离线下载的NAS
author: Dozer
layout: post
permalink: /2014/05/raspberry-pi-nas/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658386
categories:
  - 数码产品
tags:
  - Linux
  - NAS
  - 树莓派
---

### <span id="i">小米路由器</span>

最近小米路由器火了，说实在的，这配置拆开卖每个都要699这个价格。

支持AC双频的路由器就要将近100了，一个IT硬盘起码400，一个支持迅雷远程下载的 NAS 又要将近1000。

其实这些东西成本真的那么高吗？

路由器+硬盘，这价格是实打实的，就值这个价。

但现有的那些 NAS 真的有点水啊，所有相关的软件在 Linux 和 Windows 下都有开源免费的。

有点技术的都可以把家里的二手电脑打造成一个 NAS。

家里没有二手的破电脑了，而且破电脑很费电… 那就用树莓派搞起来吧！

<!--more-->

### <span id="i-2">硬件</span>

*   树莓派一个（加上一些配件）：400元
*   1T移动硬盘一个：400元
*   供电USB集线器：50元
*   网件路由器：400元

最终成本1300……（我靠！还不如买小米路由器！可惜在小米路由器推出钱我已经买了路由器和树莓派了…）

然后让我们来算算耗电量，家里没有功率计算器，所以只能算充电器的输出电压和电流了。

所以实际情况肯定比这个低，因为不可能一直是满载的嘛。

所有设备加起来大概在30W，24小时开机，电费0.6元/度。

30/1000 \* 24 \* 0.6 = 0.432元/天 这是理论最大值了，实际肯定比这个小，还可以接受，比开一台电脑好多了。

&nbsp;

### <span id="i-3">操作系统准备</span>

操作系统选用的是 RaspBian，用的人比较多，教程也多一点，喜欢 ArchLinux 的也可以用它。

下载地址：<a href="http://www.raspberrypi.org/downloads/" target="_blank">http://www.raspberrypi.org/downloads/</a>

安装脚本：<a href="http://www.raspberrypi.org/documentation/installation/installing-images/README.md" target="_blank">http://www.raspberrypi.org/documentation/installation/installing-images/README.md</a>

下载下来是一个镜像文件，在各个平台用对应的工具把镜像写入 SD 卡就行了，非常简单。

然后就插卡开机了！

&nbsp;

### <span id="i-4">下载部分</span>

#### <span id="i-5">准备硬盘</span>

各种格式支持：

<pre class="lang:sh decode:true">sudo apt-get install ntfs-3g
sudo apt-get install exfat-nofuse</pre>

装上这两个模块后，就可以支持 NTFS 和 exFAT 了。但是实测下来，这两种格式很吃 CPU，而树莓派最弱的就是 CPU了，所以最好用 ext4 格式！否则下载、传输性能会大打折扣。

把分区1格式化成 ext4 格式：

<pre class="lang:sh decode:true">sudo mkfs.ext4 /dev/sda1</pre>

&nbsp;

#### <span id="i-6">挂载硬盘</span>

我们先新建一个文件夹用来挂载硬盘：

<pre class="lang:sh decode:true">mkdir -p /home/pi/Share/usb</pre>

编辑`/etc/fstab`文件，就可以进行开机自动挂在配置了：

<pre class="lang:default decode:true">/dev/sda1       /home/pi/Share/usb      ext4    defaults,noatime        0       0
/dev/sda1       /home/pi/Share/usb      ntfs    defaults,noatime,uid=1000,gid=1000        0       0
/dev/sda1       /home/pi/Share/usb      exfat    defaults,noatime,uid=1000,gid=1000        0       0</pre>

在`/etc/fstab`文件后面加上一行，只要一行就行了，上面3行分别对应着三种不同的硬盘格式。

解释一下：

*   `noatime`代表不记录文件访问时间，可以大大提升性能。
*   NTFS 和 exFAT 并没有 Linux/Unix 权限系统，所以需要加上`uid=1000,gid=1000`指定这个文件的拥有者。

编辑完后，重启即可生效，不重启的话，可以执行以下命令：

<pre class="lang:sh decode:true">sudo mount -a</pre>

挂在完成后输入`mount`就可以看到当前系统所有的挂载记录，找找`/dev/sda1`是否在这个列表中，是的话就代表挂载成功了。

&nbsp;

#### <span id="i-7">迅雷路由器固件</span>

这个真是神器啊！家里的小米电视插上硬盘式支持迅雷远程下载的，但是小米电视是 Android 系统的，是不是很神奇？

其实，迅雷已经有了高端大气的迅雷路由器固件，它可以运行在很多系统中，包括各种 Linux/Unix。

树莓派当然也是支持的！

到论坛下载固件，树莓派需要下载这个版本：`<span style="color: #555555;">armel_v5te_glibc</span>`，具体选择什么版本和 CPU 架构有关。

因为迅雷没有开源，所以它只能针对各种架构和库，编译了各种版本。

最新版下载地址：<a href="http://luyou.xunlei.com/thread-3155-1-1.html?_t=1398873558" target="_blank">http://luyou.xunlei.com/thread-3155-1-1.html?_t=1398873558</a>

&nbsp;

先说明一下，这个路由器固件是免费的，但是如果要和自己的帐号绑定，那你的帐号必须是会员。

一年99元，为什么要花这个钱？因为家里的光纤猫没办法破解，所以 BT 速度非常非常慢！

（官方说是必须要会员的，但是我会员过期后依然能用，大家可以自己试试看）

你可以自己在树莓派上尝试着搭建一下其他下载功能，速度从来不会超过 100K。在国内用迅雷的速度还是非常快的！

&nbsp;

下面到安装步骤了，我们先把上面的压缩包放到任何一个目录中，我这里放到了`/home/pi/xunlei`中。

启动方式：

<pre class="lang:sh decode:true">/home/pi/xunlei/portal</pre>

如果没什么问题的话，就会在看到它输出了一串激活码，类似`H2DS72`。

打开 <a href="http://yuancheng.xunlei.com/" target="_blank">http://yuancheng.xunlei.com/</a> 后点添加，输入激活码即可。

[<img class="alignnone size-medium wp-image-1486" src="/uploads/2014/05/xunlei-300x184.png" alt="xunlei" width="300" height="184" />][1]

这样就搞定了？是的…非常简单！但是我们还是需要添加一下开机自动启动。

先创建一个服务：

<pre class="lang:sh decode:true">sudo vi /etc/init.d/xunlei</pre>

然后配置一下启动脚本：

<pre class="lang:default decode:true">#!/bin/sh
#
# Xunlei initscript
#
### BEGIN INIT INFO
# Provides:          xunlei
# Required-Start:    $network $local_fs $remote_fs
# Required-Stop::    $network $local_fs $remote_fs
# Should-Start:      $all
# Should-Stop:       $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start xunlei at boot time
# Description:       A downloader
### END INIT INFO

do_start()
{
        ./home/pi/xunlei/portal
}

do_stop()
{
        ./home/pi/xunlei/portal -s
}

case "$1" in
  start)
    do_start
    ;;
  stop)
    do_stop
    ;;
esac</pre>

最后开启自动启动

<pre class="lang:sh decode:true">sudo update-rc.d xunlei defaults</pre>

至此，迅雷远程下载就配置完成了，之后需要下载的话只要登录迅雷远程下载网站即可，在外网也可以哦！

&nbsp;

### <span id="i-8">共享部分</span>

#### <span id="Samba">Samba</span>

Samba 是最常用的了，Windows、Linux、小米电视都支持！

先安装相关组件：

<pre class="lang:sh decode:true">sudo apt-get install samba samba-common-bin</pre>

编辑配置文件`/etc/samba/smb.conf`：

<pre class="lang:default decode:true ">[global]
    workgroup = WORKGROUP
    security = user
    guest account = pi
    map to guest = bad user
    wins support = yes
    log level = 1
    max log size = 1000

[usb]
    path = /home/pi/Share/usb
    read only = no
    force user = pi
    force group = pi
    guest ok = yes</pre>

重启服务：

<pre class="lang:sh decode:true">sudo service samba restart</pre>

打开你的其它电脑，看看是不是可以看到了？如果看不到可以用IP访问。

&nbsp;

#### <span id="DLNA">DLNA</span>

DLNA 管理各种媒体文件比较好，性能和 Samba 也差不多，反正两者可以共存，主要看你的设备支持什么了。

小米电视都支持，iPad 的话用 DLNA 流媒体比较好一点。

然后 DLNA 就是被设计成播放流媒体的，所以大文件的视频肯定是 DLNA 性能更好一点。

&nbsp;

可是，我在小米电视上实测后发现，用 DLNA 播放会有卡顿。特别是快进的时候，需要几秒的缓冲。而在小米电视上用 Samba 是非常顺畅的。

后来我又用 Macbook Pro 试了一下，DLNA 和 Samba 的流畅度都是一样的，快进都不需要缓存。

看上去小米电视的 DLNA 还需要进一步优化！

&nbsp;

安装相关组件：

<pre class="lang:sh decode:true">sudo apt-get install minidlna</pre>

编辑配置文件`/etc/minidlna.conf`，主要就是修改一下媒体文件路径：

<pre class="lang:default decode:true">#监视所有类型
media_dir=/home/pi/Share

#也可以监视指定类型
#   * "A" for audio    (eg. media_dir=A,/var/lib/minidlna/music)
#   * "P" for pictures (eg. media_dir=P,/var/lib/minidlna/pictures)
#   * "V" for video    (eg. media_dir=V,/var/lib/minidlna/videos)
media_dir=A,/home/pi/Share
media_dir=P,/home/pi/Share
media_dir=V,/home/pi/Share</pre>

重启服务：

<pre class="lang:sh decode:true">sudo service minidlna restart</pre>

DLNA 配置很简单，现在打开支持 DLNA 的软件，看看是不是出现东西了？

&nbsp;

FTP

FTP 配置起来也很简单，但是作为 NAS，一个是给播放器播放，一个是给电脑操作文件。

前者有 DLNA，后者有 Samba，Samba 各种系统都是直接支持的，所以我个人觉得 FTP 完全没必要啊。

&nbsp;

### <span id="i-9">最后</span>

树莓派算是搞定了，性能一般般，主要是受到了树莓派 CPU 的限制，如果有一台性能高一点、功耗低一点的机器，再把这套东西迁移过去。

 [1]: /uploads/2014/05/xunlei.png
