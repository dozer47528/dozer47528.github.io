---
title: PhoneGap 与 Application Cache
author: Dozer
layout: post
permalink: /2013/05/phonegap-and-application-cache/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - Application Cache
  - html
  - HTML5
  - PhoneGap
---

### <span id="i">一个想法</span>

在研究 PhoneGap 的时候一直在想一个问题，怎么提高移动网络下的网络性能？特别是静态文件，多次加载完全是浪费。

HTTP 协议中控制缓存也比较纠结，总会有个 <a href="http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.5" target="_blank"><strong>304</strong></a> 请求，而且各种协议，各种 HTTP header，都不统一。而且 304 实际上也是进行了一次 HTTP 请求的。

因为用的是 PhoneGap，可以用 Navtive Code 来进行扩展，所以想到一个点子，是否能有一个静态文件升级功能？远程有一个文件标记着静态文件包的最新版本，如果有更新，这个插件就自动把静态文件下载到本地。然后 PhoneGap 打开的页面使用本地缓存的静态文件即可。完全不需要任何请求！

<!--more-->

&nbsp;

### <span id="HTML_Application_Cache">HTML Application Cache</span>

正当我纠结怎么实现的时候，发现了 HTML5 种已经有类似的东西了，而且实现的功能和我的需求一模一样。因为它就是为离线应用设计的。

> 离线访问对基于网络的应用而言越来越重要。虽然所有浏览器都有缓存机制，但它们并不可靠，也不一定总能起到预期的作用。HTML5 使用 ApplicationCache 接口解决了由离线带来的部分难题。
> 
> 使用缓存接口可为您的应用带来以下三个优势：
> 
> 1.  离线浏览 &#8211; 用户可在离线时浏览您的完整网站
> 2.  速度 &#8211; 缓存资源为本地资源，因此加载速度较快。
> 3.  服务器负载更少 &#8211; 浏览器只会从发生了更改的服务器下载资源。
> 
> 应用缓存（又称 AppCache）可让开发人员指定浏览器应缓存哪些文件以供离线用户访问。即使用户在离线状态下按了刷新按钮，您的应用也会正常加载和运行。

详细介绍：<a href="http://www.html5rocks.com/zh/tutorials/appcache/beginner/" target="_blank"><strong>http://www.html5rocks.com/zh/tutorials/appcache/beginner/</strong></a>

&nbsp;

### <span id="i-2">一些坑</span>

#### <span id="_mime_type">后缀与 mime type：</span>

上面的那篇文章说，缓存清单文件并没有标准的后缀名，你可以自定义一个后缀名并在你的 Web 服务器上指定 mime type。

例如：

<pre class="toolbar:2 lang:default decode:true">AddType text/cache-manifest .appcache</pre>

既然没有标准的后缀名，那我就偷懒了，一开始尝试的时候我直接用了 <span style="background-color: #eeeeee;">.txt</span> 格式。

Chrome 正常，iPhone 上的浏览器正常，但是 Android 手机上的浏览器不正常！

一开始我折腾了大半天，后来感觉会不会是 mime type 的问题？于是我设置了一下，后来就正常了！看上去一定要设置一下 mime type，不要偷懒！

那后缀名到底是什么呢？虽然说没有标准，但是我发现 tomcat 的配置中默认已经有了，默认是 <span style="background-color: #eeeeee;">.appcache</span> ，然后看到网上的教程也都是它，所以基本上已经达成共识了。

&nbsp;

#### <span id="i-3">请注意引用缓存清单的页面：</span>

在折腾的过程中，发现了一个很纠结的问题。

我的 <span style="background-color: #eeeeee;">index.html</span> 页面引用了一个 <span style="background-color: #eeeeee;">.css</span> 文件，和一个 <span style="background-color: #eeeeee;">.appcache</span> 文件，并把 <span style="background-color: #eeeeee;">.css</span> 文件加入了缓存清单中。诡异的是，<span style="background-color: #eeeeee;">index.html</span> 明明不在缓存清单中，却被缓存了起来。

那如果我的页面是一个动态网页怎么办？

查找相关资料后发现，这个页面一定要被缓存起来的，这不是 BUG，这是标准。

为何？因为这个功能是用来做离线应用的，不把这个页面缓存起来就不能离线了。

还好我们想做的是单页面应用程序，<span style="background-color: #eeeeee;">index</span> 页面本来就是不会动的，所以没有什么问题。

那如果你的页面是一个动态网页怎么办？

网上有这么几种方案，但感觉都不是很可取：

1.  动态输出 .appcache 缓存清单，实现缓存功能：<a href="http://www.sitesketch101.com/creating-a-dynamic-html5-cache-manifest/" target="_blank"><strong>http://www.sitesketch101.com/creating-a-dynamic-html5-cache-manifest/</strong></a>
2.  利用 iframe 事先动态页面的 Application Cache 功能：<a href="http://labs.ft.com/2012/11/using-an-iframe-to-stop-app-cache-storing-masters/" target="_blank"><strong>http://labs.ft.com/2012/11/using-an-iframe-to-stop-app-cache-storing-masters/</strong></a>

