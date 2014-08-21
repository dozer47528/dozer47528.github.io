---
title: '不继承 IEnumerable<T> 或 IQueryable<T> 的类型怎么使用 LINQ 查询'
author: Dozer
layout: post
permalink: /2011/08/to-enable-custom-linq-querying-of-generic-type/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - .Net
  - CLR
  - IL
  - LINQ
---

最近想研究如何自定义 LINQ Provider ，但是一直无法入手，先写点收获吧~

MSDN 上的这篇文章（**<a href="http://msdn.microsoft.com/zh-cn/library/bb882640.aspx" target="_blank">《启用数据源以进行 LINQ 查询》</a>**）中写到：

如果想对自己的数据源进行 LINQ 查询，那必须使用一下四种方法的其中一种。

1.  实现 IEnumerable<T> 接口
2.  实现标准的查询方法
3.  实现 IQueryable<T> 接口
4.  扩展已经实现的 LINQ 查询

看到其中第二条，让人心生疑惑，那下面就来探讨一下吧~

&nbsp;

### <span id="_LINQ">什么类型可以进行 LINQ 查询？</span>

<pre class="brush:csharp">var queryLondonCustomers = from cust in customers
                           where cust.City == "London"
                           select cust;</pre>

很简单的几行代码，这就是 LINQ，这里有几个关键字： <span style="color: #0000ff;">from</span>, <span style="color: #0000ff;">in</span>, <span style="color: #0000ff;">where</span>, <span style="color: #0000ff;">select …</span>

这几个是新增的关键字，还有别的好多个~

关键看这里的 customers ，这里就是一个可以被 LINQ 查询的对象。

<!--more-->

按照一般的思路，它一定是继承了某个接口，所以可以用 LINQ 查询。

在学习 LINQ 的时候我们常常会看到两个接口：IEnumerable<T> 和 IQueryable<T> ，难道是这两个？

<span style="color: #999999;"><em>备注：这两个接口的区别是，前者提供的是对内存中数据的查询，后者提供的是对远程数据的查询，这里就不展开了。</em></span>

&nbsp;

如果你没有深入了解，恐怕你就会认为的确如此了。

这里有两个疑点：

1.  如果你说是 IQueryable<T>，那还可以理解，因为这是一个新的接口，但是为什么 IEnumerable<T> 也可以呢？这个可不是一个新接口哦，一般情况下，新版本的 .net 怎么可能修改以前的接口呢？
2.  如果真是如此，那在 MSDN 的文章中为什么说就算不集成这两个接口，只要实现了基本的查询语句就可以实现 LINQ 查询呢？

让我们继续探讨吧！

&nbsp;

### <span id="IL">反编译看IL代码</span>

一段代码

<pre class="brush:csharp">class Program
{
    static void Main(string[] args)
    {
        var data = Enumerable.Range(1, 5).ToArray();

        var q = from _ in data
                where _ &gt; 3
                select _;
    }
}</pre>

&nbsp;

让我们看看它的 IL 代码（部分）

<pre class="brush:csharp">IL_0029: ldsfld class [mscorlib]System.Func`2&lt;int32, bool&gt; ConsoleApplication1.Program::'CS$&lt;&gt;9__CachedAnonymousMethodDelegate1'
IL_002e: call class [mscorlib]System.Collections.Generic.IEnumerable`1&lt;!!0&gt; [System.Core]System.Linq.Enumerable::Where&lt;int32&gt;(class [mscorlib]System.Collections.Generic.IEnumerable`1&lt;!!0&gt;, class [mscorlib]System.Func`2&lt;!!0, bool&gt;)
IL_0033: stloc.1
IL_0034: ret</pre>

&nbsp;

关键代码：[System.Core]System.Linq.Enumerable::Where<int32>

让我们找到它的出处

<pre class="brush:csharp">namespace System.Linq
{
    public static class Enumerable
    {
        public static IEnumerable&lt;TSource&gt; Where&lt;TSource&gt;(this IEnumerable&lt;TSource&gt; source, Func&lt;TSource, bool&gt; predicate) {
            if (source == null) throw Error.ArgumentNull("source");
            if (predicate == null) throw Error.ArgumentNull("predicate");
            if (source is Iterator&lt;TSource&gt;) return ((Iterator&lt;TSource&gt;)source).Where(predicate);
            if (source is TSource[]) return new WhereArrayIterator&lt;TSource&gt;((TSource[])source, predicate);
            if (source is List&lt;TSource&gt;) return new WhereListIterator&lt;TSource&gt;((List&lt;TSource&gt;)source, predicate);
            return new WhereEnumerableIterator&lt;TSource&gt;(source, predicate);
        }
    }
}</pre>

&nbsp;

其实，它最终只是调用了 IEnumerable<T> 的一个扩展方法，难怪别人总说上面的代码其实等效于这个

