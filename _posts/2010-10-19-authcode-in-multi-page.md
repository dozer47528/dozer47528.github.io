---
title: 多页面验证码冲突的解决办法
author: Dozer
layout: post
permalink: /2010/10/authcode-in-multi-page/
duoshuo_thread_id:
  - 1171159103977075159
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - Asp.net
  - MVC
  - 验证码
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 场景：</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 其他网站的“解决办法”：</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 基本思路：</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">4</span> 验证码管理类——概况：</a>
    </li>
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">5</span> 验证码管理类——用法：</a>
    </li>
    <li>
      <a href="#Aspnet"><span class="toc_number toc_depth_1">6</span> 验证码管理类——Asp.net 用法：</a>
    </li>
    <li>
      <a href="#MVC"><span class="toc_number toc_depth_1">7</span> 验证码管理类——MVC 用法：</a>
    </li>
    <li>
      <a href="#i-6"><span class="toc_number toc_depth_1">8</span> 可扩展性：</a>
    </li>
    <li>
      <a href="#i-7"><span class="toc_number toc_depth_1">9</span> 后记：</a>
    </li>
  </ul>
</div>

### <span id="i"><span style="line-height: 19px;"><strong>场景：</strong></span></span>

某网站在许多地方需要验证码（例如：文件下载、发表留言等），所以用户可能会打开多个包含验证码的页面，根据常规验证码实现的思路，会导致冲突，只有最后一个页面的验证码是可以用的，如何解决？

### <span id="i-2"><strong>其他网站的“解决办法”：</strong></span>

1、大部分网站，例如中国移动和中国电信的网站并没有做任何优化，只有最后打开的一个网页的验证码可用。如果这个验证码仅仅是用来验证登陆的话问题不大。

2、中国联通的网站用一个小技巧解决了这个问题。给输入验证码的输入框绑定一个事件，每次获得焦点的时候获取一个新的验证码，这样也就保证了，不管你在哪输入验证码，每当你想要输入的时候，它就给你一个最新的。

3、xun6网盘的解决方案，用了一个key，给每一个验证码标一个key，这样也就防止了冲突。

