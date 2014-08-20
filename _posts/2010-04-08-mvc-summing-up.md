---
title: MVC 小技巧总结
author: Dozer
layout: post
permalink: /2010/04/mvc-summing-up/
duoshuo_thread_id:
  - 1171159103977075148
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - Asp.net
  - MVC
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#1IISIIS6MVC"><span class="toc_number toc_depth_1">1</span> 1、不对IIS做任何修改，如何在IIS6下运行MVC？</a>
    </li>
    <li>
      <a href="#2AreasController"><span class="toc_number toc_depth_1">2</span> 2、不同Areas的Controller重复导致的问题</a>
    </li>
    <li>
      <a href="#3Filter"><span class="toc_number toc_depth_1">3</span> 3、关于Filter</a>
    </li>
    <li>
      <a href="#4MVCjs"><span class="toc_number toc_depth_1">4</span> 4、MVC中控制js代码（修改版）</a>
    </li>
    <li>
      <a href="#5WebDebugconfig_WebReleaseconfig"><span class="toc_number toc_depth_1">5</span> 5、Web.Debug.config 和 Web.Release.config 的用法</a>
    </li>
    <li>
      <a href="#6MVC"><span class="toc_number toc_depth_1">6</span> 6、MVC中捕捉错误</a>
    </li>
  </ul>
</div>

> 刚用MVC完成了一个小项目，MVC技术又有了一次提升，所以，再次写一点总结性的东西。
> 
> 开发环境：Visual Studio 2010 RC, MVC 2 RC, Entity Framework, SQL Server 2008

&nbsp;

### <span id="1IISIIS6MVC">1、不对IIS做任何修改，如何在IIS6下运行MVC？</span>

&nbsp;

这个可以参考我前面一篇文章

（原创，和微软官方做法不同，可以不修改IIS设置就达到目的）

传送门：<a href="/2010/02/run-mvc-in-iis6/" target="_blank"><strong>http://www.dozer.cc/2010/02/run-mvc-in-iis6/</strong></a>

<!--more-->

&nbsp;

### <span id="2AreasController">2、不同Areas的Controller重复导致的问题</span>

&nbsp;

两个不同的Areas会有不同的命名空间，但是会有相同的 Controller

而在网站MapRoute的时候却只能识别 Controller，因此会出现错误。

&nbsp;

假设，我在新建一个MVC项目后，直接新建一个Areas，并且命名为Admin，新建一个Home Controller

运行，弹出以下错误：

&nbsp;

<span style="font-size: large;"><span style="color: #ff0000;"><strong>“/”应用程序中的服务器错误。</strong></span></span>

<span style="color: #800000;"><strong>The controller name &#8216;Home&#8217; is ambiguous between the following types:</strong></span>

<span style="color: #800000;"><strong>MvcApplication1.Controllers.HomeController</strong></span>

<span style="color: #800000;"><strong>MvcApplication1.Areas.Admin.Controllers.HomeController</strong></span>

&nbsp;

遇到这种情况，只要这样就可以了

&nbsp;

<pre class="brush:csharp">context.MapRoute(
"Web_default",
"{controller}/{action}/{id}",
new {controller="Home", action = "Index", id = "" },
new string[] { "MvcApplication1.Areas.Web.Controllers" }
);</pre>

调用 MapRoute 的时候在后面多传入一个 String[] ，并且填入你需要 Route 的那个 Areas 的 Controller 所在的命名空间

注意！2个地方都要改

&nbsp;

&nbsp;

### <span id="3Filter">3、关于Filter</span>

&nbsp;

MVC提供的4个Filter很方便，但是有一个问题，Filter中不能直接调用 ViewData,TempData等字段。

虽然可以在传入的 filterContext 中调用到，但是很不方便。

这时候，其实可以把4个Filter继承一下，自己写一个新的，并在内部放入ViewData等私有字段

用 IAuthorizationFilter 来举个例子：

&nbsp;

