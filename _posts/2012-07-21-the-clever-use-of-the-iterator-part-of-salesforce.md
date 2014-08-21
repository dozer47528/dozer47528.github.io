---
title: 迭代器的妙用之 Salesforce API
author: Dozer
layout: post
permalink: /2012/07/the-clever-use-of-the-iterator-part-of-salesforce/
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - Salesforce
  - yield
  - 延迟加载
  - 延迟求值查询
  - 迭代器
---

### <span id="i">上期回顾</span>

在前两篇文章中（<a href="/2012/07/lazy-load-and-lazy-evaluation-queries/" target="_blank"><strong>延迟加载与延迟求值查询</strong></a>、<a href="/2012/07/the-clever-use-of-the-iterator/" target="_blank"><strong>迭代器的妙用</strong></a>），介绍了很多延迟加载、延迟求值查询和迭代器的知识。

本文也是利用了相关技术，巧妙了实现了一个功能。

&nbsp;

### <span id="Salesforce_API">Salesforce API 的调用</span>

最近会进行 <a href="http://zh.wikipedia.org/wiki/Salesforce.com" target="_blank"><strong>Salesforce</strong> </a>开发，过程中需要在 C# 中调用 Salesforce 提供的 API。

Salesforce API 请求数据库的时候和执行 SQL 语句差不多，但是你没办法一下子读取到所有数据！

如果想要得到一张表中的所有数据，你只能这么读：

<pre class="brush: csharp; gutter: true">var qResult = connection.query("SELECT FirstName, LastName FROM Contact");
var qResult2 = connection.queryMore(qResult.getQueryLocator());
var qResult3 = connection.queryMore(qResult2.getQueryLocator());</pre>

这是最粗暴的读取方式，每次读取只能得到200条数据，如果想要更多的数据，必须利用上次返回结果里的一串字符串，然后就可以得到后面一批数据了。

<!--more-->

笨办法就是用一个局部变量，每次查询结束后，把结果放进去，最后一起返回即可。

但这样内存中会有大量的数据，其实这里，也可以像上一篇文章那样，把细节封装起来！

&nbsp;

### <span id="i-2">利用迭代器封装细节</span>

<pre class="brush: csharp; gutter: true">public IEnumerable&lt;Contact&gt; GetAllContact()
{
    QueryResult results = null;
    do
    {
        results = results == null ?
                    connection.query("SELECT FirstName, LastName FROM Contact"):
                    connection.queryMore(results.getQueryLocator());

        foreach(var record in results.getRecords)
        {
            yield return record;
        }
    }while(!results.isDone())
}</pre>

思路很简单，直接进入一个 do-while 循环，如果是第一次就直接读取，如果不是第一次就利用上次的结果继续读取。

然后把数据用 yield return 返回即可。

&nbsp;

最终，外部调用这个方法的时候，只要不用 ToList() 等方法，它是延迟加载+延迟求值查询的，并不会一次性读出所有的数据，性能非常棒！
