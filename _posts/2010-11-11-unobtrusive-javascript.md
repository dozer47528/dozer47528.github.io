---
title: Unobtrusive JavaScript in ASP.NET MVC 3
author: Dozer
layout: post
permalink: /2010/11/unobtrusive-javascript/
categories:
  - 编程技术
tags:
  - javascript
  - MVC
  - 数据验证
---

### Unobtrusive JavaScript 是什么？

<pre class="brush:xml">&lt;!--以下是常规Javascript下写出来的Ajax--&gt;
&lt;div id="test"&gt;
    &lt;a href="/" onclick="Sys.Mvc.AsyncHyperlink.handleClick(this, new Sys.UI.DomEvent(event), { insertionMode: Sys.Mvc.InsertionMode.replace, httpMethod: 'GET', updateTargetId: 'test' });"&gt;测试&lt;/a&gt;
&lt;/div&gt;

&lt;!--以下是Unobtrusive Javascript下写出来的Ajax--&gt;
&lt;div id="test"&gt;
    &lt;a data-ajax="true" data-ajax-method="GET" data-ajax-mode="replace" data-ajax-update="#test" href="/"&gt;测试&lt;/a&gt;
&lt;/div&gt;</pre>

以上的代码分别是 MVC 3 在“关闭”和“开启” Unobtrusive JavaScript 后生成的 Ajax.ActionLink。

那 Unobtrusive JavaScript到 底是什么呢？简单地来说，就是一种代码分离的思想，把行为层和表现层分离开。

&nbsp;

具体的可以查看维基百科下对 <a href="http://en.wikipedia.org/wiki/Unobtrusive_JavaScript" target="_blank"><strong>Unobtrusive JavaScript</strong></a> 的解释。

<!--more-->

&nbsp;

### Unobtrusive JavaScriptin ASP.NET MVC 3

&nbsp;

Unobtrusive JavaScript 的好处显而易见，但是如何在MVC3使用Unobtrusive JavaScript呢？

**1、引用相应的Javascript文件**

&nbsp;

<pre class="brush:xml">&lt;script src="@Url.Content("~/Scripts/jquery-1.4.1.min.js")" type="text/javascript"&gt;&lt;/script&gt;
&lt;script src="@Url.Content("~/Scripts/jquery.unobtrusive-ajax.min.js")" type="text/javascript"&gt;&lt;/script&gt;
&lt;script src="@Url.Content("~/Scripts/jquery.validate.min.js")" type="text/javascript"&gt;&lt;/script&gt;
&lt;script src="@Url.Content("~/Scripts/jquery.validate.unobtrusive.min.js")" type="text/javascript"&gt;&lt;/script&gt;</pre>

&nbsp;

这四个文件包含在 MVC 3 的 Scripts 文件夹中，直接引用即可。

值得注意的是：jquery.unobtrusive-ajax.min.js 和 jquery.validate.unobtrusive.min.js 是两个用来让 jquery 支持 Unobtrusive JavaScript 的库。

在 jQuery 官网上看不到，打开后发现，原来是微软自己写的。

另外，以前用来实现 MVC Ajax 和客户端验证的三个文件 MicrosoftAjax, MicrosoftMvcAjax.js, MicrosoftMvcValidation.js 不需要再引用了。

原因就是因为，微软在 MVC 3 使用 jQuery 来实现 Ajax 了，而上面两个 javascript 库就相当于是两个 <a href="http://zh.wikipedia.org/zh/%E9%80%82%E9%85%8D%E5%99%A8%E6%A8%A1%E5%BC%8F" target="_blank"><strong>Adapter（适配器）</strong></a>

&nbsp;

**2、开启 Unobtrusive JavaScript**

MVC3中的Web.Config文件中默认多了两个配置项

这里是一个全局设置，你可以打开或者关闭。

<img class="alignnone size-full wp-image-100" title="uj1" alt="uj1" src="/uploads/2011/01/uj1.png" width="439" height="88" />

另外，你也可以在任何一个 Action 或 Controller 中执行以下代码，灵活地进行控制，来处理一些特殊的 Action 或 Controller。

&nbsp;

<pre class="brush:csharp">HtmlHelper.ClientValidationEnabled = true;
HtmlHelper.UnobtrusiveJavaScriptEnabled = true;</pre>

&nbsp;

