---
title: 把 ref 和 out 关键字说透
author: Dozer
layout: post
permalink: /2011/10/ref-and-out-keywords/
duoshuo_thread_id:
  - 1171159103977075189
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - out
  - ref
  - 值类型
  - 引用类型
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#ref_out"><span class="toc_number toc_depth_1">1</span> ref 和 out 的区别</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 几个简单的演示</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">3</span> 问题一：关于值类型</a><ul>
        <li>
          <a href="#i-3"><span class="toc_number toc_depth_2">3.1</span> 个人总结有几个原则：</a>
        </li>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">3.2</span> 总结：</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">4</span> 问题二：关于引用类型</a>
    </li>
  </ul>
</div>

### <span id="ref_out">ref 和 out 的区别</span>

网上有很多这方面的文章，但是大部分人总是纠结于他们在原理上的那一点点细微的区别，所以导致了难以区分它们，也不知道什么时候改用哪一个了。

但是如果从试用场景的角度对它们进行区别的话，以后你一定不会再纠结了。

当你明白它们的适用场景后，再去扣其中的原理，使用中的一些问题也就迎刃而解了~

&nbsp;

简单的来说，它们的区别在于：

**ref 关键字 是作用是把一个变量的引用传入函数，和 C/C++ 中的指针几乎一样，就是传入了这个变量的栈指针。**

**out 关键字 的作用是当你需要返回多个变量的时候，可以把一个变量加上 out 关键字，并在函数内对它赋值，以实现返回多个变量。**

<!--more-->

### <span id="i">几个简单的演示</span>

上面说了 ref 和 out 的作用，非常简单，但是在具体使用的时候却遇到了很多麻烦，因为 C# 中本身就区分了引用类型和值类型。

我先举几个例子，来看看会出现哪些诡异的情况

&nbsp;

**代码段一：**

<pre class="brush:csharp">static void Main(string[] args)
{
    int a;
    Test1(out a);//编译通过

    int b;
    Test2(ref b);//编译失败
}

static void Test1(out int a)
{
    a = 1;
}
static void Test2(ref int b)
{
    b = 1;
}</pre>

这两个关键字看起来用法一样，为什么会有合格现象？

网上的答案很简单：out 关键字在传入前可以不赋值，ref 关键字在传入前一定要赋值。

这是什么解释？受之于鱼但并没有授之予渔！这到底是为什么呢？

想知道背后真正原理的呢，就继续看下去吧，后面我讲会讲到这里的区别。

&nbsp;

**代码二：**

<pre class="brush:csharp">static void Main(string[] args)
{
    object a = new object(), b = new object(), c = new object();

    Test1(out a);
    Test2(ref b);
    Test3(c);
    //最终 a,b,c 分别是什么？
    //a,b = null
    //c 还是 object
}

static void Test1(out object a)
{
    a = null;
}
static void Test2(ref object b)
{
    b = null;
}
static void Test3(object c)
{
    c = null;
}</pre>

新建三个 object，object是引用类型；三个函数，分别是 out,ref和普通调用；执行了一样的语句；最后的结果为什么是这样呢？

如果你只是从浅层次理解了 out 和 ref 的区别，这个问题你一定回答不上了。（我以前也不知道）

所以，这是为什么呢？继续往下看。

&nbsp;

^_^ 相信很多人晕了，我的目的达到了。（邪恶的笑~~）

那么，下面，我为大家从两个角度来分析一下。

对于值类型来说，加 out、加 ref 和什么都不加有什么共同点和区别？

对于引用类型来说，加 out、加 ref 和什么都不加有什么共同点和区别？

&nbsp;

&nbsp;

### <span id="i-2">问题一：关于值类型</span>

普通的传递值类型很简单了，传的只是一个值，没难度，平时都是这么用的，很好区分，所以这里就不惨和进去了。

接下来是 ref 和 out 的区别，为什么要了解区别呢？当然是为了了解怎么用它们，简单的来说就是需要了解：什么时候该用哪个。

&nbsp;

#### <span id="i-3"><strong>个人总结有几个原则：</strong></span>

**如果你是为了能多返回一个变量，那么就应该用 out：**

用 out 关键字有几个好处：可以不关心函数外是否被赋值，并且如果在函数内没有赋值的话就会编译不通过。（提醒你一定要返回）

你可以把它当成是另一种形式的 return 来用，我们来做一个类比：

