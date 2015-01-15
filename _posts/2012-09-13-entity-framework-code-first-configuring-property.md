---
title: Entity Framework Code First 配置介绍：属性
author: Dozer
layout: post
permalink: /2012/09/entity-framework-code-first-configuring-property/
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

### 配置方法介绍

在 Code First 之前，其实大家都知道一种配置方法：

    class AnimalType
    {
      public int Id { get; set; }
      [Required]
      public string TypeName { get; set; }
    }

没错，这就是 Code First 的配置方法之一：Data Annotations

直译叫做数据批注，原理就是在对应的字段上加上<span style="background-color: #eeeeee;"> System.ComponentModel.DataAnnotations</span> 命名空间下的一些 Attribute，就可以实现各种配置了。

这种作法在 Model First 和 Database First 的时代就有了，也可以同时被用来做 MVC 的数据验证。

<!--more-->

另外一种配置方法叫做：Fluent API

这个实在不好翻译，我更喜欢称呼它的原名。

示例如下：

    class VetContext:DbContext
    {
      public DbSet<Patient> Patients { get; set; }
      public DbSet<Visit> Visits { get; set; }
      protected override void OnModelCreating(DbModelBuilder modelBuilder)
      {
        modelBuilder.Entity<AnimalType>()
                    .ToTable("Species");
        modelBuilder.Entity<AnimalType>()
                    .Property(p => p.TypeName).IsRequired();
       }
    }

&nbsp;

那最终到底选择哪种呢？

个人建议还是选择 Fluent API。

因为它提供的功能更多；而且它可以完全脱离 Model，便于分层，EF 是仓促层的东西，尽量不要入侵 Model。

所以它非常适合 DDD，这里有一位高人的实例程序，非常的棒：**<a href="http://www.cnblogs.com/daxnet/archive/2012/06/20/2555938.html" target="_blank">传送门</a>**

&nbsp;

### 属性长度

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      max (type specified by database)
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      MinLength(nn)<br /> MaxLength(nn)<br /> StringLength(nn)
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).HasMaxLength(nn)
    </td>
  </tr>
</table>

长度是用来描述 <span style="background-color: #eeeeee;">String </span>或者 <span style="background-color: #eeeeee;">Byte </span>数组的，默认会被设置成对应类型的最大值。例如在 SQL Server 中，它们分别会被设置成 <span style="background-color: #eeeeee;">nvarchar(max)</span> 和 <span style="background-color: #eeeeee;">varbinary(max)</span>。

&nbsp;

### 数据类型

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      根据不同的数据提供者，会有不同的默认数据类型。<br /> 在 SQL Server 中：<br /> String : nvarchar(max)<br /> Integer : int<br /> Byte Array : varbinary(max)<br /> Boolean : bit
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      Column(TypeName=“xxx”)
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).HasColumnType (“xxx”)
    </td>
  </tr>
</table>

&nbsp;

### 可空配置

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      主键、外键: 不为空<br /> 引用类型 (String, arrays): 可空<br /> 值类型 (all numeric types, DateTime, bool, char) : 不为空<br /> Nullable<T>  : 可空
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      Required
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).IsRequired
    </td>
  </tr>
</table>

&nbsp;

### 主键映射

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      命名为 Id 的属性<br /> 命名为 [类型名] + Id 的属性
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      Key
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.HasKey(t=>t.PropertyName)
    </td>
  </tr>
</table>

&nbsp;

### 配置标识规范属性

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      数据库默认标识规范
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      DatabaseGenerated(DatabaseGeneratedOption)
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName)<br /> .HasDatabaseGeneratedOption(DatabaseGeneratedOption)
    </td>
  </tr>
</table>

&nbsp;

### 为乐观并发配置 TimeStamp/RowVersion 字段

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      无
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      TimeStamp
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).IsRowVersion()
    </td>
  </tr>
</table>

&nbsp;

### 为没有 Timestamp 的字段配置乐观并发

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      无
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      ConcurrencyCheck
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).IsConcurrencyToken()
    </td>
  </tr>
</table>

&nbsp;

### 配置非Unicode的数据库类型

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      所有的 String 都会被配制成 Unicode 编码的数据库类型
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      无法配置
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).IsUnicode(boolean)
    </td>
  </tr>
</table>

&nbsp;

### 配置 Decimals

<table border="1" cellspacing="0" cellpadding="0">
  <tr>
    <td>
      Convention
    </td>

    <td>
      Decimals 18, 2
    </td>
  </tr>

  <tr>
    <td>
      Data Annotation
    </td>

    <td>
      无法配置
    </td>
  </tr>

  <tr>
    <td>
      Fluent
    </td>

    <td>
      Entity<T>.Property(t=>t.PropertyName).HasPrecision(n,n)
    </td>
  </tr>
</table>

&nbsp;

### 配置复杂类型

这块比较复杂，也比较少用，感兴趣的可以去翻阅原文。

 [1]: /2012/09/entity-framework-code-first-configuring-intro/ "Entity Framework Code First 配置介绍"
 [2]: /2012/09/entity-framework-code-first-configuring-property/ "Entity Framework Code First 配置介绍：属性"
 [3]: /2012/09/entity-framework-code-first-configuring-relationships/ "Entity Framework Code First 配置介绍：引用关系"
 [4]: /2012/09/entity-framework-code-first-configuring-database-mappings/ "Entity Framework Code First 配置介绍：数据库映射"
