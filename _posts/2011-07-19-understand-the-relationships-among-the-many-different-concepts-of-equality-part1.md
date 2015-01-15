---
title: '理解 .Net 中的各种“相等”关系 &#8211; Part1'
author: Dozer
layout: post
permalink: /2011/07/understand-the-relationships-among-the-many-different-concepts-of-equality-part1/
categories:
  - 编程技术
tags:
  - DotNet
  - CSharp
  - 读书笔记
---

### 申明

原文为《<a href="http://books.google.com/books?id=6qkSQQAACAAJ" target="_blank"><strong>Effective C#</strong></a>》中内容，作者为 <a href="http://www.google.com/search?q=Addison+Wesley" target="_blank"><strong>Addison Wesley</strong></a>

仅做翻译和修改（原文太长太罗嗦），但并不修改作者的原意。

&nbsp;

### C# 中的相等关系

当你定义了一个自己的类型后，你需要明确一下“相等”关系对你的类型来说意味着什么。

你可以使用 C# 提供的四种方法来判断他们是否相等。

    public static bool ReferenceEquals(object left, object right);
    public static bool Equals(object left, object right);
    public virtual bool Equals(object right);
    public static bool operator ==(MyClass left, MyClass right);

前两个是 Object 的静态方法，第三个是实例的方法，最后一个是 == 操作符。

变成语言允许你自定义这四个方法，但是并不提倡。前两个一定不要碰；实例的 Equals() 方法需要经常重写；== 操作符偶尔需要重写，特别是当考虑到值类型性能的时候。

除此以外，在这四个方法之间也有一定的联系，当你修改其中一个的时候也会影响到另外的几个。

<!--more-->

这四个方法也不是比较相等的唯一方法，引用类型重写 Equals() 的时候必须实现 IEquatable<T> 接口，值类型则需要实现 IStructuralEquality 接口。也就是说，其实总共有六种方法。

*<span style="color: #808080;">（这个 IStructuralEquality 网上都搜索不到任何信息，知识在 MSDN 的一篇文章中提到了一下，在代码中也找不到，难道是被扼杀在萌芽之中了？）</span>*

C#中，判断引用类型是否相等是看他们是不是被引用到了同一个对象上；而判断值类型是否相等，就看他们的结构和值是否相等。

这就是为什么“相等”测试需要那么多不同的方法。

&nbsp;

### Object 类型中的两个静态方法

**首先要明确一下，这两个方法你比应该去重新定义它**

**Object.ReferenceEquals()** 这个方法返回两个引用类型是否被引用到了同一个对象上，也就是说他们拥有相同的身份；

所以这个方法比较的是相同的“身份”，而不是相同的“值”，也就是说让你对两个值类型进行比较的时候，结果永远是 false；

    int i = 5;
    int j = 5;
    if (Object.ReferenceEquals(i, j))
    	Console.WriteLine("Never happens.");
    else
    	Console.WriteLine("Always happens.");
    if (Object.ReferenceEquals(i, i))
    	Console.WriteLine("Never happens.");
    else
    	Console.WriteLine("Always happens.");

&nbsp;

**Object.Equals()** 这个方法你也不应该去重新定义它，这个方法是当你不确定两个变量在运行中的类型时采用的，Object 是所有类型的基类，所以这个方法可以传入任何类型；

这个方法是这样实现的：

    public static new bool Equals(object left, object right)
    {
    	// Check object identity
    	if (Object.ReferenceEquals(left, right) )
    		return true;
    	// both null references handled above
    	if (Object.ReferenceEquals(left, null) || Object.ReferenceEquals(right, null))
    		return false;
    	return left.Equals(right);
    }

&nbsp;

现在理解为什么不应该重新定义这两个方法了吗？因为第一个你不能去重新定义它，而第二个你没必要去重新定义它，因为它最后调用的是类型本身的 Equals() 方法。
