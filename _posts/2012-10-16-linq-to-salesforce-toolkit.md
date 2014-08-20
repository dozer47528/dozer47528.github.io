---
title: Linq To Salesforce Toolkit
author: Dozer
layout: post
permalink: /2012/10/linq-to-salesforce-toolkit/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658345
categories:
  - 编程技术
tags:
  - LINQ
  - LINQ Provider
  - Salesforce
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 简介</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 使用指引</a><ul>
        <li>
          <a href="#i-3"><span class="toc_number toc_depth_2">2.1</span> 下载项目</a>
        </li>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">2.2</span> 编译整个项目</a>
        </li>
        <li>
          <a href="#_LinqToSalesforce_dll"><span class="toc_number toc_depth_2">2.3</span> 使用 LinqToSalesforce 的 dll</a>
        </li>
        <li>
          <a href="#_LinqToSalesforceToolkit"><span class="toc_number toc_depth_2">2.4</span> 使用 LinqToSalesforce.Toolkit 项目中的代码</a>
        </li>
        <li>
          <a href="#_Salesforce_API"><span class="toc_number toc_depth_2">2.5</span> 在你的项目中引用 Salesforce API</a>
        </li>
        <li>
          <a href="#i-5"><span class="toc_number toc_depth_2">2.6</span> 开始使用吧！</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-6"><span class="toc_number toc_depth_1">3</span> 示例代码</a>
    </li>
    <li>
      <a href="#_Test"><span class="toc_number toc_depth_1">4</span> 如何使用 Test 项目</a>
    </li>
  </ul>
</div>

### <span id="i">简介</span>

上篇文章中（**<a title="Linq To Salesforce" href="/2012/09/linq-to-salesforce/" target="_blank">Linq To Salesforce</a>**），我只要介绍了 Linq To Salesforce 的基本原理。

但很多人更关心的是如何使用，后来我又写了一个 Tooltik 项目，不仅包括了查询，还包括了一些基本的增删改的封装，可以帮助开发者快速开发和 Salesforce API 交互的应用程序，算是开袋即食吧！

&nbsp;

### <span id="i-2">使用指引</span>

#### <span id="i-3">下载项目</span>

首先到 Github 上下载 <a href="https://github.com/dozer47528/LinqToSalesforce" target="_blank"><strong>Linq To Salesforce</strong></a> 项目。

<!--more-->

&nbsp;

#### <span id="i-4">编译整个项目</span>

[<img class="alignnone size-full wp-image-888" title="sln" alt="" src="/uploads/2012/10/sln.png" width="349" height="171" />][1]

&nbsp;

#### <span id="_LinqToSalesforce_dll">使用 LinqToSalesforce 的 dll</span>

dll 只要使用 LinqToSalesforce 这个 dll 即可。

还有一部分代码需要你可以自己实现，也可以利用 Toolkit 项目里的代码。

但是为什么不把这些代码卸载一起呢？因为 Salesforce API 把实体和查询方法都放在借口里了，我的这些查询逻辑需要用到这些代码，所以无法集成在一个 dll 中。

&nbsp;

#### <span id="_LinqToSalesforceToolkit">使用 LinqToSalesforce.Toolkit 项目中的代码</span>

复制 <span style="background-color: #eeeeee;">SalesforceHelper.cs</span> 和 <span style="background-color: #eeeeee;">SalesforceProvider.cs</span> 两个文件到你自己的项目中。

删除两个文件中的引用：<span style="background-color: #eeeeee;">using LinqToSalesforce.Toolkit.Mock;</span>

注意，Mock 文件夹不需要复制！这两个类需要依赖 Salesforce API ，而我这里并没有使用真的 Salesforce API，而是写了一些 Mock 类。

&nbsp;

#### <span id="_Salesforce_API">在你的项目中引用 Salesforce API</span>

使用过 Salesforce API 的人应该知道，这里就不阐述了，引用 Salesforce 网站上下载下来的强类型 wsdl 文件即可。

再两个 Toolkit  代码中，加入 Salesforce API 的命名空间。

这时候，就已经起作用了，因为我的 Mock 类的类名和方法名和 Salesforce API 中的名字是一样的，此时，不需要再做更多的修改了。

&nbsp;

#### <span id="i-5">开始使用吧！</span>

具体使用方法可以参考 Test 项目，Test 中同样用到了 Toolkit 项目中的代码，后面的使用已经非常简单了！

可以非常方便的应付增删改查了！

&nbsp;

### <span id="i-6">示例代码</span>

偷懒了，为了让大家感受一下 LinqToSalesforce 强大的功能，免去直接下载后查看的麻烦，我这里直接贴出测试类吧。

各个方法中展示了各种功能点。

