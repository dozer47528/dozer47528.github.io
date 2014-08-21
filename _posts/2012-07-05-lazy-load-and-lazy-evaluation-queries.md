---
title: 延迟加载与延迟求值查询
author: Dozer
layout: post
permalink: /2012/07/lazy-load-and-lazy-evaluation-queries/
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - 延迟加载
  - 延迟求值查询
---

### <span id="i">对延迟加载的片面认识</span>

很多人对延迟加载的初步认识就是，在使用 LINQ for Entity 的时候，查询语句不会立即执行查询，只有在使用 foreach 或者 ToList() 等方法的时候，才会去查询数据库。

那如果我用的不是 LINQ for IQueryable，而是 LINQ for IEnumerable（前者往往是查询远程数据的，后者查询的都是内存数据），例如自己的一些数据库访问层，返回的数据就是 List<T>，内存已经在数据中了，是不是就没有延迟加载了呢？

非也！

&nbsp;

### <span id="i-2">延迟加载的实现原理</span>

LINQ for IQueryable 查询的往往是远程数据的，当你调用 Where()，Single() 等方法的时候，并没有去查询数据库，而是保存为表达式树了。

只有当你使用 foreach 或者 ToList() 等方法的时候，才会把之间的所有表达式转换成 SQL 或其他查询方法，然后和远程数据交互。

具体原理可以查看下来文章：<a href="http://blogs.msdn.com/b/mattwar/archive/2008/11/18/linq-links.aspx" target="_blank">http://blogs.msdn.com/b/mattwar/archive/2008/11/18/linq-links.aspx</a>

<!--more-->

LINQ for IEnumerable 是针对于内存中数据的查询语句，数据既然已经在内存中了，那么还需要延迟加载吗？

其实，这时候准确的说应该叫延迟求值查询（Lazy Evaluation Queries），而不是延迟加载。总之，它们还是有区别的！

