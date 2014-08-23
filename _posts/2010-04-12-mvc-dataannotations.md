---
title: '深入浅出 MVC 数据验证 2.0 [附演示源码]'
author: Dozer
layout: post
permalink: /2010/04/mvc-dataannotations/
categories:
  - 编程技术
tags:
  - AspDotNet
  - Entiy Framework
  - MVC
  - 数据验证
---

> 今天在这里给大家介绍一下MVC的数据验证框架。
> 
> 在1.0版中，很多朋友提出了怎么使用客户端验证，今天找了一些资料，发现了客户端验证的方法。

&nbsp;

### 1、MVC中的数据验证框架有何优点？

&nbsp;

在Asp.net时代，或者没有使用MVC的验证框架，一般是在BLL层中进行数据验证，但是BLL层的返回值又只能返回一个东西，比如一个字符串，而实际情况中，数据验证是很复杂的。

这时候，BLL层和网站会分离的不彻底，因为很多代码不得不在网站中写。

&nbsp;

而在MVC的数据验证框架中，甚至可以不用BLL层，而在比BLL层更底层的Model层书写数据验证的代码。

并且最后能在网页上显示出来。

此图这就是最后的效果

<img class="alignnone size-full wp-image-55" title="1" alt="1" src="/uploads/2011/01/1.jpg" width="427" height="329" />

<!--more-->

&nbsp;

### 2、深入浅出？

&nbsp;

此框架有个优点，非常灵活，我这里用正常的三层架构来写。

因为灵活，我可以把数据验证写在任何一层。

&nbsp;

i)写在Controller里：这是最简单的方法，但是也是最不推荐的方法， 因为不能体现分层思想

ii)写在BLL中：如果对一个数据验证的时候，需要牵扯到别的数据，就应该把验证写在这一层，比如一个Article Model的Category值是1，查询这个分类是否存在

iii)写在Model中：一些底层的标准应该写在这一层，因为这些标准在任何情况下都不能违反，比如帐号名长度不能超过20个字符

&nbsp;

下面，我会一步步讲3中验证方法介绍给大家

&nbsp;

&nbsp;

### 3、前端和后端的结合

&nbsp;

完整地看过MVC教程的人应该都知道如何使用 ModelState，其实MVC验证框架就是利用它，将验证的结果显示在页面中。

下面看一个例子：

&nbsp;

<pre class="brush:csharp">[HttpPost]
//如果表单中input的name属性和Model的字段一样，那可以直接以Model形式传入一个Action
public ActionResult Exp1(Models.UserModel user)
{
    //判断
    if (user.Name.Length &gt; 20)
    {
        //如果错误，调用ModelState的AddModelError方法，第一个参数需要输入出错的字段名
        ModelState.AddModelError("Name", "名字不得超过20个字符");
    }
    //判断ModelState中是否有错误
    if (ModelState.IsValid)
    {
        //如果没错误，返回首页
        return RedirectToAction("Index");
    }
    else
    {
        //如果有错误，继续输入信息
        return View(user);
    }
}</pre>

这里在Controller中一个Action中进行了数据验证，并且把结果放入了ModelState中，那怎么在前端页面显示呢？

&nbsp;

如果不了解MVC的验证框架，其实可以直接自动生成，看看标准做法

在代码上右击，点Add View

选择创建强类型View，并且在内容中选择Edit

<img class="alignnone size-full wp-image-56" title="2" alt="2" src="/uploads/2011/01/2.jpg" width="479" height="526" />

&nbsp;

这是自动生成的View

<img class="alignnone size-full wp-image-57" title="3" alt="3" src="/uploads/2011/01/3.jpg" width="613" height="549" />

&nbsp;

OK，下面我可以运行了。。。

<img class="alignnone size-full wp-image-58" title="4" alt="4" src="/uploads/2011/01/4.jpg" width="455" height="472" />

&nbsp;

由于前端的页面View是自动生成的，所以有些读者可能没看懂，为什么我刚刚在后端的数据验证信息会显示到前端去了呢？

其实关键就是利用了这个：<%= Html.ValidationMessageFor(model => model.Name) %>