[<img class="alignnone size-medium wp-image-174" title="authcode" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/authcode-300x63.png" width="300" height="63" />][1]

<!--more-->

### <span id="i-3"><strong>基本思路：</strong></span>

我的解决方案应该和xun6的差不多，也是用了一个key，来代表本次会话，然后根据这个key去得到验证码。

基本思路如下：

[<img class="alignnone size-medium wp-image-175" title="visio" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/visio-215x300.png" width="215" height="300" />][2]

左：直接打开或刷新页面时的流程

中：不刷新页面更换验证码的流程

右：验证流程

&nbsp;

关键：如果一个表单中有验证码，那么也需要在这个表单中存储一下这个会话的ID，用来对应服务端的验证码

&nbsp;

&nbsp;

### <span id="i-4"><strong>验证码管理类——概况：</strong></span>

可以看到，这个过程中，流程是固定的，所以完全自己设计一个类，来实现这个“复杂”的过程，因为我懒得每次都重写一遍~

（懒人才能促进科技的发展，哈哈~）

&nbsp;

直接看类设计图吧，关键看一下公有方法（我隐藏了字段，属性和私有方法，因为这些只是浮云~）：

[<img class="alignnone size-medium wp-image-176" title="uml" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/uml-300x215.png" width="300" height="215" />][3]

&nbsp;

&nbsp;

### <span id="i-5"><strong>验证码管理类——用法：</strong></span>

1、IAuthCodeBuilder接口，这是什么？因为验证码生成的步骤区别很大，大家自由一套办法，所以需要传入一个验证码构造者来生成和输出验证码，实现该接口即可。

[<img class="alignnone size-medium wp-image-177" title="interface" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/interface-300x156.png" width="300" height="156" />][4]

2、再看构造函数和Initialize方法，无参数的构造函数&Initialize函数，需要配合Unity来使用，用来实现依赖注入。如果你不想使用依赖注入，可以修改我的源码，把他们上面的Attribute去掉即可~

&nbsp;

3、另外几个构造函数，IAuthCodeBuilder前面已经解释过了，另外一个字符串是什么？因为最终是以字典的形式保存在Session中的，所以需要有个名字，默认是&#8221;AuthCode”。

&nbsp;

4、关键函数之：Create

根据上面生成图片的流程图，在此过程中，得到了会话ID后需要调用此函数，把会话ID和验证码保存到Session中。

&nbsp;

5,、关键函数之：Authorize

提交表单后，根据用户输入的验证码和会话ID,判断是否正确。

&nbsp;

&nbsp;

### <span id="Aspnet"><strong>验证码管理类——Asp.net 用法：</strong></span>

**1、后端代码 Default.aspx.cs**

&nbsp;

<pre class="brush:csharp">public partial class _Default : System.Web.UI.Page
{
    public string imageURL;
    public string sessionID;

    protected void Page_Load(object sender, EventArgs e)
    {
        var ticks = DateTime.Now.Ticks.ToString();
        imageURL = "AuthCode.ashx?id=" + ticks;
        sessionID = ticks;
    }

    protected void Button1_Click(object sender, EventArgs e)
    {
        AuthCodeManager am = new AuthCodeManager(new AuthCodeBuilder());
        Response.Write("&lt;script&gt;alert('" + am.Authorize(Request["sessionID"], TextBox1.Text).ToString() + "');&lt;/script&gt;");
        TextBox1.Text = "";
    }
}</pre>

**生成：**

这里的图片和隐藏的input，尽量不要用服务端控件，服务端控件会导致一个问题：传送门

另外，这里的写法是一种前端页面和后端代码的传值方法，这样写感觉和 MVC 的 ViewData 有异曲同工之妙~

每次页面刷新都需要生成新的验证码，不管是 Get 还是 Post，所以写在 Page_Load 函数中，并且不需要判断 IsPostBack

**验证：**

验证的过程很简单，从表单中读取会话ID和用户输入的验证码，然后去验证一下即可。

&nbsp;

**2、前端页面 Default.aspx**

&nbsp;

<pre class="brush:xml">&lt;asp:TextBox ID="TextBox1" runat="server"&gt;&lt;/asp:TextBox&gt;
&lt;img id="AuthImage" src="&lt;%=imageURL %&gt;" alt="Alternate Text" onclick="javascript:Refesh();"/&gt;
&lt;input type="hidden" id="sessionID" name="sessionID" value="&lt;%=sessionID %&gt;" /&gt;
&lt;script type="text/javascript"&gt;
    function Refesh() {
        var ticks = new Date().getTime();
        document.getElementById('AuthImage').setAttribute('src', 'authcode.ashx?id=' + ticks);
        document.getElementById('sessionID').value = ticks;
    }
&lt;/script&gt;</pre>

图片：读取后端代码中的图片地址

会话ID：同上 图片的onclick事件：随机生成一个字符串，然后修改图片的地址和会话ID，浏览器检测到图片地址变了，自动读取新的图片

&nbsp;

**3、图片 AuthCode.ashx**

&nbsp;

<pre class="brush:csharp">public class AuthCode : IHttpHandler, IRequiresSessionState
{
    public void ProcessRequest(HttpContext context)
    {
        string id = context.Request["id"];
        AuthCodeManager am = new AuthCodeManager(new AuthCodeBuilder());
        context.Response.ContentType = "image/jpeg";
        context.Response.Clear();
        context.Response.BinaryWrite(am.Create(id).ToArray());
    }

    public bool IsReusable
    {
        get
        {
            return false;
        }
    }
}</pre>

AuthCodeBuilder：这是一个继承了IAuthCodeBuilder借口的类，大家可以自己写，也可以参考我里面的源代码

流程：和上面说的一样

IRequiresSessionState：这个，比较纠结了，必须继承这个借口，才可以调用 HttpContext.Current.Session

&nbsp;

**4、运行一下吧！**

[<img class="alignnone size-medium wp-image-178" title="run" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/run-300x215.png" width="300" height="215" />][5]

打开2个页面，左边的先打开，右边的后打开

&nbsp;

[<img class="alignnone size-medium wp-image-179" title="run2" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/01/run2-300x214.png" width="300" height="214" />][6]

在先打开的页面中输入验证码，没有冲突哦~

&nbsp;

&nbsp;

### <span id="MVC"><strong>验证码管理类——MVC 用法：</strong></span>

**1、后端代码 HomeController.cs**

&nbsp;

<pre class="brush:csharp">public class HomeController : Controller
{
    public ActionResult Index()
    {
        Bind();
        ViewData["Message"] = "欢迎使用 ASP.NET MVC!";

        return View();
    }

    [HttpPost]
    public ActionResult Index(string sessionID,string code)
    {
        Bind();
        AuthCodeManager am = new AuthCodeManager(new AuthCodeBuilder());
        if (am.Authorize(sessionID, code))
        {
            Response.Write("&lt;script&gt;alert('成功！');&lt;/script&gt;");
        }
        else
        {
            Response.Write("&lt;script&gt;alert('失败！');&lt;/script&gt;");
        }
        return View();
    }

    public ActionResult AuthCode(string id)
    {
        AuthCodeManager am = new AuthCodeManager(new AuthCodeBuilder());
        return File(am.Create(id).ToArray(), "image/jpeg");
    }

    protected void Bind()
    {
        var ticks = DateTime.Now.Ticks.ToString();
        ViewData["imageURL"] = "home/authcode/" + ticks;
        ViewData["sessionID"] = ticks;
    }
}</pre>

其中，包含了每次刷新页面都重新生成验证码（Bind方法）、验证和图片生成（AuthCode方法）

&nbsp;

**2、前端页面 Index.aspx**

&nbsp;
{% raw %}

    <%using (Html.BeginForm())
    
      {%>
    
    <input type="text" name="code" value="" />
    
    <img id="AuthImage" src="<%=ViewData["imageURL"] %>" alt="Alternate Text" onclick="javascript:Refesh();" />
    
    <input type="hidden" id="sessionID" name="sessionID" value="<%=ViewData["sessionID"] %>" />
    
    <script type="text/javascript">
    
        function Refesh() {
    
            var ticks = new Date().getTime();
    
            document.getElementById('AuthImage').setAttribute('src', 'home/authcode/' + ticks);
    
            document.getElementById('sessionID').value = ticks;
    
        }
    
    </script>
    
    <input type="submit" name="submit" value="提交" />
    
    <%}%>
{% endraw %}

基本和Asp.net的一样，只是针对MVC修改了一下

&nbsp;

&nbsp;

### <span id="i-6"><strong>可扩展性：</strong></span>

公布源码，大家觉得我有写的不好的地方，可以直接修改。但是我也考虑到了可扩展性。

比如，设置会话ID和得到会话ID都是后端代码执行了，不知道大家有没有更好的解决方案？

所以我在写Create和Authorize这两个方法时重写了两个缺少sessionID参数的重载

&nbsp;

<pre class="brush:csharp">/// &lt;summary&gt;
/// 得到请求ID
/// &lt;/summary&gt;
/// &lt;returns&gt;&lt;/returns&gt;
protected virtual string GetSessionID()
{
    throw new NotImplementedException("请重写该方法后再调用！");
}

/// &lt;summary&gt;
/// 自动获取当前请求ID的验证，请重写GetSessionID()方法后再调用！
/// &lt;/summary&gt;
/// &lt;param name="authcode"&gt;验证码&lt;/param&gt;
/// &lt;returns&gt;是否通过&lt;/returns&gt;
public virtual bool Authorize(string authcode)
{
    return Authorize(GetSessionID(), authcode);
}</pre>

他们会调用GetSessionID这个虚方法，然后在调用多参数的重载方法。

使用的时候需要继承我的类，重写GetSessionID这个方法。

&nbsp;

另外几个扩展点和这个差不多，大家看源码就可以了~

&nbsp;

&nbsp;

### <span id="i-7"><strong>后记：</strong></span>

**F&Q：**

Q：如果一个人打开了N多页面怎么办？

A：针对这个，我主要采取了2个手段：

1、只要这个会话ID验证了，就删除

2、如果有人不停刷新页面，这个会话ID无法被正常删除，所以会话ID列队我设置了最大程度，超过最大长度则清理（没人会打开1000多个页面吧？ &#8211; -|，就算打开了1000多个，那丢失了几个也很正常了~）

&nbsp;

Q：安全性？

A：客户端只能得到一个会话ID，这个会话ID虽然和真实的验证码有一对一的映射，但是这个映射在服务端。而且，同一个图片地址，每次调用都会生成一个新的验证码。

&nbsp;

本文写了2个多小时，喜欢的朋友请帮忙点一下支持~谢谢！

&nbsp;

最后，也是最重要的：**<a href="/wp-content/uploads/2011/01/AuthCodeManager.zip" target="_blank">源代码&示例程序下载</a>**

&nbsp;

&nbsp;

&nbsp;

 [1]: http://www.dozer.cc/wp-content/uploads/2011/01/authcode.png
 [2]: http://www.dozer.cc/wp-content/uploads/2011/01/visio.png
 [3]: http://www.dozer.cc/wp-content/uploads/2011/01/uml.png
 [4]: http://www.dozer.cc/wp-content/uploads/2011/01/interface.png
 [5]: http://www.dozer.cc/wp-content/uploads/2011/01/run.png
 [6]: http://www.dozer.cc/wp-content/uploads/2011/01/run2.png