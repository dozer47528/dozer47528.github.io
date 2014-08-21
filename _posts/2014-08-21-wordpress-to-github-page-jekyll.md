---
title: 电信光纤猫 HG8245C 破解
author: Dozer
layout: post
permalink: /2014/08/wordpress-to-github-page-jekyll/
categories:
  - 互联网
tags:
  - Wordpress
  - github
  - Jekyll
published: false
---

### <span id="HG8245C">HG8245C</span>

搬家后最痛苦的一件事就是，电信新版的光纤猫不能破解！所以不能从 NAT 改桥接让路由器直接拨号。

我也时常去网上搜搜破解教程，最近终于在淘宝找到了！最终花了60元找人远程搞定。

卖家人不错，我也帮忙推荐一下：<a href="http://item.taobao.com/item.htm?id=38921723002" target="_blank">http://item.taobao.com/item.htm?id=38921723002</a>

<!--more-->

&nbsp;

### <span id="i">光纤猫改桥接有什么好处</span>

*   禁用光纤猫的路由功能，直接让路由器拨号，方便管理提升性能
*   由2次 NAT 变成1次 NAT 后，解决 <a href="http://zh.wikipedia.org/wiki/UPnP" target="_blank"><strong>UPnP</strong></a> 失效的问题
*   自己的路由器可以暴露给外网，设置 <a href="http://zh.wikipedia.org/wiki/DMZ" target="_blank"><strong>DMZ</strong></a> 主机后可以进一步把家里的服务器暴露给外网

&nbsp;

### <span id="UPnP">UPnP</span>

经常下 BT 的应该知道 BT 软件都会检测是否可以从外网连接，如果家里用的是路由器的话，你的电脑就没办法暴露给外网了。

解决办法有很多，DMZ 主机就是把其中一台机器暴露给外网；通过 UPnP 可以穿透 NAT 让局域网内的多台电脑的指定端口映射到外网。

但是！如果是一个电信的光纤猫路由器+一个自己的路由器，你就没没有完美的方案了。

因为电信的光纤猫路由器不能设置 DMZ 主机，虽然内置支持 UPnP，但是2次 NAT 后 UPnP 就失效了。

（这块非专业，只能讲讲大概的原理，具体的就不解释了）

&nbsp;

所以在这种网络结构下，你会发现自己下 BT 会奇慢！

没事，我可以用迅雷啊，为什么迅雷快呢？因为迅雷会自动查找类似资源，你下的是 BT，迅雷也会帮你找到其他 HTTP 或者 FTP 的资源。可是，如果你不是迅雷会员速度就会大打折扣，这么好的服务迅雷也不会免费给你用的…

所以，终极解决办法就是破解光纤猫，让路由器自己拨号，这样就可以只做1次 NAT，局域网内所有的 UPnP 都是有效的。

[<img class="alignnone size-medium wp-image-1540" src="/uploads/2014/08/upnp-300x213.png" alt="upnp" width="300" height="213" />][1]

&nbsp;

### <span id="DMZ">DMZ</span>

DMZ 主机就是，电信光纤猫是不能设置任何高级功能的，所以它拨号成功后外网只能访问到它，而它为了安全会组织任何外网对它本身的访问。

所以我内网架设的任何服务在外网都是无法访问到的。

破解后简单了，自己的路由器设置 DMZ 主机，把外网访问全部映射到家里的服务器上。

我之前讲过用树莓派搭建 <a title="利用树莓派组建支持迅雷离线下载的NAS" href="/2014/05/raspberry-pi-nas/" target="_blank">NAS</a>，一般都会架设一个 <a href="https://www.transmissionbt.com/" target="_blank"><strong>Transmission</strong></a> 进行 BT 下载，它会提供一个 Web 管理界面，内网没问题，那我在公司想要下载怎么办？貌似没办法了，因为我的内部站点在外网完全无法访问到。

后来，是通过迅雷的远程下载固件间接解决了这个问题，它的远离是自身主动把数据上传到迅雷服务器，而不是直接从外网连接到内部的 NAS 上。

&nbsp;

但是破解光纤猫后就不存在这个问题了，家里的树莓派就这样完全暴露给外网了！在外干什么事情都很方便了~

但是 IP 是动态的啊，怎么办？

这个还不简单？DD-WRT 支持 <a href="http://zh.wikipedia.org/wiki/%E5%8B%95%E6%85%8BDNS" target="_blank"><strong>DDNS</strong></a> 功能，免费的域名很挫，没关系，用自己的域名做一个 CNAME 就完美了！

&nbsp;

至此，家庭多媒体中心接近完美了！

下一步是什么？树莓派性能太差，小米电视2 已经支持 4K，树莓派的读写性能已经跟不上了，现在 4K 片源还不多，等多了以后，就该把它换了~

 [1]: /uploads/2014/08/upnp.png
