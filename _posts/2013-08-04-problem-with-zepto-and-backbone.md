---
title: zepto 和 backbone 配合使用的坑
author: Dozer
layout: post
permalink: /2013/08/problem-with-zepto-and-backbone/
posturl_add_url:
  - yes
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
duoshuo_thread_id:
  - 1171159103985658371
categories:
  - 编程技术
tags:
  - javascript
  - zepto
---

### <span id="i">问题代码</span>

最近有那么一段 js 代码，困扰了很久很久，开发环境又是 PhoneGap，所以没办法调试 js…

代码大致逻辑如下：

<pre class="lang:js decode:true">var options

options.error = function (model, xhr, options) {
    if (xhr.status === 401) {
        //todo: login

        Backbone.sync(method, model, options)
        return
    }
}

options.success = function (model, xhr, options) {
	//todo:
}

Backbone.sync(method, model, options)</pre>

逻辑很简单，就是如果登陆的时候返回401错误，就重新登陆一下，登陆完成后重新请求数据。

这段代码没有问题，但是这个逻辑 + zepto + backbone 就有问题了。

代码在第二次请求的时候，就会报一个错误： xhr 是一个对象而不是一个函数。

<!--more-->

&nbsp;

### <span id="i-2">问题根源</span>

看了一下 backbone 和 zepto 的源代码后，发现了这个问题的根源！

&nbsp;

backbone 会把请求的 xhr 对象赋值到传入的 options 对象上，所以第二次请求的 options 对象上会有一个 xhr 对象。

而 zepto 在收到 options 的时候，会判断是否有 xhr ，如果没有的话，就设置一个默认的函数，内部逻辑是：`new window.XMLHttpRequest()`。

这就是为什么会报那个错误啦。

&nbsp;

### <span id="i-3">解决办法</span>

解决办法其实也非常简单啦，在第二次调用的时候把 options 里的 xhr 对象删除即可。

<pre class="lang:default decode:true  crayon-selected">options.error = function (model, xhr, options) {
    if (xhr.status === 401) {
        //todo: login
        delete options.xhr
        Backbone.sync(method, model, options)
        return
    }
}</pre>
