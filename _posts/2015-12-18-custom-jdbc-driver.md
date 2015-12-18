---
title: 自定义 JDBC Driver 连接公司数据库
author: Dozer
layout: post
permalink: /2015/12/custom-jdbc-driver.html
categories:
  - 编程技术
tags:
  - Java
  - MySQL
---

### DataGrip

![DataGrip](/uploads/2015/12/datagrip.jpg)

JetBrains 家最近发布了新的数据库管理工具：DataGrip

Mac 上其实一直没有好用的数据库管理工具。Sequel Pro 一天一崩溃；MySQL 官方的各种快捷键很奇怪，而且只支持 MySQL；其他的就更别说了，根本没到可用这个级别。

DataGrip 就不一样了，用惯了 Intellij IDEA 后会非常熟悉。

DataGrip 的大部分功能（基本是所有功能，目前还真没发现什么不一样的）其实在 Intellij IDEA 里都有，那为什么还要额外装一个呢？

好吧，其实我是买了 JetBrains 家所有产品的授权，所以对我来说都不需要额外付钱了。

所以其实无论你是用 Intellij IDEA、 PyCharm 还是别的 JetBrains 家产品，都可以找到同样的数据库管理功能。

<!--more-->

&nbsp;

### 迁移数据库配置时的问题

以前用 Sequel Pro，一天一崩溃实在是无法忍，DataGrip 发布后就决定用它了。

但是就出现了一个烦心事，我做的项目适合数据库打交道的，所以 Sequel Pro 里包含着大量的数据库地址和账号密码的配置。

而且这些配置都是公司统一管理的，账号密码都是无规律的，而且这些配置都在配置中心，全部找一遍起码花上大半个小时，无法忍啊！

但正是因为我们公司是统计管理数据库配置信息的，所以只要知道了数据库的名字和环境，都可以通过调用对应的 API 来获得所有的配置信息。

所以，不如自定义一个 JDBC Driver？

JetBrains 家的数据库管理工具支持自定义 JDBC Driver，所以只要实现一个 JDBC Driver 然后自动去读取配置不就非常方便了？


&nbsp;

### 代码实现

代码真的非常简单，实现一下`java.sql.Driver `接口即可。

然后如果你们公司也是类似的管理方式，那么去读取一下配置即可。


	public class ZebraDriver implements Driver {
		public Connection connect(String args, Properties info) throws SQLException {
			// 读取各种配置
			return new com.mysql.jdbc.Driver().connect(url, info);
		}
	
		public boolean acceptsURL(String url) throws SQLException {
			return true;
		}
	
		public DriverPropertyInfo[] getPropertyInfo(String url, Properties info) throws SQLException {
			return new DriverPropertyInfo[0];
		}
	
		public int getMajorVersion() {
			return 1;
		}
	
		public int getMinorVersion() {
			return 0;
		}
	
		public boolean jdbcCompliant() {
			return false;
		}
	
		public Logger getParentLogger() throws SQLFeatureNotSupportedException {
			return Logger.getLogger(ZebraDriver.class.getName());
		}
	}

最后别忘了把这个项目打成完整地`jar`包，要把 MySQL Driver 也打进去。

具体的可以去看一下[maven-assembly-plugin](http://maven.apache.org/plugins/maven-assembly-plugin/)

&nbsp;

### DataGrip 配置教程

其实这个教程对所有 JetBrains 家产品通用。

首先打开数据库配置界面，然后选择添加 Driver：

![DataGrip](/uploads/2015/12/datagrip-step1.png)

这里有几个关键点：

1. 选择对应的`jar`包
2. 然后上面的`class`要选自己的`class`
3. `Dialect`选`MySQL`

![DataGrip](/uploads/2015/12/datagrip-step2.png)

接下来就可以创建新的数据源了，选择刚才新建的 Driver，然后填入相关参数。具体参数是怎么样的，要看你内部是怎么实现的了。

我这里的规则是`database@env`，所以只要在`url`里填写一下就行了，别的任何东西都不需要填写，非常方便。

![DataGrip](/uploads/2015/12/datagrip-step3.png)

最后测试连接，成功！

![DataGrip](/uploads/2015/12/datagrip-step4.png)