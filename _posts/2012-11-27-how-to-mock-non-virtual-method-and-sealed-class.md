---
title: 如何 Mock 非虚方法和密封类？
author: Dozer
layout: post
permalink: /2012/11/how-to-mock-non-virtual-method-and-sealed-class/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658351
categories:
  - 编程技术
tags:
  - Mock
  - non-virtual
  - sealed
  - 单元测试
  - 密封类
  - 非虚函数
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 问题</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 寻找</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 实现思路和技术细节</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">4</span> 具体实现步骤</a><ul>
        <li>
          <a href="#i-5"><span class="toc_number toc_depth_2">4.1</span> 源代码解决方案结构</a>
        </li>
        <li>
          <a href="#MockHelper"><span class="toc_number toc_depth_2">4.2</span> MockHelper 的使用</a>
        </li>
        <li>
          <a href="#_MockHelper"><span class="toc_number toc_depth_2">4.3</span> 配置自动运行 MockHelper</a>
        </li>
        <li>
          <a href="#i-6"><span class="toc_number toc_depth_2">4.4</span> 编写测试代码</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-7"><span class="toc_number toc_depth_1">5</span> 注意事项</a><ul>
        <li>
          <a href="#_Moq_Mock"><span class="toc_number toc_depth_2">5.1</span> 一定要用 Moq 等 Mock 框架</a>
        </li>
        <li>
          <a href="#_MSTest"><span class="toc_number toc_depth_2">5.2</span> 注意配置一下 MSTest</a>
        </li>
        <li>
          <a href="#i-8"><span class="toc_number toc_depth_2">5.3</span> 所有测试框架都支持吗？</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-9"><span class="toc_number toc_depth_1">6</span> 最后</a>
    </li>
    <li>
      <a href="#i-10"><span class="toc_number toc_depth_1">7</span> 缺陷</a>
    </li>
  </ul>
</div>

### <span id="i">问题</span>

很常见的问题，没有接口，那如何 <a href="http://zh.wikipedia.org/wiki/%E6%A8%A1%E6%8B%9F%E5%AF%B9%E8%B1%A1" target="_blank"><strong>Mock</strong></a> 非虚方法和<a href="http://msdn.microsoft.com/zh-cn/library/ms173150(v=vs.80).aspx" target="_blank"><strong>密封类</strong></a>？

我在上一篇文章（<a title="单元测试有感" href="/2012/11/thinking-in-unit-test/" target="_blank"><strong>单元测试有感</strong></a>）中介绍了单元测试的原则，也提到了一些技巧，但是代码是以前写的，总会有很多不能克服的地方，还有也不可能把所有的方法改成 <span style="background-color: #eeeeee;">vitrual </span>，或者所有的类都有接口。

&nbsp;

### <span id="i-2">寻找</span>

一开始搜索：mock non-virtual ，找到了一篇文章：<a href="http://stackoverflow.com/questions/1073684/mocking-non-virtual-methods-in-c-sharp" target="_blank"><strong>传送门</strong></a>

文中提到了一个神器：<a href="http://www.typemock.com/" target="_blank"><strong>Typemock</strong></a>，貌似它可以实现，但是它是收费的…

大致看了看它的原理，和 <a href="http://www.sharpcrafters.com/" target="_blank"><strong>PostSharp</strong> </a>（PostSharp是用来做 <a href="http://zh.wikipedia.org/wiki/%E9%9D%A2%E5%90%91%E4%BE%A7%E9%9D%A2%E7%9A%84%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1" target="_blank"><strong>AOP</strong></a> 的）差不多，都是会去修改编译完成的 dll 文件，简单粗暴！

虽然粗暴，但貌似的确是一个不错的方法，别的项目正常编译，Test 项目中为了测试，把所有的方法加上 Virtual 关键字，这样不就行了吗？

思路是清晰了，可惜工具都是收费了，直到看到了<a href="http://blog.zhaojie.me/" target="_blank"><strong>老赵的博客</strong></a>。

*   <a href="http://blog.zhaojie.me/2012/01/make-things-mockable-with-mono-cecil.html" target="_blank">http://blog.zhaojie.me/2012/01/make-things-mockable-with-mono-cecil.html</a>
*   <a href="http://www.findex.cn/item.php?id=421685" target="_blank">http://www.findex.cn/item.php?id=421685</a>

