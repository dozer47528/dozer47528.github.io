---
title: WordPress 迁移 Github Page + Jekyll
author: Dozer
layout: post
permalink: /2014/08/wordpress-to-github-page-jekyll.html
categories:
  - 互联网
tags:
---

### 关于这次迁移

#### 为什么迁移


博客写了5年，最烦的就是维护 WordPress 了。WordPress 的写作体验实在是太糟糕了，而且后台非常卡！

近几年 git 兴起，也衍生出了 Markdown 这样最适合程序员的写作方式。另外自己在一年内从 Windows 脑残粉变成了 *nux 脑残粉，更喜欢在 Bash 下干各种事情了。

所以趁阿里云过期之际，顺便把迁移这事做了。

恩，Github Page 是免费的！每个月立省 70！


#### 为什么不迁移

Github Page + Jekyll 的方案很早就有了，我为什么到现在才迁移呢？

其实之前也考虑过，但是主要是遇到了如下难题：

* 之前的文章是以 html 的形式存在数据库的，怎么做迁移？
* 分类和标签怎么迁移？
* 之前的静态资源怎么办？
* 博客的 URL 会变吗？
* 评论怎么办！

只是很久之前遇到的问题，今天回头看看发现，各个难点都有了很好的解决方案了。

所以这里给大家介绍一下~

<!--more-->

&nbsp;

### 搭建 Github Page 和 Jekyll

这部分不难，而且文章很多，所以直接贴官方教程了。英文的，但是讲的很详细：[传送门](http://jekyllrb.com/docs/home/)

这里要补充一点：网上很多教程是关于一个项目怎么建一个项目 Github Page 的，这个需要拉一个单独的分支。

但是如果你是一个项目专门用来写博客，那就不一样了。

* 你的项目名必须是`[your github username].github.io`，访问的 URL 是 `[your github username].github,io`，如果不是这样的规范的话，页面会无法访问
* 你的项目只要在`master`分支即可，不需要特殊的分支

&nbsp;

### 文章迁移

这里需要下载一个 WordPress 插件，插件在 Github 上，自己点`Download ZIP`后上传插件就行了。

下载地址：[传送门](https://github.com/benbalter/wordpress-to-jekyll-exporter)

使用方法就不介绍了，文章导出来后会包含一个`_posts`文件夹和你的静态文件。直接复制到你新建的 Jekyll 项目中即可。

`_posts`是 Jekyll 放文章的地方，导出的文章是`.md`后缀名的，可是为什么还是 html？

好吧，html 转 Markdown 有点难，但是没关系，Markdown 是完美支持 html 的，实测下来我所有文章的格式都没有问题！

&nbsp;

另外导出的文章分类和标签也全部都在：

![w2j-article](/uploads/2014/08/w2j-article.png)

&nbsp;

不知道为什么导出的压缩包有点问题，有些静态文件解压失败。没关系，自己到服务器上下载下来就行了。

`jekyll server`跑一下看看效果，所有的文章都搞定了！一个插件把文章，分类，标签，静态文件，URL，全部都解决了。

&nbsp;

### 评论迁移

之前我把评论同步到了多说，但是多说不太好用，最近国内外的博客都流行[**Disqus**](https://disqus.com/)，一用才发现，太好用了！特别是它的导入导出功能。

![disqus](/uploads/2014/08/disqus.png)

到 WordPress 中选导出`WXR`文件，然后直接上传即可。它还提到了一个插件，如果你文章较多，可能会有点问题，国内访问它毕竟速度不快，所以建议手动导出后再手动导入，也非常简单。

因为我博客的 URL 都没有变，所以不需要做什么调整。如果你的域名变了或者后面的路径变了，这里还可以做映射！是不是很强大？

![disqus-migrate](/uploads/2014/08/disqus-migrate.png)

好了，没过多久我的评论也迁移完了。

&nbsp;

### 批量处理

上面的各种工具已经很完美了，但是还是美中不足，我的很多文章还是需要做一下批量处理。

例如我想把静态文件的路径换一下，之前的路径是`/uploads/2014/08/image.png`

但是我已经不用 WordPress 啦！而且工具导出的很多 URL 都是绝对路径，所以做一下替换吧。

我找了很多方案，但是都有缺陷，最后发现最方便的还是用`perl`来实现，果然是文本处理神器！

&nbsp;

基本用法：`perl -i -p -e 's/${查询的正则表达式}/${被替换的正则表达式}/g' *`

这里就举几个例子，大家举一反三，就可以实现各种功能：

`perl -i -p -e 's/http:\/\/www\.dozer\.cc\/wp-contect//g' *`

另外可以用正则的 Group 概念，可以给所有没有`alt`的`img`加上默认的`alt`：

`perl -i -p -e 's/(<img)([^(alt)]*\/>)/<img alt="default_alt"\2/g' *`

总之，都是些正则表达式的技巧，非常方便！

&nbsp;

### 迁移完成

没花太多时间就迁移完成了！后面更多的是样式的优化，最后，欢迎大家的光临！
