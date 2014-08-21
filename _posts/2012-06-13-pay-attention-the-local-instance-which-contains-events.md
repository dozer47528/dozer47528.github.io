---
title: 请注意绑定了事件的局部对象
author: Dozer
layout: post
permalink: /2012/06/pay-attention-the-local-instance-which-contains-events/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103979703995
categories:
  - 编程技术
tags:
  - .Net
  - CSharp
  - GC
  - 垃圾回收
---

### <span id="GeoCoordinateWatcher">GeoCoordinateWatcher 的诡异问题</span>

前两天在做 **<a href="http://zh.wikipedia.org/wiki/Windows_Phone" target="_blank">WP7</a>** 开发，需要用到 **<a href="http://zh.wikipedia.org/wiki/GPS" target="_blank">GPS</a>** 定位，这里会用到一个 **<a href="http://msdn.microsoft.com/zh-cn/library/system.device.location.geocoordinatewatcher.aspx" target="_blank">GeoCoordinateWatcher</a>** 类。

写了一段代码后发现自己写错了，但是它竟然可以运行！再仔细一推敲，发现了很多坑。

&nbsp;

我在 <a href="http://stackoverflow.com/" target="_blank"><strong>stackoverflow</strong></a> 上也报告了这个问题：**<a href="http://stackoverflow.com/questions/10992100/how-to-dispose-the-local-variable-that-contains-event" target="_blank">传送门</a>**

问题代码如下：

<pre class="brush: csharp; gutter: true">private void button1_Click(object sender, RoutedEventArgs e)
{
    GeoCoordinateWatcher watcher = new GeoCoordinateWatcher();
    watcher.PositionChanged += new EventHandler&lt;GeoPositionChangedEventArgs&lt;GeoCoordinate&gt;&gt;(watcher_PositionChanged);
    watcher.Start();
}

void watcher_PositionChanged(object sender, GeoPositionChangedEventArgs&lt;GeoCoordinate&gt; e)
{
    Debug.WriteLine(e.Position.Timestamp.ToString());
}</pre>

上述代码中，理论上 watcher 实例在按钮点击事件后应该会被销毁，所以下面的 PositionChanged 事件应该也不会被触发。

一开始这么写，是我的错误，但是看到这个问题后，我才发现我的程序是可以正常运作的…

调试后才发现，这个对象永远不会被销毁，每按一次就会多一个实例，并且你找不到它！

GPS 位置每改变一次，所有的实例就会输出调试信息。

<!--more-->

### <span id="i">网友的解答</span>

发帖后，很多老外给予我帮助，一个人说：每次绑定事件，这个实例的 **<a href="https://www.google.com/search?q=%E5%BC%95%E7%94%A8%E8%AE%A1%E6%95%B0" target="_blank">引用计数</a>** 就会加一，所以除非取消事件绑定，否则它不会被销毁。

嗯… 初看很有道理，但是其实有很多问题：

1.  C# 中用的是垃圾回收，而不是引用计数，两者是不同的。具体可以看看这个：**<a href="http://blogs.msdn.com/b/abhinaba/archive/2009/01/30/back-to-basics-mark-and-sweep-garbage-collection.aspx" target="_blank">传送门</a>**
2.  如果非要说是事件的原因，那也应该是实例引用了委托，然后委托再引用了事件的提供这吧？

&nbsp;

我将信将疑地发了第二个问题：**<a href="http://stackoverflow.com/questions/10997060/why-cant-the-instance-bound-to-an-event-be-collected-by-the-gc" target="_blank">传送门</a>**

这时，一个在我上个问题中回答过我的人（当时他回答地太简单）看不下去了。

这位老外指出了另一个人的错误，也开始道出了自己的猜想：

一定是 GeoCoordinateWatcher 在执行 start() 方法的时候将自己放置在了某个地方，保持被引用状态，所以才不会被销毁！

根本没有引用计数这个说法！

&nbsp;

### <span id="i-2">反编译后终得结果</span>

为了寻找最后的结果，决定反编译一下这个类：

<pre class="brush: csharp; gutter: true">public override bool TryStart(bool suppressPermissionPrompt, TimeSpan timeout)
{
    if (!this.IsStarted)
    {
        this.IsStarted = true;
        if (this.Status != GeoPositionStatus.Ready || this.m_position.Location.IsUnknown)
        {
            this.m_eventGetLocDone = new ManualResetEvent(false);
            ThreadPool.QueueUserWorkItem(GetInitialLocationData, suppressPermissionPrompt);
            if (timeout != TimeSpan.Zero && !this.m_eventGetLocDone.WaitOne(timeout))
            {
                this.Stop();
            }
        }
        else
        {
            this.OnPositionChanged(new GeoPositionChangedEventArgs&lt;GeoCoordinate&gt;(this.m_position));
        }
    }
    return this.IsStarted;
}</pre>

原来，**这个 start() 函数把实例内部的另外一个方法加入了线程池，并保持运行。**

****所以，就算就算实例看上去被销毁了，实际上它还是被线程池引用着。

&nbsp;

### <span id="i-3">解决方法</span>

既然找到了原因，就需要去避免它。在上面这段代码中，有两种方式可以避免：

1.  在触发 PositionChanged 事件后对实例执行 stop() 函数，这样可以让这个线程停下来。
2.  在父实例中，保持对 watcher 的引用，这样做更好，可以随时开关，也不用但是产生多余的实例。

&nbsp;

### <span id="i-4">其他类似的类</span>

由于这个问题，我又想到了很多别的类，也会有同样的用法，那的类会有怎么样的表现呢？

我这里测试了一下 **<a href="http://msdn.microsoft.com/zh-cn/library/system.net.webclient(v=vs.80).aspx" target="_blank">WebClient</a>**：

<pre class="brush: csharp; gutter: true">private void Form1_Load(object sender, EventArgs e)
{
    for (var k = 0; k &lt; 10000; k++)
    {
        StartWebClient();
    }
}
private void StartWebClient()
{
    WebClient client = new WebClient();
    client.DownloadStringCompleted += client_DownloadStringCompleted;
    client.DownloadStringAsync(new Uri("http://www.dozer.cc"));
}
int count = 0;
public void client_DownloadStringCompleted(object sender, DownloadStringCompletedEventArgs e)
{
    count++;
    label1.Text = count.ToString();
}</pre>

测试后发现，WebClient 也和上面的一样！DownloadStringCompleted 事件根本也会被触发！

执行完上述代码后，程序会保持对 10000 个实例的引用，内存占用高达 100MB。

[<img class="alignnone size-medium wp-image-773" title="explorer" alt="" src="/uploads/2012/06/explorer-300x60.png" width="300" height="60" />][1]

但是还好，一般情况下也不会用那么多实例，而且 WebClient 不像前面那个，WebClient 执行一次后就停止了，然后就会被回收了。

&nbsp;

### <span id="i-5">总结</span>

最后，发现了问题以后肯定要避免以下了。

首先像 WebClient 这样只会出发一次事件的，可以不去管它，最终也会被回收。没必要外父实例内保持引用。

但是，像 GeoCoordinateWatcher 这样持续触发事件的，一定不能这么些了！否则你会多出很多多余的实例！

具体怎么做就需要根据不同的类进行不同的处理了。总之一定要注意！

 [1]: /uploads/2012/06/explorer.png