不理解强类型方法、或还在使用MVC1.0的读者可以看这个：<%= Html.ValidationMessage(&#8220;Name&#8221;) %>

（除了ValidationMessage函数外，还有其它几个函数，可以达到不同的效果，读者可以自行研究下，这几个函数都是以Validation开头的）

&nbsp;

*小结：在Controller中验证数据，放入ModelState（其核心是一个字典），然后在利用函数读取*

*这样，就达到了数据验证时前端和后端相结合的效果。*

&nbsp;

&nbsp;

### 4、如何将数据验证代码放入业务逻辑层？

&nbsp;

上面那部分，我们看到了MVC数据验证框架的核心，ModelState。

只要在ModelState中添加错误就可以在前端页面中显示了。

&nbsp;

所以，这个部分的关键就是让BLL操作ModelState

这里，有2中方法可以参考，其中，第二种方案我是参考了xVal来实现的

&nbsp;

**i)方案一：在调用BLL函数的时候直接传入ModelState对象**

优点：这个是最好理解的，我直接传入ModelState对象，让BLL操作它不就可以了？

缺点：BLL是业务逻辑层，它不应该知道自己被谁调用了，也就是说，BLL层中不应该出现任何MVC特有的东西(ModelState对象)

&nbsp;

下面就让我来实现它：

<pre class="brush:csharp">//BLL
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;

namespace MvcApplication1.BLL
{
    public static class UserBLL
    {
        public static void Edit(Models.UserModel user, ModelStateDictionary ModelState)
        {
            if (user.Name.Length &gt; 20)
            {
                //如果错误，调用ModelState的AddModelError方法，第一个参数需要输入出错的字段名
                ModelState.AddModelError("Name", "名字不得超过20个字符");
            }
            if (ModelState.IsValid)
            {
                //在这里我可以写一些代码，因为完成了验证，我就可以开始更新数据库了
            }
        }
    }
}</pre>

&nbsp;

<pre class="brush:csharp">//controler
[HttpPost]
public ActionResult Exp2(Models.UserModel user)
{
    //调用BLL中的函数
    BLL.UserBLL.Edit(user, ModelState);

    if (ModelState.IsValid)
    {
        return RedirectToAction("Index");
    }
    else
    {
        //这里，前端页面不用改，所以我直接利用第一个例子中的前端页面
        return View("Exp1",user);
    }
}</pre>

OK，直接运行，结果和上一个方法一样

*总结：在调用BLL的时候把ModelState传入*

&nbsp;

**ii)方案二：通过错误捕捉，将BLL和Controller关联起来**

如果使用方案一，会出现这样一个问题：

如果我的项目不用MVC了，要移植怎么办？

新的架构中也有类似于ModelState的东西。总不能把所有的BLL改一遍吧？

所以，我们需要方案二。

&nbsp;

这里是通过编写一个自定义Exception类，然后这个自定义Exception类有2个功能：

1、加入错误

2、把错误转换到ModelState中（如果要转移到别的架构，可以再写一个新的转移方法）

&nbsp;

下面的代码就是这个自定义Exception类

<pre class="brush:csharp">//ModelExceptions
//必须继承自Exception
public class ModelExceptions : Exception
{
    //存放错误信息的List
    List&lt;string[]&gt; errors = new List&lt;string[]&gt;();

    //判断是否有错误
    public bool IsValid
    {
        get
        {
            return errors.Count == 0 ? true : false;
        }
    }

    //增加错误信息
    public void AddError(string name, string message)
    {
        this.errors.Add(new string[] { name, message });
    }

    //填充ModelState
    public void FillModelState(ModelStateDictionary modelstate)
    {
        foreach (var e in this.errors)
        {
            modelstate.AddModelError(e[0], e[1]);
        }
    }
}</pre>

&nbsp;

接下来是在Controller中的代码

<pre class="brush:csharp">//Controller
[HttpPost]
public ActionResult Exp3(Models.UserModel user)
{
    //用try来捕捉错误
    try
    {
        BLL.UserBLL.Edit(user);
    }
    catch (ModelExceptions e)
    {
        //如果发生了错误，就填充到ModelState中
        e.FillModelState(ModelState);
    }
    if (ModelState.IsValid)
    {
        return RedirectToAction("Index");
    }
    else
    {
        //这里，前端页面不用改，所以我直接利用第一个例子中的前端页面
        return View("Exp1", user);
    }
}</pre>

&nbsp;

