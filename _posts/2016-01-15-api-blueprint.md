---
title: API Blueprint
author: Dozer
layout: post
permalink: /2016/01/api-blueprint.html
categories:
  - 编程技术
tags:
  - 团队
---

### 对 API 文档的幻想

你对 API 文档有哪些需求？写起来方便看起来舒服？

这两个应该是文档最基本的需求了。

其实，前后端配合开发的时候，还常常会有这样一种需求：

“你接口定义好了吗？定义好了的话能不能先帮我做一个 Mock Server 让我先跑起来？”

<!--more-->

 &nbsp;

### apiary

曾经和前端同事合作开发的时候，就意外发现了这样一个网站。

在上面可以用 Markdown 的语法写文档，只要用统一的格式边写，它就能自动生成漂亮的展示页面和 Mock Server。

 ![apiary](/uploads/2016/01/apiary.png)

网站做的非常好，免费版可以供小团队使用。

最近发现，这家公司把它们的这套 API 标准开源了，还有对应的 Parser，Renderer，Mock Server，Editor等等。配套设施非常全，完全可以自己搭一个了。



相关标准和工具在这里：[https://apiblueprint.org/](https://apiblueprint.org/)

&nbsp; 

### 编辑器

编辑器其实非常简单，因为是基于 Markdown 的，所以如果你的编辑器支持 Markdown 语法高亮就行了，总之就是你爱用什么就用什么。

但是社区也有人做了一些插件，例如 [api-blueprint-preview](https://atom.io/packages/api-blueprint-preview) 就可以更方便地预览最终效果，还有这个插件 [linter-api-blueprint](https://github.com/zdne/linter-api-blueprint) 可以检查语法错误。

Atom 下插件最多，总之编辑器完全不是个问题。

API Blueprint 有自己的后缀名：`apib`，而且 github 可以识别它！

 &nbsp;

### Renderer

Renderer 是什么呢？它主要负责把你用 Markdown 写的文档渲染成静态 HTML 页面。

这里介绍一下：[aglio](https://github.com/danielgtaylor/aglio)



安装起来非常简单：

`npm install -g aglio`

用起来也同样简单：

`aglio -i document.apib  --theme-template triple -o output.html`

最终效果：

![aglio](/uploads/2016/01/aglio.png)



它可以多种模板，也可以自定义样式，更多需求可以看它的文档。

 &nbsp;

### Mock Server

Mock Server 就要靠另一个工具了：[drakov](https://github.com/Aconex/drakov)



安装起来同样很简单：

`npm install -g drakov`

然后跑起来：

`drakov -f "*.md"`

你会看到如下信息：

![drakov](/uploads/2016/01/drakov.png)

然后直接去浏览器中访问即可。

&nbsp;

### 自动化

相关工具都搞定了，还缺什么呢？主要就差自动化部署了，每次人肉重启是不可能的。

但这块没有现成的工具，或者说这块可以和现有的很多工具配合，例如配合 Jenkins 再写点脚本，很快就能实现了。
