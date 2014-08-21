---
title: Linq To Salesforce
author: Dozer
layout: post
permalink: /2012/09/linq-to-salesforce/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658344
categories:
  - 编程技术
tags:
  - LINQ
  - LINQ Provider
  - Salesforce
  - 表达式树
---

### <span id="i">锤子与钉子</span>

手中有锤子，眼前的一切就都变成钉子了…

手上有 <a href="http://msdn.microsoft.com/zh-cn/library/bb397926.aspx" target="_blank"><strong>LINQ</strong></a>，就想把一切都转换成 LINQ。<a href="http://www.salesforce.com/cn/" target="_blank"><strong>Salesforce</strong> </a>API 也不例外。

Salesforce 的 API 调用方法还算简单，可以自动生成实体，但是有如下缺点：

1.  查询语句还是原始的 <a href="http://www.salesforce.com/us/developer/docs/api/Content/sforce_api_calls_soql.htm" target="_blank"><strong>SOQL</strong> </a>，类似于 SQL
2.  每次查询最多 200 个对象，如果超过了，还需要用 QueryMore 方法继续查询

总之，我想把 Salesforce API 查询语句转换为 LINQ 的查询形式，是否可行？

<!--more-->

### <span id="i-2">调研</span>

如果网上有好的框架可以用，那何必自己写呢？

但是可能使用 Salesforce 的很少，利用 .net 调用 Salesforce 的就更少了。

但是还是找到了几个框架：

<http://salesforce-entity-framework.smartcode.com/>

<http://www.devart.com/dotconnect/salesforce/>

<http://www.rssbus.com/ado/salesforce/features.aspx>

&nbsp;

其中，devart.com 的那个我试用了一下，非常庞大！还会出现各种错误，因为它不仅仅是 Linq To Salesforce，它其实是 Linq To Entity Framework，所以还包括了实体设计等功能，而 Linq To Salesforce 仅仅是把 Linq 查询转换成 <a href="http://www.salesforce.com/us/developer/docs/api/Content/sforce_api_calls_soql.htm" target="_blank"><strong>SOQL</strong> </a>罢了。

所以还是放弃了。

而且这些框架都是收费的，都太重量级了，所以还是自己写一个吧。

&nbsp;

### <span id="_Linq_To_Salesforce">自己实现 Linq To Salesforce</span>

自己实现 Linq To Salesforce 最关键的就是把<a href="http://msdn.microsoft.com/zh-cn/library/bb397951.aspx" target="_blank"><strong>表达式树</strong></a>转换成SOQL：

<pre class="brush: csharp; gutter: true">var result = Query&lt;Contract&gt;()
                .Where(c =&gt; c.CreatedDate &gt; DateTime.Now.AddMonths(-1))
                .ToList();
// SELECT Id FROM Contract WHERE CreatedDate &gt; 20120801T00:00:00.000Z</pre>

所以，关键点就是解析表达式树了，你可以自己用自己的逻辑实现解析表达式树，但是更推荐用微软的 IQueryable、IQueryProvider 和 ExpressionVisitor 来实现标准的表达式树解析。

这里推荐两篇文章：

<http://blogs.msdn.com/b/mattwar/archive/2008/11/18/linq-links.aspx>

<http://msdn.microsoft.com/zh-cn/library/bb546158.aspx>

还有第一篇文章中的一个示例项目：

<http://iqtoolkit.codeplex.com/>

&nbsp;

### <span id="_Linq_To_Salesforce-2">我的 Linq To Salesforce</span>

我的项目已经发布到了 Github 上了：<https://github.com/dozer47528/LinqToSalesforce>

#### <span id="i-3">框架内容简介：</span>

<span style="background-color: #eeeeee;">SalesforceQuery</span>：职责是保存 IQueryProvider 和 Expression 的引用，并调用 <span style="background-color: #eeeeee;">IQueryProvider</span> 得到最终结果；

<span style="background-color: #eeeeee;">SalesforceProviderBase</span>： <span style="background-color: #eeeeee;">IQueryProvider </span>的具体实现，抽象类，需要自己继承后实现关键算法，职责是调用 <span style="background-color: #eeeeee;">ExpressionVisitor</span> 把表达式树解析成 SOQL 语句；

<span style="background-color: #eeeeee;">SalesforceVisitor</span>：<span style="background-color: #eeeeee;">ExpressionVisitor</span> 的具体实现，职责就是把表达式树解析成 SOQL 语句。

