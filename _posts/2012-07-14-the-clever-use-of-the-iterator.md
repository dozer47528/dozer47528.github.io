---
title: 迭代器的妙用
author: Dozer
layout: post
permalink: /2012/07/the-clever-use-of-the-iterator/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103981243063
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - yield
  - 延迟加载
  - 延迟求值查询
  - 迭代器
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 延迟查询与延迟求值查询</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 业务场景与常规解决办法</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 迭代器的妙用</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">4</span> 性能测试</a>
    </li>
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">5</span> 总结</a>
    </li>
  </ul>
</div>

### <span id="i">延迟查询与延迟求值查询</span>

在我的<a href="/2012/07/lazy-load-and-lazy-evaluation-queries/" target="_blank"><strong>上一篇文章</strong></a>中，给大家介绍了延迟查询与延迟求值查询的实现原理和注意事项。

前几天在项目开发的时候，发现了一个非常好的应用场景，可以利用延迟查询与延迟求值查询达到非常棒的结果！

&nbsp;

### <span id="i-2">业务场景与常规解决办法</span>

大家平时是否经常有这样的一个场景？

场景：数据库一个表中有十万、百万条数据，有这么一个作业偏偏要把它们都独取出来，然后一条条地进行处理。（单条数据之间没有依赖关系）

处理：一下子读出来？不可能吧… 那只能利用类似分页的方法，一部分一部分地取了。

<!--more-->

解决办法如下：

<pre class="brush: csharp; gutter: true">public void ProcessingData()
{
    var index = 0;
    while (true)
    {
        var result = GetFromDatabase(index, 200);
        foreach (var item in result)
        {
            //do something with item
        }
        if (result.Count &lt; 200) { break; }
    }
}

public List&lt;string&gt; GetFromDatabase(int index, int size)
{
    //do something
    return result;
}</pre>

代码非常简单，利用类似分页的思想，每次读取200条数据，当取出来的数据不满200条时，代表后面没有数据了，也就不会继续读取后面的页码了。

**但是这样的代码是否可用封装起来？**

&nbsp;

### <span id="i-3">迭代器的妙用</span>

什么叫封装起来？封装就是隐藏实现细节，这块的逻辑代码实在不应该暴露给业务逻辑层。

其实，利用 yield return （C# 中的 <a href="http://msdn.microsoft.com/zh-cn/library/9k7k7cf0.aspx" target="_blank"><strong>yield</strong> </a>关键字可以很方便地实现迭代器），就可以非常简单地实现这个想法了。

实现代码如下：

<pre class="brush: csharp; gutter: true">static void Main(string[] args)
{
    foreach (var item in GetIEnumerableData())
    {
        Console.Write(item);
    }
}
static IEnumerable&lt;string&gt; GetIEnumerableData()
{
    var index = 0;
    while (true)
    {
        var result = GetFromDatabase(index, 200);
        foreach (var item in result)
        {
            yield return item;
        }
        if (result.Count &lt; 200) { break; }
    }
}
static List&lt;string&gt; GetFromDatabase(int index, int size)
{
    var result = new List&lt;string&gt;();
    for (var k = 0; k &lt; size; k++)
    {
        if (size * index + k &gt; 1000000) { break; };
        result.Add(Guid.NewGuid().ToString());
    }
    return result;
}</pre>

上面，我制造了100万个 string 对象，模拟数据库读取出来的数据。

另外，需要注意的是业务逻辑层调用的时候不能转换成其他集合类型（例如 List<T>）等，一转换就相当于直接把所有数据读取到内存中了。

可以看到，Main 方法中利用 foreach 调用返回结果时，底层每次只会读取200条数据，如果 Main 方法中 foreach break 了，后面的数据也不会继续读取了。

&nbsp;

### <span id="i-4">性能测试</span>

理论上，这样子读取的话，每次只会有200条数据在内存中，我将这种方式和直接全部独到内存中的方式进行了内存占用对比。

结果如下，上图是用迭代器实现延迟加载与延迟求值查询的结果，下图是全部读到内存中的结果：

[<img class="alignnone size-medium wp-image-809" title="memory1" alt="" src="/uploads/2012/07/memory1-300x80.png" width="300" height="80" />][1]

[<img class="alignnone size-medium wp-image-810" title="memory2" alt="" src="/uploads/2012/07/memory2-300x71.png" width="300" height="71" />][2]

前者内存占用6M，后者为100多M。

其实这个结果不用测就能猜到了，内存中加载200个对象和100万个，肯定是有天壤之别的。

&nbsp;

### <span id="i-5">总结</span>

如果大家的业务场景中，也需要用到遍历整张表的数据且数据很大的时候，都可以利用这种方式批量处理。其实每次处理200个并不是最优方案，具体的需要根据你单个数据的大小进行调整。

但是千万记住，不要把 IEnumerable<T> 转换成 List<T> 等集合，一转换就相当于全部读取出来了。

&nbsp;

 [1]: http://www.dozer.cc/uploads/2012/07/memory1.png
 [2]: http://www.dozer.cc/uploads/2012/07/memory2.png