---
title: 责任链模式
author: Dozer
layout: post
permalink: /2014/11/chain-of-responsibility.html
categories:
  - 编程技术
tags:
  - Java
  - 设计模式
---

### Chain of Responsibility

> 在 面向对象程式设计里, 责任链模式是一种软件设计模式，它包含了一些命令对象和一系列的处理对象。每一个处理对象决定它能处理哪些命令对象，它也知道如何将它不能处理的命令对象传递给该链中的下一个处理对象。该模式还描述了往该处理链的末尾添加新的处理对象的方法。
> 
> 传送门：[责任链模式](http://zh.wikipedia.org/wiki/%E8%B4%A3%E4%BB%BB%E9%93%BE%E6%A8%A1%E5%BC%8F)

Java 中见到最多的对责任链模式的应用就是在`Servlets Filters`中了：

	public class LogFilter implements Filter  {
	   @Override
	   public void  init(FilterConfig config) 
	                         throws ServletException{ }
	
	   @Override                      
	   public void  doFilter(ServletRequest request, 
	                 ServletResponse response,
	                 FilterChain chain) 
	                 throws java.io.IOException, ServletException {
	
	      // do something
	      
	      chain.doFilter(request,response);
	   }
	}

<!--more-->

&nbsp;

### 如何自己实现一个 Filter Chain

责任链模式非常适合做`Filter`，如果你的组件中需要像`Servlets Filters`一样注入各种`Filter`，那可以自己实现一套`Filter`机制。

首先是一个`Filter`接口：

	public interface FilterWithChain {
		Object getData(ChainTest source, FilterChainWrapper chain);
	}

接口中的方法根据自己的需求定制，需要用到什么参数就传进来，但是有1个参数必不可少，那就是`FilterChainWrapper chain`。这将会是责任链模式的核心。

那就让我们实现`FilterChainWrapper`吧：

	public class FilterChainWrapper implements FilterWithChain {
	
		private final List<FilterWithChain> filters;
	
		public int index = 0;
	
		public FilterChainWrapper(List<FilterWithChain> filters) {
			this.filters = filters;
		}
	
		@Override
		public Object getData(ChainTest source, FilterChainWrapper chain) {
			if (index < filters.size()) {
				return filters.get(index++).getData(source, chain);
			} else {
				return source.getDataOrigin();
			}
		}
	}

然后是一个`Filter`的实现类：

	public class FilterWithChainImpl implements FilterWithChain {
		@Override
		public Object getData(ChainTest source, FilterChainWrapper chain) {
			// do something
			return chain.getData(source, chain);
		}
	}

最后是需要用到`Filter`的主体类，这里将演示怎么调用`Filter Chain`：

	public class ChainTest {	
		private static List<FilterWithChain> fiveChainFilter;
		
		static {
			fiveChainFilter = new ArrayList<>();
			fiveChainFilter.add(new FilterWithChainImpl());
			fiveChainFilter.add(new FilterWithChainImpl());
			fiveChainFilter.add(new FilterWithChainImpl());
			fiveChainFilter.add(new FilterWithChainImpl());
			fiveChainFilter.add(new FilterWithChainImpl());
		}
		
		public void withFiveChain() {
			FilterChainWrapper chain = new FilterChainWrapper(fiveChainFilter);
			chain.getData(this, chain);
		}
		
		public Object getDataOrigin() {
			//do something
			return null;
		}
	}

&nbsp;

### Filter Chain 的优缺点

`Filter Chain`最大的优点就是性能，在整个调用过程中，只有一次对象创建：


	FilterChainWrapper chain = new FilterChainWrapper(fiveChainFilter);

无论有多少个`Filter`，都只有一次，那它的优势到底有多大呢？下一个章节会具体分析。

&nbsp;

我们先谈谈`Filter Chain`的缺点：

`Filter Chain`最大的缺点在于，`ChainTest`是真正的业务类，但`FilterChainWrapper`中却不得不包含`ChainTest`的业务代码，哪怕只有一行，也是不合理的。而且这也迫使`ChainTest`讲很多方法暴露成`public`了。

&nbsp;

### 用 lambda 表达式来实现 Filter Chain

既然说`Filter Chain`性能好，那到底有多好呢？

我这里又用了4种方式来实现了`Filter`，具体的代码在这里：

[https://github.com/dozer47528/chain-test](https://github.com/dozer47528/chain-test)

* 利用匿名类来实现：代码略复杂，不够干净，写起来略烦，不剥离业务逻辑。
* 利用`lambda`表达式来实现：代码最干净，写起来最简单，不剥离业务逻辑。
* 利用`lambda`表达式和`Filter Chain`相结合来实现：代码很干净，写起来还算可以，不剥离业务逻辑。
* `Filter Chain`：代码最烦，业务逻辑被迫剥离。

其中，匿名类是在 jdk8 以下对`lambda`表达式的另一种实现，核心差不多，代码量稍微多一点。

因为代码量有点大，所以直接可以直接看项目即可。

&nbsp;

### 利用 jmh 进行微基准测试

这里正好介绍一下在`Java`中如何利用`jmh`进行微基准测试。

首先需要在`pom.xml`中依赖相关组件：

    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-core</artifactId>
        <version>1.1.1</version>
    </dependency>
    <dependency>
        <groupId>org.openjdk.jmh</groupId>
        <artifactId>jmh-generator-annprocess</artifactId>
        <version>1.1.1</version>
    </dependency>

然后直接创建一个类并加上一些注解即可：

	@Benchmark  //标注这是一个微基准测试
	@BenchmarkMode(Mode.Throughput)  //测试模式，这里是测试吞吐量
	@OutputTimeUnit(TimeUnit.MILLISECONDS)  //时间单位
	@Threads(value = 5)  //线程数
	@Warmup(iterations = 2, time = 1)  //热身次数
	@Measurement(iterations = 5, time = 1)  //循环次数和每次循环的时间
	@Fork(value = 2)  //进程数
	public void withFiveChainAndLambda() {
		FilterChainAndLambdaWrapper chain = new FilterChainAndLambdaWrapper(fiveChainWithLambdaFilter);
		chain.doFilter(() -> originMethod(), chain);
	}

最后还需要在 Eclipse 或者 Intellij 中安装 jmh 插件，不安装的话可以通过命令行执行。

&nbsp;

那上面4中实现的性能到底如何呢？（下面测试的是吞吐量，数字越大越好）



	Benchmark                                Mode  Samples       Score       Error   Units
	c.d.ChainTest.withFiveCallBack          thrpt       10   35277.617 ±  8759.203  ops/ms
	c.d.ChainTest.withFiveChain             thrpt       10  105702.626 ±  9383.335  ops/ms
	c.d.ChainTest.withFiveChainAndLambda    thrpt       10   82992.075 ± 19440.107  ops/ms
	c.d.ChainTest.withFiveLambda            thrpt       10   33136.952 ±  5626.830  ops/ms
	c.d.ChainTest.withOneCallBack           thrpt       10  105173.192 ± 11270.208  ops/ms
	c.d.ChainTest.withOneChain              thrpt       10  292336.527 ± 42589.521  ops/ms
	c.d.ChainTest.withOneChainAndLambda     thrpt       10  165933.621 ± 35242.708  ops/ms
	c.d.ChainTest.withOneLambda             thrpt       10  109378.187 ± 18834.925  ops/ms


为什么效果差那么多？因为利用`Filter Chain`来实现的代码每次只是额外创建一个对象，而且创建的类不会随着`Filter`的增加而增加。

`lambda`表达式和`Filter Chain`相结合，每次额外创建两个对象，也不会随着`Filter`的增加而增加。

但是另外两种实现会额外创建很多的对象，而且`Filter`越多，创建的也越多！

&nbsp;

### 如何选择

从性能测试上来看，它们性能差别巨大，但实际上，我的测试代码中没有真正的逻辑代码。虽然它们性能上有差距，但实际情况下，每次请求调用测试一般都是个位数的，所以大家还是要根据自己的场景来做选择。

其实，如果你是在写业务代码，很多时候就直接用`AOP`来实现类似功能了，例如一个`Service`的一个方法，在一次请求中只有一次调用，如果要在这里做一个`LogFilter`，那对性能影响微乎其微。

但是如果你是在做一些中间件，那在一次请求中的调用次数会非常多，这时候就不能掉以轻心了！尽量用最佳的性能去写你的代码。