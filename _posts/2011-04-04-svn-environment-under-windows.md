---
title: Windows 下 SVN 环境的搭建
author: Dozer
layout: post
permalink: /2011/04/svn-environment-under-windows/
duoshuo_thread_id:
  - 1171159103977075171
posturl_add_url:
  - yes
categories:
  - 编程技术
tags:
  - ankhsvn
  - CVS
  - SVN
  - TortoiseSVN
  - VisualSVN
  - 版本控制
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#SVN"><span class="toc_number toc_depth_1">1</span> SVN 是什么？</a>
    </li>
    <li>
      <a href="#SVN-2"><span class="toc_number toc_depth_1">2</span> SVN 从哪里下载？</a>
    </li>
    <li>
      <a href="#_VisualSVN"><span class="toc_number toc_depth_1">3</span> 利用 VisualSVN 搭建服务端</a>
    </li>
    <li>
      <a href="#_ankhsvn_SVN_Visual_Studio"><span class="toc_number toc_depth_1">4</span> 利用 ankhsvn 将 SVN 与 Visual Studio 结合</a>
    </li>
  </ul>
</div>

### <span id="SVN">SVN 是什么？</span>

SVN(Subversion) 是近年来崛起的版本管理工具，是 CVS 的接班人。目前，绝大多数开源软件都使用 SVN 作为代码版本管理软件。

版本控制是程序员必备的工具，SVN 是目前的最佳选择。

&nbsp;

**为什么不用 CVS？**

SVN是其替代品，优于 CVS

&nbsp;

**为什么不用其他产品？**

这类产品都没有相互兼容性，例如 Team Foundation Server 只能和 Visual Studio 配合使用，或者安装其专门的工具。

而 SVN 更像是一种协议，只要遵守它的协议，就可以开发出对应的产品，例如 Visual Studio 插件。

<!--more-->

### <span id="SVN-2">SVN 从哪里下载？</span>

正因为 SVN 其实是一个协议，所以没有官方的产品，所以你可以选择各种第三方开发的产品。

我们这里主要介绍一下三个：

服务端：<a href="http://www.visualsvn.com/server/download/" target="_blank"><strong>VisualSVN</strong></a>

客户端：<a href="http://tortoisesvn.net/downloads.html" target="_blank"><strong>TortoiseSVN</strong></a>

Visual Studio 插件：<a href="http://ankhsvn.open.collab.net/" target="_blank"><strong>ankhsvn</strong></a>

*点击名字进入下载页面，它们都是免费的！*

&nbsp;

### <span id="_VisualSVN">利用 VisualSVN 搭建服务端</span>

**安装：**

傻瓜式下一步

&nbsp;

**配置：**

[<img class="alignnone size-full wp-image-279" title="virsualsvn" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/04/virsualsvn.png" width="205" height="244" />][1]

这是右边的控制台，可以新建 SVN 项目，也可以新建用户和群组，傻瓜式，熟悉 Windows 的你一定没有问题！

&nbsp;

利用 TortoiseSVN 搭建客户端

**安装：**

同样是傻瓜式下一步

&nbsp;

**使用：**

**如何创建一个 SVN 项目？**（如果你的项目已经在服务器上了，可以直接跳到第二步）

1.  到 SVN 服务端新建一个项目，并且可以右击得到项目地址（也可以世界附加到以前的项目中）
2.  在本地的项目文件加上右击：导入(Import) *[TortoiseSVN 是一个 Windows 资源管理器的外壳工具]*
3.  输入项目的地址

[<img class="alignnone size-medium wp-image-280" title="import" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/04/import-300x220.png" width="300" height="220" />][2]

&nbsp;

**如何从服务器下载一个项目并和本地文件关联？**

到这步位置，一个项目已经上传到服务器了，但是它们之间并没有建立版本控制关系

&nbsp;

在你需要放这个项目的文件夹中右击：检出(Checkout)

[<img class="alignnone size-medium wp-image-281" title="checkout" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/04/checkout-300x231.png" width="300" height="231" />][3]

如果你刚刚执行了第一步上传到服务器，那么填写检出目录的时候直接填写那个目录即可（会覆盖）

这样，你本地的文件和服务器的文件已经创建了关联

&nbsp;

你可以直接把那你的项目文件移动到别的地方，因为所有的版本控制信息全部保存在项目文件下的 .svn 文件中，所以如果你移动了整个项目，这个文件也会被一起移动，不用担心数据丢失！

&nbsp;

**如何使用版本控制？**

期待我下一篇文章，详细介绍 TortoiseSVN 在使用中的各种问题

&nbsp;

### <span id="_ankhsvn_SVN_Visual_Studio">利用 ankhsvn 将 SVN 与 Visual Studio 结合</span>

安装完 ankhsvn 的 Visual Studio 在解决方案管理器中年，可以看到版本控制状态图标，具体的使用方法和 TortoiseSVN 其实是相同的。

[<img class="alignnone size-medium wp-image-282" title="ankhsvn" alt="" src="http://www.dozer.cc/wp-content/uploads/2011/04/ankhsvn-175x300.png" width="175" height="300" />][4]

 [1]: http://www.dozer.cc/wp-content/uploads/2011/04/virsualsvn.png
 [2]: http://www.dozer.cc/wp-content/uploads/2011/04/import.png
 [3]: http://www.dozer.cc/wp-content/uploads/2011/04/checkout.png
 [4]: http://www.dozer.cc/wp-content/uploads/2011/04/ankhsvn.png