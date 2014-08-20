---
title: iOS 推送的服务端实现
author: Dozer
layout: post
permalink: /2013/03/push-notifications-server-side-implement/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658360
categories:
  - 编程技术
tags:
  - Android
  - APNS
  - CSharp
  - iOS
  - java
  - Php
  - Push Notifications
  - 推送
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#Apple_Push_Notification_Service"><span class="toc_number toc_depth_1">1</span> Apple Push Notification Service</a>
    </li>
    <li>
      <a href="#Push_Sharp"><span class="toc_number toc_depth_1">2</span> Push Sharp</a>
    </li>
    <li>
      <a href="#APNS_Java"><span class="toc_number toc_depth_1">3</span> APNS Java</a>
    </li>
    <li>
      <a href="#Php"><span class="toc_number toc_depth_1">4</span> Php 实现</a>
    </li>
  </ul>
</div>

### <span id="Apple_Push_Notification_Service">Apple Push Notification Service</span>

最近研究手机开发，iOS 的 <a href="http://en.wikipedia.org/wiki/Apple_Push_Notification_Service" target="_blank"><strong>APNS</strong></a> 真的是比 Android 先进很多啊～

虽然 Android 现在也有同样的东西了，但是在中国基本是废掉的…

APNS 原理和 iOS 设备上的实现，可以在下文中获得答案：（右上角可以切换成中文）

<a href="http://www.raywenderlich.com/3443/apple-push-notification-services-tutorial-part-12" target="_blank">http://www.raywenderlich.com/3443/apple-push-notification-services-tutorial-part-12</a>  
但是，客户端实现了，服务端怎么实现了？

上面的教程中用 Php 实现了服务端的推送，代码也非常简单，原理也不难，就是实现 SSL Socket 并按照协议给苹果的服务器发送数据。

原文中的 Php 只用了不到50行就实现了。然后苦苦寻找，终于找到了 C# 版本和 Java 版本。

如果了解 APNS 原理后就会知道，iOS服务端只需要一个通用的 key（一个 App 一个 key），key 的密码，还有设备的 token（一个设备一个 token），就可以给设备发送推送了。

<!--more-->

&nbsp;

### <span id="Push_Sharp">Push Sharp</span>

.Net 实现：<a href="https://github.com/Redth/PushSharp" target="_blank"><strong>https://github.com/Redth/PushSharp</strong></a>

这个项目原名是 APNS Sharp ，作者后来准备做一个通用的项目，不仅可以支持 APNS，也可以支持各种设备的推送，所以取名 Push Sharp。

老的项目不再维护的，所以大家以后可以用新的项目。

用 nuget 下载 Push Sharp 后新建一个控制台项目，然后把 key 放在项目中。

代码如下：

<pre class="lang:c# decode:true">[STAThread]
static void Main(string[] args)
{
    //Create our service    
    PushService push = new PushService();

    //Wire up the events
    push.Events.OnNotificationSent += Events_OnNotificationSent;
    push.Events.OnNotificationSendFailure += Events_OnNotificationSendFailure;

    //Configure and start Apple APNS
    var appleCert = File.ReadAllBytes(Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "key.p12"));
    push.StartApplePushService(new ApplePushChannelSettings(false, appleCert, "xxxxx"));
    push.QueueNotification(NotificationFactory.Apple()
                .ForDeviceToken("xxxxxxxxxx")
                .WithAlert("Alert Text!")
                .WithSound("default")
                .WithBadge(7));
    Console.ReadKey();

}

private static void Events_OnNotificationSendFailure(PushSharp.Common.Notification notification, Exception notificationFailureException)
{
    Console.WriteLine("发送失败！");
}

private static void Events_OnNotificationSent(PushSharp.Common.Notification notification)
{
    Console.WriteLine("发送成功！");
}</pre>

&nbsp;

[<img class="alignnone size-medium wp-image-1095" alt="push" src="/uploads/2013/03/push-200x300.png" width="200" height="300" />][1]

是不是很简单？

&nbsp;

### <span id="APNS_Java">APNS Java</span>

Java 实现：<a href="https://github.com/notnoop/java-apns" target="_blank"><strong>https://github.com/notnoop/java-apns</strong></a>

Java 实现起来也非常简单，同样是用一个开源的类库。作者已经用 Maven 发布了，直接在 Maven 里搜索 com.notnoop.apns 即可。

实现代码如下：

<pre class="lang:java decode:true">public static void main( String[] args )
{
	ApnsService service =
		    APNS.newService()
		    .withCert("key.p12", "xxxxx")
		    .withSandboxDestination()
		    .build();

	String payload = APNS.newPayload().alertBody("Can't be simpler than this!").build();
	String token = "xxxxxx";
	service.push(token, payload);
}</pre>

最终手机上也收到了推送！

&nbsp;

### <span id="Php">Php 实现</span>

最上面的那篇教程中有哦～

同样贴上代码：

<pre class="lang:php decode:true">&lt;?php

// Put your device token here (without spaces):
$deviceToken = 'xxxxxx';

// Put your private key's passphrase here:
$passphrase = 'xxxx';

// Put your alert message here:
$message = 'My first push notification!';

////////////////////////////////////////////////////////////////////////////////

$ctx = stream_context_create();
stream_context_set_option($ctx, 'ssl', 'local_cert', 'ck.pem');
stream_context_set_option($ctx, 'ssl', 'passphrase', $passphrase);

// Open a connection to the APNS server
$fp = stream_socket_client(
	'ssl://gateway.sandbox.push.apple.com:2195', $err,
	$errstr, 60, STREAM_CLIENT_CONNECT|STREAM_CLIENT_PERSISTENT, $ctx);

if (!$fp)
	exit("Failed to connect: $err $errstr" . PHP_EOL);

echo 'Connected to APNS' . PHP_EOL;

// Create the payload body
$body['aps'] = array(
	'alert' =&gt; $message,
	'sound' =&gt; 'default'
	);

// Encode the payload as JSON
$payload = json_encode($body);

// Build the binary notification
$msg = chr(0) . pack('n', 32) . pack('H*', $deviceToken) . pack('n', strlen($payload)) . $payload;

// Send it to the server
$result = fwrite($fp, $msg, strlen($msg));

if (!$result)
	echo 'Message not delivered' . PHP_EOL;
else
	echo 'Message successfully delivered' . PHP_EOL;

// Close the connection to the server
fclose($fp);</pre>

 [1]: http://www.dozer.cc/wp-content/uploads/2013/03/push.png