---
title: Entity Framework Code First 配置介绍：引用关系
author: Dozer
layout: post
permalink: /2012/09/entity-framework-code-first-configuring-relationships/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985008120
categories:
  - 编程技术
tags:
  - Code First
  - Entiy Framework
  - Fluent API
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 目录</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 引用关系</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 默认规则</a>
    </li>
    <li>
      <a href="#_Fluent_API"><span class="toc_number toc_depth_1">4</span> 利用 Fluent API 来配置引用关系</a>
    </li>
    <li>
      <a href="#i-4"><span class="toc_number toc_depth_1">5</span> 配置一对多与一对一关系</a>
    </li>
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">6</span> 配置多对多关系</a>
    </li>
    <li>
      <a href="#i-6"><span class="toc_number toc_depth_1">7</span> 总结</a>
    </li>
  </ul>
</div>

### <span id="i">目录</span>

[**简介**][1]

[**配置实体的属性**][2]

**[配置实体间的引用关系][3]**

[**配置数据库映射**][4]

&nbsp;

### <span id="i-2">引用关系</span>

Entity Framework 中配置了对象之间的引用关系后，在查询数据的时候会非常方便。

但是很多老系统中都是没有显示指定外键的，大多是靠在子对象中加一个主对象的 ID 来解决问题。

这时候如果不配置一下的话，是根本无法实现两个对象之间的引用关系的。因为 Entity Framework 并不知道那一列是用来确定引用关系的。

所以，这章将会介绍它默认的规则，也会介绍如何自由地配置引用关系。

<!--more-->

### <span id="i-3">默认规则</span>

当你不配置任何东西的时候，Entity Framework 默认会认为你的数据库是这样的：

*   如果你的实体中有另一个实体的集合类型导航属性，Code First 默认会认为它们是一对多的关系；
*   如果你的一个实体上有另一个实体的导航属性（不能两者都有对方的导航属性），Code First 也会默认认为它们是一对多的关系；
*   如果你的两个实体上都有对方的集合类型导航属性，Code First 默认会认为它们是多对多的关系；
*   如果你的两个实体上都有对方的导航属性，Code First 默认会认为它们是一对一的关系；
*   默认情况下，Code First 对外键和表名（多对多的关联表）都有要求。

综上：如果你是先建立实体再创建数据库，可以不用配置而使用默认规则；但是如果你是现有数据库，一般很难完全匹配，总会需要配置一些东西。

&nbsp;

### <span id="_Fluent_API">利用 Fluent API 来配置引用关系</span>

Attribute 配置法（Data Annotations）无法 实现所有功能，建议使用 Fluent API 来实现，具体配置遵循一下标准：

<span style="background-color: #eeeeee;">Entity.Has[Multiplicity](Property).With[Multiplicity](Property).Map(Option)</span>

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

### <span id="i-4">配置一对多与一对一关系</span>

<pre class="brush: csharp; gutter: true">public class User
{
    public int ID { get; set; }
    public string Name { get; set; }
    public virtual IList&lt;Article&gt; Articles { get; set; }
}
public class Article
{
    public int ID { get; set; }
    public string Name { get; set; }
    public virtual User Owner { get; set; }
}</pre>

上述代码中有两个实体，它们是一对多的关系。

完整的配置代码如下：

<pre class="brush: csharp; gutter: true">public class TestContext : DbContext
{

    public DbSet&lt;User&gt; UserSet { get { return Set&lt;User&gt;(); } }
    public DbSet&lt;Article&gt; ArticleSet { get { return Set&lt;Article&gt;(); } }

    protected override void OnModelCreating(DbModelBuilder modelBuilder)
    {
        modelBuilder
            .Configurations
            .Add(new UserTypeConfiguration())
            .Add(new ArticleTypeConfiguration());
        base.OnModelCreating(modelBuilder);
    }
}

