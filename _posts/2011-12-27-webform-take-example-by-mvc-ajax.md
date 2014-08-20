---
title: 那些 WebForm 可以从 MVC 借鉴的东西 —— Ajax
author: Dozer
layout: post
permalink: /2011/12/webform-take-example-by-mvc-ajax/
duoshuo_thread_id:
  - 1171159103977075193
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - Ajax
  - Asp.net
  - javascript
  - MVC
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#MVC"><span class="toc_number toc_depth_1">1</span> MVC 的优雅</a>
    </li>
    <li>
      <a href="#WebForm"><span class="toc_number toc_depth_1">2</span> WebForm 中就不行了吗？</a>
    </li>
    <li>
      <a href="#_MVC_Ajax"><span class="toc_number toc_depth_1">3</span> 如何实现 MVC 中的 Ajax 用法</a>
    </li>
    <li>
      <a href="#_UserControl"><span class="toc_number toc_depth_1">4</span> 后端输出 UserControl：方法一</a>
    </li>
    <li>
      <a href="#_UserControl-2"><span class="toc_number toc_depth_1">5</span> 后端输出 UserControl：方法二</a>
    </li>
    <li>
      <a href="#_WebForm_MVC_Unobtrusive_JavaScript"><span class="toc_number toc_depth_1">6</span> 如何在 WebForm 中使用 MVC 的 Unobtrusive JavaScript</a>
    </li>
  </ul>
</div>

### <span id="MVC">MVC 的优雅</span>

用过 MVC 中局部更新的同学肯定会觉得其中的写法真的是非常的优雅：

<pre class="brush:csharp">public ActionResult Index()
{
    var data = UserService.GetUserList();
    if (Request.IsAjaxRequest())
    {
        return PartialView("UserList", data);
    }
    else
    {
        return View(data);
    }
}</pre>

如果在页面上加上一个刷新按钮后，第一次显示就能读取到这个 PartialView 的内容，点即刷新后就可以刷新页面。

这里的读取逻辑本应该是一样的，应该是写在同一个地方的，MVC 做到了这一点。

<!--more-->

### <span id="WebForm">WebForm 中就不行了吗？</span>

不是说 WebForm 中就不能实现类似的功能了，其实同样的功能完全可以通过 Ajax 或 UpdatePannel 来实现，并且也可以公用逻辑代码。

但是不这么做当然是因为它们有一定的缺陷。

&nbsp;

**Ajax+json：**

这个写过的人肯定都明白它有多痛苦，特别是但更新的内容是一个复杂表格的时候… 我觉得没人会这么做吧？

**Ajax+后台拼接 Html：**

这种写法也大有人在，但是这实在是太不雅了！直接 PASS！

**UpdatePannel：**

UpdatePannel 对懒人和新手来说真是一个好东西啊。不用懂任何原理就可以实现 Ajax 无刷新更新数据。

但是它有一个很大的缺点，每次请求都会传送 ViewState，特别是当一个页面的 ViewState 很多的时候：