&nbsp;

**3、如果不需要用 Unobtrusive JavaScript 呢？**

如果不需要用的话根据上面的方法关闭即可。

但是要注意一点！这时候，如果你需要用 Ajax 或者客户端验证，务必引用MVC3以前版本中的三个 javascript文件：MicrosoftAjax, MicrosoftMvcAjax.js, MicrosoftMvcValidation.js

否则就不能实现Ajax 和客户端验证了。

&nbsp;

&nbsp;

### Unobtrusive Ajax in ASP.NET MVC 3

原文：<a href="http://bradwilson.typepad.com/blog/2010/10/mvc3-unobtrusive-ajax.html" target="_blank"><strong>《Unobtrusive Ajax in ASP.NET MVC 3》</strong></a>

&nbsp;

**关于 AjaxOptions**

MVC 中 AjaxHelper 的扩展方法，提供了一系列的 Ajax 方法，例如：ActionLink RouteLink, BeginForm, BeginRouteForm 等。它们的使用方法和 HtmlHelper很像，主要的区别就在于 AjaxHelper 有一个 AjaxOptions 参数。

&nbsp;

<pre class="brush:csharp">public class AjaxOptions {
    public string Confirm { get; set; }
    public string HttpMethod { get; set; }
    public InsertionMode InsertionMode { get; set; }
    public int LoadingElementDuration { get; set; }
    public string LoadingElementId { get; set; }
    public string OnBegin { get; set; }
    public string OnComplete { get; set; }
    public string OnFailure { get; set; }
    public string OnSuccess { get; set; }
    public string UpdateTargetId { get; set; }
    public string Url { get; set; }
}</pre>

&nbsp;

这些属性会告诉 MVC 如何生成你的 Ajax 代码。

&nbsp;

**传统的生成方式**

当 unobtrusive 模式被关闭的时候，MVC 会把代码写在你的 <a> 标签或者 <form> 标签中，并且靠 MicrosoftAjax.js 和 MicrosoftMvcAjax.js 来执行相应的代码。

&nbsp;

<pre class="brush:xml">&lt;form
    action="/ajax/callback"
    id="form0"
    method="post"
    onclick="Sys.Mvc.AsyncForm.handleClick(this, new Sys.UI.DomEvent(event));"
    onsubmit="Sys.Mvc.AsyncForm.handleSubmit(this, new Sys.UI.DomEvent(event), { insertionMode: Sys.Mvc.InsertionMode.replace, loadingElementId: 'loading', updateTargetId: 'updateme' });"&gt;</pre>

&nbsp;

MVC1 和 MVC2 中就是这样做的。

&nbsp;

**依赖于 Unobtrusive JavaScript 的生成方式**

当 unobtrusive 模式打开的时候，代码彻底的改变了，而且是那么地简洁！

&nbsp;

<pre class="brush:xml">&lt;form
    action="/ajax/callback"
    data-ajax="true"
    data-ajax-loading="#loading"
    data-ajax-mode="replace"
    data-ajax-update="#updateme"
    method="post"&gt;</pre>

&nbsp;

你会发现这些HTML代码是非常容易读懂的。

&nbsp;

**映射AjaxOptions属性**

下表列出了 AjaxOptions 和 HTML 5 的映射关系

<table border="1" cellspacing="0" cellpadding="4">
  <tr>
    <th>
      AjaxOptions
    </th>
    
    <th>
      HTML attribute
    </th>
  </tr>
  
  <tr>
    <td>
      Confirm
    </td>
    
    <td>
      data-ajax-confirm
    </td>
  </tr>
  
  <tr>
    <td>
      HttpMethod
    </td>
    
    <td>
      data-ajax-method
    </td>
  </tr>
  
  <tr>
    <td>
      InsertionMode
    </td>
    
    <td>
      data-ajax-mode *
    </td>
  </tr>
  
  <tr>
    <td>
      LoadingElementDuration
    </td>
    
    <td>
      data-ajax-loading-duration **
    </td>
  </tr>
  
  <tr>
    <td>
      LoadingElementId
    </td>
    
    <td>
      data-ajax-loading
    </td>
  </tr>
  
  <tr>
    <td>
      OnBegin
    </td>
    
    <td>
      data-ajax-begin
    </td>
  </tr>
  
  <tr>
    <td>
      OnComplete
    </td>
    
    <td>
      data-ajax-complete
    </td>
  </tr>
  
  <tr>
    <td>
      OnFailure
    </td>
    
    <td>
      data-ajax-failure
    </td>
  </tr>
  
  <tr>
    <td>
      OnSuccess
    </td>
    
    <td>
      data-ajax-success
    </td>
  </tr>
  
  <tr>
    <td>
      UpdateTargetId
    </td>
    
    <td>
      data-ajax-update
    </td>
  </tr>
  
  <tr>
    <td>
      Url
    </td>
    
    <td>
      data-ajax-url
    </td>
  </tr>
