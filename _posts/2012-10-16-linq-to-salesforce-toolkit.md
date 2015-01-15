---
title: Linq To Salesforce Toolkit
author: Dozer
layout: post
permalink: /2012/10/linq-to-salesforce-toolkit/
categories:
  - 编程技术
tags:
  - LINQ
  - LINQ Provider
  - Salesforce
---

### 简介

上篇文章中（**<a title="Linq To Salesforce" href="/2012/09/linq-to-salesforce/" target="_blank">Linq To Salesforce</a>**），我只要介绍了 Linq To Salesforce 的基本原理。

但很多人更关心的是如何使用，后来我又写了一个 Tooltik 项目，不仅包括了查询，还包括了一些基本的增删改的封装，可以帮助开发者快速开发和 Salesforce API 交互的应用程序，算是开袋即食吧！

&nbsp;

### 使用指引

#### 下载项目

首先到 Github 上下载 <a href="https://github.com/dozer47528/LinqToSalesforce" target="_blank"><strong>Linq To Salesforce</strong></a> 项目。

<!--more-->

&nbsp;

#### 编译整个项目

[<img class="alignnone size-full wp-image-888" title="sln" alt="sln" src="/uploads/2012/10/sln.png" width="349" height="171" />][1]

&nbsp;

#### 使用 LinqToSalesforce 的 dll

dll 只要使用 LinqToSalesforce 这个 dll 即可。

还有一部分代码需要你可以自己实现，也可以利用 Toolkit 项目里的代码。

但是为什么不把这些代码卸载一起呢？因为 Salesforce API 把实体和查询方法都放在借口里了，我的这些查询逻辑需要用到这些代码，所以无法集成在一个 dll 中。

&nbsp;

#### 使用 LinqToSalesforce.Toolkit 项目中的代码

复制 `SalesforceHelper.cs` 和 `SalesforceProvider.cs` 两个文件到你自己的项目中。

删除两个文件中的引用：`using LinqToSalesforce.Toolkit.Mock;`

注意，Mock 文件夹不需要复制！这两个类需要依赖 Salesforce API ，而我这里并没有使用真的 Salesforce API，而是写了一些 Mock 类。

&nbsp;

#### 在你的项目中引用 Salesforce API

使用过 Salesforce API 的人应该知道，这里就不阐述了，引用 Salesforce 网站上下载下来的强类型 wsdl 文件即可。

再两个 Toolkit  代码中，加入 Salesforce API 的命名空间。

这时候，就已经起作用了，因为我的 Mock 类的类名和方法名和 Salesforce API 中的名字是一样的，此时，不需要再做更多的修改了。

&nbsp;

#### 开始使用吧！

具体使用方法可以参考 Test 项目，Test 中同样用到了 Toolkit 项目中的代码，后面的使用已经非常简单了！

可以非常方便的应付增删改查了！

&nbsp;

### 示例代码

偷懒了，为了让大家感受一下 LinqToSalesforce 强大的功能，免去直接下载后查看的麻烦，我这里直接贴出测试类吧。