备注：<span style="background-color: #eeeeee;">SalesforceProviderBase</span> 为什么是抽象类，还需要手动实现关键算法？因为 Salesforce 的 API 是利用强类型 **<a href="http://www.w3.org/TR/wsdl" target="_blank">WSDL </a> **生成的，它们也不是统一的，每个组织都有自己的 WSDL 文件，所以如果没有统一的查询方法和对象，我无法在框架中实现它。但是，我的 <span style="background-color: #eeeeee;">Test</span> 项目中给出了一个实现示例，非常简单的示例。

&nbsp;

#### <span id="1">使用步骤1：</span>

继承 <span style="background-color: #eeeeee;">SalesforceProviderBase<T></span> ，实现自己的 <span style="background-color: #eeeeee;">SalesforceProvider<T></span> ，这里需要重写 2 个方法：

<pre class="brush: csharp; gutter: true">protected abstract int GetCount(string cmd);
protected abstract IEnumerable&lt;T&gt; GetEnumerable(string cmd);</pre>

传入的参数都是已经解析好的 <span style="background-color: #eeeeee;">SOQL</span> 语句，第一个方法是用来返回总数的，第二个方法是用来返回 IEnumerable<T> 的。

项目中的 LinqToSalesforce.Test/SalesforceQuery/SalesforceProviderSample.cs 是一段实例代码。

&nbsp;

#### <span id="2">使用步骤2：</span>

创建 IQueryable<T> 对象：

<pre class="brush: csharp; gutter: true">protected SalesforceQuery&lt;T&gt; Query&lt;T&gt;(SelectTypeEnum selectType = SelectTypeEnum.SelectIdAndUseAttachModel) where T : sObject
{
      return new SalesforceQuery&lt;T&gt;(new SalesforceProviderSample&lt;T&gt; { SelectType = selectType });
}</pre>

接下来直接对这个对象调用 LINQ 方法即可：

<pre class="brush: csharp; gutter: true">var result = Query&lt;Contract&gt;()
    .Where(c =&gt; c.CreatedDate &gt; DateTime.Now.AddMonths(-1))
    .ToList();</pre>

&nbsp;

#### <span id="i-4">注意事项：</span>

*   实现 SalesforceProviderBase<T> 中的 GetEnumerable 方法的时候请注意利用迭代器模式取回所有数据，因为 Salesforce 默认只会返回 200 条数据。
*   <span style="background-color: #eeeeee;">SOQL</span> 没有 <span style="background-color: #eeeeee;">join</span> 查询，如果要查询关联对象的话，SOQL 是这样实现的：<span style="background-color: #eeeeee;">[SELECT Accoint.Name From Contract]<span style="background-color: #ffffff;">，而在 Linq To Salesforce 中，这种查询可能会有点麻烦，具体的可以参考 测试项目中的 <span style="background-color: #eeeeee;">SelectRelatedTest</span> 测试。</span></span>
*   <span style="background-color: #eeeeee;"><span style="background-color: #eeeeee;"><span style="background-color: #ffffff;">创建查询对象的时候，</span></span></span>SelectTypeEnum 是什么？因为 Salesforce 的特殊性（没有<span style="background-color: #eeeeee;"> Select *</span>，没有 <span style="background-color: #eeeeee;">join</span>），我默认提供了四种查询查询模式：默认查询Id字段后面再调用 Select 方法的时候使用 Select 中的类容；默认查询Id字段后面再调用 Select 方法的时候附加上 Select 中的类容（默认）；默认查询所有字段后面再调用 Select 方法的时候使用 Select 中的类容；默认查询所有字段后面再调用 Select 方法的时候附加上 Select 中的类容。
*   别用 <span style="background-color: #eeeeee;">DateTime</span> 类型和 Salesforce 中的日期类型做比较，因为在 .net 中没有日期类型，所以它们都被转换成了 <span style="background-color: #eeeeee;">DateTime</span>。但在 <span style="background-color: #eeeeee;">SOQL</span> 中，他们的格式是不一样的。所以如果要用日期类型作为筛选条件，那么请使用 <span style="background-color: #eeeeee;">SalesforceDate</span> 这个对象。

&nbsp;

### <span id="i-5">功能列表：</span>

*   支持 Select 关联对象
*   支持 First, FirstOrDefault, Single, SingleOrDefault 方法
*   支持 Count 方法

&nbsp;

最后，如果有任何问题，大家可以在我的博客留言，也可以在 Github 上和我交流。
