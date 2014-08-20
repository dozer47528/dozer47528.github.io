---
title: 工具思维
author: Dozer
layout: post
permalink: /2012/09/work-with-tools/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103984683650
categories:
  - 大杂烩
tags:
  - Facebook
  - 工具
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#Facebook"><span class="toc_number toc_depth_1">1</span> Facebook 的工具思维</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 公司的工具思维</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">3</span> 我的工具思维</a><ul>
        <li>
          <a href="#_bat"><span class="toc_number toc_depth_2">3.1</span> 利用 bat 脚本</a>
        </li>
        <li>
          <a href="#i-3"><span class="toc_number toc_depth_2">3.2</span> 写成软件</a>
        </li>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">3.3</span> 利用脚本语言</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">4</span>  结束语</a>
    </li>
  </ul>
</div>

### <span id="Facebook">Facebook 的工具思维</span>

如果说软件工程师是为用户服务，那是不是会有一类人为同行服务？

架构师算一类，为开发工程师服务，还有呢？

&nbsp;

上个月来了一位前 Facebook 的雇员给我们讲座，聊到了他的部门，说他们部门经过很好的发展后，人数减少了。

我听了以后总感觉这句话前后矛盾，“很好的发展” & “人数减少了”，在国内，我是在无法把这两个现象联系在一起。

后来在提问环节，也有人提出了同样的问题。

于是，他便引出了 Facebook 的工具思维。

<!--more-->

据他的介绍后我们了解到，在 Facebook 内，有很大一部分人是专门做开发工具的。他们部门的人减少了，是因为用更少的人做了更多的事，多余的人去做别的事情了。所以，这不是一种进步吗？

&nbsp;

### <span id="i">公司的工具思维</span>

自从那次讲座后，发现公司也开始重视这快了，特别是最近的 hackathon ，主题就是 Tools Everything。

还有关于QA，很多QA会很迷茫，QA算是软件工程师吗？

我的理解：算！QA的价值在于开发出自动化工具，进行质量测试。

总之，工具思维很重要。

&nbsp;

### <span id="i-2">我的工具思维</span>

另外，工具思维其实和这篇文章（<a href="http://blog.csdn.net/zyboy2000/article/details/5606517" target="_blank"><strong>程序员该给自己挖口井</strong></a>）的道理一样：工作再忙，抽出时间做一点重要但不紧急的事，会为你的将来节约很多时间，也会让你有很大的提升。

最近被这种思维侵入后，我的眼前开始了出现了很多钉子（手上有锤子，一切会变成钉子），但这也不是什么坏事，因为实践下来的确为我节约了很多时间。

&nbsp;

总结下我最近做的一些工具，有些还不能称之为工具，其实只是脚本。

&nbsp;

#### <span id="_bat">利用 bat 脚本</span>

队列系统在本地测试的时候有很多个版本要跑，每个版本有不同的配置，还要用最新的代码。之前我为每个环境放了一个文件夹，然后每次编译好后就拷贝到那个目录中然后再重新执行。其实只要写一些简单的 CMD 脚本保存在 bat 文件中，就可以自动实现这一过程了。但是目前我还是要手动点一下脚本文件。其实极致的方案应该是有一个文件夹监控软件，一旦发现指定文件夹或者文件有变更，就执行指定脚本。嗯！这样就完全自动了！

除此以外，我把哪些常用的复制剪贴重复性劳动都写成了对应的脚本，真的方便了很多！

&nbsp;

#### <span id="i-3">写成软件</span>

最近一位同事操作失误，导致线上的队列出了很多错误，每次让我排查的时候我都很痛苦。因为队列表中只有简单的信息，详细的信息要到日志表中才能查看。每次写 sql 脚不能很痛苦。一开始我把可变的东西封装成了变量，然后保存成了一个 sql 脚本文件。后来我又干脆直接做了一个工具，支持 本地、Alpha、Beta 和 线上的队列异常情况分析。然后世界就变得如此美好~

另外，我上一篇文章中（<a href="/2012/01/using-the-windows-search-for-fast-start-program/" target="_blank"><strong>巧用Windows下的搜索实现快速启动程序</strong></a>）提到了一种快速启动方式，但我每次都要手动去进行这个操作。

例如 Visual Studio 2012.lnk 这个快捷方式，我先要手动改成 [VS]Visual Studio 2012.lnk，然后再复制到指定的目录。那这个过程能不能自动化？当然是可以的，后来自己写了一个工具，以后只要“右键发送到”，然后可以只能提取首字母、只能提起中文拼音首字母，也可以手动输入缩写。

&nbsp;

#### <span id="i-4">利用脚本语言</span>

bat 方便，但是不强大，写成软件强大但太麻烦，其实一直很想用脚本语言来实现，也正好学习一门脚本语言。（不知道大家有什么推荐？）

我试着用了 Ruby，实现同样一个功能，可能还是因为我不太熟，它还没有用 C# 来的方便…

&nbsp;

### <span id="i-5"> 结束语</span>

既然行知有效，便持之以恒，其实自己开发工具也是很开心的一件事，但目前这些工具都是真对我个人的小工具，希望以后也能为部门的其他同事，开发更多通用，强大的工具！