各个方法中展示了各种功能点。

    [TestClass]
    public class SalesforceQueryTest
    {
        #region HelpMethod
        protected SalesforceHelper Helper = new SalesforceHelper();
        protected SalesforceQuery<T> Query<T>(SelectTypeEnum selectType = SelectTypeEnum.SelectIdAndUseAttachModel) where T : sObject
        {
            return Helper.Query<T>(selectType);
        }
        #endregion

        #region Where
        [TestMethod]
        public void WhereTest()
        {
            var result = Query<Contract>()
                .Where(c => c.CreatedDate > DateTime.Now.AddMonths(-1))
                .ToList();

            Assert.IsTrue(result.Any());
        }

        [TestMethod]
        public void WhereRelatedTest()
        {
            var result = Query<Contract>().Where(c => c.Owner.Name != "").FirstOrDefault();
            Assert.IsNotNull(result);
        }
        #endregion

        #region First

        [TestMethod]
        public void First_NoneTest()
        {
            try
            {
                var result = Query<User>().First(u => u.Name == Guid.NewGuid().ToString());
                Assert.Fail("the First() method did not throw any exception");
            }
            catch { }
        }

        [TestMethod]
        public void First_OneTest()
        {
            // find an user
            var firstUser = Query<User>().Select(u => new User { Id = u.Id }).FirstOrDefault();
            Assert.IsNotNull(firstUser);

            var result = Query<User>().First(u => u.Id == firstUser.Id);
            Assert.IsNotNull(result);
        }

        [TestMethod]
        public void First_ManyTest()
        {
            var result = Query<User>().First();
            Assert.IsNotNull(result);
        }

        [TestMethod]
        public void FirstOrDefault_NoneTest()
        {
            //query for an inexistent user should not throw an exception
            var result2 = Query<User>().FirstOrDefault(u => u.Name == Guid.NewGuid().ToString());
            Assert.IsNull(result2);
        }

        [TestMethod]
        public void FirstOrDefault_OneTest()
        {
            // find an user
            var firstUser = Query<User>().Select(u => new User { Id = u.Id }).FirstOrDefault();
            Assert.IsNotNull(firstUser);

            var result = Query<User>().FirstOrDefault(u => u.Id == firstUser.Id);
            Assert.IsNotNull(result);
        }

        [TestMethod]
        public void FirstOrDefault_ManyTest()
        {
            var result1 = Query<User>().FirstOrDefault();
            Assert.IsNotNull(result1);
        }
        #endregion

        #region Single
        [TestMethod]
        public void Single_NoneTest()
        {
            try
            {
                var result = Query<User>().Single(u => u.Name == Guid.NewGuid().ToString());
                Assert.Fail("the First() method did not throw any exception");
            }
            catch { }
        }

        [TestMethod]
        public void Single_OneTest()
        {
            // find an user
            var firstUser = Query<User>().Select(u => new User { Id = u.Id }).FirstOrDefault();
            Assert.IsNotNull(firstUser);

            var result = Query<User>().Single(u => u.Id == firstUser.Id);
            Assert.IsNotNull(result);
        }

        [TestMethod]
        public void Single_ManyTest()
        {
            try
            {
                var result = Query<User>().Single();
                Assert.Fail("the Single() method did not throw any exception");
            }
            catch { }
        }

        [TestMethod]
        public void SingleOrDefault_NoneTest()
        {
            var result = Query<User>().SingleOrDefault(u => u.Name == Guid.NewGuid().ToString());
            Assert.IsNull(result);
        }

        [TestMethod]
        public void SingleOrDefault_OneTest()
        {
            // find an user
            var firstUser = Query<User>().Select(u => new User { Id = u.Id }).FirstOrDefault();
            Assert.IsNotNull(firstUser);

            var result = Query<User>().SingleOrDefault(u => u.Id == firstUser.Id);
            Assert.IsNotNull(result);
        }

        [TestMethod]
        public void SingleOrDefault_ManyTest()
        {
            try
            {
                var result = Query<User>().SingleOrDefault();
                Assert.Fail("the SingleOrDefault() method did not throw any exception");
            }
            catch { }
        }
        #endregion

        #region Any
        [TestMethod]
        public void Any_NoneTest()
        {
            var result = Query<User>().Any(u => u.Name == Guid.NewGuid().ToString());
            Assert.IsFalse(result);
        }

        [TestMethod]
        public void Any_ManyTest()
        {
            var result = Query<User>().Any();
            Assert.IsTrue(result);
        }
        #endregion

        #region Count
        [TestMethod]
        public void Count_NoneTest()
        {
            var result = Query<User>().Count(u => u.Name == Guid.NewGuid().ToString());
            Assert.AreEqual(result, 0);
        }

        [TestMethod]
        public void Count_OneTest()
        {
            // find an user
            var firstUser = Query<User>().Select(u => new User { Id = u.Id }).FirstOrDefault();
            Assert.IsNotNull(firstUser);

            var result = Query<User>().Count(u => u.Id == firstUser.Id);
            Assert.AreEqual(result, 1);
        }

        [TestMethod]
        public void Count_ManyTest()
        {
            var result = Query<User>().Count();
            Assert.IsTrue(result > 0);
        }
        #endregion

        #region Select
        [TestMethod]
        public void SelectTest()
        {
            var user = Query<User>()
                .Select(u => new User { Name = u.Name })
                .FirstOrDefault();
            Assert.IsNotNull(user.Name);
        }

        [TestMethod]
        public void SelectRelatedTest()
        {
            var result = Query<Contract>().Select(c => new Contract
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
            var user = Query<User>(SelectTypeEnum.SelectIdAndUseAttachModel)
                .Select(u => new User { Name = u.Name })
                .FirstOrDefault();

            Assert.IsNotNull(user.Id);
            Assert.IsNotNull(user.Name);
            Assert.IsNull(user.MobilePhone);
        }

        [TestMethod]
        public void SelectIdAndUseReplaceModel_NoSelectTest()
        {
            var user = Query<User>(SelectTypeEnum.SelectIdAndUseReplaceModel)
                .FirstOrDefault();

            Assert.IsNotNull(user.Id);
            Assert.IsNull(user.Name);
            Assert.IsNull(user.MobilePhone);
        }

        [TestMethod]
        public void SelectIdAndUseReplaceModel_UseSelectTest()
        {
            var user = Query<User>(SelectTypeEnum.SelectIdAndUseReplaceModel)
                .Select(u => new User { Name = u.Name })
                .FirstOrDefault();

            Assert.IsNull(user.Id);
            Assert.IsNotNull(user.Name);
        }

        [TestMethod]
        public void SelectAllAndUseAttachModelTest()
        {
            var user = Query<User>(SelectTypeEnum.SelectAllAndUseAttachModel)
                .Select(u => new User { Name = u.Name })
                .FirstOrDefault();

            Assert.IsNotNull(user.Id);
            Assert.IsNotNull(user.Name);
            Assert.IsNotNull(user.CreatedDate);
        }

        [TestMethod]
        public void SelectAllAndUseReplaceModel_NoSelectTest()
        {
            var user = Query<User>(SelectTypeEnum.SelectAllAndUseReplaceModel)
                .FirstOrDefault();

            Assert.IsNotNull(user.Id);
            Assert.IsNotNull(user.Name);
            Assert.IsNotNull(user.CreatedDate);
        }

        [TestMethod]
        public void SelectAllAndUseReplaceModel_UseSelectTest()
        {
            var user = Query<User>(SelectTypeEnum.SelectAllAndUseReplaceModel)
                .Select(u => new User { Name = u.Name })
                .FirstOrDefault();

            Assert.IsNull(user.Id);
            Assert.IsNotNull(user.Name);
            Assert.IsNull(user.CreatedDate);
        }
        #endregion
    }

&nbsp;

### 如何使用 Test 项目

测试项目是可以连上真实环境运行的，你只要修改配置文件，即可直接运行：

1.  配置 config 中的 `sfusername` 和 `sfpassword`
2.  如果你的项目是线上项目，修改下面的 `https://test.salesforce.com/services/Soap/c/25.0`，改成 `https://login.salesforce.com/services/Soap/c/25.0`

这里为什么不用再引用自己的 Salesforce API 里？因为我这里引用了一个基础的 API，包含了 Salesforce 中基本的类，所以可以通用。

而我的测试项目测试的也都是内置对象，如果你想测试自定义对象，需要引用自己的 API。

 [1]: /uploads/2012/10/sln.png
