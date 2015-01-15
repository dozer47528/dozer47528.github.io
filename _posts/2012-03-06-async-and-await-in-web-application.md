---
title: async 与 await 在 Web 下的应用
author: Dozer
layout: post
permalink: /2012/03/async-and-await-in-web-application/
categories:
  - 编程技术
tags:
  - AspDotNet
  - async
  - await
  - MVC
  - 异步
---

### .net 中的异步

关于 .net 的异步，一篇文章是讲不完的，我这里就贴两篇文章让大家看一下：

<a href="http://blog.zhaojie.me/2008/02/use-async-operation-properly.html" target="_blank"><strong>《正确使用异步操作》</strong></a>、<a href="http://www.cnblogs.com/fish-li/archive/2011/10/23/2222013.html" target="_blank"><strong>《C#客户端的异步操作》</strong></a>、**<a href="http://www.cnblogs.com/fish-li/archive/2011/11/20/2256385.html" target="_blank">《细说ASP.NET的各种异步操作》</a>**

另外，在 .net 4.0 中还推出了新的任务并行库（TPL），也是一种新异步模式：

**<a href="http://msdn.microsoft.com/zh-cn/library/dd460717.aspx" target="_blank">《任务并行库》</a>**

最后，.net 4.5 又推出了全新的 async 和 await 关键字：

<a href="http://blog.zhaojie.me/2010/10/pdc2010-the-future-of-csharp-and-vb-by-anders-hejlsberg-1.html" target="_blank"><strong>《C#与Visual Basic的未来（上）》</strong></a>

<a href="http://blog.zhaojie.me/2010/10/pdc2010-the-future-of-csharp-and-vb-by-anders-hejlsberg-2.html" target="_blank"><strong>《C#与Visual Basic的未来（中）》</strong></a>

**<a href="http://blog.zhaojie.me/2010/11/pdc2010-the-future-of-csharp-and-vb-by-anders-hejlsberg-3.html" target="_blank">《C#与Visual Basic的未来（下）》 </a>**

最后，在这几篇文章的基础上，想和大家谈谈 async 和 await 在 Web 下的应用，包括 <a href="http://zh.wikipedia.org/wiki/ASP.NET" target="_blank"><strong>WebForm</strong></a> 和 <a href="http://zh.wikipedia.org/wiki/ASP.NET_MVC_Framework" target="_blank"><strong>MVC</strong></a>。

<!--more-->

### async 与 await 的简单介绍

仔细看完老赵的《C#与Visual Basic的未来》大家应该都能明白这两个关键字的作用是什么了。

&nbsp;

#### 适用条件：只能适用于TPL异步模式

传统的方法返回的就是需要返回的内容，而基于TPL模式的异步，返回的都是 Task<T>，其中的 T 类型就是你需要返回内容的类型。

在 <a href="http://www.microsoft.com/visualstudio/11/zh-cn" target="_blank"><strong>Visual Studio 11</strong></a> 中，只要你调用的某个方法返回的类型是 Task 或者 Task<T>，它就会提示这是一个可等待的方法。

[<img class="alignnone size-full wp-image-664" title="canwait" alt="canwait" src="/uploads/2012/03/canwait.png" width="499" height="132" />][1]

这时候，就可以利用 async 和 await 关键字了。

&nbsp;

#### 场景：解决基于事件的异步中回调函数嵌套使用中的问题

假设有这样一个场景，一个 C# 应用程序中（WinForm Or WPF）我需要从一个网站上下载一个内容，然后再根据内容里的网址再下载里面的内容。

如果直接利用 WebClient 的 DownloadString 方法，很明显 UI 线程会被阻塞，没人会这么做。

如果只是一次下载，那利用 WebClient 的 DownloadStringAsync 就可以轻松解决了，但是如果是想这样需要两次下载，而且两次下载是有关联的呢？如果是三次四次呢？

我们先来看看用基于事件的异步来实现：

    protected void DownloadAsync()
    {
        WebClient client = new WebClient();
        client.DownloadStringCompleted += client_DownloadStringCompleted;
        client.DownloadStringAsync(new Uri("http://www.website.com"));
    }
    void client_DownloadStringCompleted(object sender, DownloadStringCompletedEventArgs e)
    {
        WebClient client = new WebClient();
        client.DownloadStringCompleted+=client_DownloadStringCompleted2;
        client.DownloadStringAsync(new Uri(e.Result));
    }
    void client_DownloadStringCompleted2(object sender, DownloadStringCompletedEventArgs e)
    {
        var result = e.Result;//最终结果
        //do more
    }

