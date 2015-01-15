---
title: 利用 WCF 调试模式寻找内部错误
author: Dozer
layout: post
permalink: /2012/11/wcf-traces-and-message-logs/
categories:
  - 编程技术
tags:
  - WCF
---

### 诡异的BUG

今天同事遇到了一个诡异的 WCF 问题，我自己也遇到过，觉得很有参考意义，拿来分享一下！

现象是 WCF 调用后报错，但是没有详细的错误信息，错误内容是：连接中断（偶尔也会出现别的内容）。

最诡异的是，本地起服务，断点调试 catch 不到任何异常！

&nbsp;

自己上次也遇到了同样的问题，于是帮忙解决，WCF 的很多内部错误是不会抛出来的，所以只能通过开启 WCF 调试模式来解决。

<!--more-->

### WCF 开启调试模式

WCF 开启调试模式非常简单，找到 web.config 文件，然后打开 VS——工具——WCF 服务配置编辑器，用这个工具打开 web.config 文件即可。

当然你也可以自己写配置，但是有了这个工具会更方便一点。

[<img class="alignnone size-medium wp-image-927" title="config" alt="config" src="/uploads/2012/11/config-300x188.png" width="300" height="188" />][1]

找到这个节点后，把几个原本是禁用的选项都启用。然后 Ctrl+S 保存即可。

日志和跟踪文件默认在网站目录下，也可以通过配置改变路径。

&nbsp;

### .NET 3.5 的问题

上次我自己的问题就是在开启调试模式后查看日志解决的，但是 .NET 3.5 开启调试模式后整个网站报错了！提示找不到依赖项。

Google 后发现，因为这个工具是 VS2010 自带的，它并不知道你的 web.config 文件是什么版本的，所以在启动调试模式的时候会引入2个 dll，并且设置的是 4.0 版本的，那当然会出错了！

修改方法很简单，在 web.config 中搜索：`System.Diagnostics.XmlWriterTraceListener`

然后把原来的： <span style="background-color: #eeeeee;">type=&#8221;System.Diagnostics.XmlWriterTraceListener, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31BF3856AD364E35&#8243;</span>

改成：`type=&#8221;System.Diagnostics.XmlWriterTraceListener&#8221;` 即可。

我本来配置成 3.5 的，但是不知道为何还是不行，后来把版本信息去掉后反而可以了。

&nbsp;

### 注意点

开启调试模式后还有一个注意点，我上次开启调试模式后，一直没有成功，调试产生的文件打开后一直报错…

后来研究后才发现，原来这个调试模式有点小问题，你想要看最终生成的文件时，一定要把站点关闭。

因为没关闭的时候，还有一些内容没有写到这个文件中，只有在关闭的时候，它才会把所有内容写入，这样就不会出错了。

&nbsp;

### 查看错误信息

接下来就简单了，双击打开这个文件，错误的地方会有红色的字显示，非常明显：

[<img class="alignnone size-medium wp-image-928" title="error" alt="error" src="/uploads/2012/11/error-300x156.png" width="300" height="156" />][2]

现在一下子就明白哪里出错了把？

&nbsp;

我上次遇到的问题是：一个实体的一个字段是枚举，数据库里读出数据的时候，有一个值在这个枚举类型中并不存在。

调用的时候只显示“连接中断”，连接中断…为什么中断啊，谁知道为什么呢？调试也看不出问题！

而且断点调试也看不出任何问题，几百个实体，我也没一个个去看。

因为 .net 里是允许给一个枚举类型赋错误的数字的，但 WCF 在序列化的时候是不允许的，所以导致了我的问题。

 [1]: /uploads/2012/11/config.png
 [2]: /uploads/2012/11/error.png
