---
title: Android系统中电子邮件的解决方案
author: Dozer
layout: post
permalink: /2011/07/email-solution-in-android/
posturl_add_url:
  - yes
categories:
  - 手机
tags:
  - Gmail
  - IMAP
  - PushMail
  - QQ邮箱
---

### <span id="i">纠结的电子邮件使用体验</span>

**在使用电子邮件的时候出现了种种问题：**

*   Android 中的 Gmail 客户端非常棒！还支持推送~ 但是 Gmail 在电脑上常常被重置，这个大家懂的…
*   Android 中的 邮件客户端 使用 QQ邮箱 的时候，会出现一些问题，倒是用户体验极差
*   Android 上找不到好的邮件客户端

&nbsp;

**QQ邮箱的问题：**

QQ邮箱在 IMAP协议 的支持上会导致一些问题。

标准的 IMAP 中，垃圾箱叫 Trash，已发送邮件叫 Sent ，但是 QQ邮箱 中却不是这个名字。

所以在 Android的邮件客户端 中设置 QQ邮箱 后，删除邮件或者发送邮件以后，就会自动创建上述文件夹，而不会放到 QQ邮箱 的“已删除邮件” 和 “以发送邮件” 中…

<!--more-->

**Android 上的邮件客户端：**

试过好多邮件客户端，但是在使用 QQ邮箱 的时候还是有种种问题…

&nbsp;

### <span id="K-9_Mail">K-9 Mail</span>

偶然一次，发现了一个叫 **<a href="http://code.google.com/p/k9mail/" target="_blank">K-9 Mail</a>** 的软件

[<img class="alignnone" title="K-9 Mail" alt="K-9 Mail" src="http://code.google.com/p/k9mail/logo?cct=1304120083" width="48" height="48" />][1]

先吐槽一下：图标难看！名字难记！第一印象非常不好…

但是，从技术上来看，绝对是一流的！

&nbsp;

### <span id="K-9_Mail-2">K-9 Mail 特色</span>

*   免费
*   功能强大，可以随意定制，Geek 最爱！（但这个也可以说是一项缺点）
*   支持 PushMail（其实不是真正的PushMail，而是 IMAP IDLE 后面详解）

&nbsp;

### <span id="K-9_Mail-3">K-9 Mail 设置指点</span>

我觉得，新建邮箱什么的，都没任何难度了吧？我就不介绍了，讲点别的吧~

&nbsp;

**如何设置 “PushMail”**

再次申明，这里的 PushMail 不是真正的 PushMail

&nbsp;

步骤：

1、进入一个邮箱帐户

[<img class="alignnone size-medium wp-image-387" title="1" alt="" src="/uploads/2011/07/1-180x300.png" width="180" height="300" />][2]

&nbsp;

2、Menu——更多——设置——账户设置——正在接受邮件——高级

[<img class="alignnone size-medium wp-image-388" title="2" alt="" src="/uploads/2011/07/2-180x300.png" width="180" height="300" />][3]

&nbsp;

&nbsp;

3、这里有个注意点，虽然打开了推送，但是建议也要打开定时检查，返回上级菜单即可设置

[<img class="alignnone size-medium wp-image-389" title="3" alt="" src="/uploads/2011/07/3-180x300.png" width="180" height="300" />][4]

&nbsp;

*注意点：不要以为打开了推送就万事大吉了，首先这个不一定推送成功，另外也不是所有的邮箱都支持推送哦！Gmail 支持，QQ邮箱不支持。*

&nbsp;

**设置文件夹**

前面说到，QQ邮箱一直会出现自己创建文件夹的问题，主要就是因为邮件客户端存放邮件的文件夹和QQ邮箱默认的不同。

所以如果手动指定的话不是就解决了吗？

&nbsp;

步骤：

1、进入有个邮箱账户——Menu——更多——设置——账户设置——文件夹

[<img class="alignnone size-medium wp-image-390" title="4" alt="" src="/uploads/2011/07/4-180x300.png" width="180" height="300" />][5]

&nbsp;

&nbsp;

然后在这里制定一下对应的文件夹就行！

&nbsp;

**其他**

设置完毕后， Gmail 和 QQ邮箱 均可正常使用~

&nbsp;

### <span id="_IMAP_IDLE">什么是 IMAP IDLE</span>

IMAP IDLE 模式是 IMAP 协议的一项高级功能，在这种模式下，客端登录连接服务器后并无主动查询新邮件的动作，而是停留在 IDLE（空闲） 状态，当服务器接收到新邮件后通知客端，客端再开始查询新邮件的动作，此动作完成后，客端重新回到空闲状态。使用 IMAP IDLE 模式的好处是，服务器收到新邮件时客端马上就会收到通知。

不支持 IMAP IDLE 的客端或者服务器，检查新邮件是靠客端手动刷新或者定期查询（比如每5分钟），这种方式查询新邮件会有时间延迟，如果新邮件没有赶上上次查询，必须等到客端下次查询时才能收到通知。

IMAP IDLE 和 Push email 还是有区别的，Push email 是服务器主动把邮件推送到客端；而 IMAP IDLE 是客端主动登录服务器并保持连接才可以，用电话作例子来说，IMAP IDLE 就像是客端打电话到服务器后进入待机状态等待服务器回答，而 Push email 则是服务器直接打电话给客端。

Gmail 目前并不支持 Push email，需要通过第三方支持（如 <a href="http://mobile.emoze.com/" rel="nofollow">http://mobile.emoze.com/</a> ）才能实现 Push email 的功能，这是因为 Gmail 在客端没有登录的情况下不知道如何把邮件推送到你的手机；如果使用 IMAP IDLE 功能，服务器只会通知客端有新邮件，而下载新邮件的工作还是客端完成的，并且这个过程中客端必须一直保持与服务器的连接才能收到通知进而完成下载邮件的工作，严格说这并不是 Push。

 [1]: http://code.google.com/p/k9mail/
 [2]: /uploads/2011/07/1.png
 [3]: /uploads/2011/07/2.png
 [4]: /uploads/2011/07/3.png
 [5]: /uploads/2011/07/4.png