上面的链接是老赵的原文，可惜他好像误操作，被另一篇文章替换了。

下面的链接是别人转载的，可以看，虽然代码缩进都不对。

另外，老赵的文章提供了一个很好的思路，但是没有后续具体的操作细节，我也摸索了很久。所以，下面我会给大家介绍一下完整的、具体的实现步骤。

<!--more-->

### <span id="i-3">实现思路和技术细节</span>

实现思路其实收费的 Mock 工具已经提供了：

1.  项目中按照之前的设计原则，编写自己的代码；
2.  测试项目每次编译完成后，运行一个程序，修改需要 Mock 的 dll ；
3.  利用 Moq 等 Mock 框架，在运行时动态生成代理类；

这里，只会修改复制到 Test 运行目录的 dll，所以不会影响别的项目。

&nbsp;

技术细节的话，这里就需要用到老赵博客中提到的 <a href="http://www.mono-project.com/Cecil" target="_blank"><strong>Mono.Cecil</strong></a> 了，建议用 <a href="http://visualstudiogallery.msdn.microsoft.com/27077b70-9dad-4c64-adcf-c7cf6bc9970c" target="_blank"><strong>NuGet</strong></a> 获取最新版本。

Mono.Cecil 可以帮助你修改编译好的 dll 文件。

核心代码如下（这部分逻辑由老赵提供，我做了一定的修改）：

<pre class="lang:c# decode:true">private static void OverWrite(string file, bool hasSymbols)
{
    var asmDef = AssemblyDefinition.ReadAssembly(file, 
                          new ReaderParameters { ReadSymbols = hasSymbols });
    var classTypes = asmDef.Modules
                            .SelectMany(m =&gt; m.Types)
                            .Where(t =&gt; t.IsClass)
                            .ToList();

    foreach (var type in classTypes)
    {
        if (type.IsSealed)
        {
            type.IsSealed = false;
        }

        foreach (var method in type.Methods)
        {
            if (method.IsStatic) continue;
            if (method.IsConstructor) continue;
            if (method.IsAbstract) continue;

            if (!method.IsVirtual)
            {
                method.IsVirtual = true;
                method.IsNewSlot = true;
                method.IsReuseSlot = false;
            }
            else
            {
                method.IsFinal = false;
            }
        }
    }

    asmDef.Write(file, new WriterParameters { WriteSymbols = hasSymbols });
}</pre>

只要把这个代码封装成一个控制台应用程序，每次编译测试项目后运行一下即可。

&nbsp;

### <span id="i-4">具体实现步骤</span>

#### <span id="i-5">源代码解决方案结构</span>

[<img class="alignnone size-full wp-image-999" title="solution" alt="" src="/uploads/2012/11/solution.png" width="300" height="234" />][1]

MockHelper 是核心工具，作用就是修改编译好的 dll，一般情况下也只要使用这个即可，别的几个项目只是用来演示的。

TestDll 内包含了一个密封类和非虚函数，后面会用这个做演示，把它变成可以 Mock 的。

Test 项目就是一个 <a href="http://en.wikipedia.org/wiki/MSTest" target="_blank"><strong>MSTest</strong></a> 项目，里面演示了怎么使用 MockHelper。

NUnit 项目同样是一个演示的测试项目，但是用的是 <a href="http://www.nunit.org/" target="_blank"><strong>NUnit</strong></a>。

&nbsp;

#### <span id="MockHelper">MockHelper 的使用</span>

这个控制台应用程序其实没有什么难度，核心代码上面已经贴出来了。

另外使用的时候需要复制 MockHelper.exe、mock.txt 和 Mono.Cecil*.dll 到你的测试项目中，一共六个文件。

[<img class="alignnone size-thumbnail wp-image-1000" title="test" alt="" src="/uploads/2012/11/test-150x150.png" width="150" height="150" />][2]

使用方法就是直接运行这个控制台应用程序，然后可以传入一个参数：代表 dll 所在的文件夹。如果不传参数的话默认是在运行目录。

然后把你需要修改的 dll 全部写到 mock.txt 中。

&nbsp;

#### <span id="_MockHelper">配置自动运行 MockHelper</span>

把 MockHelper 复制过去后的关键就是要让这个 exe 可以自动运行啦！

这里用的是：后期生成事件命令行