</table>

除了这些属性外，还有一个额外的 data-ajax=&#8221;true&#8221; 属性，代表这是一个 Ajax 方法。

* = data-ajax-mode 只有在设置 UpdateTargetId 被设置后才有效。

** = data-ajax-loading-duration 只有在 LoadingElementId 被设置后才有效。

&nbsp;

**Ajax 回调**

传统 Ajax 和 unobtrusive JavaScript 的主要区别就在于 Ajax 的回调。当所有的回调函数都被定义在 Ajax 库中以后，你的代码就会变成这种理想化的风格。

当你在 MVC 3 中使用 unobtrusive Ajax 的时候，四个基本的回调函数会被因设为 jQuery.Ajax 的函数。

&nbsp;

*OnBegin => “beforeSend”*

*OnComplete => “complete”*

*OnFailure => “error”*

*OnSuccess = > “success”*

&nbsp;

你可以给他们传递一个函数名，或一段匿名函数作为处理函数。

如果你的处理函数是一个函数名，并且参数列表符合Ajax标准，那么 jQuery.Ajax 便会把值传递给这个函数并执行。

如果是匿名函数的话，过程大同小异。

&nbsp;

Ajax 回调函数的参数列表：

xhr : XMLHttpRequest 对象

status : 仅限 OnBegin

error : 仅限 OnFailure

data : 仅限 OnSuccess

&nbsp;

&nbsp;

### Unobtrusive Client Validation in ASP.NET MVC 3

原文：**<a href="http://bradwilson.typepad.com/blog/2010/10/mvc3-unobtrusive-validation.html" target="_blank">《Unobtrusive Client Validation in ASP.NET MVC 3》</a>**

&nbsp;

**传统的生成方式**

一下是 **<a href="/2010/04/mvc-dataannotations/" target="_blank">MVC 数据验证</a>**框架下对于 Model 的描述（这部分不变）

&nbsp;

<pre class="brush:csharp">public class ValidationModel {
    [Required]
    public string FirstName { get; set; }

    [Required, StringLength(60)]
    public string LastName { get; set; }

    [Range(1, 130)]
    public int Age { get; set; }
}</pre>

&nbsp;

&nbsp;

当开启客户端验证后：（具体开启方法和 Unobtrusive Javascript 大同小异，请看第二部分）

&nbsp;

<pre class="brush:xml">&lt;label for="FirstName"&gt;FirstName&lt;/label&gt;
&lt;input class="text-box single-line" id="FirstName" name="FirstName" type="text" value="" /&gt;
&lt;span class="field-validation-valid" id="FirstName_validationMessage"&gt;&lt;/span&gt;

&lt;label for="LastName"&gt;LastName&lt;/label&gt;
&lt;input class="text-box single-line" id="LastName" name="LastName" type="text" value="" /&gt;
&lt;span class="field-validation-valid" id="LastName_validationMessage"&gt;&lt;/span&gt;

&lt;label for="Age"&gt;Age&lt;/label&gt;
&lt;input class="text-box single-line" id="Age" name="Age" type="text" value="" /&gt;
&lt;span class="field-validation-valid" id="Age_validationMessage"&gt;&lt;/span&gt;

