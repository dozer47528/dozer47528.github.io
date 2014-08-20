---
title: Hack a New Year
author: Dozer
layout: post
permalink: /2013/01/hack-a-new-year/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658353
categories:
  - 大杂烩
tags:
  - Hackathon
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#Hack_a_New_Year"><span class="toc_number toc_depth_1">1</span> Hack a New Year</a>
    </li>
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">2</span> 我们做了什么？</a>
    </li>
    <li>
      <a href="#24"><span class="toc_number toc_depth_1">3</span> 24小时</a>
    </li>
    <li>
      <a href="#_Hackathon"><span class="toc_number toc_depth_1">4</span> 说说上次的 Hackathon</a>
    </li>
  </ul>
</div>

### <span id="Hack_a_New_Year">Hack a New Year</span>

新年的 <a href="http://zh.wikipedia.org/zh/Hackathon" target="_blank"><strong>Hackathon</strong></a> 刚刚结束，和上次部门的 Hackathon 完全是两种不同的感觉，有些东西有必要拿出来说说~

&nbsp;

### <span id="i">我们做了什么？</span>

我们的项目叫“闪验”，提供一种快速验证团购券的方案。

原理很简单，和 <a href="https://bu.mp/" target="_blank"><strong>Bump</strong></a> 类似，用户勾选需要验证的团购券，然后用户和商户碰一下，就可以进行验券了。

从产品的角度来讲，它有很多问题，但是我们为什么做这个？

引用我们这次活动的一句话： just for fun!

实现原理也很简单：

两台设备碰一下，把自己的地理位置和时间传给服务器，服务器会接收到许许多多 Bump 请求，然后根据距离和时间算出可能在碰撞的两个人。相互确认后就匹配成功了。

<!--more-->

### <span id="24">24小时</span>

我们组有两个 js 开发工程师，另外我还有另一位也都熟悉 js，所以我们的架构师寸老师就决定都用 js 了，为什么？因为架构师只会 js ，哈哈哈哈哈~

我们两位后端开发工程师顺便玩玩 <a href="http://zh.wikipedia.org/wiki/Node.js" target="_blank"><strong>node.js</strong></a>，所以就这样吧~

最终的技术方案如下：

*   移动终端 PhoneGap + html5
*   服务端 node.js

&nbsp;

然后，我们就开动了~

&nbsp;

研究碰撞特性

[<img class="alignnone size-medium wp-image-1031" alt="bump" src="/uploads/2013/01/bump-300x225.png" width="300" height="225" />][1]

&nbsp;

服务器和客户端的交互图

[<img class="alignnone size-medium wp-image-1032" alt="server" src="/uploads/2013/01/server-225x300.png" width="225" height="300" />][2]

&nbsp;

联测中…

[<img class="alignnone size-medium wp-image-1033" alt="all" src="/uploads/2013/01/all-300x225.png" width="300" height="225" />][3]

&nbsp;

Github 上的版本树

[<img class="alignnone size-medium wp-image-1034" alt="github" src="/uploads/2013/01/github-222x300.png" width="222" height="300" />][4]

&nbsp;

最后的产品，虽然体验不是那么棒，但是可以完整地跑通了~

一个晚上，研究了好多东西，也接触了很多新东西！

后来的总结会上，还看到了各位好多好多有趣的点子和产品~ so cool!

&nbsp;

### <span id="_Hackathon">说说上次的 Hackathon</span>

上次的 Hackathon 我们团队虽然获得了第一名，但是却远没有这次有趣。

为什么没有这次的有趣？败就败在了奖金上。这次的 Hackathon 弱化了比赛的概念，提倡大家尝试新东西，尝试没有用过的东西。

有了金钱的诱惑后，大家的目的就不一样了，做出好东西往往不是用新技术的，用自己熟悉的东西更容易做出更好的东西，但都已经是大家很熟悉的技术了，再用它做个东西出来有意思吗？而且用户跟喜欢外观漂亮的东西，有时候就算内在实力过硬，也比不过一个华丽的空壳。但是用一个晚上去做个好看的空壳有意思吗？我们又不是做设计的… 这时候，Hackathon 已经不是 Hackathon 了。

但是上次的 Hackathon 毕竟是我们部门第一次举办，最后希望我们部门也能有这么一次有趣的 Hackathon！

&nbsp;

&nbsp;

 [1]: http://www.dozer.cc/wp-content/uploads/2013/01/bump.png
 [2]: http://www.dozer.cc/wp-content/uploads/2013/01/server.png
 [3]: http://www.dozer.cc/wp-content/uploads/2013/01/all.png
 [4]: http://www.dozer.cc/wp-content/uploads/2013/01/github.png