右击项目 — 属性 — 生成事件 — 后期生成事件命令行：

<pre class="toolbar:2 lang:default decode:true">"$(ProjectDir)MockHelper\MockHelper.exe"</pre>

这里不用传参数，因为运行这个工具的是 Test 项目，而这个项目默认的运行位置就是 <span style="background-color: #eeeeee;">bin/Debug|Release</span>，所以需要修改的 dll 就在下面。

&nbsp;

#### <span id="i-6">编写测试代码</span>

TestDll 是非虚函数，而且是密封类：

<pre class="lang:c# decode:true">public sealed class TestClass : TestClassBase
{
    public string NormalMethod()
    {
        return "TestClass";
    }

    public override string VirtualMethod()
    {
        return base.VirtualMethod();
    }

    public sealed override string SealedMethod()
    {
        return base.VirtualMethod();
    }

    public override string AbstractMethod()
    {
        return "TestClass";
    }
}

public abstract class TestClassBase
{
    public virtual string VirtualMethod()
    {
        return "TestClass";
    }

    public virtual string SealedMethod()
    {
        return "TestClass";
    }

    public abstract string AbstractMethod();
}</pre>

&nbsp;

测试代码如下：

<pre class="lang:c# decode:true">[TestClass]
public class UnitTest
{
    [TestMethod]
    public void TestMethod1()
    {
        var test = new Mock&lt;TestClass&gt;();
        test.Setup(t =&gt; t.NormalMethod()).Returns("Mock");
        test.Setup(t =&gt; t.VirtualMethod()).Returns("Mock");
        test.Setup(t =&gt; t.SealedMethod()).Returns("Mock");
        test.Setup(t =&gt; t.AbstractMethod()).Returns("Mock");

        Assert.AreEqual(test.Object.NormalMethod(), "Mock");
        Assert.AreEqual(test.Object.VirtualMethod(), "Mock");
        Assert.AreEqual(test.Object.SealedMethod(), "Mock");
        Assert.AreEqual(test.Object.AbstractMethod(), "Mock");
    }
}</pre>

&nbsp;

MSTest 运行结果如下：

[<img class="alignnone size-full wp-image-1002" title="result" alt="" src="/uploads/2012/11/result.png" width="323" height="147" />][3]

&nbsp;

NUnit 运行结果如下：

[<img class="alignnone size-medium wp-image-1005" title="NUnit" alt="" src="/uploads/2012/11/NUnit-300x156.png" width="300" height="156" />][4]

&nbsp;

去掉这个工具后会报如下错误：

[<img class="alignnone size-medium wp-image-1003" title="error" alt="" src="/uploads/2012/11/error1-300x107.png" width="300" height="107" />][5]

&nbsp;

### <span id="i-7">注意事项</span>

不要看上面的步骤简单，我在配置这个的时候走了很多弯路，这里也跟大家分享一下：

&nbsp;

#### <span id="_Moq_Mock">一定要用 Moq 等 Mock 框架</span>

为什么一定要自动 Mock 框架？它的核心不就是继承一个类吗？

因为这个工具是在代码编译后才去修改 IL 代码的。也就是说，在编写的时候，它依然是密封类或者是非虚方法。

所以你如果自己去编写的话，是无法编译通过的。

那自动 Mock 框架为何可以呢？

因为这些框架是在运行的时候动态生成一个类去继承需要 Mock 的类的。在运行的时候，这个类已经被修改过了，所以是不会出错的。

&nbsp;

#### <span id="_MSTest">注意配置一下 MSTest</span>

我在一开始研究这个的时候，遇到了一个很纠结的问题。

在我的 Demo 中它是可以的，但是到了真正的项目中，它却一直出错。

后来研究后发现，在出错的项目中， Test 的运行目录不是在 <span style="background-color: #eeeeee;">bin/Debug</span> 下，

而是在 <span style="background-color: #eeeeee;">TestResults/dozer_DOZER-PC 2012-11-27 11_11_22/Out</span>

而且这个文件夹会在每次运行测试的时候创建一个新的。里面的 dll 并不是从 <span style="background-color: #eeeeee;">bin/Debug</span> 中复制过去的，所以我工具修改后的 dll 没有起到作用。