下面再来看看用 async 和 await 来实现：

    protected async void DownloadTaskAsync() {
        WebClient client = new WebClient();
        var result1 = await client.DownloadStringTaskAsync("http://www.website.com");
        WebClient client2 = new WebClient();
        var result2 = await client.DownloadStringTaskAsync(result1);
        //do more
    }

是不是简单多了？

&nbsp;

### 在 WebForm 和 MVC 中使用 async 和 await

在 .net 4.5 中，最新的 WebForm 和 MVC 都已经支持这两个关键字了。

#### 在 asp.net WebForm 中：

1.  <del>首先新建一个页面</del>
2.  <del>打开 aspx 文件，然后再顶部的属性中加入：Async=&#8221;true&#8221;</del>
3.  <del>接下来在任何一个事件中，加入这两个关键字即可</del>
4.  <del>另外在 Web.Config 中有两个奇怪的配置，有可能会导致出错，去掉有正常，这两个配置具体有什么用，我已经在 <a href="http://stackoverflow.com/questions/9562836/whats-the-meaning-of-usetaskfriendlysynchronizationcontext" target="_blank"><strong>StackOverFlow</strong></a> 上问别人了</del>

    //以下代码有错误，请勿使用
    protected async void Page_Load(object sender, EventArgs e)
    {
        WebClient client = new WebClient();
        var result1 = await client.DownloadStringTaskAsync("http://www.website.com");
        WebClient client2 = new WebClient();
        var result2 = await client.DownloadStringTaskAsync(result1);
        //do more
    }

<span style="color: #ff0000;">在 asp.net WebForm 的正确用法请参考最新文章，上述方法被证实有错误：<a href="/2012/03/async-and-await-in-asp-net-beta/" target="_blank"><span style="color: #ff0000;"><strong>传送门</strong></span></a></span>

&nbsp;

#### 在 asp.net MVC 中：

把原来继承于 Controller 改成继承于 AsyncController

在方法前加上 async，并把返回类型改成 Task<T>

    public class HomeController : AsyncController
    {
        public async Task&lt;ActionResult&gt; Test()
        {
            var result = await Task.Run(() =&gt;
            {
                Thread.Sleep(5000);
                return "hello";
            });
            return Content(result);
        }
    }

&nbsp;

#### 在 IHttpHandlder 中：

微软官方的 .net 4.5 <a href="http://www.asp.net/vnext/overview/whitepapers/whats-new#_Toc318097378" target="_blank"><strong>releace note</strong></a> 中已经提到了：

    public class MyAsyncHandler : HttpTaskAsyncHandler
    {
        // ...

        // ASP.NET automatically takes care of integrating the Task based override
        // with the ASP.NET pipeline.
        public override async Task ProcessRequestAsync(HttpContext context)
        {
            WebClient wc = new WebClient();
            var result = await
                wc.DownloadStringTaskAsync("http://www.microsoft.com");
            // Do something with the result
        }
    }

&nbsp;

####  在 IHttpModule 中：

同样是微软官方的 .net 4.5 <a href="http://www.asp.net/vnext/overview/whitepapers/whats-new#_Toc318097377" target="_blank"><strong>releace note</strong></a> 中，实现起来有点复杂，大家可以自己去看看。

&nbsp;

### 在 Web 应用程序中使用 async 和 await 的注意事项

其实不仅仅是使用这两个关键字的注意事项，而是在 Web 中只要用到了异步页，就要注意一下问题！

**Web 本来就是多线程的，为什么还要用异步编程？**

多线程只是实现异步的一种手段，的确，Web 本来就是多线程的，所以在很多时候不用异步也没什么问题。一般也不会有问题，只是有更好的方案。

大家看完**<a href="http://blog.zhaojie.me/2008/02/use-async-operation-properly.html" target="_blank">《正确使用异步操作》</a>**后就会知道，异步有多种实现方式，但是它们底层只有两种类型，一种是：“Compute-Bound Operation”，另一种是“IO-Bound Operation”。（具体的可以到文中查看）

