---
title: git reset 在持续集成系统中的问题
author: Dozer
layout: post
permalink: /2014/07/git-reset-and-continuous-integration/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658392
categories:
  - 编程技术
tags:
  - git
  - Jenkins
  - 持续集成
---

### <span id="i">持续集成</span>

公司用上持续集成后开发效率大大提升，提交代码以后就会自动打包部署，分分钟见效！

所以自己在做东西的时候，也搭建了一套类似的环境。但最近却遇到了一个深坑。

&nbsp;

### <span id="reset_and_revert">reset and revert</span>

git 中的\`reset\`和\`revert\`是两个非常有用的命令，它们的细节不是本文的重点，简单的总结一下：

*   \`reset\`可以让\`commit\`回退，就像从来没发生过一样。
*   \`revert\`可以自动生成一次完全相反的\`commit\`，以撤销之前的操作。

这次遇到的坑来自于\`reset\`，因为\`reset\`看似是一个时光机，但是有些情况下是无法抹去了。

<!--more-->

&nbsp;

#### <span id="commit">如果`commit`没有提交</span>

这种场景下用\`reset\`不会有什么副作用，因为还没有提交到服务器。

但是如果你回退到了比远程更早的版本怎么办？

&nbsp;

#### <span id="i-2">如果回退到了比远程更早的版本</span>

如果这么操作，那么最后的现象就好像是别人提交了一次\`commit\`，而你没有\`pull\`下来。

所以如果这时候你\`git pull\`一下，你\`reset\`的\`commit\`又会回来。

这样就无解了吗？其实也不一定，还有一个杀手锏：

<pre class="lang:sh decode:true">git push -f</pre>

强制替代远程版本，让它和你本地的一样。但是这样就完美了吗？

&nbsp;

#### <span id="i-3">如果别人拉取了你回退的版本</span>

这种场景就非常不可控了，因为别人不知道这是什么情况，就算你强制提交替换了远程的版本，其他人\`push\`一下，那么那个你想抹去的\`commit\`就又回来了！

所以，如果你\`push\`后，就尽量不要用\`reset\`了，除非只有你一个人！

&nbsp;

### <span id="CI">别把CI不当人</span>

坑爹之处来了！我在开发一个项目的时候，觉得反正是自己一个人，所以用了\`reset\`，也用了\`git push -f\`，远程的确把我的那些不需要的\`commit\`抹去了。

但是我的持续集成系统早已拉过我的代码了，所以我想抹去的这部分\`commit\`一直在持续集成系统中，发布的代码就和远程的代码不一样了。

这个坑导致我一段程序调了好几天，本地明明是好的，一到服务器上就是不一样了！

&nbsp;

好了，至此，吸取教训！少用\`reset\`，如果\`push\`过，坚决不用\`reset\`！