<pre class="brush:csharp">public abstract class BaseFilterAttribute : FilterAttribute
{
    //这里可以根据自己的喜好来设定
    protected HttpSessionStateBase Session;
    protected ModelStateDictionary State;
    protected ViewDataDictionary ViewData;
    protected TempDataDictionary TempData;
    protected HttpRequestBase Request;
    protected Dictionary&lt;string, string&gt; RouteValues;
    protected UrlHelper Url;

    protected void Initialize(ControllerContext filterContext)
    {
        //初始化
        Request = filterContext.RequestContext.HttpContext.Request;
        RouteValues = new Dictionary&lt;string, string&gt;();
        foreach (var v in filterContext.RequestContext.RouteData.Values)
        {
            RouteValues.Add(v.Key, v.Value.ToString());
        }
        ViewData = filterContext.Controller.ViewData;
        TempData = filterContext.Controller.TempData;
        State = ViewData.ModelState;
        Session = filterContext.RequestContext.HttpContext.Session;
        Url = new UrlHelper(filterContext.RequestContext);
    }
}

public abstract class AuthorizationFilter : BaseFilterAttribute, IAuthorizationFilter
{
    public void OnAuthorization(AuthorizationContext filterContext)
    {
        //调用初始化函数
        Initialize(filterContext);
        onAuthorization(filterContext);
    }
    //这里把原来的 OnAuthorization 替换了一下
    public abstract void onAuthorization(AuthorizationContext filterContext);
}</pre>

然后需要使用 IAuthorizationFilter 的时候只要继承上面的 AuthorizationFilter 即可

&nbsp;

&nbsp;

### <span id="4MVCjs">4、MVC中控制js代码（修改版）</span>

&nbsp;

很多网友留言，说我这一块不好。我也发现的确如此，所以想了另一种方法，虽然不是最完美，但坐到了MVC的宗旨，view和controller分离

旧版本：

大家觉得MVC的架构变了，但其实原理和Asp.net一样，还是用 Response来输出数据

所以，只要在 Action 的 Return 函数前调用 Response.Write(&#8220;text&#8221;); 即可实现。

其实和以前一样，下面举个例子，在一个页面中弹出一个对话框后再跳转到别的页面

&nbsp;

<pre class="brush:csharp">public ActionResult Test()
{
    //弹出对话框
    Response.Write(&lt;script&gt;alert('test');&lt;/script&gt;));
    //跳转到index
    Response.Write("&lt;script&gt;window.location.href='" + Url.Action("index") + "';&lt;/script&gt;");
    return null;
}</pre>

&nbsp;

修改版：

这里，我换了一种思路来实现：

&nbsp;

<pre class="brush:csharp">public ActionResult Test()
{
    ViewData["JSAlert"] = "保存成功";
    ViewData["JSHref"] = "保存成功";
    return PartialView("JS");
}</pre>

&nbsp;

然后返回一个 用户控件

&nbsp;

<pre class="brush:xml">&lt;%@ Control Language="C#" Inherits="System.Web.Mvc.ViewUserControl" %&gt;
&lt;script type="text/jscript"&gt;
alert('&lt;%=ViewData["JSAlert"] %&gt;');
window.location.href = '&lt;%=ViewData["JSHref"] %&gt;';
&lt;/script&gt;</pre>

&nbsp;

&nbsp;

### <span id="5WebDebugconfig_WebReleaseconfig">5、Web.Debug.config 和 Web.Release.config 的用法</span>

&nbsp;

利用 Web.config, Web.Debug.config, Web.Release.config

可以在不同环境下生成3中不同的Web.config版本

在VS中调试的时候，直接使用Web.config

用Debug发布的时候，使用Web.Debug.config

用Release发布的时候，使用Web.Release.config

&nbsp;

然后，这三个文件怎么用呢？

你可以实现 Web.config 存在一个字段，然后当发布的时候用 Web.Debug.config 内的字段替换掉

也可以本来不存在，发布的时候添加

更可以本来存在，发布的时候删除

&nbsp;

这里就做简单的介绍，介绍一种替代的方法：

&nbsp;

<pre class="brush:xml">//Web.config下，假设有这个字段
&lt;connectionStrings&gt;
&lt;add name="ModelContainer"
    connectionString="metadata=res://*/Model.csdl|res://*/Model.ssdl|res://*/Model.msl;provider=System.Data.SqlClient;provider connection string="Data Source=192.168.174.131,1433;Initial Catalog=Port80;User ID=port80;Password=port80;MultipleActiveResultSets=True""
    providerName="System.Data.EntityClient"/&gt;