在 Web 中，使用异步去处理“Compute-Bound Operation”是没有意义的，因为 Web 本来就是多线程的，这样做没有任何效率上的提升。（除非你在处理这个异步的时候，不需要等待这个异步执行结束就可以返回页面内容）

所以，在 Web 中，只有当你需要面对“IO-Bound Operation”的时候，去用异步页才是真的有用的。因为它是在等待磁盘或者网络响应，并不占据资源，甚至不占据工作线程。

如何区分呢？那篇文章中已经写了，另外，大部分和磁盘&网络打交道的异步操作都是“IO-Bound Operation”的。

但是，如果你真的想要提升效率，还需要你亲自去测试一下，因为要实现“IO-Bound Operation”有一定的条件。

#### WebClient、WebService 和 WCF 支持吗？

经过测试，上面这三种 Web 应用程序中使用最多的，是支持“IO-Bound Operation”的。其中，在 .net 4.5 中，WebClient 和 WCF 可以直接支持 async 和 await 关键字。（因为它们有相关的方法可以返回 Task 对象）

而 WebService（微软不建议使用，但实际上还在被大量的应用），却不支持，但是可以通过写一些代码后让它支持。

#### 数据库操作支持吗？

经过一定的配置后，它是可以支持的，但是具体的还需要进行大量的测试，毕竟不是调用几个方法那么简单。

&nbsp;

### 如何把传统的异步模式转换成 TPL 模式，以实现 async 和 await

上面提到了 WebService 并没有实现 TPL 模式，在 .net 4.5 中引用 WebService 后实现的是基于事件的异步。

<span style="color: #ff0000;">（.net 2.0 以上程序在引用 WebService 的时候，需要点“添加服务引用”——“高级”——“添加Web引用”，如果直接在服务引用中添加，会出现一定的问题。并且，就算你添加了，它也没有帮你实现基于 TPL 的异步。）</span>

#### 如何把 APM 模式转换成 TPL 模式？

其实微软在这篇文章中已经写过如何把传统的异步模式转换成 TPL 模式了：<a href="http://msdn.microsoft.com/ZH-CN/library/dd997423(VS.110).aspx" target="_blank"><strong>TPL 和传统 .NET 异步编程</strong></a>

其中 APM 转 TPL 比较简单，我就不多介绍了。

&nbsp;

#### 如何把 EAP 模式转换成 TPL 模式？

EAP 就是基于事件的异步，上面那篇文章中其实也提到了，但是写的并不是很清楚。

下面我用一段简化的代码来实现 EAP 转 TPL：

    namespace WebServiceAdapter.MyWebService
    {
        public partial class WebService
        {
            /// &lt;summary&gt;
            /// 无 CancellationToken 的调用
            /// &lt;/summary&gt;
            /// &lt;returns&gt;&lt;/returns&gt;
            public Task&lt;string&gt; HelloWorldTaskSync()
            {
                return HelloWorldTaskSync(new CancellationToken());
            }

            /// &lt;summary&gt;
            /// 有 CancellationToken 的调用
            /// &lt;/summary&gt;
            /// &lt;param name="token"&gt;&lt;/param&gt;
            /// &lt;returns&gt;&lt;/returns&gt;
            public Task&lt;string&gt; HelloWorldTaskSync(CancellationToken token)
            {
                TaskCompletionSource&lt;string&gt; tcs = new TaskCompletionSource&lt;string&gt;();

                token.Register(() =&gt;
                {
                    //注册 CancellationToken
                    this.CancelAsync(null);
                });

                //注册完成事件
                this.HelloWorldCompleted += (object sender, HelloWorldCompletedEventArgs args) =&gt;
                {
                    if (args.Cancelled == true)
                    {
                        tcs.TrySetCanceled();
                        return;
                    }
                    else if (args.Error != null)
                    {
                        tcs.TrySetException(args.Error);
                        return;
                    }
                    else
                    {
                        tcs.TrySetResult(args.Result);
                    }
                };

                //异步调用
                this.HelloWorldAsync();

                //返回 Task
                return tcs.Task;
            }
        }
    }