public class UserTypeConfiguration : EntityTypeConfiguration&lt;User&gt;
{
    public UserTypeConfiguration()
    {
        HasKey(u =&gt; u.ID);
        Property(u =&gt; u.ID)
            .IsRequired()
            .HasDatabaseGeneratedOption(DatabaseGeneratedOption.Identity);
        HasMany(u =&gt; u.Articles)
            .WithRequired(a =&gt; a.Owner)
            .Map(x =&gt; x.MapKey("UserID"));
        ToTable("User");
    }
}
public class ArticleTypeConfiguration : EntityTypeConfiguration&lt;Article&gt;
{
    public ArticleTypeConfiguration()
    {
        HasKey(a =&gt; a.ID);
        Property(a =&gt; a.ID)
            .IsRequired()
            .HasDatabaseGeneratedOption(DatabaseGeneratedOption.Identity);
        ToTable("Article");
    }
}</pre>

别的都是基本配置，这里最关键的一段代码是：

<pre class="brush: csharp; gutter: true">HasMany(u =&gt; u.Articles)
                .WithRequired(a =&gt; a.Owner)
                .Map(x =&gt; x.MapKey("UserID"));</pre>

其实这里的语义很清晰，如果我把这段英文直接翻译成中文，我觉得可以是这样子的。

“我有许多的 <span style="background-color: #eeeeee;">Article</span>，它有一个 <span style="background-color: #eeeeee;">Owner </span>且是必须的，外键被映射成了 <span style="color: #000000; background-color: #eeeeee;">UserID</span>”

是不是很清晰的关系？另外，两个实体间的关系只要在任意一个实体上配置一次就行了，但是配置方法不同。

上面是配置在主对象 <span style="background-color: #eeeeee;">User </span>上的，如果配置在 <span style="background-color: #eeeeee;">Article </span>上，语句应该是这样写的：

<pre class="brush: csharp; gutter: true">HasRequired(a =&gt; a.Owner)
                .WithMany(u =&gt; u.Articles)
                .Map(x =&gt; x.MapKey("UserID"));</pre>

“我有一个 <span style="background-color: #eeeeee;">Owner </span>切是必须的，它有很多的 <span style="background-color: #eeeeee;">Article</span>，外键被映射成了 <span style="background-color: #eeeeee;">UserID</span>”

&nbsp;

那一对一的关系怎么配置呢？

其实一对一不就是这样的吗：我有一个 XXX，它有一个 XXX，外键被映射成了 XXX。

<pre class="brush: csharp; gutter: true">HasRequired(a =&gt; a.Owner)
                .WithOptional(u =&gt; u.Article)
                .Map(x =&gt; x.MapKey("UserID"));</pre>

&nbsp;

另外，HasOptional 和 HasRequired 有什么区别呢？区别就在于，这个外键（或非显示外键）是否允许为 Null。

&nbsp;

### <span id="i-5">配置多对多关系</span>

多对多关系的语义非常简单：我有很多 XXX，它有很多XXX……

但是，最关键的就是这个 Map。

因为多对多的话，必须要配置一张映射表，具体的配置方法如下：

<pre class="brush: csharp; gutter: true">HasMany(a =&gt; a.Categories)
                .WithMany(c =&gt; c.Articles)
                .Map(x =&gt; x.ToTable("ArticleCategory")
                           .MapLeftKey("ArticleID")
                           .MapRightKey("CategoryID"));</pre>

这里在 Map 的时候，必须要配置关联左表的外键（或非显示外键）和关联右表的外键，还要指定关联表的名字。

总体而言，配置起来也非常简单！

&nbsp;

### <span id="i-6">总结</span>

以上就是 Code First 中配置引用关系的基本方法，涵盖了一对一、一对多和多对多三种关系，非常地灵活。

示例代码下载：<a href="/wp-content/uploads/2012/09/Code-First.rar" target="_blank"><strong>传送门</strong></a>

 [1]: http://www.dozer.cc/2012/09/entity-framework-code-first-configuring-intro/ "Entity Framework Code First 配置介绍"
 [2]: http://www.dozer.cc/2012/09/entity-framework-code-first-configuring-property/ "Entity Framework Code First 配置介绍：属性"
 [3]: http://www.dozer.cc/2012/09/entity-framework-code-first-configuring-relationships/ "Entity Framework Code First 配置介绍：引用关系"
 [4]: http://www.dozer.cc/2012/09/entity-framework-code-first-configuring-database-mappings/ "Entity Framework Code First 配置介绍：数据库映射"