<pre class="lang:c# decode:true brush: csharp; gutter: true">[TestClass]
public class SalesforceQueryTest
{
    #region HelpMethod
    protected SalesforceHelper Helper = new SalesforceHelper();
    protected SalesforceQuery&lt;T&gt; Query&lt;T&gt;(SelectTypeEnum selectType = SelectTypeEnum.SelectIdAndUseAttachModel) where T : sObject
    {
        return Helper.Query&lt;T&gt;(selectType);
    }
    #endregion

    #region Where
    [TestMethod]
    public void WhereTest()
    {
        var result = Query&lt;Contract&gt;()
            .Where(c =&gt; c.CreatedDate &gt; DateTime.Now.AddMonths(-1))
            .ToList();

        Assert.IsTrue(result.Any());
    }

    [TestMethod]
    public void WhereRelatedTest()
    {
        var result = Query&lt;Contract&gt;().Where(c =&gt; c.Owner.Name != "").FirstOrDefault();
        Assert.IsNotNull(result);
    }
    #endregion

    #region First

    [TestMethod]
    public void First_NoneTest()
    {
        try
        {
            var result = Query&lt;User&gt;().First(u =&gt; u.Name == Guid.NewGuid().ToString());
            Assert.Fail("the First() method did not throw any exception");
        }
        catch { }
    }

    [TestMethod]
    public void First_OneTest()
    {
        // find an user
        var firstUser = Query&lt;User&gt;().Select(u =&gt; new User { Id = u.Id }).FirstOrDefault();
        Assert.IsNotNull(firstUser);

        var result = Query&lt;User&gt;().First(u =&gt; u.Id == firstUser.Id);
        Assert.IsNotNull(result);
    }

    [TestMethod]
    public void First_ManyTest()
    {
        var result = Query&lt;User&gt;().First();
        Assert.IsNotNull(result);
    }

    [TestMethod]
    public void FirstOrDefault_NoneTest()
    {
        //query for an inexistent user should not throw an exception
        var result2 = Query&lt;User&gt;().FirstOrDefault(u =&gt; u.Name == Guid.NewGuid().ToString());
        Assert.IsNull(result2);
    }

    [TestMethod]
    public void FirstOrDefault_OneTest()
    {
        // find an user
        var firstUser = Query&lt;User&gt;().Select(u =&gt; new User { Id = u.Id }).FirstOrDefault();
        Assert.IsNotNull(firstUser);

        var result = Query&lt;User&gt;().FirstOrDefault(u =&gt; u.Id == firstUser.Id);
        Assert.IsNotNull(result);
    }

    [TestMethod]
    public void FirstOrDefault_ManyTest()
    {
        var result1 = Query&lt;User&gt;().FirstOrDefault();
        Assert.IsNotNull(result1);
    }
    #endregion

    #region Single
    [TestMethod]
    public void Single_NoneTest()
    {
        try
        {
            var result = Query&lt;User&gt;().Single(u =&gt; u.Name == Guid.NewGuid().ToString());
            Assert.Fail("the First() method did not throw any exception");
        }
        catch { }
    }

    [TestMethod]
    public void Single_OneTest()
    {
        // find an user
        var firstUser = Query&lt;User&gt;().Select(u =&gt; new User { Id = u.Id }).FirstOrDefault();
        Assert.IsNotNull(firstUser);

        var result = Query&lt;User&gt;().Single(u =&gt; u.Id == firstUser.Id);
        Assert.IsNotNull(result);
    }

    [TestMethod]
    public void Single_ManyTest()
    {
        try
        {
            var result = Query&lt;User&gt;().Single();
            Assert.Fail("the Single() method did not throw any exception");
        }
        catch { }
    }

    [TestMethod]
    public void SingleOrDefault_NoneTest()
    {
        var result = Query&lt;User&gt;().SingleOrDefault(u =&gt; u.Name == Guid.NewGuid().ToString());
        Assert.IsNull(result);
    }

    [TestMethod]
    public void SingleOrDefault_OneTest()
    {
        // find an user
        var firstUser = Query&lt;User&gt;().Select(u =&gt; new User { Id = u.Id }).FirstOrDefault();
        Assert.IsNotNull(firstUser);

        var result = Query&lt;User&gt;().SingleOrDefault(u =&gt; u.Id == firstUser.Id);
        Assert.IsNotNull(result);
    }

    [TestMethod]
    public void SingleOrDefault_ManyTest()
    {
        try
        {
            var result = Query&lt;User&gt;().SingleOrDefault();
            Assert.Fail("the SingleOrDefault() method did not throw any exception");
        }
        catch { }
    }
    #endregion

    #region Any
    [TestMethod]
    public void Any_NoneTest()
    {
        var result = Query&lt;User&gt;().Any(u =&gt; u.Name == Guid.NewGuid().ToString());
        Assert.IsFalse(result);
    }

    [TestMethod]
    public void Any_ManyTest()
    {
        var result = Query&lt;User&gt;().Any();
        Assert.IsTrue(result);
    }
    #endregion

