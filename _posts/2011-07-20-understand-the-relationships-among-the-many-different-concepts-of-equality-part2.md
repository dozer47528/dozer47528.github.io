---
title: '理解 .Net 中的各种“相等”关系 &#8211; Part2'
author: Dozer
layout: post
permalink: /2011/07/understand-the-relationships-among-the-many-different-concepts-of-equality-part2/
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - 读书笔记
---

### <span id="_Equals">实例的 Equals() 方法</span>

在讨论这个函数之前，你必须明确一下在数学中的相等关系代表着什么。你需要确保你定义的和别人理解的是相一致的。

数学中的相等关系是 自反的、对称的和可传递的

*   a == a //自反性
*   if a==b then b==a //对称性
*   if a==b && b==c then a==c //传递性

&nbsp;

**如果你不自定义实例的 Equals() 函数会发生什么：**

**引用类型 **判断的是它们之间身份的统一性，和 Object.ReferenceEquals() 等效，因为如果你不重写的话，它实际上调用的是 Object.Equals() 方法。

*<span style="color: #999999;">注意：这里的 Object.Equals() 方法并不是静态的 Object.Equals() 方法，它们传递的参数不同。</span>*

*<span style="color: #999999;">前者是：Equals(object obj)，后者是：Equals(object objA, object objB)</span>*

**值类型 **是不是也是这样呢？如果是的话，那么值类型的 Equals() 方法永远是 false 了，其实不然，值类型的 Equals() 比较的是它们的值是否相同，而不是引用。

*<span style="color: #999999;">注意：为什么会这样呢？因为所有的值类型不是直接继承 Object 的，而是继承了 ValueType ，而这个类重写了 Equals() 方法。</span>*

<!--more-->

**什么时候该重写？**

**引用类型** 默认判断的是两个变量是否引用了同一个对象，如果你需要改变这个定义，你就需要重写实例的 Equals() 方法了；

**值类型** 只要是自定义的值类型，都建议重写实例的 Equals() 方法；

引用类型什么时候该重写很好理解，值类型为什么要这么做呢？

因为只要你是自定义的值类型（struct），默认实例的 Equals() 方法会调用该类型中所有属性的 Equals() 方法来进行比较，全部相等后说明相等。

但是程序怎么知道你有哪几个属性？那当然需要用到反射技术了，反射的性能大家都知道吧？

所以，在使用自定义的值类型时，强烈建议重写实例 Equals() 方法，自己编写需要比较的属性。

&nbsp;

&nbsp;

### <span id="_Equals-2">引用类型实例 Equals() 方法的正确写法</span>

理解上面的内容后让我们再来讨论下应该怎么正确地重写 Equals() 方法。

让我们一步步地去实现它，下面是一个第一个示例：

<pre class="brush:csharp">public class Foo : IEquatable&lt;Foo&gt;
{
	public override bool Equals(object right)
	{
		// check null:
		// this pointer is never null in C# methods.
		if (object.ReferenceEquals(right, null))
			return false;
		if (object.ReferenceEquals(this, right))
			return true;

		// Discussed below.
		if (this.GetType() != right.GetType())
			return false;
		// Compare this type's contents here:
		return this.Equals(right as Foo);
	}
	#region IEquatable&lt;Foo&gt; Members
	public bool Equals(Foo other)
	{
		// 写一些代码，判断两个类型在逻辑上是否相等。
		return true; //这是伪代码
	}
	#endregion
}</pre>

&nbsp;

**设计原则：**

1.  实现 IEquatable<Foo> 接口； 具体可参考：**<http://www.cnblogs.com/ldp615/archive/2009/09/05/1560791.html>**
2.  永远不要抛出异常，所有的异常都应该返回 false；
3.  判断类型，放置派生类和父类之间关系的不确定性（如有需要，当然也可以不判断，但是逻辑会变得很复杂）；
4.  重写 GetHashCode()； 具体可参考：**<http://msdn.microsoft.com/zh-cn/library/ms182358.aspx>**

&nbsp;

&nbsp;

&nbsp;

### <span id="i"> == 操作符</span>

看完了上面的，再来看 == 操作符就简单多了。

**== 操作符的重写原则：**

1.  如果创建了自己的值类型，那就应当重写，原因和重写 Equals() 一样；
2.  引用类型尽量不要重写，因为 == 操作符对于引用类型来说，就是用来判断它们身份的，也就是是否引用到同一个对象上；

&nbsp;

### <span id="i-2">总结</span>

C#给了我们那么多种判断相等的方法，而你需要考虑的只是其中两个（实例的 Equals() 方法和 == 操作符），另外两个没必要也不应该重写，因为从逻辑上，它们永远是正确的。

*   **自定义值类型，都应该重写实例的 Equals() 函数和 == 操作符；**
*   **自定义引用类型，如果需要从逻辑上判断它们是否相等，那么就应该重写实例的 Equals() 函数；**
*   **一旦重写，就应当实现 IEquatable<T> 接口；**

这就是最终的结论了，很简单对不对？

&nbsp;

&nbsp;

### <span id="i-3">备注</span>

原文中有这么一段：

> Finally, you come to IStructuralEquality, which is implemented on System.Array and the Tuple<> generic classes. It enables those types to implement value semantics without enforcing value semantics for every comparison. It is doubtful that you’ll ever create types that implement IStructuralEquality. It is needed only for those lightweight types. Implementing IStructuralEquality declares that a type can be composed into a larger object that implements value-based semantics.

这段文字中提到的 IStructuralEquality 接口，无论是网上、MSDN、类库中都找不到，这是什么情况？等到高人解答！

&nbsp;
