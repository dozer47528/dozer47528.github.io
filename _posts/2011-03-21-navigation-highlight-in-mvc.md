---
title: MVC 下导航高亮的完美解决方案
author: Dozer
layout: post
permalink: /2011/03/navigation-highlight-in-mvc/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - javascript
  - MVC
  - 导航
---

### <span id="i">前言</span>

导航高亮一直是一个让大家头疼的问题。

&nbsp;

纯 Javascript 的话可以判断当前页面的地址和链接地址是否有关系。

这样的弊端就是自由度太低，MVC 下会出一定的问题 （MVC 下有默认的 Controller 和 Action）

&nbsp;

另一种方案是前端后端结合，为每一张页面设置一个属性，然后在页面中判断。满足条件便高亮。

这样的弊端就是，需要为你所有的页面设置属性，非常麻烦！

&nbsp;

那么有没有什么完美的解决方案？一劳永逸的？

<!--more-->

### <span id="_eval">神奇的 eval 函数</span>

Javascript 有精粹也有糟粕，其中的 eval 是大多数动态语言都拥有的精髓。我们是否可以利用这个函数呢？

**基本思路：**

给每一个 li（对应一个链接）设置一个 class，例如 class=&#8221;controller_Home&#8221;，

代表着，只要这张页面是的 controller 是 Home，就让这个链接高亮。

而在页面中，是可以通过代码直接得到 controller 和 action 的名称的，没必要为每一张页面单独手动设置。

&nbsp;

### <span id="i-2">解决方案</span>

<pre class="brush:xml">&lt;ul id="top-navigation"&gt;
    &lt;li class="controller_Home"&gt;&lt;span&gt;&lt;span&gt;@Html.ActionLink("首页","Index","Home")&lt;/span&gt;&lt;/span&gt;&lt;/li&gt;
    &lt;li class="controller_Article"&gt;&lt;span&gt;&lt;span&gt;@Html.ActionLink("文章管理","Index","Article")&lt;/span&gt;&lt;/span&gt;&lt;/li&gt;
    &lt;li class="controller_User"&gt;&lt;span&gt;&lt;span&gt;@Html.ActionLink("用户管理","Index","User")&lt;/span&gt;&lt;/span&gt;&lt;/li&gt;
&lt;/ul&gt;
&lt;input id="controller" type="hidden" value="@Html.ViewContext.RouteData.Values["controller"]"/&gt;
&lt;input id="action" type="hidden" value="@Html.ViewContext.RouteData.Values["action"]"/&gt;</pre>

**View 中的代码如上所示：**

1.  首先给所有的 li 加上一个 class
2.  然后再利用两个 hidden ，把 controller 和 action 的名字放到前端页面中

&nbsp;

<pre class="brush:js">$(function () {
    SetNavClass('mainNav', 'active');
});

function SetNavClass(ulId, className) {
    var controller = $('#controller').val();
    var action = $('#action').val();
    eval('controller_' + controller + ' = true');
    eval('action_' + action + ' = true');
    list = $('#' + ulId + ' *');

    for (var k = 0; k &lt; list.length; k++) {
        item = list[k];
        str = GetClassName(item).toLowerCase();
        try {
            if (eval(str)) $(item).addClass(className);
        } catch (e) { }
    }
}
function GetClassName(item) {
    var classStr = $(item).attr('class');
    if (classStr == null) return "";
    classes = classStr.split(' ');
    for (var k = 0; k &lt; classes.length; k++) {
        if (classes[k].indexOf('controller') &gt; -1 || classes[k].indexOf('action') &gt; -1) return classes[k];
    }
}</pre>

**以上是 Javascript 的代码：**

1.  读取 controller 和 action 的名字
2.  利用 eval 函数给 controller\_[controller名字] 和 action\_[action名字] 这两个变量赋值
3.  取出 class 中的表达式
4.  利用 eval 函数执行表达式，判断最后的结果，如果满足条件就加上高亮的 class

&nbsp;

上述代码不需要为每个页面编写，只需要在母版页中编写一次即可，再引用这段 Javascript 函数。

如果你的 ul ID 和 高亮 class 名字不一样，那么只要在调用这个函数的时候传入你自己的就行了。

&nbsp;

### <span id="i-3">高级应用</span>

就这么简单？仅此而已？

如果真的是这样，那么完全可以直接利用 Javascript 判断页面地址来实现。

那么让我们来玩一些好玩的吧~

因为是 eval 函数，所以完全可以在这个 class 中编写复杂的表达式（其实就是 Javascript 表达式）

&nbsp;

<pre class="brush:xml">&lt;li class="controller_Home||controller_About"&gt;&lt;span&gt;&lt;span&gt;@Html.ActionLink("首页", "Index", "Home")&lt;/span&gt;&lt;/span&gt;&lt;/li&gt;
&lt;li class="controller_Article&&action_Add"&gt;&lt;span&gt;&lt;span&gt;@Html.ActionLink("文章管理", "Index", "Article")&lt;/span&gt;&lt;/span&gt;&lt;/li&gt;</pre>

**以上两行代码表示：**

1.  controller 只要是 Home，或者 About，都会激活这个链接
2.  controller 必须是 Article，action 必须是 Add

&nbsp;

也就是说，在这个 class 里可以输入复杂的 Javascript，这样就可以实现复杂的导航激活功能了！