<pre class="brush:csharp">var data = Enumerable.Range(1, 5).ToArray();
var q = from _ in data
        where _ &gt; 3
        select _;

var q2 = data.Where(_ =&gt; _ &gt; 3);//等效于上面一行代码</pre>

&nbsp;

让我们来理一下思路：

*   LINQ 查询里的 where 关键字等效于调用 Where 这个方法（别的关键字也是如此）；
*   这个 Where 方法不在接口内，而是在针对这个接口的扩展方法内；
*   LINQ 查询对接口貌似没有约束，仅仅是看你是否有这个方法（目前仅仅是猜测）。

&nbsp;

为了验证上面的是否正确，那就让我们来动手实践一下吧！

&nbsp;

### <span id="_LINQ-2">为自定义类型提供 LINQ 查询</span>

按照刚才分析的，是不是只要给自己的类型提供几个方法就行了呢？

动手吧！

我们先来实现 select 和 where 关键字吧~

先看看 .net 源码中的函数吧，这样我们才能知道这个函数需要传入什么，需要返回什么。

<pre class="brush:csharp">namespace System.Linq
{
    public static class Enumerable
    {
        public static IEnumerable&lt;TSource&gt; Where&lt;TSource&gt;(this IEnumerable&lt;TSource&gt; source, Func&lt;TSource, bool&gt; predicate) {
        }
        public static IEnumerable&lt;TResult&gt; Select&lt;TSource, TResult&gt;(this IEnumerable&lt;TSource&gt; source, Func&lt;TSource, TResult&gt; selector) {
        }
    }
}</pre>

这里不用看具体的实现，只要看传入的参数和返回类型就行了。

那么接下来就让我们写自己的类型吧！

<pre class="brush:csharp">class Program
{
    static void Main(string[] args)
    {
        var mySchool = new School();
        var q = from _ in mySchool
                where _.Contains("a")
                select _;
    }
}

class School
{
    protected List&lt;string&gt; Student { get; set; }
    public School()
    {
        //生成一个 Student 序列
        Student = new List&lt;string&gt;
                        {
                            "abc",
                            "xyz",
                            "123"
                        };
    }
    public School Where(Func&lt;string, bool&gt; predicate)
    {
        //这里对List有增删了，所以不能直接用foreach，删除不满足条件的学生
        for (var k = 0; k &lt; Student.Count; k++)
        {
            if (predicate(Student[k])) continue;
            Student.RemoveAt(k);
            k--;
        }
        return this;
    }
    public School Select(Func&lt;School, School&gt; selector)
    {
        //这里就不实现了
        return this;
    }
}</pre>

这里的场景：

School 类型，并不是什么枚举类型，但是需要用 where 做一些过滤，用 order 做一些排序，里面的数据呢，是不暴露出来的。

所以如果不继承 IEnumerable<T> 或 IQueryable<T> 的接口话，只要模仿它们的扩展方法，实现一些基本的方法即可。

具体的实现貌似没找到什么好的资料，只能自己慢慢摸索了~ 这其中还有一些泛型，可以根据自己的需求做相应的修改！

&nbsp;

### <span id="i">反思</span>

从上面的种种迹象表明，LINQ 应该是编译器级别的东西，而不是 .net CLR 级的东西（这个仅仅是个人猜测）

写完了这些，我一直在想微软为什么要真么做？

按照一般的设计思路，理想状态下，应该有一个统一的接口来约束，然后所有继承这个接口的类型都可以进行 LINQ 查询。

但是为什么没这么做呢？

&nbsp;

**个人分析：**

微软想要实现 Linq to everything，所以要让一切数据支持 LINQ，一般可以认为实现 IEnumerable<T> 接口的类型都是数据，也就是说要让所有实现 IEnumerable<T> 接口的类型都可以实现 LINQ 查询。

但是这是一个接口，不是一个抽象类，不能写具体的方法。LINQ 查询只要用的 IEnumerable<T> 接口所提供的函数就行了。

所以扩展方法是一个非常明智的选择！

&nbsp;

那 IQueryable<T> 是怎么回事呢？IQueryable<T> 中包含一个 IQueryProvider 类型，它可以将本地的查询转换为远程的查询，忽略内部实现，你可以认为 IEnumerable<T> 和 IQueryable<T>是一样的。

&nbsp;

不继承 IEnumerable<T> 的就不是数据了吗？恐怕不是吧~

不是说 Ling to everything 吗？为什么不对 Object 写 LINQ 查询呢？

首先不是所有的 Object 都是数据，另外 Object 也没有可以依赖的方法供数据查询用。

&nbsp;

所以如果是你自己的类型，并且不实现 IEnumerable<T> 或 IQueryable<T> 接口，那么你只要自己写一些函数就行了！

而且可以自由地控制，例如：如果排序方法对你的类型来说没有意义，那你可以不写它。

虽然我还是觉得这样的设计略微有点不严谨，但它的确很方便~