&lt;script type="text/javascript"&gt;
//&lt;![CDATA[
if (!window.mvcClientValidationMetadata) { window.mvcClientValidationMetadata = []; }
window.mvcClientValidationMetadata.push({"Fields":[{"FieldName":"FirstName","ReplaceValidationMessageContents":true,"ValidationMessageId":"FirstName_validationMessage","ValidationRules":[{"ErrorMessage":"The FirstName field is required.","ValidationParameters":{},"ValidationType":"required"}]},{"FieldName":"LastName","ReplaceValidationMessageContents":true,"ValidationMessageId":"LastName_validationMessage","ValidationRules":[{"ErrorMessage":"The LastName field is required.","ValidationParameters":{},"ValidationType":"required"},{"ErrorMessage":"The field LastName must be a string with a maximum length of 60.","ValidationParameters":{"max":60},"ValidationType":"length"}]},{"FieldName":"Age","ReplaceValidationMessageContents":true,"ValidationMessageId":"Age_validationMessage","ValidationRules":[{"ErrorMessage":"The field Age must be between 1 and 130.","ValidationParameters":{"min":1,"max":130},"ValidationType":"range"},{"ErrorMessage":"The Age field is required.","ValidationParameters":{},"ValidationType":"required"},{"ErrorMessage":"The field Age must be a number.","ValidationParameters":{},"ValidationType":"number"}]}],"FormId":"form0","ReplaceValidationSummary":true,"ValidationSummaryId":"validationSummary"});
//]]&gt;
&lt;/script&gt;</pre>

&nbsp;

当 unobtrusive JavaScript 关闭后，你会看到以上代码（和 MVC 2 中相同）。

你会发现在后面多了一段 Javascript 代码，而这里，便是对表单验证的核心。

&nbsp;

**依赖于 Unobtrusive JavaScript 的生成方式**

开启 Unobtrusive Javascript 后，代码完全改变了

&nbsp;

<pre class="brush:xml">&lt;label for="FirstName"&gt;FirstName&lt;/label&gt;
&lt;input class="text-box single-line" data-val="true" data-val-required="The FirstName field is required." id="FirstName" name="FirstName" type="text" value="" /&gt;
&lt;span class="field-validation-valid" data-valmsg-for="FirstName" data-valmsg-replace="true"&gt;&lt;/span&gt;

&lt;label for="LastName"&gt;LastName&lt;/label&gt;
&lt;input class="text-box single-line" data-val="true" data-val-length="The field LastName must be a string with a maximum length of 60." data-val-length-max="60" data-val-required="The LastName field is required." id="LastName" name="LastName" type="text" value="" /&gt;
&lt;span class="field-validation-valid" data-valmsg-for="LastName" data-valmsg-replace="true"&gt;&lt;/span&gt;

&lt;label for="Age"&gt;Age&lt;/label&gt;
&lt;input class="text-box single-line" data-val="true" data-val-number="The field Age must be a number." data-val-range="The field Age must be between 1 and 130." data-val-range-max="130" data-val-range-min="1" data-val-required="The Age field is required." id="Age" name="Age" type="text" value="" /&gt;
&lt;span class="field-validation-valid" data-valmsg-for="Age" data-valmsg-replace="true"&gt;&lt;/span&gt;</pre>

&nbsp;

其中最大的改变就是下面的 Javascript 代码消失了，转而变为 HTML 5 的各种属性。

&nbsp;

**属性是如何生成的**

当表单中的一项在后端代码中有数据验证的时候，MVC 会现在 它的属性中加上 data-val=&#8221;true&#8221;，并且讲所有规则以 data-val-rulename=&#8221;message&#8221; 的形式，加在属性上。

如果想使用默认的客户端验证信息，你只要把属性值留空，那么客户端验证会自动生成形如 data-val-rulename-paramname=&#8221;paramvalue&#8221; 的属性。

&nbsp;

**桥接 HTML 和 jQuery ： 适配器**

写一个客户端验证有两个步骤：1、为 jQuery 验证编写验证规则，2、在 HTML 代码中加上属性，并且使用适配器转换为对应的 jQuery 验证规则。（这个在非 MVC 中也适用）

你可以调用 jQuery.validator.unobtrusive.adapters. 来编写适配规则。

这里有三个方法能帮助你注册三种很常规的适配器。(addBool, addSingleVal, and addMinMax)

*具体的方法大家可以看一下原文，因为 jquery.validate.unobtrusive.min.js 已经把这些适配规则都写好了，所以不加以阐述了，如果想了解原理的话可以去看一下~*

&nbsp;

&nbsp;

### ENDING

最后，还不太了解 MVC 数据验证的朋友可以看一下我的另一篇文章：**<a href="/2010/04/mvc-dataannotations/" target="_blank">深入浅出 MVC 数据验证 2.0 [附演示源码]</a>**
