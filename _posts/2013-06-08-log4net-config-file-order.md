---
title: log4net 配置文件加载优先级
author: Dozer
layout: post
permalink: /2013/06/log4net-config-file-order.html
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  -
categories:
  - 编程技术
tags:
  - DotNet
  - log4net
---

### 坑坑坑

最近把项目中所有的日志都改成了 <a href="http://logging.apache.org/log4net/" target="_blank">log4net</a> ，同事也蠢蠢欲动，用起了 log4net。

但是一个大坑扑面而来…

&nbsp;

现象是这样的，同事有两个项目：

控制台引用程序：在 assembly 里配置了 log4net 的配置文件地址。

业务逻辑层：引用了 log4net 并写日志了。

&nbsp;

然后日志始终无法输出！

之前我一直天真地以为，解决方案中任何一个项目只要加上了`[assembly: log4net.Config.XmlConfigurator(Watch=true)]`就可以正确地加载配置了！

<!--more-->

&nbsp;

最后发现是业务逻辑层没有加上 assembly 这段代码，所以没有成功加载配置。

我自己的项目中在每个项目中都加上了，所以并没有问题。

那再进一步想想，如果多个项目中配置不同怎么办？

&nbsp;

结果到底怎么样呢？于是便有了此文…

&nbsp;

### log4net 加载配置的几种方式

官方文档非常详细：<a href="http://logging.apache.org/log4net/release/manual/configuration.html" target="_blank">http://logging.apache.org/log4net/release/manual/configuration.html</a>

总结一下就是三种方式：

1.  加 assembly attribute
2.  app.config 中配置
3.  显示调用

但是这三种方式之间有什么关系呢？E 文不好，也没看到官网上有详细的介绍。

所以，只能自己实践了。

&nbsp;

### Assembly Attribute

上面的三种方式并非独立，而是在隐约之中有着一些关联。

先说 assembly 方式，这个方法很简单，如果你只是一个简单的项目，那么在这个项目的`AssemblyInfo.cs`文件上加上`[assembly: log4net.Config.XmlConfigurator(Watch=true)]`即可。

至于上面参数的怎么用，直接参考文档即可。

上面这行的意思是直接从`app.config`中读取配置即可。

但是同事的项目为什么没有生效呢？！很诡异有木有！

&nbsp;

后来经过研究后发现，当你的程序第一次调用`LogManager.GetLogger`的时候，它就会从这个 dll 的 assembly 信息上读取相关的配置。

如果你的这个 dll 上没有加 assembly attribute，那么这个日志会输出失败。

更悲催的是，后面所有 dll 中的日志都会失败…

log4net 认为你根本就没想配置它…

同事的业务逻辑层没有加 assembly attribute，然后主程序虽然加了，但是主程序没有用 log4net。

&nbsp;

另外如果两个项目都加了 assembly attribute，并且配置的路径不同，那么会采用哪一个呢？

你第一次调用的 log 是哪一个 assembly 中的，就会启用哪一个，而且后面会一直用这个。

&nbsp;

### app.config 中配置

下面说说第二种方式，在配置文件中加配置：

    <appSettings>
      <add key="log4net.Config" value="log4net.config"/>
      <add key="log4net.Config.Watch" value="True"/>
    </appSettings>

官网说，如果你用了 assembly attribute 的配置方式，配置文件中的这两个节点会把 attribute 上的写死属性给覆盖。

官网这句话的意思是，一定要有了 attribute ，这两个配置才有效？但是我发现没有加 attribute 这两个配置也是有效的。

总之，这两个配置的优先级最高，如果你的各个项目中、或者引用了别人的 dll，都用了 attribute，加上这两个配置后，就可以把它们统一了，非常有用的配置！

&nbsp;

### 显示调用

最后说说显示调用的方式：

`log4net.Config.XmlConfigurator.Configure(new FileInfo("log4net.xml"));`

一般都是在程序的入口处加上这句话，这样就可以设置配置文件的位置了。

那大家肯定也会疑惑了，这种方式和上面两种方式的优先级是怎么样的？

经过实际测试后，我发现，就算已经加载了前面的配置，只要再次调用这种方式，配置都会变成新的。

也就是说，这种配置方法有绝对的控制权！

&nbsp;

### 最终方案

OK，了解了他们的优先级和各种关系后，就要想想最终方案了。

我希望最终的方案可以满足一下条件：

1.  <span style="line-height: 13px;">主程序引用子项目，子项目用了 log4net，主项目不用显示加载 log4net，只要加上配置即可，默认在 app.config 中；</span>
2.  可以通过配置文件来修改 log4net 的配置位置；
3.  可以在程序运行中动态修改 log4net 配置（比如通过界面操作）。

&nbsp;

嗯，如果要满足以上条件，那么就需要把上面三种方式配合起来使用了，我的建议是这样子的：

1.  <span style="line-height: 13px;">所有用 log4net 的项目都加上 assembly attribute；</span>
2.  如果配置在 app.config 中，不需要写任何而外的配置，如果配置在单独文件中，利用配置修改 log4net 配置位置；
3.  想要动态修改 log4net 配置路径的话，直接显示调用。

好了，最后的方案是不是很完美？

既符合“约定优于配置”的原则，也符合“灵活配置”的原则，完美了！
