---
title: 不要在 ASP.NET 4.5 Beta 的 Page 类事件上直接使用 async 与 await
author: Dozer
layout: post
permalink: /2012/03/async-and-await-in-asp-net-beta.html
categories:
  - 编程技术
tags:
  - AspDotNet
  - async
  - await
  - MVC
  - 异步
---

### 发现问题

在我的上一篇文章<a href="/2012/03/async-and-await-in-web-application.html" target="_blank"><strong>《async 与 await 在 Web 下的应用》</strong></a>中，我提到了 asp.net 4.5 在 Web.Config 中的一个奇怪配置：

    <appSettings>
      <add key="aspnet:UseTaskFriendlySynchronizationContext" value="true" />
    </appSettings>

在 <a href="http://stackoverflow.com/questions/9562836/whats-the-meaning-of-usetaskfriendlysynchronizationcontext" target="_blank"><strong>Stack Overflow</strong></a> 上提问后，终于有人回答我了。

看了别人的回复后，才发现了我上篇文章中的问题。

下面代码中的这种用法是错误的：

    protected async void Page_Load(object sender, EventArgs e)
    {
        WebClient client = new WebClient();
        var result1 = await client.DownloadStringTaskAsync("http://www.website.com");
        WebClient client2 = new WebClient();
        var result2 = await client.DownloadStringTaskAsync(result1);
        //do more
    }

<!--more-->

### 在事件上直接使用 async 引发的错误

#### 代码段一：

    public partial class WebForm1 : System.Web.UI.Page
    {
        protected string Msg { get; set; }
        protected async void Page_Load(object sender, EventArgs e)
        {
            using (WebService service = new WebService())
            {
                Msg = await service.Method1TaskSync();
            }
        }

        protected async void Button_Test_Click(object sender, EventArgs e)
        {
            using (WebService service = new WebService())
            {
                Msg = await service.Method2TaskSync();
            }
        }
    }

试问，最后的 Msg 的值是什么？应该是哪个方法的返回值？

如果去掉异步，那答案肯定是 Method2。那加上异步后呢？

这里用的是 async 和 await 来实现了异步，所以逻辑上的先后次序应该和代码上的先后次序一样。

但是上述代码两个事件会一起执行！导致了一定的问题！

总结一下上面代码的问题：当页面中的 Page_Load 事件和别的事件都用了 async 和 await 后会出现执行次序错误、死锁等问题。它们并不会按次序执行。

&nbsp;

#### 代码段二：

    <appSettings>
      <add key="aspnet:UseTaskFriendlySynchronizationContext" value="true" />
    </appSettings>

&nbsp;

    <%@ Page Language="C#" AutoEventWireup="true" CodeBehind="WebForm1.aspx.cs" Inherits="AsyncAwait.WebForm1"
        Async="true" %>

    <!DOCTYPE html>
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head runat="server">
        <title></title>
    </head>
    <body>
        <form id="form1" runat="server">
        <div>
            <%:Msg %>
        </div>
        </form>
    </body>
    </html>

后端代码和上面一样的代码，只不过把 UseTaskFriendlySynchronizationContext 的配置改成了 true，并且把数据显示到了页面上。

执行后发现：根本无法显示内容，页面在异步执行结束前就已经输出完毕了。

&nbsp;

### UseTaskFriendlySynchronizationContext 的作用和错误引发的原因

其实在老外的回答中已经说明了全部，我这里主要是翻译+精简一下。

&nbsp;

#### UseTaskFriendlySynchronizationContext 的作用：

之前版本的 asp.net 所使用的异步不符合 CLR 的规范，而只有 RegisterAsyncTask 这个方法是符合 CLR 规范的。

所以 asp.net 4.5 中，加入这个新的配置是为了禁用掉之前不符合约定的功能，只要把这个配置设置为了 true，别的异步方案全部会失效。（代码段二主要就是演示了这个现象）

&nbsp;

#### 引发错误的原因：

async 和 await 关键字在底层主要是利用 SynchronizationContext 来实现了异步。（具体原理我也没研究过）

而这个方案首先不符合 CLR 规范，另外也会引起很多问题。（代码段一主要就是演示了其中一个问题）

&nbsp;

### 目前正确的写法

首先，建议把 UseTaskFriendlySynchronizationContext 设置为 true。

另外，正确的写法如下：

    public partial class WebForm1 : System.Web.UI.Page
    {
        protected string Msg { get; set; }
        protected void Page_Load(object sender, EventArgs e)
        {
            RegisterAsyncTask(new PageAsyncTask(Method1));

        }
        private async Task Method1()
        {
            using (WebService service = new WebService())
            {
                Msg = await service.HelloWorldTaskSync();
            }
        }

        protected void Button_Test_Click(object sender, EventArgs e)
        {
            RegisterAsyncTask(new PageAsyncTask(Method2));
        }

        private async Task Method2()
        {
            using (WebService service = new WebService())
            {
                Msg = await service.HelloWorldTaskSync();
            }
        }
    }

如果需要写异步，一定要用 RegisterAsyncTask 方法，实测证明，支持多次调用，而且会按次序执行。

&nbsp;

老外说了，他们也想直接在事件上加 async 来写，但是由于技术原因并没有实现，希望在正式版或者未来的版本中可以实现吧！

&nbsp;

#### 参考资料：

<a href="http://stackoverflow.com/questions/9562836/whats-the-meaning-of-usetaskfriendlysynchronizationcontext" target="_blank">http://stackoverflow.com/questions/9562836/whats-the-meaning-of-usetaskfriendlysynchronizationcontext</a>

<a href="http://social.msdn.microsoft.com/Forums/en-NZ/async/thread/b2e8c51e-2808-46d0-92e9-b825321d0af8" target="_blank">http://social.msdn.microsoft.com/Forums/en-NZ/async/thread/b2e8c51e-2808-46d0-92e9-b825321d0af8</a>
