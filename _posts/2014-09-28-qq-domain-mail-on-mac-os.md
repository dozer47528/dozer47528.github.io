---
title: Mac OS 中使用QQ域名邮箱
author: Dozer
layout: post
permalink: /2014/09/qq-domain-mail-on-mac-os/
categories:
  - 操作系统
tags:
  - Mac
  - IMAP
  - 域名
  - QQ邮箱

---

### Google 被墙之后

Google 被彻底墙掉之后，最不方便的就是手机端的邮件、联系人和日历的同步了。

电脑上可以翻墙，手机上没买 VPN，也不想手机一直开着 VPN 啊…

寻思了一番后，发现国内目前做得比较好的也就只有QQ邮箱了，对应的功能全部有。

<!--more-->

&nbsp;

### 吐槽QQ邮箱团队

用了QQ邮箱以后，才发现，遍地是坑！

我还帮QQ邮箱团队做了超级完整的功能验证：

<table class="table table-bordered">
<tr><td>平台</td><td>协议</td><td>帐号</td><td>现象</td></tr>
<tr><td>iOS</td><td>exchange</td><td>all</td><td>无法连接</td></tr>
<tr><td>iOS</td><td>内置QQmail</td><td>域名邮箱</td><td>显示验证失败</td></tr>
<tr><td>iOS</td><td>imap</td><td>all</td><td>mail app crash</td></tr>
<tr><td>mac</td><td>内置QQmail</td><td>域名邮箱</td><td>显示验证失败</td></tr>
<tr><td>所有</td><td>caldav,carddav</td><td>域名邮箱</td><td>显示验证失败</td></tr>
</table>

结论就是，没有一个平台是可以正常使用的！

另外我通过一些熟人关系找到了很多QQ邮箱相关的开发，还有直接给QQ邮箱发邮件，没有一个能解决这些问题的！

看上去这块的同步功能是小众功能，没人用，就没人管了是吧？

&nbsp;

### 使用域名邮箱

我的需求的确是非常小众的，Mac OS 上要同步域名邮箱的日历和联系人。

如果我不用域名邮箱，直接在 Mac OS 内置的QQ邮箱同步中输入常规账号，是一切正常的。

但是如果这么操作的话就会有一个问题：发出去的邮件是常规账号，而不是我的域名账号了。

但是日历同步和联系人同步其实无所谓用哪个账号的。后来发现 Mac Mail 可以修改邮箱的发送服务器，那是不是可以通过这个曲线救国呢？

&nbsp;

#### 用常规账号登陆

![sync-qq](/uploads/2014/09/sync-qq.png)

第一步比较简单了，直接用常规账号(`xxxx@qq.com`)登陆即可。

登录好以后，功能一切正常，只是发件账号是`xxxx@qq.com`，而我想用绑定的域名邮箱`xxxx@dozer.cc`来发送邮件。

&nbsp;

#### 修改Mail的发送服务器

![mac-mail](/uploads/2014/09/mac-mail.png)

接下来打开 Mail，然后修改它的发送服务器，你也可以修改它的收件服务器。

修改完后功能一切正常，发出去的邮件也是我的域名邮箱了。

好了，问题暂时解决，希望QQ邮箱团队可以关注一下这个严重的问题！

