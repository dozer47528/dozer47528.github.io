---
title: Entity Framework Code First 配置介绍：引用关系
author: Dozer
layout: post
permalink: /2012/09/entity-framework-code-first-configuring-relationships.html
categories:
  - 编程技术
tags:
  - Code First
  - Entiy Framework
  - Fluent API
---

### 目录

[**简介**][1]

[**配置实体的属性**][2]

**[配置实体间的引用关系][3]**

[**配置数据库映射**][4]

&nbsp;

### 引用关系

Entity Framework 中配置了对象之间的引用关系后，在查询数据的时候会非常方便。

但是很多老系统中都是没有显示指定外键的，大多是靠在子对象中加一个主对象的 ID 来解决问题。

这时候如果不配置一下的话，是根本无法实现两个对象之间的引用关系的。因为 Entity Framework 并不知道那一列是用来确定引用关系的。

所以，这章将会介绍它默认的规则，也会介绍如何自由地配置引用关系。

<!--more-->

### 默认规则

当你不配置任何东西的时候，Entity Framework 默认会认为你的数据库是这样的：

*   如果你的实体中有另一个实体的集合类型导航属性，Code First 默认会认为它们是一对多的关系；
*   如果你的一个实体上有另一个实体的导航属性（不能两者都有对方的导航属性），Code First 也会默认认为它们是一对多的关系；
*   如果你的两个实体上都有对方的集合类型导航属性，Code First 默认会认为它们是多对多的关系；
*   如果你的两个实体上都有对方的导航属性，Code First 默认会认为它们是一对一的关系；
*   默认情况下，Code First 对外键和表名（多对多的关联表）都有要求。

综上：如果你是先建立实体再创建数据库，可以不用配置而使用默认规则；但是如果你是现有数据库，一般很难完全匹配，总会需要配置一些东西。

&nbsp;

### 利用 Fluent API 来配置引用关系

Attribute 配置法（Data Annotations）无法 实现所有功能，建议使用 Fluent API 来实现，具体配置遵循一下标准：

`Entity.Has[Multiplicity](Property).With[Multiplicity](Property).Map(Option)`

其中，Has[Multiplicity] 包含以下三种方法：

*   HasOptional
*   HasRequired
*   HasMany

另外，With[Multiplicity] 同样也包含一下三种方法：

*   WithOptional
*   WithRequired
*   WithMany

<div>
  最后的 Map 是用来映射外键（非显示外键也行）的。
</div>

<div>
</div>

但是这到底怎么用呢？后面将会用一个实例来演示一下。

&nbsp;

### 配置一对多与一对一关系

    public class User
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public virtual IList<Article> Articles { get; set; }
    }
    public class Article
    {
        public int ID { get; set; }
        public string Name { get; set; }
        public virtual User Owner { get; set; }
    }

上述代码中有两个实体，它们是一对多的关系。

完整的配置代码如下：

    public class TestContext : DbContext
    {

        public DbSet<User> UserSet { get { return Set<User>(); } }
        public DbSet<Article> ArticleSet { get { return Set<Article>(); } }

        protected override void OnModelCreating(DbModelBuilder modelBuilder)
        {
            modelBuilder
                .Configurations
                .Add(new UserTypeConfiguration())
                .Add(new ArticleTypeConfiguration());
            base.OnModelCreating(modelBuilder);
        }
    }

    public class UserTypeConfiguration : EntityTypeConfiguration<User>
    {
        public UserTypeConfiguration()
        {
            HasKey(u => u.ID);
            Property(u => u.ID)
                .IsRequired()
                .HasDatabaseGeneratedOption(DatabaseGeneratedOption.Identity);
            HasMany(u => u.Articles)
                .WithRequired(a => a.Owner)
                .Map(x => x.MapKey("UserID"));
            ToTable("User");
        }
    }
    public class ArticleTypeConfiguration : EntityTypeConfiguration<Article>
    {
        public ArticleTypeConfiguration()
        {
            HasKey(a => a.ID);
            Property(a => a.ID)
                .IsRequired()
                .HasDatabaseGeneratedOption(DatabaseGeneratedOption.Identity);
            ToTable("Article");
        }
    }

别的都是基本配置，这里最关键的一段代码是：

    HasMany(u => u.Articles)
                    .WithRequired(a => a.Owner)
                    .Map(x => x.MapKey("UserID"));

其实这里的语义很清晰，如果我把这段英文直接翻译成中文，我觉得可以是这样子的。

“我有许多的 `Article`，它有一个 `Owner`且是必须的，外键被映射成了 `UserID`”

是不是很清晰的关系？另外，两个实体间的关系只要在任意一个实体上配置一次就行了，但是配置方法不同。

上面是配置在主对象 `User`上的，如果配置在 `Article`上，语句应该是这样写的：

    HasRequired(a => a.Owner)
                    .WithMany(u => u.Articles)
                    .Map(x => x.MapKey("UserID"));

“我有一个 `Owner`切是必须的，它有很多的 `Article`，外键被映射成了 `UserID`”

&nbsp;

那一对一的关系怎么配置呢？

其实一对一不就是这样的吗：我有一个 XXX，它有一个 XXX，外键被映射成了 XXX。

    HasRequired(a => a.Owner)
                    .WithOptional(u => u.Article)
                    .Map(x => x.MapKey("UserID"));

&nbsp;

另外，HasOptional 和 HasRequired 有什么区别呢？区别就在于，这个外键（或非显示外键）是否允许为 Null。

&nbsp;

### 配置多对多关系

多对多关系的语义非常简单：我有很多 XXX，它有很多XXX……

但是，最关键的就是这个 Map。

因为多对多的话，必须要配置一张映射表，具体的配置方法如下：

    HasMany(a => a.Categories)
                    .WithMany(c => c.Articles)
                    .Map(x => x.ToTable("ArticleCategory")
                               .MapLeftKey("ArticleID")
                               .MapRightKey("CategoryID"));

这里在 Map 的时候，必须要配置关联左表的外键（或非显示外键）和关联右表的外键，还要指定关联表的名字。

总体而言，配置起来也非常简单！

&nbsp;

### 总结

以上就是 Code First 中配置引用关系的基本方法，涵盖了一对一、一对多和多对多三种关系，非常地灵活。

示例代码下载：<a href="/uploads/2012/09/Code-First.rar" target="_blank"><strong>传送门</strong></a>

 [1]: /2012/09/entity-framework-code-first-configuring-intro/ "Entity Framework Code First 配置介绍"
 [2]: /2012/09/entity-framework-code-first-configuring-property/ "Entity Framework Code First 配置介绍：属性"
 [3]: /2012/09/entity-framework-code-first-configuring-relationships/ "Entity Framework Code First 配置介绍：引用关系"
 [4]: /2012/09/entity-framework-code-first-configuring-database-mappings/ "Entity Framework Code First 配置介绍：数据库映射"