    #region Count
    [TestMethod]
    public void Count_NoneTest()
    {
        var result = Query&lt;User&gt;().Count(u =&gt; u.Name == Guid.NewGuid().ToString());
        Assert.AreEqual(result, 0);
    }

    [TestMethod]
    public void Count_OneTest()
    {
        // find an user
        var firstUser = Query&lt;User&gt;().Select(u =&gt; new User { Id = u.Id }).FirstOrDefault();
        Assert.IsNotNull(firstUser);

        var result = Query&lt;User&gt;().Count(u =&gt; u.Id == firstUser.Id);
        Assert.AreEqual(result, 1);
    }

    [TestMethod]
    public void Count_ManyTest()
    {
        var result = Query&lt;User&gt;().Count();
        Assert.IsTrue(result &gt; 0);
    }
    #endregion

    #region Select
    [TestMethod]
    public void SelectTest()
    {
        var user = Query&lt;User&gt;()
            .Select(u =&gt; new User { Name = u.Name })
            .FirstOrDefault();
        Assert.IsNotNull(user.Name);
    }

    [TestMethod]
    public void SelectRelatedTest()
    {
        var result = Query&lt;Contract&gt;().Select(c =&gt; new Contract
        {
            Id = c.Id,
            IsDeleted = c.IsDeleted,
            Account = new Account
            {
                Name = c.Account.Name,
                Owner = new User { Name = c.Account.Owner.Name },
            },
        }).FirstOrDefault();

        Assert.IsNotNull(result);
        Assert.IsNotNull(result.IsDeleted);
        Assert.IsNotNull(result.Account.Name);
        Assert.IsNotNull(result.Account.Owner.Name);
        Assert.IsNull(result.Account.Owner.Phone);
    }
    #endregion

    #region SelectType
    [TestMethod]
    public void SelectIdAndUseAttachModelTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectIdAndUseAttachModel)
            .Select(u =&gt; new User { Name = u.Name })
            .FirstOrDefault();

        Assert.IsNotNull(user.Id);
        Assert.IsNotNull(user.Name);
        Assert.IsNull(user.MobilePhone);
    }

    [TestMethod]
    public void SelectIdAndUseReplaceModel_NoSelectTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectIdAndUseReplaceModel)
            .FirstOrDefault();

        Assert.IsNotNull(user.Id);
        Assert.IsNull(user.Name);
        Assert.IsNull(user.MobilePhone);
    }

    [TestMethod]
    public void SelectIdAndUseReplaceModel_UseSelectTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectIdAndUseReplaceModel)
            .Select(u =&gt; new User { Name = u.Name })
            .FirstOrDefault();

        Assert.IsNull(user.Id);
        Assert.IsNotNull(user.Name);
    }

    [TestMethod]
    public void SelectAllAndUseAttachModelTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectAllAndUseAttachModel)
            .Select(u =&gt; new User { Name = u.Name })
            .FirstOrDefault();

        Assert.IsNotNull(user.Id);
        Assert.IsNotNull(user.Name);
        Assert.IsNotNull(user.CreatedDate);
    }

    [TestMethod]
    public void SelectAllAndUseReplaceModel_NoSelectTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectAllAndUseReplaceModel)
            .FirstOrDefault();

        Assert.IsNotNull(user.Id);
        Assert.IsNotNull(user.Name);
        Assert.IsNotNull(user.CreatedDate);
    }

    [TestMethod]
    public void SelectAllAndUseReplaceModel_UseSelectTest()
    {
        var user = Query&lt;User&gt;(SelectTypeEnum.SelectAllAndUseReplaceModel)
            .Select(u =&gt; new User { Name = u.Name })
            .FirstOrDefault();

        Assert.IsNull(user.Id);
        Assert.IsNotNull(user.Name);
        Assert.IsNull(user.CreatedDate);
    }
    #endregion
}</pre>

&nbsp;

### <span id="_Test">如何使用 Test 项目</span>

测试项目是可以连上真实环境运行的，你只要修改配置文件，即可直接运行：

1.  配置 config 中的 <span style="background-color: #eeeeee;">sfusername</span> 和 <span style="background-color: #eeeeee;">sfpassword</span>
2.  如果你的项目是线上项目，修改下面的 <span style="background-color: #eeeeee;">https://test.salesforce.com/services/Soap/c/25.0</span>，改成 <span style="background-color: #eeeeee;">https://login.salesforce.com/services/Soap/c/25.0</span>

这里为什么不用再引用自己的 Salesforce API 里？因为我这里引用了一个基础的 API，包含了 Salesforce 中基本的类，所以可以通用。

而我的测试项目测试的也都是内置对象，如果你想测试自定义对象，需要引用自己的 API。

 [1]: /uploads/2012/10/sln.png