转换好后再去配合使用 async 和 await 关键字就方便多了：

    protected async void Page_Load(object sender, EventArgs e)
    {
        using (WebService service = new WebService())
        {
            await service.HelloWorldTaskSync();
        }
    }

&nbsp;

### 性能测试

#### 测试的理论：

异步页最大的用处就是在处理“IO-Bound Operation”的时候可以不占据工作线程，验证逻辑如下：

*   限制网站应用程序的工作线程，然后同时请求一个页面，请求数大于工作线程数。
*   请求的页面会访问一个 WebService ，这个 WebService 会延迟5秒，对于网站来说，这个5秒就是“IO-Bound Operation”。
*   如果限制了工作线程数后，异步页所有请求都可以在5秒完成，那说明的确没有占据工作线程。反之则说明理论错误！

&nbsp;

#### 前期准备：

最开始我使用浏览器测试，但是一直有问题，没解决，所以改用 ab.exe 来测试了。

后来发现了原因，原来浏览器在请求的时候带上了 Cookie，所以自然会启用 Session，而 Session 是线程安全的，所以会造成阻塞。

具体的可以看一下 Fish-Li 的文章：<a href="http://www.cnblogs.com/fish-li/archive/2011/07/31/2123191.html" target="_blank"><strong>Session，有没有必要使用它？</strong></a>

用 ab.exe 我一开始限制的工作线程是10，然后同时请求50，但是无论是异步页还是同步页，总耗时都差不多…

后来仔细看老赵的文章（<a href="http://blog.zhaojie.me/2009/01/lab-async-request.html" target="_blank"><strong>体会ASP.NET异步处理请求的效果</strong></a>）才发现，原来在 Vista & Win7 中最大请求数被限制在10了，所以多于10的请求根本没到达网站应用程序。

最后我把工作线程限制在2，然后同时请求10，终于得到了正确的理论数据！

&nbsp;

#### 工具准备：

我这里用的工具是 apache 下那只的 ab.exe，简单好用！

另外我也写了相关的代码来支持测试。

下载地址在文章最后。

&nbsp;

#### 开始测试：

运行 WebService，提供一个会延时5秒的服务。

然后运行网站，有三个页面：

*   NoAsyncPage.aspx ：传统的页面
*   AsyncPage_IO.aspx：异步页面，和传统页面一样，都是调用 WebService ，但是是用异步调用
*   AsyncPage_CPU.aspx：为了验证在异步中执行“Compute-Bound Operation”是没有意义的

&nbsp;

在CMD中，依次用 ab.exe 调用这三个页面：

    ab -c 10 -n 10 http://localhost:6360/noasyncpage.aspx
    ab -c 10 -n 10 http://localhost:6360/asyncpage_io.aspx
    ab -c 10 -n 10 http://localhost:6360/asyncpage_cpu.aspx

&nbsp;

最终运行结果如下：

*   NoAsyncPage.aspx ：26.39秒
*   AsyncPage_IO.aspx：5.29秒
*   AsyncPage_CPU.aspx：26.54秒

&nbsp;

#### 数据分析：

仔细分析下数据，会发现都符合理论：

*   NoAsyncPage.aspx ：没有采用异步，2个工作线程，10个请求，总时间在10*5/2=25以上。
*   AsyncPage_IO.aspx：采用异步页，不占据工作线程，10个请求同时执行。
*   AsyncPage_CPU.aspx：虽然采用了异步页，但是异步的时候依然占据了一个工作线程，而且还多了新建线程和切换线程的损耗。

&nbsp;

[<img class="alignnone size-medium wp-image-665" title="async" alt="async" src="/uploads/2012/03/async-300x194.png" width="300" height="194" />][2]

最终结果非常让人满意，特别是AsyncPage_IO.aspx，如果我们把访问量大，并且需要等在磁盘或者是网络的页面都改写成这样，那可以大大减少IIS管线的消耗！

&nbsp;

### 源代码和工具下载

<a href="/wp-content/uploads/2012/03/AsyncSample.zip" target="_blank">AsyncSample</a>

*请用 Visual Studio 11 打开*

 [1]: /uploads/2012/03/canwait.png
 [2]: /uploads/2012/03/async.png