然后是在BLL中的代码

<pre class="brush:csharp">//BLL
public static void Edit(Models.UserModel user)
{
    var e = new ModelExceptions();
    if (user.Name.Length &gt; 20)
    {
        //如果错误，调用ModelState的AddModelError方法，第一个参数需要输入出错的字段名
        e.AddError("Name", "名字不得超过20个字符");
    }
    if (e.IsValid)
    {
        //在这里我可以写一些代码，因为完成了验证，我就可以开始更新数据库了
    }
    else
    {
        //如果有错误，就抛出错误
        throw e;
    }
}</pre>

&nbsp;

*总结：简单的做法，在后期会反而会带来很多麻烦，所以推荐方案二。而且方案二也不是很麻烦，反而让人感觉很清晰*

&nbsp;

&nbsp;

### 5、如何将数据验证代码放入Model中？

&nbsp;

前面，在BLL中验证数据已经很好了，但是又出现了一个问题

一个Model，很多限制是固定的，比如长度不能超过20个字符

但是我在BLL中有很多过程，比如修改，删除等

那我岂不是要在所有的过程中都多这个进行验证？

其实你也可以通过写一个函数来解决这个问题

&nbsp;

但是，我(Model)的名字有没有超过20个字符是我自己的事情，凭什么要你来鉴定？我自己说了算！

&nbsp;

*插播笑话一则：在我家，大事我说了算，小事我老婆说了算~ 那什么是大事？什么是小事？像美国打不打伊拉克，这就是大事；别的都是小事……*

&nbsp;

OK，言归正传…

如何把数据验证交给Model呢？这里需要引用一个DLL

<img class="alignnone size-full wp-image-59" title="5" alt="5" src="/uploads/2011/01/5.jpg" width="431" height="385" />

然后在Model中这样做

<pre class="brush:csharp">using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.ComponentModel.DataAnnotations;

namespace MvcApplication1.Models
{
    public class UserModel
    {
        public string Name { get; set; }

        //属性前加上Attribute
        [Required(ErrorMessage = "密码不能为空")]
        [StringLength(20, ErrorMessage = "密码长度不能超过20个字符")]
        public string Password { get; set; }
    }
}</pre>