return 语句的特点：接收 return 的变量事先不需要赋值（当然如果赋值了也没关系），在函数内必须 return。

可以看到 out 关键字的作用、行为、特点 和 return 是完全一样的。因为它当初设计的目的就是为了解决这个问题的。

&nbsp;

**如果你想要像引用类型那样调用值类型，那你就可以 ref：**

传入值类型的引用后，你可以用它，也可以不用它，你也可以重新修改它的各个属性，而函数外也可以随之改变。

我们来把 “传值类型的引用” 和 “传引用类型” 来做一个类比：

<pre class="brush:csharp">static void Main(string[] args)
{
    int a;
    Test1(ref a);//错误	1	使用了未赋值的局部变量“a”

    object b;
    Test2(b);//错误	2	使用了未赋值的局部变量“b”
}
static void Test1(ref int a) { }

static void Test2(object b) { }</pre>

传入加了 ref 的值类型 和 传入一个引用类型 的作用、行为、特点都是类似的。

同样，他们同时要遵守一个原则：传入前必须赋值，这个是为什么呢？

如果赋值后，传入两个函数的分别是 int a 的指针 和 object b 的指针。

而不赋值的话，a 和 b 根本还不存在，那它们又怎么会有地址呢？

&nbsp;

注意：如果你只写了 object a ，而在后面的代码中没有赋值，它并没有真正地分配内存。

我们可以看一下三个操作的 IL 代码：

<pre class="brush:csharp">private static void Main(string[] args)
{
    //IL_0000: nop
    object a;//没做任何事

    //IL_0002: ldnull
    //IL_0003: stloc.1
    object b = null;//在栈中增加了一个指针，指向 null

    //IL_0004: newobj instance void [mscorlib]System.Object::.ctor()
    //IL_0009: stloc.2
    object c = new object();//在栈中增加了一个指针，指向新建的 object 对象
}</pre>

传入引用类型的目的是把一个已经存在的对象的地址传过去，而如果你只是进行了 object a 声明，并没做复制，这行代码跟没做任何事！

所以，除非你使用了 out 关键字，在不用关键字和用 ref 关键字的情况下，你都必须事先复制。 out 只是一种特殊的 return

&nbsp;

#### <span id="i-4"><strong>总结：</strong></span>

现在你是否明白，当变量什么情况下该用什么关键字了吗？其实有时候 ref 和 out 都可以达到目的，你需要根据你的初衷，和它们的特点，来衡量一下到底使用哪个了！

另外，我们来看看两个同样的函数，用 out 和 ref 时候的 IL 代码

原函数：

<pre class="brush:csharp">private static void Test1(out int a)
{
    a = 1;
}
private static void Test2(ref int a)
{
    a = 1;
}</pre>

IL代码：

<pre class="brush:csharp">.method private hidebysig static
		void Test1 (
			[out] int32& a
		) cil managed
	{
		// Method begins at RVA 0x2053
		// Code size 5 (0x5)
		.maxstack 8

		IL_0000: nop
		IL_0001: ldarg.0
		IL_0002: ldc.i4.1
		IL_0003: stind.i4
		IL_0004: ret
	} // end of method Program::Test1

	.method private hidebysig static
		void Test2 (
			int32& a
		) cil managed
	{
		// Method begins at RVA 0x2059
		// Code size 5 (0x5)
		.maxstack 8

		IL_0000: nop
		IL_0001: ldarg.0
		IL_0002: ldc.i4.1
		IL_0003: stind.i4
		IL_0004: ret
	} // end of method Program::Test2</pre>

发现了吗？ 它们在函数内部完全是一样的！因为他们的原理都是传入了这个变量的引用。只是 out 关键字前面出现了一个标记 [out]

它们在原理上的区别主要在于编译器对它们进行了一定的限制。

最上面“代码段一”中的问题你现在明白了吗？

&nbsp;

&nbsp;

### <span id="i-5">问题二：关于引用类型</span>

对于值类型来说，最难区别的是 ref 和 out，而对于引用类型来说就不同了。

首先，引用类型传的是引用，加了 ref 以后也是引用，所以它们是一样的？暂时我们就这么认为吧~ 我们暂时认为它们是一样的，并统称为：传引用。

所以，对于引用类型来说，out 和 传引用 的区别跟对于值类型传 ref 和 out 的区别类似，具体适用场景也和值类型类似，所以就不多加阐述了。

&nbsp;

