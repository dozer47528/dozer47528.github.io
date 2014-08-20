---
title: iOS 证书与推送证书的注意事项
author: Dozer
layout: post
permalink: /2013/06/ios-certificates-and-push-notifications-certificates/
posturl_add_url:
  - yes
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
duoshuo_thread_id:
  - 1171159103985658366
categories:
  - 编程技术
tags:
  - iOS
  - 推送
  - 证书
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#iOS"><span class="toc_number toc_depth_1">1</span> iOS 证书与推送证书</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 基本流程和各个环节的文件</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">3</span> 注意事项</a><ul>
        <li>
          <a href="#i-3"><span class="toc_number toc_depth_2">3.1</span> 下载根证书</a>
        </li>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">3.2</span> 一定要把证书放在“登陆”分类中</a>
        </li>
        <li>
          <a href="#i-5"><span class="toc_number toc_depth_2">3.3</span> 别忘了重新生成描述文件</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-6"><span class="toc_number toc_depth_1">4</span> 最后</a>
    </li>
  </ul>
</div>

### <span id="iOS">iOS 证书与推送证书</span>

之前研究 iOS 开发，这书这块折腾了我很久很久！

老外这篇文章写得很清晰：

<a href="http://www.raywenderlich.com/32960/apple-push-notification-services-in-ios-6-tutorial-part-1" target="_blank">http://www.raywenderlich.com/32960/apple-push-notification-services-in-ios-6-tutorial-part-1</a>

之前是有中文版的，后来针对 iOS6 有了更新，所以暂时还没有中文版。

这篇文章写的最详细，按照它说的一步步做下去，就可以实现推送了～

但是期间还是遇到了很多坑，而且总感觉没有完全理解，所以便有了这篇文章，自己帮自己梳理一下，也给大家一些帮助。

流水账式的教程我就不写了，上面那篇文章很详细了～

<!--more-->

&nbsp;

### <span id="i">基本流程和各个环节的文件</span>

1.  <span style="line-height: 13px;">生成“证书签名请求文件”：这个文件是后面所有证书的源头，所以一定要保留好！</span>
2.  生成“个人开发证书”：在开发环境每个人需要一个个人开发证书
3.  新建 App：App 创建后将无法删除，这个环节没有文件
4.  生成“描述文件”：这个环节结束后就可以开始调试没有推送的程序了
5.  生成“推送证书”：每个 App 都会有一个推送证书
6.  导出“推送证书”到“个人信息交换文件”：这个文件是给服务端用来和推送服务器通讯的
7.  重新生成“描述文件”：生成推送证书后，第四步的描述文件会失效

&nbsp;

### <span id="i-2">注意事项</span>

#### <span id="i-3">下载根证书</span>

如果你用的是老版本的 iOS 开发中心，会提示你下载根证书；但是新版本却不提示了，很奇怪。

搜索后才知道从哪里下载：<a href="http://www.apple.com/certificateauthority/" target="_blank">http://www.apple.com/certificateauthority/</a>

进去后下载：Worldwide Developer Relations

只有安装了这个证书后，上述的所有证书才可以生效。

&nbsp;

#### <span id="i-4">一定要把证书放在“登陆”分类中</span>

[<img class="alignnone size-medium wp-image-1328" alt="key" src="/uploads/2013/06/key-189x300.png" width="189" height="300" />][1]

&nbsp;

有一次，我弄证书的时候，这些证书都跑到“系统”分类下了，结果就找不到了，然后我郁闷了大半天…

因为我确信我的操作步骤没有问题啊…

后来挪到“登陆（Login）”分类中就好了。

&nbsp;

#### <span id="i-5">别忘了重新生成描述文件</span>

之前我的 App 没有推送，所以我做了一个个人开发证书和一个描述文件。

后来弄了推送证书后，我以为推送证书只是给服务端推送用的，所以依然在用老的描述文件。

结果 App 中每次尝试获得 token 的时候就抱错…

后来才知道，原来如果你添加了推送功能后，一定要重新生成描述文件！

&nbsp;

### <span id="i-6">最后</span>

最后想说的是：

在按照教程做的时候，想想为什么；

这个过程真的太复杂了！很难一次成功，别放弃！我前前后后起码搞了几十遍…

 [1]: http://www.dozer.cc/wp-content/uploads/2013/06/key.png