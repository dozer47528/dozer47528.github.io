---
title: Entity Framework Code First 配置介绍
author: Dozer
layout: post
permalink: /2012/09/entity-framework-code-first-configuring-intro.html
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

### 简介

自从 Code First 推出后，大家慢慢地把开发模式转换了过来，也从中发现了很多优点。

但是，公司最近的一个需求一直无法被满足。（因为之前不知道 Code First 那么强大）

&nbsp;

目前的代码中，有实体，有数据库，实体间有关联，但是数据库中无显示外键。

大家第一眼看到有数据库的时候，肯定会想到用 Database First。但是，生成的对象之间并没有引用关系，因为没有显示外键，如果没有引用关系，那又何必用 ORM 呢？

<!--more-->

其实，如果掌握了 Code First 的配置技巧，这些都不再是问题了！

掌握配置技巧后，你可以非常灵活的对实体和数据库进行映射。

包括且不限制于一下特点：

指定列名、指定表名、指定数据类型；

无外键也可配置多种引用关系，一对多、一对一、多对多；

等等…

&nbsp;

所以，Code First 不仅适合从头开始写的项目，也适合已经存在实体或者存在数据库的项目。

那么，就让我们开始吧！

&nbsp;

### 备注

本系列主要来自于《Programming Entity Framework Code First》，示例代码由本人亲自编写。

 [1]: /2012/09/entity-framework-code-first-configuring-intro/ "Entity Framework Code First 配置介绍"
 [2]: /2012/09/entity-framework-code-first-configuring-property/ "Entity Framework Code First 配置介绍：属性"
 [3]: /2012/09/entity-framework-code-first-configuring-relationships/ "Entity Framework Code First 配置介绍：引用关系"
 [4]: /2012/09/entity-framework-code-first-configuring-database-mappings/ "Entity Framework Code First 配置介绍：数据库映射"
