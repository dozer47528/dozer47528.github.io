---
title: 用好 Google.com
author: Dozer
layout: post
permalink: /2011/11/use-google-in-china/
duoshuo_thread_id:
  - 1171159103977075190
posturl_add_url:
  - yes
categories:
  - 互联网
tags:
  - GFW
  - Google
---

### <span id="i">墙内墙外</span>

GFW现在真的是越来越过分了，以前用 Google 搜索，只不过是会屏蔽关键字，现在正常情况下也会经常上不去！

本文将介绍几个小技巧，让你更舒适地使用 Google 搜索

&nbsp;

### <span id="_Googlecom_Googlecomhk">用好 Google.com 而不是 Google.com.hk</span>

话说这两个有区别吗？看上去只是 Google 在不同国家设定一个网站镜像，使用的数据不应该是一样的嘛？

其实整体来说是差不多的，但是 Google.com 是美国的镜像，各国的法律不同，相对来说 Google.com 更宽松一点，所以可以在上面搜索到更多的东西！

另外，Google.com 上面的功能也会有点不一样，例如 Google Instant 这个功能也只有在 Google.com 上能体验了。

总之，如果你喜欢原汁原味的 Google.com 就一起来设置吧~

<!--more-->

**设置方法：**

在不设置的情况下，当你输入 Google.com 的时候，它会自动跳转到你所在地区的主页，大陆目前会跳转到 Google.com.hk

也就是 Google 香港

这时候，注意右下角的 **<span class="Apple-style-span" style="line-height: normal;">Google.com in English </span>** ，点一下！ 一秒变成 Google.com

&nbsp;

另外经过网友提醒，其实你可以直接输入 http://www.google.com/ncr 来到达 Google.com

这里 ncr 的意思就是：no country redirect

&nbsp;

**语言设置：**

英文得很不习惯？没关系，点击右上角的 齿轮，然后再点 Search settings

在里面可以把界面语言设置成简体中文，另外也不要忘记在需要搜索的勾选内勾上英语和繁体中文

这样，你的 Google.com 就变成了简体中文界面了，并且它还能搜索到英文和繁体中文的内容

[<img class="alignnone size-medium wp-image-492" title="google_1" alt="" src="/uploads/2011/11/google_1-300x230.png" width="300" height="230" />][1]

&nbsp;

&nbsp;

**其他设置：**

在同一个页面中，其实还有一些别的设置，

例如：SafeSearch Filtering 这个选项，建议设置 Do not filter my search results

这是防止暴力和色情的，但是有些时候一些正常的名次也会被过滤，特别是学医的，你们会很痛苦吧？

把这个去掉后 Google.com 将不会过滤这些词语了。

&nbsp;

PS.这个功能只有在界面语言设置成英文的情况下才能使用。

也就是说，如果你要搜索一个包含暴力或色情的中文词语（或许你只是为了学术或艺术），你只要把界面语言设置成英文，再把搜索语言中勾上中文，并关闭搜索过滤就可以了！

&nbsp;

### <span id="i-2">如何防止关键字屏蔽</span>

虽然没有研究过，但是从目前的症状来看，GFW 在屏蔽关键字的时候使用了 DNS 挟持。

也就是说，只要手动修改 HOSTS 文件即可达到不被屏蔽的效果。

&nbsp;

修改 Hosts 前

[<img class="alignnone size-medium wp-image-493" title="google_3" alt="" src="/uploads/2011/11/google_3-300x145.png" width="300" height="145" />][2]

&nbsp;

&nbsp;

修改 Hosts 后

[<img class="alignnone size-medium wp-image-494" title="google_2" alt="" src="/uploads/2011/11/google_2-300x176.png" width="300" height="176" />][3]

&nbsp;

&nbsp;

除此以外，还可以搜到很多水果哦~~

&nbsp;

**言归正传，下面就让我们来设置一下吧：**

这里，我们会使用 Google.cn 的 IP 作为 Google.com 的 IP，具体原理涉及到一定的网络知识，照做就行了~

运行 —— 输入“CMD” ——输入 “ping google.cn”

然后记下这个 IP

&nbsp;

用记事本打开 C:＼Windows＼System32＼drivers＼ets＼hosts 这个文件

然后在里面输入：

<pre>203.208.46.210	www.google.com
203.208.46.210	www.google.com.hk</pre>

保存！

&nbsp;

注意，Google.cn 的 IP 经常会变，但是一般不影响使用，当你发现什么时候不能用了，再去更新一下即可。

 [1]: /uploads/2011/11/google_1.png
 [2]: /uploads/2011/11/google_3.png
 [3]: /uploads/2011/11/google_2.png