<pre class="brush: csharp; gutter: true">var list = new List&lt;int&gt;{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
var result1 = list.Where(_ =&gt; _ &lt; 5).Where(_ =&gt; _ != 8);
var result2 = list.Where(_ =&gt; _ &lt; 5).ToList().Where(_ =&gt; _ != 8);</pre>

先看上述代码，大家觉得执行 result1 和 result2 的时候有什么区别吗？

其实区别不大，后者多了 ToList() 方法。但是，他们在性能上有很大的差别！

抛开 ToList() 在类型转换上的损耗（其实这里没有类型转换，没什么损耗），从执行过程上，前者只是把 list 循环了一次，而 后者把 list 循环了2次！

**所以，在使用 LINQ 的时候，如果返回的是一个集合，强烈建议不要调用 ToList() 方法，数据在最终使用的时候也只不过是用 foreach 来调用，出于便捷性和性能的考虑，调用 ToList() 都不是一个好的决策。**

但是为什么第一行查询只会跑一次循环呢？

&nbsp;

### <span id="i-3">迭代器与延迟求值查询</span>

大家有没有发现在这个章节我把延迟加载改成了延迟求值查询？因为严格的来说，LINQ for IEnumerable 查询的数据已经在内存中了，那还需要加载什么呢？

另外，理解原理后，大家也会明白，这里其实是延迟求值查询，而不是延迟加载。

延迟求值查询指的是：对集合调用 Where() 等方法后，并不会立刻进行循环。只有当对集合调用 foreach 或 ToList() 等方法的时候，才会真正地进行循环，并且只会循环一次。

关于这个问题，《More Effective C#》中的 item32:Prefer Lazy Evaluation Queries 解释地非常详细了。大家也可以搜索到中文版。

&nbsp;

简单地来说，LINQ 技术中，所有对于 IEnumerable 的扩展方法都使用了迭代器，所以多次调用这几个方法并不会进行多次循环，而是会合并成一个循环。

具体原理可以查看本书原文，也可以买中文版看，或到这里查看网友的<a href="http://www.cnblogs.com/kongyiyun/archive/2010/10/14/1851613.html" target="_blank"><strong>翻译</strong></a>。

&nbsp;

### <span id="i-4">延迟加载和延迟求值查询的思考</span>

由于之前的片面认识，导致我一直认为延迟加载只有在使用 LINQ to Entity 等 ORM 框架的时候，才会有用。

不仅我是这样，相信很多人在写 BLL 层输出数据的时候，也都是用 List<T> 作为输出类型的。

&nbsp;

所以往往在网站中是这么设计的：

*   BLL层：在对数据源进行各种操作，排序、筛选、分页等，最后输出的时候用 ToList() 方法输出；如果不是 Entity Framework 等 ORM 框架的话，也直接输出 List<T>。
*   WEB层：把数据源传递给前端页面，用 foreach 在页面上输出。

&nbsp;

上述步骤看似好，其实这样的设计也没什么问题。性能也很不错！

在 BLL 层对同一个数据源调用各种方法，期间并不真正地调用数据库，而是在最后调用一次数据库。

理论上，把数据输出到页面或者 controller 后，不应该有任何逻辑代码了，但实际上，还是有可能会在这几个地方修改集合的；最关键的是，就算如此，你也额外多做了一次循环。

一次是在 BLL 层 ToList() 的时候，一次是在页面上 foreach 的时候。

&nbsp;

但是大家看微软 **<a href="http://asp.net/" target="_blank">http://asp.net/</a>** 上的例子后就会发现，上面的例子从来不会调用 ToList() 方法，所有的输出类型都是 IEnumerable 或者 IQueryable，在页面上也只不过是使用 foreach 操作。

&nbsp;

所以，在将来的项目中，推荐大家在 BLL 层返回的类型都是 IEnumerable<T>；如果用的是 LINQ for IQueryable，例如 Entity Framework 技术，应该把返回类型写为 IQueryable<T>。

因为如果把 Entity Framework 查询出来的集合（类型是 IQueryable<T> ）转换为 IEnumerable<T> 的话，再次调用任何方法，就不会把操作存放在表达式树中了。具体可以看下一个章节。

&nbsp;

### <span id="IQueryableltTgt_IEnumerableltTgt">IQueryable<T> 显示转换为 IEnumerable<T> 时出现的问题</span>

LINQ 技术中，为 IQueryable<T> 接口和 IEnumerable<T> 写了两套扩展方法（LINQ 技术中的各种函数使用扩展方法实现的）。

所以，虽然 IQueryable<T> 继承于 IEnumerable<T>，当把前者的显示类型转换成后者的时候，调用同样的函数（其实只是名字看起来相同，底层和方法的参数都不同）的执行过程是不一样的。

它们内部实现方法并不同，IQueryable<T> 的实现方法是表达式树，IEnumerable<T> 的实现方法是迭代器。

所以如果这么做的话，当类型为 IQueryable<T> 时，相应的操作会保存为表达式树；IEnumerable<T> 时，操作会保存为枚举器。也就是说，这时一半为延迟查询、一半为延迟求值查询了。这样的性能当然没有全部是延迟查询来得好。

&nbsp;

### <span id="i-5">自己实现延迟求值查询</span>

另外，如果你没有用 LINQ，老版本 .NET？或者是需要一些复杂的操作 .NET 现有类库无法满足怎么办？

怎么样才能和 LINQ 提供的查询方法一样，利用迭代器实现一次循环而非多次循环呢？

请看如下代码：

<pre class="brush: csharp; gutter: true">static void Main(string[] args)
{
    var list = new List&lt;int&gt; { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    var result = Test2(Test1(list));
    Console.WriteLine("这里并没有输出！");
    result.ToList();
}

static IEnumerable&lt;int&gt; Test1(IEnumerable&lt;int&gt; list)
{
    foreach (var l in list)
    {
        Console.WriteLine(l + " in Test1");
        yield return l;
    }
}

static IEnumerable&lt;int&gt; Test2(IEnumerable&lt;int&gt; list)
{
    foreach (var l in list)
    {
        Console.WriteLine(l + " in Test2");
        yield return l;
    }
}</pre>

执行结果如下：

[<img class="alignnone size-medium wp-image-795" title="console" alt="" src="/uploads/2012/07/console-215x300.png" width="215" height="300" />][1]

&nbsp;

如果这两个方法是一般的方法实现，那么，在执行第二条语句的时候，result 就已经有值了，而且也会在控制台有输出。

另外，也应该是先循环 Test1 方法，再循环 Test2 方法，所以输出的结果应该先全部是 &#8220;Test1&#8243; ，然后再是 &#8220;Test2&#8243;。

&nbsp;

但实际执行结果却很不同，在执行第二条语句的时候，没有有任何输出，代表并没有执行任何代码，而只是以迭代器的形式存放了起来。

而在使用 ToList() 的时候，总共进行了一个循环，对每一个元素分别调用 Test1 和 Test2 中的代码。

可见，你只需要把以前方法的返回类型改成 IEnumerable<T> ，并利用 yield return 输出元素即可。

PS.当然，如果用的是 Entity Framework 等 LINQ for IQueryable<T> 技术，类型最好应该为 IQueryable<T>。

&nbsp;

### <span id="i-6">不适用场景</span>

这种方法虽然能在特定的场景下提升性能，但是并不是适合所有场景。因为利用此方法后，相当于把集合中的元素一个个执行对应的方法，最终合并成了一个循环。

很明显，语义被破坏了，所以在这么些的时候，一定要保证各个元素之间没有关联，或者没有整体关联。如果有相应的关系，恐怕会影响最终的结果。

但是，LINQ 用了这么久，真没出现过因为延迟查询而影响执行结果的情况，可使用这类方法的时候，还是要注意是否会影响影响最终结果！

 [1]: /uploads/2012/07/console.png
