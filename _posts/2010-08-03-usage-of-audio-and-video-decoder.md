---
title: '关于各种音频&#038;视频解码器的使用'
author: Dozer
layout: post
permalink: /2010/08/usage-of-audio-and-video-decoder/
duoshuo_thread_id:
  - 1171159103977075160
posturl_add_url:
  - yes
categories:
  - 软件
tags:
  - Mediacoder
  - 解码器
---

### <span id="i"><strong>一、开源？免费？怎么用啊…</strong></span>

ffmpeg, lame… 这些都是开源利器，最近在研究最新的音乐站，由于硬盘空间有限，再加上定位的需要，我们没必要放音质很高的音乐。

所以决定把用户上传的音乐压缩一下。

老习惯 google一下：c# 音频 转换

结果发现毫无头绪，后来才知道，原来最方便的方法是：调用ffmpeg,lame等开源利器！

&nbsp;

这时候，问题来了，怎么用？

继续 google

还是毫无头绪！ 自己看文档，却一直出错，悲剧啊~

&nbsp;

相信很多朋友也遇到了类似的问题。

&nbsp;

所以，本文给大家一些指导性的方法。不是告诉大家怎么用，而是告诉大家从哪里可以知道怎么用~

<!--more-->

### <span id="i-2"><strong>二、如何获得帮助文档</strong></span>

a) 最方便的当然是google搜索一下啦~

中文文档非常少！建议把搜索语言改成英文的，然后再去搜索

&nbsp;

b) 直接调用，查看帮助

i. 先调用相应的解码器，它会提示怎么查看帮助，然后传入相应的参数即可

[<img title="cmd1" alt="" src="/uploads/2011/01/cmd1.png" width="677" height="234" />][1]

&nbsp;

ii.但是好长啊，其实还可以把帮助输出到文件

[<img class="alignnone size-full wp-image-187" title="cmd2" alt="" src="/uploads/2011/01/cmd2.png" width="677" height="234" />][2]

&nbsp;

### <span id="i-3"><strong>三、是否有捷径？</strong></span>

上述方法依然很麻烦，特别是对相关知识不了解的朋友

&nbsp;

那是否有捷径？

答案是肯定的~ 这次不是google，而是另一个利器：MediaCoder

&nbsp;

下载MediaCoder（免费、开源的视频转换利器）后，设置一下 选项—用户界面模式—专家模式

这时候，我们发现了这个~

&nbsp;

此时，我只需要在上面的图形界面中调整相应的参数，就可以在这里看到自动生成的参数设置方法了~~

[<img class="alignnone size-medium wp-image-188" title="mediacoder" alt="" src="/uploads/2011/01/mediacoder-300x225.png" width="300" height="225" />][3]

&nbsp;

好方便！

&nbsp;

### <span id="C"><strong>四、C#中调用</strong></span>

C#中调用它们的方法和平时调用CMD差不多

&nbsp;

<pre class="brush:csharp">Process p = new Process();
p.StartInfo.FileName = "c:\\lame.exe";//这里用lame举例子
p.StartInfo.Arguments = " --vbr-new -V 7 -b -B -q 2 --noreplaygain --add-id3v2 \"c:\\test.mp3\" \"c:\\test2.mp3\"";//这里是参数
p.StartInfo.UseShellExecute = false;
p.StartInfo.RedirectStandardInput = true;//可能接受来自调用程序的输入信息
p.StartInfo.RedirectStandardOutput = true;//由调用程序获取输出信息
p.StartInfo.CreateNoWindow = true;//不显示程序窗口
p.Start();//启动程序
p.WaitForExit();//如果想等待程序退出后再运行，就加上这条，如果不等待，直接继续运行就不要这行了</pre>

但是有个问题还没解决，就是怎么实时获取转换状态~

望高手指点

&nbsp;

感谢四楼这位朋友的提醒，关于控制台输出信息的截取，可以参考这篇文章：**<a href="http://blog.csdn.net/jinjazz/archive/2008/05/07/2413039.aspx" target="_blank">http://blog.csdn.net/jinjazz/archive/2008/05/07/2413039.aspx</a>**

&nbsp;

 [1]: /uploads/2011/01/cmd1.png
 [2]: /uploads/2011/01/cmd2.png
 [3]: /uploads/2011/01/mediacoder.png