引用 System.ComponentModel.DataAnnotations 命名空间，并且在Model属性前加上Attribute(C# 新特性：特征)，这样就可以了

请自行查看System.ComponentModel.DataAnnotations命名空间，看看可以有哪些验证方法

当然也可以自定义验证，查看默认验证的定义，看看它继承了哪个类，自己仿写就可以了

&nbsp;

我这里没有取消掉BLL中的验证，2种验证可以混合使用

&nbsp;

OK，那在Controller和BLL中需要做什么？我们需要做一定的修改

<pre class="brush:csharp">//Controller
[HttpPost]
//MVC在传入这个Model的时候已经进行了验证，并且把错误放去了ModelState
public ActionResult Exp4(Models.UserModel user)
{
    try
    {
        //别的不变，除了这里，我们需要传入ModelState.IsValid
        BLL.UserBLL.Edit(user,ModelState.IsValid);
    }
    catch (ModelExceptions e)
    {
        e.FillModelState(ModelState);
    }
    if (ModelState.IsValid)
    {
        return RedirectToAction("Index");
    }
    else
    {
        return View("Exp1", user);
    }
}

//BLL
public static void Edit(Models.UserModel user,bool IsValid)
{
    var e = new ModelExceptions();
    if (user.Name.Length &gt; 20)
    {
        e.AddError("Name", "名字不得超过20个字符");
    }
    //别的不变，但在这里，我除了要判断e中是否有错误外，还要判断ModelState中是否有错误
    if (e.IsValid && IsValid)
    {
        //在这里我可以写一些代码，因为完成了验证，我就可以开始更新数据库了
    }
    else
    {
        throw e;
    }
}</pre>

&nbsp;

我注释了相对了上个例子改动的地方

并且混合使用了2中验证方法

<img class="alignnone size-full wp-image-60" title="6" alt="6" src="/uploads/2011/01/6.jpg" width="429" height="243" />

什么时候用Model验证？ 验证Model固有的属性

什么时候用BLL验证？ 当需要验证一些复杂关系的时候

&nbsp;

另外，为什么要把ModelState.IsValid传入BLL？

因为Model验证是在这个Model传入这个方法的时候就已经完成的

<img class="alignnone size-full wp-image-61" title="7" alt="7" src="/uploads/2011/01/7.jpg" width="512" height="544" />

如果不传入，那BLL验证中虽然没错误，但不代表整个过程没有错误。

对数据库的操作要知道完整的验证信息，如果不传入，会导致程序BUG

&nbsp;

*总结：合理的根据情况来放置数据验证代码的位置才是王道*

&nbsp;

&nbsp;

### 6、如何更改错误提示的样式？

&nbsp;

我这里用了MVC基本的那个例程，里面包含了CSS样式表

而默认情况下，虽然会出现譬如“名称过长”这样的文字信息，但是却没有样式（默认是正常字体，正常颜色）

&nbsp;

那如何修改？

其实打开MVC默认的CSS样式表就不难发现，这些错误信息都有固定的class，所以只要写一个CSS的class即可

<img class="alignnone size-full wp-image-62" title="8" alt="8" src="/uploads/2011/01/8.jpg" width="254" height="212" />

那怎么才能知道class名是什么呢？ 最方便的方法，做好页面后在浏览器中看一下即可

&nbsp;

&nbsp;

### 7、Entity Framework中，如何在Model中编写数据验证？

&nbsp;

Entity Framework会自动生成Model，虽然是可以修改的，但是强烈建议不要直接修改Model原始代码

其实微软早就想到这一点了，它生成的Model都是 partial class(部分类)

也就是说，同一个类的代码可以分几部分，写在不同的地方

&nbsp;

具体写法如下，写在不同的地方，但需要在同一个命名空间下

<pre class="brush:csharp">[MetadataType(typeof(UserMetaData))]
public partial class User { }
public class UserMetaData
{
    [Required(ErrorMessage = "名字为空")]
    [StringLength(10, ErrorMessage = "名字长度不得超过10个字符")]
    public string Name { get; set; }

    [Required(ErrorMessage = "密码为空")]
    [StringLength(20, ErrorMessage = "密码长度不得超过20个字符")]
    public string Password { get; set; }

    [Required(ErrorMessage = "帐号为空")]
    [StringLength(10, ErrorMessage = "帐号长度不得超过10个字符")]
    public string Passport { get; set; }
}</pre>

这样写好后，便可以在Entity Framework中使用Model验证了

&nbsp;

&nbsp;

### 8、如何使用客户端验证

&nbsp;

任何平台都可以靠js来实现客户端验证，但是我这里探讨的是MVC的数据验证。

那MVC的客户端数据验证有什么不同呢？

&nbsp;

不同之处就在于，你可以不用写一行javascript代码！

下面让我们来实现它

&nbsp;

先添加3个javascript文件，请按顺序添加：

<img class="alignnone size-full wp-image-63" title="9" alt="9" src="/uploads/2011/01/9.jpg" width="677" height="170" />

&nbsp;

然后在View里添加一行代码：（注意要添加在Form前）

<img class="alignnone size-full wp-image-64" title="10" alt="10" src="/uploads/2011/01/10.jpg" width="392" height="124" />

注意点：这里，其实是这个函数把Model验证转换成了javascript代码，对！它只能转换Model验证，BLL验证无法转换，因为BLL验证涉及到复杂的代码，不可能全部转换成javascript吧？并且BLL验证很多还需要和数据库交互。

那如果想把BLL验证也做成“客户端”验证怎么办？（只有可能用ajax实现无刷新验证，而不是真正的客户端验证）

目前看来先只能手写了

如有收获，我会继续更新~

&nbsp;

&nbsp;

### 9、Ending

&nbsp;

<img class="alignnone size-full wp-image-65" title="11" alt="11" src="/uploads/2011/01/11.jpg" width="484" height="342" />

&nbsp;

演示中的源码（更新至2.0)：<a href="/wp-content/uploads/2011/01/MVC%E6%95%B0%E6%8D%AE%E9%AA%8C%E8%AF%81.zip" target="_blank"><strong>下载</strong></a>

&nbsp;

如果感觉有收获，那就点一下支持吧~

如有疑问或者我文章中有不妥之处，请在下方留言，或者发送邮件到：dozer.cc@gmail.com