[<img class="alignnone size-large wp-image-528" title="updatepannel" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/12/updatepannel-1024x782.png" width="640" height="488" />][1]

是不是很恐怖… 这还叫 Ajax 吗？还不如直接刷新页面呢！

另外，有很多人写 WebForm 完全不用控件，当然也包括 UpdatePannel。

**MVC风格：**

MVC 中的 Ajax 写法可以说是吸取了以上几种方法的有点，摒弃了它们的缺点。

首先它是纯粹的 Ajax 请求，不包含任何多余的数据（没有 ViewState）。

另外它把生成 Html 的工作交给了 UserControl（MVC 中称为 PartialView）。

最后，它也实现了代码的重用。

&nbsp;

&nbsp;

### <span id="_MVC_Ajax">如何实现 MVC 中的 Ajax 用法</span>

想在 WebForm 中使用类似 MVC 中的 Ajax 写法，难点主要就是两个：后端输出 UserControl + 前端代码

&nbsp;

后端输出 UserControl 是为了把重复的代码写在 UserControl 中，并且可以被直接访问到。所以这里的难题是，如何让 UserControl 能够被直接访问。

默认 UserControl 是禁止访问的，因为它本身并不是继承与 IHttpHandler 所以无法直接输出，这里不懂的可以去搜索一下 <a href="http://www.google.com/search?q=IHttpHandler" target="_blank"><strong>IHttpHandler</strong></a>。

&nbsp;

后台能输出 UserControl 后其实已经非常简单了，前端部分自己写 js 就可以实现了，点击后 Ajax 请求 UserControl 的地址，得到数据后填充即可。

但是体验过 MVC 中 Ajax 的人都知道，这部分在 MVC 中也是不用写任何代码的，特别是 MVC 中的 <a href="/2010/11/unobtrusive-javascript/" target="_blank"><strong>Unobtrusive JavaScript</strong></a>，让代码更优美了。

所以，这里的难点并不是前端代码，而是如何使用  **<a href="/2010/11/unobtrusive-javascript/" target="_blank">Unobtrusive JavaScript</a>。**

&nbsp;

&nbsp;

### <span id="_UserControl">后端输出 UserControl：方法一</span>

怎么输出 UserControl？如果你不理解 Asp.net 核心的一些对象，也完全可以实现。

其实最简单的就是，把 .ascx 的页面用 .aspx 的页面包装一下，就可以啦！

&nbsp;

**我们先新建一个 .ascx 页面：**

[<img class="alignnone size-large wp-image-530" title="ascx" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/12/ascx-1024x743.png" width="640" height="464" />][2]

并在里面写上一些代码，这里是用来随便输出一些时间的，页面上需要点“刷新”来更新这些数据。

&nbsp;

**接下来我们新建一个 .aspx 页面：**

[<img class="alignnone size-large wp-image-531" title="wrap" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/12/wrap-1024x743.png" width="640" height="464" />][3]

这个页面完全是一个空页面，仅仅是为了把 UserControl 输出。

&nbsp;

突然发现，输出 UserControl 就这样实现了！

这时候，前端请求它的时候只要请求这个 TimeList_.aspx 即可，相当于是它的外壳。

&nbsp;

&nbsp;

### <span id="_UserControl-2">后端输出 UserControl：方法二</span>

上面的那个方法虽然好用，但是总感觉的怪怪的，也略显麻烦。

其实上述的过程就是一个把 UserControl类 用 Page类 包裹的过程，这个过程完全可以用代码来实现。

&nbsp;

**首先我们先要自己实现一个 HttpHandler 来输出 UserContol：**

<pre class="brush:csharp">namespace WebApplication1
{
    public class AjaxHandler : IHttpHandler
    {
        //private const string FLAG = ".ajax";//去掉这里的注释即可实现自定义后缀
        public void ProcessRequest(HttpContext context)
        {
            var page = new Page();
            var writer = new StringWriter();
            var url = context.Request.AppRelativeCurrentExecutionFilePath;

            //判断后缀是否为指定的后缀，是的话就替换成 .ascx
            //if (url.IndexOf('?') &lt; 0 || url.IndexOf('?') &gt; url.IndexOf(FLAG)) { url = url.Replace(FLAG, ".ascx"); }//去掉这里的注释即可实现自定义后缀

            //加载控件，并输出页面
            var control = page.LoadControl(url);
            page.Controls.Add(control);
            context.Server.Execute(page, writer, false);
            context.Response.Write(writer.ToString());
        }

        public bool IsReusable
        {
            get
            {
                return true;
            }
        }
    }
}</pre>

&nbsp;

**接下来修改 Web.Config 文件，在这里添加一条记录，让所有的 .ascx 页面都由这个 AjaxHandler 来处理：**

<pre class="brush:xml">&lt;system.web&gt;
      &lt;httpHandlers&gt;
        &lt;add verb="*" path="*.ascx" type="WebApplication1.AjaxHandler,WebApplication1"/&gt;
      &lt;/httpHandlers&gt;
    &lt;/system.web&gt;</pre>

这里，type 中传入的两个参数分别是这个 HttpHandler 的完整名称，包括前面的命名空间；都好后面是这个 HttpHandler 所在的 dll 文件名。

&nbsp;

**让我们来直接访问一下：**

[<img class="alignnone size-full wp-image-533" title="timelist" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/12/timelist.png" width="369" height="161" />][4]

&nbsp;

成功！还有一个问题，怎么使用自定义扩展名？

只要把 HttpHandler 中的两行注释去掉，并且在 Web.Config 文件中的 path=&#8221;*.ascx&#8221; 改成 path=&#8221;.[自定义]&#8221; 就行了。

&nbsp;

&nbsp;

### <span id="_WebForm_MVC_Unobtrusive_JavaScript">如何在 WebForm 中使用 MVC 的 Unobtrusive JavaScript</span>

看过 <a href="/2010/11/unobtrusive-javascript/" target="_blank"><strong>Unobtrusive JavaScript</strong></a> 的人都知道，这种方式可以让 js 代码和 html 完全分离。也就是说，只要 WebForm 输出了同样格式的 html，并引用了相关的 js，就可以实现这个功能了！让我们一步步实现它。

&nbsp;

我们先来用一个MVC 项目输出一个“刷新”按钮。

得到了如下代码：

<pre class="brush:xml">&lt;a data-ajax="true" data-ajax-method="GET" data-ajax-mode="replace" data-ajax-update="#testDiv" href="/Home/ajax"&gt;刷新&lt;/a&gt;</pre>

这里的 html 代码和是否使用 MVC 没有关系，那我们就尝试着直接在 WebForm 里直接打入以上代码吧。

另外，我们也要引入2个js，jquery.js 和 jquery.unobtrusive-ajax.js

前者去下载最新版即可，后者可以新建一个 MVC3 的项目后在项目中找到。

&nbsp;

最终代码如下：

<pre class="brush:xml">&lt;%@ Page Language="C#" AutoEventWireup="true" CodeBehind="Default.aspx.cs" Inherits="WebApplication1.Default" %&gt;

&lt;%@ Register Src="TimeList.ascx" TagName="TimeList" TagPrefix="uc1" %&gt;
&lt;!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"&gt;
&lt;html xmlns="http://www.w3.org/1999/xhtml"&gt;
&lt;head runat="server"&gt;
    &lt;script src="Scripts/jquery-1.5.1.js" type="text/javascript"&gt;&lt;/script&gt;
    &lt;script src="Scripts/jquery.unobtrusive-ajax.js" type="text/javascript"&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
    &lt;form id="form1" runat="server"&gt;
    &lt;div id="timeList"&gt;
        &lt;uc1:TimeList ID="TimeList1" runat="server" /&gt;
    &lt;/div&gt;
    &lt;a data-ajax="true" data-ajax-method="GET" data-ajax-mode="replace" data-ajax-update="#timeList"
        href="/timelist.ascx"&gt;刷新&lt;/a&gt;
    &lt;/form&gt;
&lt;/body&gt;
&lt;/html&gt;</pre>

&nbsp;

前面，我在链接中的 attribute 是直接复制 MVC3 项目<span style="color: #000000;">生成的 html 代码，那在 WebForm 里怎么生成这个代码呢？</span>

<span style="color: #000000;">其实只要把 MVC3 中的一个 class 和 enum 赋值过来即可。它们分别是：AjaxOptions 和 InsertionMode</span>

利用 AjaxOptions 这个类的 ToUnobtrusiveHtmlAttributes 方法就可以生成一组符合标准的 attribute，然后再用代码把这些 attribute 附加到 a 标签上即可。

[<img class="alignnone size-full wp-image-535" title="ajaxoptions" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/12/ajaxoptions.png" width="671" height="332" />][5]

这里要注意的是，从 MVC3 源码中赋值过来的 AjaxOptions 在 .Net3.5 下会有点问题，自己编译一下修改下即可。

主要就是有几个方法在 .Net3.5 中不存在，所以只能自己实现了，但效果是一样的，它并没有依赖很多东西。

&nbsp;

下面是一段参考代码：

.aspx.cs页面：

<pre class="brush:csharp">protected string GetAttributes(AjaxOptions ajaxOptions)
{
    var sb = new StringBuilder(" ");
    foreach (var attribute in ajaxOptions.ToUnobtrusiveHtmlAttributes())
    {
        sb.Append(string.Format("{0}=\"{1}\" ", attribute.Key, attribute.Value));
    }
    return sb.ToString();
}</pre>

.aspx 页面：

<pre class="brush:xml">&lt;a &lt;%=GetAttributes(new WebApplication1.AjaxOptions{ UpdateTargetId = "timeList"}) %&gt; href="/timelist.ascx"&gt;刷新&lt;/a&gt;</pre>

看上去还没那么优雅，但是已经能实现这个功能了！

&nbsp;

 [1]: http://www.dozer.cc/wp-content/uploads/2011/12/updatepannel.png
 [2]: http://www.dozer.cc/wp-content/uploads/2011/12/ascx.png
 [3]: http://www.dozer.cc/wp-content/uploads/2011/12/wrap.png
 [4]: http://www.dozer.cc/wp-content/uploads/2011/12/timelist.png
 [5]: http://www.dozer.cc/wp-content/uploads/2011/12/ajaxoptions.png