&lt;/connectionStrings&gt;

//在Web.Debug.config下

&lt;connectionStrings&gt;
&lt;add name="ModelContainer"
        connectionString&lt;/span&gt;="metadata=res://*/Model.csdl|res://*/Model.ssdl|res://*/Model.msl;provider=System.Data.SqlClient;provider connection string="Data Source=.\sqlexpress;Initial Catalog=Port80;Integrated Security=True""
        providerName="System.Data.EntityClient"
        xdt:Transform="Replace"
        xdt:Locator="Match(name)"/&gt;
&lt;/connectionStrings&gt;</pre>

&nbsp;

这样，在用Debug发布的时候，那个字段就会被替换掉，具体用法在Web.Debug.config文件内写了一个网站，上面有全部的语法

&nbsp;

&nbsp;

### <span id="6MVC">6、MVC中捕捉错误</span>

&nbsp;

MVC中，有一个Filter可以捕捉错误，但是它的用法是利用Attribute来实现的，而且只能加在Controller和Action上，所以不能捕捉别出的错误

其实理论上所有的错误肯定产生于 Controller 中，但有2种情况下，就不会被捕捉了

1、页面不存在的时候，找不到对应的 Controller，那没有任何 Controller 被执行，所以自然也不会捕捉到错误了

2、在 IAuthorizationFilter 下发生错误的时候，错误捕捉代码在 IExceptionFilter 中，而 IAuthorizationFilter 的优先权高于 IExceptionFilter，所以也就捕捉不到了

那有没有别的方法？参考了一个老外的代码，发现了一种完美的方法

&nbsp;

<pre class="brush:csharp">protected void Application_Error(object sender, EventArgs e)
{

    Exception exception = Server.GetLastError();

    Response.Clear();

    HttpException httpException = exception as HttpException;
    RouteData routeData = new RouteData();
    routeData.Values.Add("controller", "Error");

    if (httpException == null)
    {
        routeData.Values.Add("action", "Index");
    }
    else //It's an Http Exception, Let's handle it.
    {

        switch (httpException.GetHttpCode())
        {
            case 404:
                // Page not found.
                routeData.Values.Add("action", "HttpError404");
                break;
            case 500:
                // Server error.
                routeData.Values.Add("action", "HttpError500");
                break;
            // Here you can handle Views to other error codes.
            // I choose a General error template
            default:
                routeData.Values.Add("action", "General");
                break;
        }
    }

    // Pass exception details to the target error View.
    routeData.Values.Add("error", exception.Message);

    // Clear the error on server.
    Server.ClearError();

    // Call target Controller and pass the routeData.
    IController errorController = new WEB.Controllers.ErrorController();
    errorController.Execute(new RequestContext(
    new HttpContextWrapper(Context), routeData));

}</pre>

&nbsp;

把这段代码放到 Global.asax 中，并且新建一个 Controller 叫做 Error

&nbsp;

<pre class="brush:csharp">namespace WEB.Controllers
{
    public class ErrorController : Controller
    {
        public ActionResult Index(string error)
        {
            ViewData["Title"] = "WebSite 网站内部错误";
            ViewData["Description"] = error;
            return View("Index");
        }

        public ActionResult HttpError404(string error)
        {
            ViewData["Title"] = "HTTP 404- 无法找到文件";
            ViewData["Description"] = error;
            return View("Index");
        }

        public ActionResult HttpError500(string error)
        {
            ViewData["Title"] = "HTTP 500 - 内部服务器错误";
            ViewData["Description"] = error;
            return View("Index");
        }

        public ActionResult General(string error)
        {
            ViewData["Title"] = "HTTP 发生错误";
            ViewData["Description"] = error;
            return View("Index");
        }
    }
}</pre>

&nbsp;

这样，就可以捕捉所有错误了。

&nbsp;

但其实，这样也不是完美的，因为如果你参考了我第一个问题中，在IIS6下不修改IIS设置，运行了MVC，那当后缀名不是.aspx的时候，错误不会被捕捉

因为这时候输入的地址根本没有交给网站来处理，IIS直接抛出了错误，因为IIS认为这个后缀名不是你所能执行的