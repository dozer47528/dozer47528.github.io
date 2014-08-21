---
title: java 访问 Salesforce API
author: Dozer
layout: post
permalink: /2012/11/java-to-salesforce-api/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658348
categories:
  - 编程技术
tags:
  - java
  - Salesforce
  - wsdl
---

### <span id="net_to_java">.net to java</span>

最近部门准备转 java 了，大家都积极性很高，看上去 .net 还是不受待见啊～

言归正传，之前和 salesforce 的 API 交互都是用 .net 做的, WebService，没什么难度，网上千篇一律，都是标准的方法。

但是 java 就不一样了，各种方法，各种问题…

最后终于捣鼓出了一个可用的版本。

&nbsp;

&nbsp;

<em id="__mceDel"><!--more--></em>

&nbsp;

### <span id="i">调用步骤</span>

不管是用什么语言调用，其实总是那么几步，只是有的语言简单一点，有的语言复杂一点罢了。

步骤如下（绿色的代表和 .net 一样，无需演示）：

1.  <span style="color: #008000;">下载 wsdl 文件</span>
2.  根据 wsdl 文件生成对应的代码
3.  初始化对象
4.  登录，得到登录结果
5.  利用登录结果，设置 session id
6.  利用登录结果，设置 server url
7.  进行下一步操作：查询、新增、修改等

.net 的实现很多，下面就介绍一下 java 中的实现。

&nbsp;

### <span id="_wsdl">根据 wsdl 文件生成对应的代码</span>

这一步就折腾了我很久，因为网上有各种方法，但每个教程都是不可用的，可能过时了。

网上主要有三种方法：

1.  官方的 wsdl2java 工具：**<a href="http://wiki.developerforce.com/page/Introduction_to_the_Force.com_Web_Services_Connector" target="_blank">传送门</a>**
2.  利用 Apache Axis：**<a href="http://axis.apache.org/axis/" target="_blank">传送门</a>**
3.  利用 Eclipse 生成

&nbsp;

#### <span id="i-2">方案一</span>

第一个工具是官方的，根据教程，一直报错，我下的明明是 jdk 1.7 的版本，电脑上也是 1.7 的，但一直提示版本错误…

&nbsp;

#### <span id="i-3">方案二</span>

第二个方案用的是一个开源的框架：Axis

这个工具有三种用法，这里我就介绍一种我觉得最好的方式吧。

下载好后，把 lib 文件夹下的 jar 包都引用到你的 project 中：

[<img class="alignnone size-medium wp-image-910" title="lib" alt="" src="/uploads/2012/11/lib-300x211.png" width="300" height="211" />][1]

然后找到这个 jar 包：

<span style="background-color: #eeeeee;">axis.jar/org.apache.axis.wsdl.WSDL2Java.class</span>

里面有个 main 函数，运行它：

[<img class="alignnone size-medium wp-image-911" title="run" alt="" src="/uploads/2012/11/run-300x246.jpg" width="300" height="246" />][2]

第一次运行肯定是不行的，应为还没配置传入参数呢。

打开 run configurations，传入 wsdl 文件的位置：

[<img class="alignnone size-medium wp-image-912" title="args" alt="" src="/uploads/2012/11/args-300x238.png" width="300" height="238" />][3]

最后利用这个配置 run 一下即可，F5 刷新一下就会在根目录下看到 com 文件夹，把它拖动到 src 文件夹下即可。

[<img class="alignnone size-full wp-image-913" title="src" alt="" src="/uploads/2012/11/src.png" width="300" height="154" />][4]

到这步， wsdl to java 算是完成了！

&nbsp;

#### <span id="i-4">方案三</span>

eclipse 其实可以自动生成，底层其实就是调用了 Axis。

使用方法很简单，在 project 上 new 一个 Web Service Client 对象，然后输入 wsdl 地址即可。

[<img class="alignnone size-medium wp-image-914" title="wsdl" alt="" src="/uploads/2012/11/wsdl-300x283.png" width="300" height="283" />][5]

最终它会自动引用相关 jar 包，并且生成代码，效果和方法二是一样的。

但引用的 jar 包是 eclipse 下的，不是最新的，所以还是建议大家手动操作。

&nbsp;

### <span id="i-5">登录 & 后续操作</span>

上面 wsdl to java 完成后，就可以开始写 hello world 了。

注意！上面的方法一生成的是 salesforce 封装过的（可以看方案一的教程）。

因为我方法一没有成功，所以就没办法演示了，我也更推荐用标准的调用方式来操作。

直接上代码：

<pre class="lang:default decode:true brush: java; gutter: true">package Main;

import java.rmi.RemoteException;

import javax.xml.rpc.ServiceException;

import com.sforce.soap.enterprise.LoginResult;
import com.sforce.soap.enterprise.QueryResult;
import com.sforce.soap.enterprise.SessionHeader;
import com.sforce.soap.enterprise.SforceServiceLocator;
import com.sforce.soap.enterprise.SoapBindingStub;
import com.sforce.soap.enterprise.fault.InvalidIdFault;
import com.sforce.soap.enterprise.fault.LoginFault;
import com.sforce.soap.enterprise.fault.UnexpectedErrorFault;
import com.sforce.soap.enterprise.sobject.SObject;

public class main {
	public static void main(String[] args) throws InvalidIdFault,
			UnexpectedErrorFault, LoginFault, RemoteException, ServiceException {

		//init binding
		SoapBindingStub binding = (SoapBindingStub) new SforceServiceLocator()
				.getSoap();

		//login
		LoginResult result = binding.login("xxxxxxxx",
				"xxxxxxxxxx");

		//set session
		SessionHeader session = new SessionHeader();
		session.setSessionId(result.getSessionId());
		binding.setHeader(new SforceServiceLocator().getServiceName()
				.getNamespaceURI(), "SessionHeader", session);

		//set server url
		binding._setProperty(SoapBindingStub.ENDPOINT_ADDRESS_PROPERTY,
				result.getServerUrl());

		//query test
		QueryResult q = binding.query("Select Id from Contract limit 1");
		SObject[] recordSObjects = q.getRecords();
	}
}</pre>

&nbsp;

### <span id="i-6">注意点</span>

最后还有一个注意点， 调用 salesforce API 时，线上的 wsdl 和 开发环境的 wsdl 是一样的，除了一个配置不同。

.net 中引用这个 wsld 的时候配置会自动写入 config 文件中，而 java 中却写死了，所以你需要搜索下它到底在哪？

[<img class="alignnone size-medium wp-image-915" title="url" alt="" src="/uploads/2012/11/url-300x131.png" width="300" height="131" />][6]

这里就需要你自己修改一下了，最好也是写入配置中，具体怎么设计就看你自己了。

&nbsp;

### <span id="i-7">示例代码</span>

下载地址：<a href="/wp-content/uploads/2012/11/Salesforce1.zip" target="_blank"><strong>http://www.dozer.cc/uploads/2012/11/Salesforce1.zip</strong></a>

&nbsp;

&nbsp;

 [1]: /uploads/2012/11/lib.png
 [2]: /uploads/2012/11/run.jpg
 [3]: /uploads/2012/11/args.png
 [4]: /uploads/2012/11/src.png
 [5]: /uploads/2012/11/wsdl.png
 [6]: /uploads/2012/11/url.png
