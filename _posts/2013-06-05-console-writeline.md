---
title: Console.WriteLine 的坑
author: Dozer
layout: post
permalink: /2013/06/console-writeline/
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  -
categories:
  - 编程技术
tags:
  - DotNet
  - 性能
---

### 扫地老太太

据说在每一个互联网公司里，都有一个扫地的老太太。很偶然地，当她经过一个程序员的身边，扫一眼屏幕上的代码，会低声提醒对方说：小心，栈溢出了…

别看这是一个笑话，我那天真的遇上了！

只不过扫地老太太变成了前端工程师…

&nbsp;

那天我在优化一个作业，里面有大批量的数据，为了监控我 `Console.WriteLine` 了。

然后前端工程师说：喂，不要用那么多的控制台输出，会影响性能的！

什么？控制台输出会影响性能？

我的三观瞬间崩塌了…

<!--more-->

&nbsp;

### 测试性能

我还是不相信这个残酷的现实，所以决定自己测试一下…

    class Program
    {
    	private static readonly ILog log = LogManager.GetLogger (typeof(Program));
    	private const int TestTimes = 10000;

    	static void Main (string[] args)
    	{
    		var a = NoWriteLine ();
    		var b = WriteLine ();
    		var c = Log4NetDebug ();
    		var d = Log4NetError ();
    		var e = DebugWriteLine ();

    		Console.WriteLine ("没有输出：" + a);
    		Console.WriteLine ("有输出：" + b);
    		Console.WriteLine ("Debug输出：" + e);
    		Console.WriteLine ("Log4Net没有输出：" + c);
    		Console.WriteLine ("Log4Net有输出：" + d);
    	}

    	private static long NoWriteLine ()
    	{
    		var watcher = new Stopwatch ();
    		watcher.Start ();

    		for (var k = 0; k &lt; TestTimes; k++) {
    		}
    		watcher.Stop ();
    		return watcher.ElapsedTicks;
    	}

    	private static long DebugWriteLine ()
    	{
    		var watcher = new Stopwatch ();
    		watcher.Start ();

    		for (var k = 0; k &lt; TestTimes; k++) {
    			Debug.WriteLine (k);
    		}
    		watcher.Stop ();
    		return watcher.ElapsedTicks;
    	}

    	private static long WriteLine ()
    	{
    		var watcher = new Stopwatch ();
    		watcher.Start ();

    		for (var k = 0; k &lt; TestTimes; k++) {
    			Console.WriteLine (k);
    		}
    		watcher.Stop ();
    		return watcher.ElapsedTicks;
    	}

    	private static long Log4NetDebug ()
    	{
    		var watcher = new Stopwatch ();
    		watcher.Start ();

    		for (var k = 0; k &lt; TestTimes; k++) {
    			log.Debug (k);
    		}
    		watcher.Stop ();
    		return watcher.ElapsedTicks;
    	}

    	private static long Log4NetError ()
    	{
    		var watcher = new Stopwatch ();
    		watcher.Start ();

    		for (var k = 0; k &lt; TestTimes; k++) {
    			log.Error (k);
    		}
    		watcher.Stop ();
    		return watcher.ElapsedTicks;
    	}
    }

&nbsp;

最终执行结果如下：

**Debug：**

> 没有输出：1103
>
> 有输出：792840
>
> Debug输出：31345359
>
> Log4Net没有输出：58874
>
> Log4Net有输出：3511244

&nbsp;

**Release：**

> 没有输出：934
>
> 有输出：635316
>
> Debug输出：223
>
> Log4Net没有输出：33297
>
> Log4Net有输出：2246490

&nbsp;

可以看到，一万次循环控制台输出，要消耗那么多时间！平均一次63毫秒。

对于我那个作业，5W 多次循环，每次循环多次控制台输出（大约5次），算下来竟然需要三个小时…

我的作业竟然浪费了三个小时在控制台输出上…

我的三观再次崩塌…

&nbsp;

### 解决方案

我上面的测试中已经提供了多种解决方案了，总之千万别用控制台输出了！

第一种方案是 `Debug.WriteLine`，Release 模式下不会有任何性能问题，但是控制台看不到输出！必须云星仔 VS 中才可以看到输出。

第二种方案是写一个自己的 WriteLine，然后可以用配置，或者 C# 条件编译使其在生产环境中不会消耗那么多时间。

第三种方案就是用 log4net 了，输出 `Debug` ，生产环境中配置成 INFO 及以上即可。

&nbsp;

个人推荐 log4net 方案，可以对所有日志有全局的控制。

虽然也有所损耗，但是还是降了一个数量级的，除非你对性能要求非诚非常高。
