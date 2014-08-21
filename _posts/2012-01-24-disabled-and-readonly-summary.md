---
title: disabled 和 readonly 总结
author: Dozer
layout: post
permalink: /2012/01/disabled-and-readonly-summary/
categories:
  - 编程技术
tags:
  - Asp.net
  - html
  - javascript
  - WebForm
---

### <span id="i">问题重现</span>

前段时间做网站遇到了一点纠结事，在下面两个场景出现了问题：

&nbsp;

#### <span id="disabled_readonly">disabled 和 readonly 的提交问题</span>

有一个 <a href="http://www.w3school.com.cn/htmldom/dom_obj_text.asp" target="_blank"><strong>text</strong></a> 类型的 <a href="http://www.w3school.com.cn/tags/tag_input.asp" target="_blank"><strong>input</strong></a>，用户无法直接提交内容，但是 js 会自动根据别的一些表单修改其中的内容。

也就是说，它的内容也是要被提交到后端的。

首先，当我把这个 input 设置成 <a href="http://www.w3school.com.cn/htmldom/prop_checkbox_disabled.asp" target="_blank"><strong>disabled</strong></a> 后竟然在 post 的时候就不提交了！

后来搜索之，原来通过用 <a href="http://www.w3school.com.cn/tags/att_input_readonly.asp" target="_blank"><strong>readonly</strong></a> 后就可以提交了，难道这么快就解决了？

于是，我就 happy 地签入了… 然后 QA 就来找我麻烦了… T.T

又是哪里出问题了呢？前面的问题是 html 和浏览器的标准决定的，在这方面已经解决了。但是为什么提交后，后端表单明明接收到了却还是出问题了呢？

<!--more-->

#### <span id="readonly_Aspnet">readonly 在 Asp.net 中的问题</span>

先说现象吧，同一个场景，我在前端会用 js 修改这个 text 的属性，所以提交的 value 和一开始的 value 会是不同的。

但是在 Asp.net 中出现了什么神奇的现象呢？

原来就算你在前端修改了这个 text ，就算 Asp.net 的底层，也就是 Request.Form 里接收到了这个值，就算看上去一切正常…

可是！Asp.net 不会把这个值赋给这个控件。也就是说，如果把一个 Asp.net 的控件属性设置成了 readonly ，就算你在前端修改了，它也依然是原来的值。

看上去很奇怪，但是仔细一想，微软在这块真的是太严谨了！什么是 readonly？ readonly 就是只读！

js 是不可信的，严格的来说我这里的确是不安全的。

> 所以，在这种场景下，我建议这么做：
> 
> 1.  既然这个属性是根据别的表单生成的，那后端也可以生成同样的东西，所以这段代码应该在后端再写一遍。*（任何前端验证都是不可靠的！）*
> 2.  前端虽然不会传回去，但是也要设置一下，让用户直观地看到。
> 3.  如果不考虑安全，可以从 Request.Form 里取值了。

&nbsp;

#### <span id="checkbox_radio_readonly">checkbox, radio 等控件无法设置 readonly 的问题</span>

类似的场景，只不过对象换成了 <a href="http://www.w3school.com.cn/htmldom/dom_obj_checkbox.asp" target="_blank"><strong>checkbox</strong></a>, **<a href="http://www.w3school.com.cn/htmldom/dom_obj_radio.asp" target="_blank">radio</a>**等控件。

我也需要用 js 修改这个 input ，但是不能让用户直接修改。

但这次在前端就出问题了，**因为 readonly 属性对很多控件无效！***（具体的可以看后面的总结）*

最搞笑的是，在 Chrome 里如果设置成 readonly 的话，它会变灰，但是却可以点！

> 解决方案：
> 
> 1.  设置成 disabled ，然后同样在后端写逻辑，生成正确的值。
> 2.  有时候无法生成逻辑，就是需要在后端取值，所以可以把这些控件的 onclick 事件重写成 return false; 这样就可以阻止事件冒泡了，用户点击就无效了。

&nbsp;

### <span id="i-2">总结</span>

看完几个场景的解决方法，其实只有了解原理后才能应付一切问题。

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td width="160" height="18">
      类型
    </td>
    
    <td width="230">
      如何禁用
    </td>
    
    <td width="249">
      如何只读
    </td>
  </tr>
  
  <tr>
    <td height="18">
      button
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      checkbox
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      onclick=&#8221;return false;&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      file
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      onclick=&#8221;return false;&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      hidden
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      password
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      radio
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      onclick=&#8221;return false;&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      reset
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      submit
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      text
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      textarea
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      readonly=&#8221;readonly&#8221;
    </td>
  </tr>
  
  <tr>
    <td height="18">
      select
    </td>
    
    <td>
      disabled=&#8221;disabled&#8221;
    </td>
    
    <td>
      onclick=&#8221;return false;&#8221;
    </td>
  </tr>
</table>

1.  disabled 标签对所有表单元素都有效，全都不会被提交。
2.  如果在前端给控件设置 readonly，或者 onclick=&#8221;return false&#8221; 后 Asp.net 可以接收到修改后的值。
3.  如果在 Asp.net 中设置了 readonly 属性后，后端无法接收到修改后的值。
