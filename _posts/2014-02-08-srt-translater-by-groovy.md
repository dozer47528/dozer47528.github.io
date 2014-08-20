---
title: Groovy 版字幕批量翻译脚本
author: Dozer
layout: post
permalink: /2014/02/srt-translater-by-groovy/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658382
categories:
  - 编程技术
tags:
  - github
  - Google
  - groovy
  - java
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#Google_Translate_Toolkit"><span class="toc_number toc_depth_1">1</span> Google Translate Toolkit</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 思路</a>
    </li>
    <li>
      <a href="#Groovy"><span class="toc_number toc_depth_1">3</span> Groovy</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">4</span> 源代码</a>
    </li>
  </ul>
</div>

### <span id="Google_Translate_Toolkit">Google Translate Toolkit</span>

2013年在线教育很火啊，从没有资源到不知道怎么选资源…

其中 <a href="https://www.coursera.org/" target="_blank"><strong>Coursera</strong> </a>做的真的很棒，最赞的是，提供了视频和字幕的下载。

但是E文不好，想在地铁上用 iPad 看的话会很不方便，如果有翻译多好~

<!--more-->

&nbsp;

搜索了一下，先是找到了这个：

http://translate.google.com/toolkit

直接上传字幕文件就可以翻译了！赞！

&nbsp;

但是不能批量处理，而且是机器翻译的，专业课程翻译不是最好，如果能有中英对照的字幕那就更赞了！

既然它不支持，只能自动动手丰衣足食了。

&nbsp;

### <span id="i">思路</span>

最近正好用 Groovy 用得比较爽，而且它可以直接写 script，一个文件就可以了。

程序逻辑很简单，一行行分析字幕，如果发现是文本就调用翻译接口翻译，然后把翻译好的内容添加在原字幕的下面即可。

翻译 API 怎么办？Google Translate API 已经不再免费了，Bing Translate API 有5000/每月的限制，完全不够用啊！

后来经过网友启发，发现 Google Translate 网页版在翻译的时候其实只是调用一次 GET 请求，参数也很简单，而且没有任何身份认证！

那就… 拿来当接口用呗！

&nbsp;

### <span id="Groovy">Groovy</span>

用惯了 C# 后写 Java 真的很痛苦，但是遇到 Groovy 后一切都变了！

期间遇到了一个难题，上述接口毕竟不是专门的接口，所以它返回的不是标准的 json，它返回的竟然是 js ！

<pre class="lang:js decode:true">[[["你好世界","Hello World","Nǐ hǎo shìjiè",""]],,"en",,[["你好",[1],false,false,867,0,1,0],["世界",[2],false,false,867,1,2,0]],[["Hello",1,[["你好",867,false,false],["您好",102,false,false],["打招呼",0,false,false],["招呼",0,false,false],["啰",0,false,false]],[[0,5]],"Hello World"],["World",2,[["世界",867,false,false],["全球",0,false,false],["世",0,false,false],["国际",0,false,false],["的世界",0,false,false]],[[6,11]],""]],,,[["en"]],2]</pre>

一开始想办法用文本解析，但是还要处理各种转义符，非常麻烦。

后来想到既然 Groovy 可以动态执行代码，为何不当它是 Groovy 代码执行？上面不就是声明了一个数组嘛，语法和 Groovy 里的一样。

<pre class="lang:java decode:true">def result = Eval.me(html)</pre>

然后就这样一行代码解决了。

但是上面有用多个逗号代表空元素的语法 Groovy 不支持，所以只能用正则表达式替换掉了。

<pre class="lang:java decode:true ">html = html.replaceAll(/,+/, ",")</pre>

&nbsp;

### <span id="i-2">源代码</span>

最后直接贴上项目地址：<a href="https://github.com/dozer47528/srt-translater" target="_blank">https://github.com/dozer47528/srt-translater</a>

我下载了一个课程，并用它批量转换了所有字幕！