可是为什么我的 Demo 中没有这样？后来发现后面一个项目启用了**<a href="http://msdn.microsoft.com/zh-cn/library/ms182473(v=vs.80).aspx" target="_blank">测试部署</a>**功能，虽然不知道这个功能具体的用处，但是取消后出错的项目也正常了！

取消方法：测试 — 编辑测试设置 — 本地（另一个也要同样配置） — 部署 — 取消启用部署。

注意！配置有两份，要同时取消后才可以生效。

&nbsp;

#### <span id="i-8">所有测试框架都支持吗？</span>

原则上，只要你有办法在运行测试之前跑一下这个工具就可以支持所有的测试框架。

从上面可以看到，MSTest 和 NUnit 的配置方法是完全一样的。

经过测试，我们公司的自动化部署、测试框架是可以支持这个的，别的环境可能需要一些修改和配置，难度并不是很大。

&nbsp;

### <span id="i-9">最后</span>

项目地址：<a href="https://github.com/dozer47528/MockHelper" target="_blank">https://github.com/dozer47528/MockHelper</a>

最后，感谢老赵提供的思路！我这里其实只是具体实现一下。

其实，这个是无奈之举，大家最好还是老老实实地多用接口吧！

&nbsp;

### <span id="i-10">缺陷</span>

这两天我在继续研究 Mock Private 方法，思路很简单，就是把这个 Private 方法改成 Virtual + Protected。

但是一直失败，手动修改成 Virtual + Protected 一切正常！

看这个方法的 IL 代码，手动修改的和程序修改的完全一模一样！可是为什么就是不能 Moq 呢？

我在 Moq 中 Mock 了 Protect 方法，没有报错，看上去 Mock 成功了：

<pre class="toolbar:2 lang:c# decode:true">test.Protected().Setup&lt;string&gt;("PrivateMethod").Returns("Mock");</pre>

但是在调用了时候还是调用了原来的方法。

后来只能通过调试 Moq 源码找原因，看看到底在哪一步发生了问题。

后来终于找到了原因，那是什么原因导致了我这个方法明明改成了 Virtual + Protected ，但是却无法被重写呢？

&nbsp;

这个方法修改后的 IL 代码和手工写的 IL 代码的确是完全一样的。但是，调用这个函数的函数生成的 IL 代码是不一样的：

[<img class="alignnone size-medium wp-image-1014" title="non-virtual" alt="" src="/uploads/2012/11/non-virtual-300x102.png" width="300" height="102" />][6]

原来，我手动修改和自动修改有一个被忽略掉的地方，就是调用被修改函数的函数。这里的 IL 代码，一个是 <span style="background-color: #eeeeee;">call</span>，一个是 <span style="background-color: #eeeeee;">callvirt</span>。

前者只会调用自身的函数，就算后面后覆盖（new），也不会受到影响。

而后者如果继承后被覆盖了（override），它会调用最新的方法。

其实自动修改的程序集已经有矛盾了，因为别的方法以为它是 non-virtual，而它实际上是可以被覆盖的。但是别的方法不知道它可以被覆盖，所以就算被覆盖了，最终的效果和 new 一样。

&nbsp;

这是我在研究 Mock Private 方法的时候发现的问题。了解原理后，我也发现了此文的缺陷。此文虽然在研究 Public 的方法。但是，如果连个 Public 的方法 A 和 B。

如果 A 调用了 B，那 Mock 了 B 以后，A 依然会调用原来的 B 方法。

所以，如果你的这个类是 Mock 以后，被别的类调用的，那么无所谓，内部可以不存在任何联系；但是如果你是为了测试 A  方法而 Mock 了 B 方法，那么在这种场景下就会出问题了！

最后，我想还是老老实实的改原来的代码吧，除非把这个工具再加强一步，所有调用 B 的地方，全部从 call 改成 callvirt 。但是这个工作量就太大了，而且差不多就是自己实现一个 Typemock 了。本来是想做一个轻量级的，结果做着做着就越来越庞大了，那继续下去也没有意义了，因为已经有现成的了。

但是，在这个过程中，还真的学习到了不少东西！

 [1]: /uploads/2012/11/solution.png
 [2]: /uploads/2012/11/test.png
 [3]: /uploads/2012/11/result.png
 [4]: /uploads/2012/11/NUnit.png
 [5]: /uploads/2012/11/error1.png
 [6]: /uploads/2012/11/non-virtual.png