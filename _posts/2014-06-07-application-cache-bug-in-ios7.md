---
title: 使用 Application Cache 后在 iOS7 中出现的 bug
author: Dozer
layout: post
permalink: /2014/06/application-cache-bug-in-ios7/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658389
categories:
  - 编程技术
tags:
  - Application Cache
  - iOS
  - javascript
---
### history 对象失效

最近我们的站点准备正式上 Application Cache 了！

但是在测试的时候发现了一些问题，\`history.back()\`方法好像有点问题，\`history.length\`也永远是1。

后来搜了一下，找到了一篇文章：<a href="http://www.imore.com/ios-7-safari-features-and-bugs-html5-developers-need-be-aware" target="_blank">iOS 7 Safari: Features and bugs HTML5 developers need to be aware of</a>

里面提到了：

> If your app uses AppCache and you are managing state via hash or other mechanisms, the history object will never update, disabling history.back.

<!--more-->

这么“大”的 BUG 为什么 Apple 一直不修复呢？

因为它的出发需要几个条件：

1.  使用了单页面应用程序
2.  使用了 Application Cache
3.  使用了\`history.back()\`做后退功能

看上去很苛刻，但是这样的网站应该不少啊！

对了，这个 BUG 在 iOS8 中已经修复，但是 iOS7 现在是主流，所以还得修复。

&nbsp;

### 利用 url stack 来解决问题

这个问题怎么解决呢？

其实想想也很简单，关键就2点：

1.  捕捉页面跳转事件
2.  拦截\`history.back()\`方法

&nbsp;

最近看到一句话：Talk is cheap. Show me the code.

中文翻译特搞笑：屁话少说，放码过来。

好了，上代码：

<pre class="lang:js decode:true">var historyUrl = [];

window.addEventListener('hashchange', function() {
    historyUrl.push(location.hash);
    
    //历史记录太多的话删掉一点，数量自己控制
    if (historyUrl.length &gt; 10) {
        historyUrl.shift();
    }
    console.log(historyUrl);
});

history.back = function() {
    if (historyUrl.length &lt; 2) {
        location.hash = 'index';
        return;
    }

    historyUrl.pop();
    var hash = historyUrl.pop();
    location.hash = hash;
}</pre>

解决起来还是非常简单的！
