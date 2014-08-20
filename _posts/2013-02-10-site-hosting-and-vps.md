---
title: 建站指引 —— 虚拟主机与VPS
author: Dozer
layout: post
permalink: /2013/02/site-hosting-and-vps/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658356
categories:
  - 互联网
tags:
  - Godaddy
  - VPS
  - 云主机
  - 虚拟主机
  - 阿里云
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 何处来安放你，我的网站？</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 家里电脑开着当主机</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 虚拟主机</a>
    </li>
    <li>
      <a href="#VPS"><span class="toc_number toc_depth_1">4</span> VPS</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">5</span> 我的方案</a>
    </li>
  </ul>
</div>

### <span id="i">何处来安放你，我的网站？</span>

买了域名以后第二件事情就是需要找一个空间放你的网站了。

下面有这几种方案可供大家选择：

&nbsp;

### <span id="i-2">家里电脑开着当主机</span>

这个方案不用我教，大家都是做这行的，虽然不是运维但基本也肯定都懂吧？

但是这个方案有一些风险。

家里的电信IP是动态的，解决方案有：**<a href="http://www.iplaysoft.com/peanuthull.html" target="_blank">花生壳</a>**（只有买了花生壳的域名才可以）、<a href="https://www.dnspod.cn/support/index/fid/201" target="_blank"><strong>DNSPOD</strong></a>（需要把 NameServer 迁移到 DNSPOD）。

好吧，就算你把动态 IP 的问题解决了，有一个新的难题会摆在你面前。

现在很多网络供应商的路由器都是封闭式的，导致你的电脑在外网不可见。

所以这个方案真的很不靠谱，就算全部靠定了，你也不能一直把家里的电脑开着吧？

<!--more-->

### <span id="i-3">虚拟主机</span>

<a href="http://zh.wikipedia.org/zh/%E8%99%9A%E6%8B%9F%E4%B8%BB%E6%9C%BA" target="_blank"><strong>虚拟主机</strong></a>相当于给你一个 IIS 或者 Apache 服务器，国内的服务商都很抠门，一般都只允许创建一个网站；而国外的虚拟主机岂止是一个大方啊。

来一个对比吧（上图是Godaddy的，下图是万网）：

[<img class="alignnone size-medium wp-image-1059" alt="godaddy" src="/uploads/2013/02/godaddy-300x276.png" width="300" height="276" />][1]<img class="alignnone size-medium wp-image-1058" style="color: #333333; font-style: normal;" alt="wan" src="/uploads/2013/02/wan-300x249.png" width="300" height="249" />

对比一下最便宜的套餐吧：

<table border="1">
  <tr>
    <td>
    </td>
    
    <td>
      <strong>Godaddy</strong>
    </td>
    
    <td>
      <strong>万网</strong>
    </td>
  </tr>
  
  <tr>
    <td>
      空间大小
    </td>
    
    <td>
      100G
    </td>
    
    <td>
      0.5G
    </td>
  </tr>
  
  <tr>
    <td>
      数据库
    </td>
    
    <td>
      10个数据库
    </td>
    
    <td>
      30M SQL Lite
    </td>
  </tr>
  
  <tr>
    <td>
      流量
    </td>
    
    <td>
      无限
    </td>
    
    <td>
      20G/月
    </td>
  </tr>
  
  <tr>
    <td>
      价格
    </td>
    
    <td>
      $5.99/月（优惠期$1.99/月）
    </td>
    
    <td>
      ￥580/年
    </td>
  </tr>
</table>

还用比较吗？基本三围上，国内的只是国外的一个零头。

国外的服务也是好到家啊，我有一次买了，后来想退款。我都用了几天了，结果还是给我全额退款了。

Godaddy 支持支付宝，所以非常方便。

&nbsp;

Godaddy 也有缺点：

1.  在国内访问速度有点慢
2.  在国内可能被墙，正是因为太出名，所以太多的不和谐内容，IP 是共享的，所以可能会被墙

&nbsp;

### <span id="VPS">VPS</span>

<a href="http://zh.wikipedia.org/wiki/%E8%99%9A%E6%8B%9F%E4%B8%93%E7%94%A8%E6%9C%8D%E5%8A%A1%E5%99%A8" target="_blank"><strong>虚拟专用服务器</strong></a>，在国内一般简称 VPS。

简单的来说就是给你一台服务器，任你摆布，最常用的就是当作 Web 服务器了。

而实际上你得到的只是一台虚拟机，但说了给你分配多少的资源，就会给你多少的资源，这点可以放心，使用起来和真实电脑是一样的。

现在不是流行云吗？其实所谓的云主机就是 VPS… 加上一个云字，就变成新东西了…

真要说云主机和 VPS 的区别，那就是云主机一般都支持灵活的搭配方案。你可以选择你需要的 CPU、内存、磁盘、带宽、操作系统等等。

搭配很自由，最终根据你的搭配方案来定价格。

我看了下阿里云最新的云主机价格，真的已经完全领先虚拟主机了，价格都和虚拟主机差不多了。

[<img class="alignnone size-medium wp-image-1064" alt="ali" src="/uploads/2013/02/ali-175x300.png" width="175" height="300" />][2]

基本配置，跑你一个网站没问题了。所以如果你爱折腾，你会折腾的话，云主机肯定是首选了。

&nbsp;

推荐一些 VPS 和云主机：

<a href="http://www.aliyun.com/" target="_blank"><strong>阿里云</strong></a>：阿里旗下的，阿里云高层可能在策略等方面不咋的，但是阿里在这方面的技术还是一流的。如果选国内，那阿里云就是首选了。

<a href="http://www.burst.net/" target="_blank"><strong>Burst</strong></a>：国外老牌的 VPS ，很受国内用户青睐。淘宝上有很多代购，因为它不支持支付宝，所以你只能用支持 Visa 的信用卡了，比较麻烦。

&nbsp;

另外，因为 VPS 或者云主机只要空间够你可以随意使用，所以完全可以和熟人一起合租。

另外的另外，我绝对不会告诉你外国的 VPS 可以当私人的翻墙工具~

&nbsp;

### <span id="i-4">我的方案</span>

我不会告诉你我的空间一分钱不要的，哈哈。

N年前，我买 Godaddy 的域名，送到了一个免费的虚拟主机（相当于 Godaddy 最低的配置）。

官方说会有广告，但是我从来没看到，我也很奇怪…

 [1]: http://www.dozer.cc/uploads/2013/02/godaddy.png
 [2]: http://www.dozer.cc/uploads/2013/02/ali.png