**虽然我们说直接传和加 ref 都可以统称为传引用，但是它们还是有区别的！而且是一个很隐蔽的区别。**

我们再来看一下最上面的代码段二：

<pre class="brush:csharp">static void Main(string[] args)
{
    object a = new object(), b = new object(), c = new object();

    Test1(out a);
    Test2(ref b);
    Test3(c);
    //最终 a,b,c 分别是什么？
    //a,b = null
    //c 还是 object
}

static void Test1(out object a)
{
    a = null;
}
static void Test2(ref object b)
{
    b = null;
}
static void Test3(object c)
{
    c = null;
}</pre>

out 关键字就相当于 return ，所以内部赋值为 null ，就相当于 return 了 null

可是，为什么引用类型还要加 ref 呢？它本身部已经是引用了吗？为什么加了以后就会有天大的区别呢？！

&nbsp;

用一句话概括就是：不加 ref 的引用是堆引用，而加了 ref 后就是栈引用！ @_@ 好搞啊。。什么跟什么？让我们一步步说清楚吧！

&nbsp;

**正常的传递引用类型：**

[<img class="alignnone size-medium wp-image-480" title="ref1" alt="" src="/uploads/2011/10/ref1-300x79.png" width="300" height="79" />][1]

**加了 ref 的传递引用类型：**

[<img class="alignnone size-medium wp-image-481" title="ref2" alt="" src="/uploads/2011/10/ref2-300x79.png" width="300" height="79" />][2]

这两张图对于上面那句话的解释很清楚了吧？

如果直接传，只是分配了一个新的栈空间，存放着同一个地址，指向同一个对象。

内外指向的都是同一个对象，所以对 对象内部的操作 都是同步的。

但是，如果把函数内部的 obj2 赋值了 null，只是修改了 obj2 的引用，而 obj1 依然是引用了原来的对象。

所以上面的例子中，外部的变量并没有收到影响。

同样，如果内部的对象作了  obj2 = new object() 操作以后，也不会对外部的对象产生任何影响！

&nbsp;

而加了 ref  后，传入的不是 object 地址，传入的是 object 地址的地址！

所以，当你对 obj2 赋 null 值的时候，其实是修改了 obj1 的地址，而自身的地址没变，还是引用到了 obj1

&nbsp;

虽然在函数内部的语句是一样的，其实内部机制完全不同。我们可以看一下IL代码，一看就知道了！

<pre class="brush:csharp">.method private hidebysig static
		void Test1 (
			object a
		) cil managed
	{
		// Method begins at RVA 0x2053
		// Code size 5 (0x5)
		.maxstack 8

		IL_0000: nop
		IL_0001: ldnull
		IL_0002: starg.s a
		IL_0004: ret
	} // end of method Program::Test1

	.method private hidebysig static
		void Test2 (
			object& a
		) cil managed
	{
		// Method begins at RVA 0x2059
		// Code size 5 (0x5)
		.maxstack 8

		IL_0000: nop
		IL_0001: ldarg.0//多了这行代码
		IL_0002: ldnull
		IL_0003: stind.ref
		IL_0004: ret
	} // end of method Program::Test2</pre>

上面是直接传入，并赋 null 值的

下面是加 ref 的

我们可以发现仅仅是多了一行代码：IL_0001: ldarg.0

其实，这样代码的作用就是讲参数0加载到堆栈上，也就是先根据引用，找到了外部的变量，然后再根据外部的变量，找到了最终的对象！

&nbsp;

那现在你知道什么时候该加 ref，什么时候不用加 ref 了吗？

再看了一个例子：

<pre class="brush:csharp">private static void Test1(List&lt;int&gt; list)
{
    list.Clear();
}
private static void Test2(ref List&lt;int&gt; list)
{
    list = new List&lt;int&gt;();
}</pre>

同样是清空一个 List，如果没加 ref ，只能用 clear。

而加了 ref 后可以直接 new 一个新的~

如果你没加 ref 就直接 new 一个新的了，抱歉，外部根本不知道有这个东西，你们操作的将不是同一个 List

&nbsp;

**所以，你一定要了解这点，并注意一下几件事：**

1、一般情况下不要用 ref

2、如果你没加 ref，千万别直接给它赋值，因为外面会接收不到…

&nbsp;

&nbsp;

现在你全部明白了吗？^_^

 [1]: /uploads/2011/10/ref1.png
 [2]: /uploads/2011/10/ref2.png