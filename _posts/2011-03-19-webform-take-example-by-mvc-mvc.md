---
title: 那些 WebForm 可以从 MVC 借鉴的东西 —— MVC
author: Dozer
layout: post
permalink: /2011/03/webform-take-example-by-mvc-mvc/
categories:
  - 编程技术
tags:
  - AspDotNet
  - MVC
  - WebForm
---

### 前言

WebForm 可以从 MVC 中借鉴 MVC？放心，这并不是病句~

此 MVC 非彼 MVC！

MVC 其实是 Model, View, Controller 的意思，它是一种思想~

维基百科的解释：**<a href="http://zh.wikipedia.org/zh/MVC" target="_blank">传送门</a>**

<!--more-->

### MVC 和 三层架构的区别

个人觉得，MVC 中的 Model, View, Controller 三者和在一起，就成为了三层架构中的 Web 层，是三层架构中（Dal, BLL, Web）中 Web 层的再次分化。

曾经的 WebForm 是以页面为基本单位的，而在 MVC 中，并不一定是以页面为基本单位了，页面（View）只是控制器（Controller）在输出数据时用到的模板，所以他们并不一定是一一对应的，有时候同一个模板会被同好多次；同样，一个控制器也可以有选择性地使用不同的模板，他们之间没有必然联系。

只不过在默认情况下，一个 Action（一个 Controller 中会有多个 Action） 会对应了一个 View。

&nbsp;

所以，MVC 和三层架构 是可以一起使用的

&nbsp;

### 为什么要在 WebForm 中借鉴 MVC 的思想

前面说了，MVC 和 WebForm 最大的区别就是让后端代码和前端页面之间实现了更彻底的分离。

什么叫更彻底的分离？虽然 WebForm 中已经实现了分离，但是一张页面上的数据，只能在它的后台进行赋值。

这个主要体现在跨页面传递数据和子页面给母版页传值的问题上，给我们带来了很大的麻烦。

但在 MVC 中却不同，因为控制器和页面之间主要靠 ViewData 来传递数据。

&nbsp;

### 怎么在 WebForm 借鉴 MVC

其实，MVC 的优势主要在于有了 ViewData，那么只要在 WebForm 中实现这个功能即可。

这点不是很难，首先，你肯定不能再使用 Asp.net 的控件了（没人会用了吧？除非是一个很低劣的网站）

第二，你需要存放 ViewData

<pre class="brush:csharp">namespace Utility
{
    public class MasterPageHelper : MasterPage
    {
        protected IDictionary&lt;string, object&gt; ViewData
        {
            get
            {
                return
                    (Dictionary&lt;string, object&gt;)
                    (Session["ViewData"] ?? (Session["ViewData"] = new Dictionary&lt;string, object&gt;()));
            }
        }
        protected dynamic Model
        {
            get { return ViewData["Model"]; }
            set { ViewData["Model"] = value; }
        }
        protected void Page_Load(object sender, EventArgs e)
        {
            Unload += PageHelper_Unload;
        }
        void PageHelper_Unload(object sender, EventArgs e)
        {
            if (Session["ViewData"] == null) return;
            Session["ViewData"] = null;
            GC.Collect();
        }
    }
}</pre>

这里，我先自己继承了原来的 MasterPage, Page 和 UserController 类。

在创建页面的时候呢就继承自己的类。

&nbsp;

上面的代码中我做了什么呢？

其实，我就是在 Session 中分配了一块空间，用来存放 ViewData，并在页面呈现完毕后清空它。

仅此而已，非常简单~

但是，却实现了跨页面传递数据的功能。

因为页面继承了自己的类，所以在前端页面中，也可以直接访问到 ViewData 和 Model

&nbsp;

### 更多…

其实除了这个以外，MVC 中还有很多值得借鉴的地方，例如上面一篇文章提到的 Routing 功能。

结合这个，就可以模仿 MVC 那样，拥有类似 Controller & Action 的功能了
