---
title: 关于一个2.0下实现扩展方法所引发的错误
author: Dozer
layout: post
permalink: /2011/12/the-error-of-extensionattribute/
categories:
  - 编程技术
tags:
  - DotNet
  - CSharp
---

### <span id="i">错误产生环境及非完美解决办法</span>

错误提示：<span style="color: #ff0000;">缺少编译器要求的成员“System.Runtime.CompilerServices.ExtensionAttribute..ctor”</span>

这个错误真的非常诡异，因为双击这个错误的时候无法定位到出错的地方。

而且这个错误实在是非常不明确。

其实，产生这个错误的人大部分是因为引用了 Newtonsoft.Json.Net20.dll 这个类库。

网上简单的解决方式是：“删除 Newtonsoft.Json.Net20.dll 后重新引用”

<!--more-->

### <span id="i-2">问题产生的原因</span>

既然是这个类库导致的，那当然要研究下这个类库啦。

Google 后发现其实老外早有研究过了：

**<a href="http://stackoverflow.com/questions/205644/error-when-using-extension-methods-in-c-sharp" target="_blank">http://stackoverflow.com/questions/205644/error-when-using-extension-methods-in-c-sharp</a>**

&nbsp;

**那我在这里其实也就是翻译加解释一下：**

产生这个错误的根本原因是：

这个类库是写给 2.0 的程序用的，而 2.0 中并没有扩展方法，但这个类库又想用扩展来写。

所以他自己编写了一个 Attribute 来实现了扩展方法

（具体实现方法：<a href="http://msdn.microsoft.com/en-us/magazine/cc163317.aspx#S7" target="_blank"><strong>http://msdn.microsoft.com/en-us/magazine/cc163317.aspx#S7</strong></a>）

<pre class="brush:csharp">namespace System.Runtime.CompilerServices
{
    /// &lt;remarks&gt;
    /// This attribute allows us to define extension methods without
    /// requiring .NET Framework 3.5. For more information, see the section,
    /// &lt;a href="http://msdn.microsoft.com/en-us/magazine/cc163317.aspx#S7"&gt;Extension Methods in .NET Framework 2.0 Apps&lt;/a&gt;,
    /// of &lt;a href="http://msdn.microsoft.com/en-us/magazine/cc163317.aspx"&gt;Basic Instincts: Extension Methods&lt;/a&gt;
    /// column in &lt;a href="http://msdn.microsoft.com/msdnmag/"&gt;MSDN Magazine&lt;/a&gt;,
    /// issue &lt;a href="http://msdn.microsoft.com/en-us/magazine/cc135410.aspx"&gt;Nov 2007&lt;/a&gt;.
    /// &lt;/remarks&gt;

    [AttributeUsage(AttributeTargets.Method | AttributeTargets.Class | AttributeTargets.Assembly)]
    internal sealed class ExtensionAttribute : Attribute { }
}</pre>

其实扩展方法是一个编译器的功能，VS2008开始支持，并不影响 IL 代码，所以通过这个方法就可以在 2.0 中使用扩展方法了。

因为这个 Attribute 在 .net 3.0 中是已经存在的，所以当你在 3.0 的程序中引用了 Newtonsoft.Json.Net20.dll，就会出现冲突了。

&nbsp;

### <span id="i-3">解决办法</span>

1.  <span class="Apple-style-span" style="line-height: 18px;">在 3.0 或以上的程序中引用高版本的 Newtonsoft.Json.Net20.dll</span>
2.  <span class="Apple-style-span" style="line-height: 18px;">删除 Newtonsoft.Json.Net20.dll 的引用后重新引用（如果你担心升级 dll 会出现问题的话，可以采用这招，但在编译的时候会不定时出错）</span>
3.  <del><span class="Apple-style-span" style="line-height: 18px;">尝试自己修改它的源代码，例如修改这个 Attribute 的命名空间等，但最终还是失败了，发现是行不通的。</span></del>
