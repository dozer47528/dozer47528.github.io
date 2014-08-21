---
title: '[翻译] jQuery UI CSS Framework &#8211; Part1:Intro and How To Style a Button'
author: Dozer
layout: post
permalink: /2011/03/translate-jquery-ui-css-framework-part1-intro-and-how-to-style-a-button/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - CSS
  - html
  - jQuery
  - jQuery UI
---
原文链接：<a href="http://www.fbloggs.com/2010/01/20/the-jquery-ui-css-framework-part-1-intro-and-how-to-style-a-button/" target="_blank"><strong>传送门</strong></a>

&nbsp;

本文是 <a href="http://docs.jquery.com/UI/Theming/API" target="_blank"><strong>jQuery UI CSS Framework</strong></a> 系列文章的第一篇，这是一套强大的 CSS 选择器，你可以使用它来构建一套统一界面的 Web 应用程序。jQuery UI 的 DEMO 页面演示了很多 UI 部件（当然和 ExtJS 等比起来还是有差距的~），但是相对于你以前的工作方式和别的 UI 组件，它还是能帮到你许多的。这里，我们将解释一下这个框架，讲解一下它的优缺点，并用一个例子（一个 Button 的例子）来演示一下。

&nbsp;

**什么是 jQuery UI CSS Framework ？**

它是一套复合 jQuery UI 标准部件集的 CSS 选择器，可以很有效地帮助你设计自己的网页。

传送门：官方文档 <a href="http://docs.jquery.com/UI/Theming/API" target="_blank"><strong>http://docs.jquery.com/UI/Theming/API</strong></a>

<!--more-->

**jQuery UI CSS Framework 的优点 **

下面是我认为的优点：

1.  它为你处理设计难题：例如在做圆角的时候，只要标记一个 ”ui-corner-all” class 即可
2.  它为你提供一个一致的外观
3.  你可以使用它的 UI 部件（例如：tabs, dialog boxes, accordions 等），并获得相同的外观和体验
4.  UI 是一套皮肤，你可以在 <a href="http://jqueryui.com/themeroller/" target="_blank"><strong>这里</strong></a> 设计你自己的皮肤，并且可以非常容易地更换它（不用修改任何代码）

&nbsp;

**该框架的缺点**

1.  选择器没有很好的文档支持，你只能翻阅手册，或靠自己理解它真正的用处（因为它也仅仅是靠一个 class 来识别的）
2.  用 em 作为度量单位，而不是 px
3.  该框架并不完整，不是所有你想要的东西都可以被找到
4.  有时候你往往需要按照网上的例子做

&nbsp;

**如何了解这个框架？**

1.  你可以通过如下途径了解这个框架：
2.  阅读官方文档：**<a href="http://jqueryui.com/docs/Theming/API" target="_blank">传送门</a>**
3.  查看官方的例子，用 FireBug 等工具查看它们的用法
4.  查看论坛和相关书籍：<a href="http://book.douban.com/subject/4136994/" target="_blank"><strong>《jQuery UI 1.7》</strong></a>

&nbsp;

&nbsp;

**使用案例**

下面是一个简单的例子：

<pre class="brush:xml">&lt;button id="cancel" type="button"  class="ui-state-default ui-corner-all"&gt;Cancel&lt;/button&gt;</pre>

<table>
  <tr>
    <td>
      <a href="/wp-content/uploads/2011/03/uibuttonie.png"><img class="alignnone size-full wp-image-264" title="uibuttonie" alt="" src="/uploads/2011/03/uibuttonie.png" width="102" height="40" /></a>
    </td>
    
    <td>
      <a href="/wp-content/uploads/2011/03/uibuttonfirefox.png"><img class="alignnone size-full wp-image-263" title="uibuttonfirefox" alt="" src="/uploads/2011/03/uibuttonfirefox.png" width="111" height="37" /></a>
    </td>
    
    <td>
      <a href="/wp-content/uploads/2011/03/uibuttonchrome.png"><img class="alignnone size-full wp-image-262" title="uibuttonchrome" alt="" src="/uploads/2011/03/uibuttonchrome.png" width="123" height="39" /></a>
    </td>
  </tr>
  
  <tr>
    <td>
      IE 下的效果
    </td>
    
    <td>
      Firefox 下的效果
    </td>
    
    <td>
      Chrome 下的效果
    </td>
  </tr>
</table>

可以看到，我们很快捷地就创建了一个具有统一外观和圆角的按钮（虽然在 IE 下它没有显示出来…）

上面用到了2个 class，第一个代表这个按钮现在的状态（默认、悬停、按下 等），第二个是用来标记圆角的。

这里就是最简单的用法了，更多的 class 可以参考官方的文档。
