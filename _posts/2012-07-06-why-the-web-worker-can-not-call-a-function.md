---
title: Web Worker 为何不能直接调用函数？
author: Dozer
layout: post
permalink: /2012/07/why-the-web-worker-can-not-call-a-function/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103980681366
categories:
  - 编程技术
tags:
  - HTML5
  - javascript
---

### <span id="Web_Worker">Web Worker 的奇怪用法</span>

当我第一次看到 <a href="http://www.w3schools.com/html5/default.asp" target="_blank"><strong>HTML5</strong> </a>中 <a href="http://en.wikipedia.org/wiki/Web_worker" target="_blank"><strong>Web Worker</strong></a> 的用法时，非常地疑惑：

<pre class="brush: javascript; gutter: true">var worker = new Worker('worker.js');</pre>

既然是新起一个线程，为什么要调用外部的 js 文件，而不是直接传入一个函数呢？

<pre class="brush: javascript; gutter: true">var worker = new Worker(function(){
    //do something
});</pre>

因为调用外部 js 会非常的麻烦。

<!--more-->

### <span id="Web_Worker-2">Web Worker 实现原理猜想</span>

由于这样奇怪的调用方法，我开始有了一种猜想，HTML5 中的 Web Worker 是不是和样子实现的呢？

猜想：

Javascript 底层是单线程的，但是浏览器在加载页面的时候是可以支持多线程的，多个页面之间的 Javascript 是不会相互影响的。

所以可以新建一个页面，然后把让这个页面引用这个外部的 JS 文件，这样就可以实现多线程了。

直接玩不后，windows.open 打开的子窗口与父窗口之间也可以相互通讯，最终实现了 Web Worker。

&nbsp;

### <span id="Web_Worker-3">Web Worker 实现原理猜想试验</span>

为了验证这个猜想，特意写了一段代码。

HTML 页面：

<pre class="brush: xhtml; gutter: true">&lt;!DOCTYPE HTML&gt;
&lt;html&gt;
 &lt;head&gt;
	  &lt;script&gt;
		function ReCall(data){
			alert(data);
		}
		var win = window.open();
		win.document.write('&lt;script src="work.js" type="text/javascript" &gt;&lt;\/script&gt;');
	  &lt;/script&gt;
  &lt;/head&gt;
 &lt;body&gt;
	&lt;button onclick="alert('ok!')"&gt;click me!&lt;/button&gt;
 &lt;/body&gt;
&lt;/html&gt;</pre>

JS 文件：

<pre class="brush: javascript; gutter: true">function onmessage() { 
	for(var k=0;k&lt;10000000;k++){
		console.log('test');
	}
	self.opener=null;
	self.open('', '_self');
	self.close();
}
onmessage();</pre>

运行后发现，子页面依然把父页面阻塞了，父页面的按钮点了也没用！

可见 Web Worker 并不是这样子实现的。

&nbsp;

### <span id="Web_Worker-4">Web Worker 设计原理</span>

最后，求助了 Stack Overflow：<http://stackoverflow.com/questions/11354992/why-the-web-worker-cant-call-a-function>

也找到了一篇 IBM 的文章：[http://www.ibm.com/developerworks/cn/web/1112\_sunch\_webworker/][1]

总结一下：

虽然不知道底层具体是怎么实现的，但是从 IBM 的文章中可以看到，Web Worker 的确新起了一个线程，Javascript 不再是单线程的了！

但是为什么要这么用呢？

从网友的回答中看，我觉得这么设计的主要原因是为了隔离运行环境。因为 Javascript 的多线程不是线程安全的，或许底层还没有那么完善，所以为了防止出现问题，只能把它们完全隔离了。所以无法直接调用本页面中的函数，一调用本页面中的函数，就无法隔离了。

或许将来，会有更好的多线程机制出现，期待吧！

&nbsp;

 [1]: http://www.ibm.com/developerworks/cn/web/1112_sunch_webworker/
