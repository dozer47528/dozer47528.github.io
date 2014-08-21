---
title: Entity Framework Code First 配置介绍：数据库
author: Dozer
layout: post
permalink: /2012/09/entity-framework-code-first-configuring-database-mappings/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985329717
categories:
  - 编程技术
tags:
  - Code First
  - Entiy Framework
  - Fluent API
---

### <span id="i">目录</span>

[**简介**][1]

[**配置实体的属性**][2]

**[配置实体间的引用关系][3]**

[**配置数据库映射**][4]

&nbsp;

### <span id="i-2">映射表名和组织架构名</span>

<pre class="brush: csharp; gutter: true">//Data Annotations
[Table("PersonPhotos")]
public class PersonPhoto

[Table("Locations", Schema="dbo")]
public class Destination

//Fluent API
modelBuilder.Entity&lt;Destination&gt;().ToTable("Locations", "dbo");</pre>

<!--more-->

### <span id="i-3">映射数据库列</span>

<pre class="brush: csharp; gutter: true">//Data Annotations
[Column("LocationID")]
public int DestinationId { get; set; }
[Required, Column("LocationName")]
public string Name { get; set; }

//Fluent API
public class DestinationConfiguration :
 EntityTypeConfiguration&lt;Destination&gt;
{
  public DestinationConfiguration()
  {
    Property(d =&gt; d.Nam
      .IsRequired().HasColumnName("LocationName");
    Property(d =&gt; d.DestinationId).HasColumnName("LocationID");</pre>

&nbsp;

### <span id="i-4">映射两个实体到同一张表</span>

<pre class="brush: csharp; gutter: true">//Data Annotations
[Table("People")]
public class Person
[Table("People")]
public class PersonPhoto

//Fluent API
modelBuilder.Entity&lt;Person&gt;().ToTable("People");
modelBuilder.Entity&lt;PersonPhoto&gt;().ToTable("People");</pre>

有人会问，这样做的好处是什么？那最大的好处当然是延迟加载啦。

让很多数据在同一张表，加载的时候你又想只加载一部分的时候，可以利用这种方式把同一张表分割到两个实体中。

<pre class="brush: csharp; gutter: true">[Required]
public virtual PersonPhoto Photo { get; set; }

var people = context.People.ToList();
var firstPerson = people[0];
SomeCustomMethodToDisplay(firstPerson.Photo.Caption);</pre>

如上述代码所示，一开始读取 <span style="background-color: #eeeeee;">People</span> 的时候只会读取表中的一部分数据。当需要读取额外的数据的时候，Entity Framework 默认会使用延迟加载。

&nbsp;

### <span id="i-5">映射两个表到同一个实体</span>

当两个实体有引用关系的时候，一般都会在这个实体A上定义一个实体B的引用。

除了定义引用外，也可以直接把实体B的字段引射到实体A上，也就是把两个表映射到同一个实体中。

<pre class="brush: actionscript3; gutter: true">public class DestinationConfiguration :
  EntityTypeConfiguration&lt;Destination&gt;
{
  public DestinationConfiguration()
  {
    Property(d =&gt; d.Name)
     .IsRequired().HasColumnName("LocationName");
    Property(d =&gt; d.DestinationId).HasColumnName("LocationID");
    Property(d =&gt; d.Description).HasMaxLength(500);
    Property(d =&gt; d.Photo).HasColumnType("image");
    // ToTable("Locations", "baga");
    Map(m =&gt;
        {
          m.Properties(d =&gt; new
             {d.Name, d.Country, d.Description });
          m.ToTable("Locations");
        });
    Map(m =&gt;
        {
          m.Properties(d =&gt; new { d.Photo });
          m.ToTable("LocationPhotos");
        });
  }
}</pre>

&nbsp;

### <span id="i-6">控制实体是否映射到数据库</span>

在 DbContext 中，如果你新增了一个 <span style="background-color: #eeeeee;">DbSet<Entity></span> 属性，这个实体就会被映射到数据库中；

另外，一个已经映射到数据库中的实体引用了另一个实体，那么它也会被映射到数据库中；

最后，如果你没有添加任何引用，而仅仅是增加了一个该实体的配置（哪怕是空的），这个实体也会被映射到数据库中。

&nbsp;

### <span id="i-7">控制实体不被映射到数据库</span>

<pre class="brush: csharp; gutter: true">//Data Annotations
[NotMapped]
public class MyInMemoryOnlyClass

//Fluent API
modelBuilder.Ignore&lt;MyInMemoryOnlyClass&gt;();</pre>

配置后，就算这个实体被另一个已经映射的实体引用，那么它也不会被映射到数据库中。

&nbsp;

### <span id="i-8">控制属性不被否映射到数据库</span>

<pre class="brush: csharp; gutter: true">//Data Annotations
[NotMapped]
public string TodayForecast

//Fluent API
Ignore(d =&gt; d.TodayForecast);</pre>

&nbsp;

### <span id="i-9">映射继承关系</span>

#### <span id="Code_First_Table_Per_Hierarchy_TPH">Code First 的默认层级关系：每个层级关系一张表[Table Per Hierarchy (TPH)]</span>

如果定义了如下两个类：

<pre class="brush: csharp; gutter: true">public class Lodging
{
  public int LodgingId { get; set; }
  public string Name { get; set; }
  public string Owner { get; set; }
}
public class Resort : Lodging
{
  public string Entertainment { get; set; }
  public string Activities { get; set; }
}</pre>

这两个实体会被配置在同一张表中，并且会被自动加上一个 <span style="background-color: #eeeeee;">Discriminator</span> 列（默认是），用来区分存放在这个表中的到底是什么类型。

你也可以用 Fluent API 来配置这个用来鉴别的列叫什么，和鉴别方式：

<pre class="brush: csharp; gutter: true">//通过文本来鉴别
Map(m =&gt;
    {
        m.ToTable("Lodgings");
        m.Requires("LodgingType").HasValue("Standard");
    })
.Map&lt;Resort&gt;(m =&gt;
    {
        m.Requires("LodgingType").HasValue("Resort");
    });

//通过布尔类型来鉴别
Map(m =&gt;
{
  m.ToTable("Lodging");
  m.Requires("IsResort").HasValue(false);
})
.Map&lt;Resort&gt;(m =&gt;
{
  m.Requires("IsResort").HasValue(true);
});</pre>

&nbsp;

#### <span id="Code_First_Table_Per_TpyeTPT">Code First 的另一种层级关系：每个类型一张表[Table Per Tpye(TPT)]</span>

另外，也可以配制成每一种类型一张表：

<pre class="brush: csharp; gutter: true">//Data Annotations
[Table("Resorts")]//只需要在子类上指定一个表名即可
public class Resort : Lodging
{
  public string Entertainment { get; set; }
  public string Activities { get; set; }
}

//Fluent API
//可以是
modelBuilder.Entity&lt;Resort&gt;().ToTable("Resorts");

//或者
modelBuilder.Entity&lt;Lodging&gt;().Map(m =&gt;
   {
     m.ToTable("Lodgings");
   }).Map&lt;Resort&gt;(m =&gt;
   {
     m.ToTable("Resorts");
   });</pre>

&nbsp;

#### <span id="_TPT_Table_Per_Concrete_Type_TPC">和 TPT 类似的一种关系：每个类型完整地映射在一张表中[Table Per Concrete Type (TPC)]</span>

TPC 和 TPT 的区别就是，TPT 的子类只存放比父类多出来的几个字段，而 TPC 会存放所有的字段。

<pre class="brush: csharp; gutter: true">modelBuilder.Entity&lt;Lodging&gt;()
 .Map(m =&gt;
 {
   m.ToTable("Lodgings");
 })
 .Map&lt;Resort&gt;(m =&gt;
 {
   m.ToTable("Resorts");
   m.MapInheritedProperties();
 });</pre>

 [1]: /2012/09/entity-framework-code-first-configuring-intro/ "Entity Framework Code First 配置介绍"
 [2]: /2012/09/entity-framework-code-first-configuring-property/ "Entity Framework Code First 配置介绍：属性"
 [3]: /2012/09/entity-framework-code-first-configuring-relationships/ "Entity Framework Code First 配置介绍：引用关系"
 [4]: /2012/09/entity-framework-code-first-configuring-database-mappings/ "Entity Framework Code First 配置介绍：数据库映射"