&nbsp;

具体怎么选，到底用不用，就需要你自己去抉择了。

&nbsp;

#### <span id="Android_PhoneGap">Android 下 PhoneGap 应用程序的问题：</span>

又是 Android 下，我在 iPhone 中，PhoneGap 跑起来后一点问题都没，上了 Android 就死活不成功。

最郁闷的是， Application Cache 会有几个事件，可以通过这几个事件判断 Application Cache 是否正常。在 Android 的浏览器下，功能是好的，事件也被正确触发了。

但是上了 PhoneGap 后，事件被正确地触发了，但是功能却总是有问题。

后来同样是在网上找到了解决方案：

<pre class="lang:java decode:true">public class HelloWorld extends DroidGap {
	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		// Set by &lt;content src="index.html" /&gt; in config.xml

		super.init();
		android.webkit.WebSettings settings = super.appView.getSettings();
		String appCachePath = this.getCacheDir().getAbsolutePath();
		settings.setAppCachePath(appCachePath);
		settings.setAllowFileAccess(true);
		settings.setAppCacheEnabled(true);

		// super.loadUrl(Config.getStartUrl());
		super.loadUrl("http://192.168.0.104:8080/cache/index.html");
	}
}</pre>

为什么要多加这些代码？因为 Android 中的 Web浏览器控件默认是禁用 Application Cache 功能的。加上以上代码后恢复正常。

可让我郁闷的是，PhoneGap 2.5 发布的时候，说自己修复了这个问题了。之前的版本的确需要手动开启 Application Cache，2.5中已经把这个问题修复了。可我在 2.6 中依然遇到了这个问题， 十分诡异…

&nbsp;

#### <span id="i-4">跨域：</span>

Application Cache 和 ajax 请求一样无法跨域，PhoneGap 中一般是用一个本地的 <span style="background-color: #eeeeee;">index</span> 文件，然后把类库也打包在本地，而一些业务的 <span style="background-color: #eeeeee;">js</span> 和经常变的 <span style="background-color: #eeeeee;">css</span> 就放在服务器上。这样的话，就遇到跨域的问题了，<span style="background-color: #eeeeee;">index</span> 文件和 <span style="background-color: #eeeeee;">.appcache</span> 文件不在同一个域下。

很纠结，很难解决，后来一想：打包在本地不就是为了缓存起来加快访问速度吗？Application Cache 也是解决同样的问题。既然有了 Application Cache，那为何还要把一些静态文件打包放在本地呢？

嗯，把整个网站都放到服务器上，包括 <span style="background-color: #eeeeee;">index.html</span> ，然后问题就解决了。

&nbsp;

#### <span id="_Application_Cache">禁用 Application Cache：</span>

在折腾的过程中，我想把缓存去掉了。于是我把 <span style="background-color: #eeeeee;">index.html</span> 中对缓存清单的引用去掉了，但是却没有效果！

后来仔细想了一下，浏览器更新的流程如下：

先缓存了 <span style="background-color: #eeeeee;">index.html</span> 和 <span style="background-color: #eeeeee;">.css</span> 文件，我把 index.html 中对缓存清单的引用去掉了，可是 <span style="background-color: #eeeeee;">.appcache</span> 文件还在服务器上。浏览器打开页面的时候直接去访问 <span style="background-color: #eeeeee;">.appcache</span> 文件，发现没有变更，就认为缓存没有更新了。

所以在这种场景下，修改<span style="background-color: #eeeeee;"> index.html</span> 是没有效果的，你必须把 <span style="background-color: #eeeeee;">.appcache</span> 删掉后才可以禁用 Application Cache。

&nbsp;

#### <span id="i-5">完整更新和二次刷新：</span>

下面说的是两个暂时无法解决的问题，是 Application Cache 的机制所决定的。

首先是完整更新的问题，如果你的缓存清单更新了，它会把清单里的所有静态文件下载一遍。虽然问题也不大，但是为何不能指定更新的文件呢？

可它的机制目前就是这样的，无解。

&nbsp;

另一个很郁闷的问题：如果你的缓存清单更新了，用户需要刷新2次后才能用到你最新的文件。

第一次刷新会更新缓存的文件，但是页面已经加载好之前的文件了，<span style="background-color: #eeeeee;">js</span> 也已经执行完了。

第二次刷新才会用到更新好的文件。

仔细想想这样做也是有道理的，因为不可能每次刷新都去等缓存清单加载后再去加载。加载完成后也不可能再把新的文件替换并执行，特别是 <span style="background-color: #eeeeee;">js</span> 。

其实这个问题也是有办法解决的，因为缓存更新完毕后会触发一个事件，可以在这个事件里提醒用户是否要刷新页面？或者直接强制刷新？总之这里的问题其实不会很大。
