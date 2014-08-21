---
title: 利用 git 共享 Home 目录下的各种配置
author: Dozer
layout: post
permalink: /2014/07/use-git-to-share-config/
categories:
  - 操作系统
tags:
  - cygwin
  - git
  - Github
  - Linux
  - Mac
  - Windows
---

### <span id="_git">为什么是 git</span>

工作的时候，常常在 Mac, Linux 和 Windows(Cygwin) 之间切换，它们都是 *nix，很多配置都是可以共享的。

例如`.zshrc`, `.gitconfig`, `.tmux.conf` 等等。

公司回家后用 Windows(Cygwin) 办公，很多配置和 Mac 不一样，非常不顺手，但是又怎么同步能？

最难的是，它们虽然大致相同，但还是有一些不同的！

<!--more-->

&nbsp;

现在各种云都上T了，而且也都跨平台了，那为什么需要用 git 来实现 Home 目录下的各种配置同步呢？

主要原因是两个：

1.  各种云很难选择仅仅同步个别文件，它们都是按文件夹级别的
2.  git 通过分支策略，可以有继承关系

&nbsp;

### <span id="i">实现步骤</span>

第一步：在 github 或者 bitbucket 上新建一个项目

bitbucket 可以新建私有项目，我的配置里没什么敏感信息，所以就放 github 了。

&nbsp;

第二步：立刻建议一个`.gitignore`文件，并手动添加你需要同步的文件

在`.gitignore`中直接忽略所有文件`*`。

为什么这么做？Home 目录里大部分是不需要同步的，需要同步的文件你可以强制加入 git 中：

<pre class="lang:sh decode:true ">git add -f yourfile</pre>

&nbsp;

第三步：整理各种配置的继承关系并建立分支

我用的是`ohmyzsh`，所以主要的配置都在`.zshrc`中，为了实现各个环境的特殊配置，可以加入如下代码在`master`分支中：

<pre class="lang:sh decode:true"># Include
if [ -f ~/.env_profile ]; then
        . ~/.env_profile
fi
if [ -f ~/.mac_profile ]; then
        . ~/.mac_profile
fi
if [ -f ~/.linux_profile ]; then
        . ~/.linux_profile
fi
if [ -f ~/.cygwin_profile ]; then
        . ~/.cygwin_profile
fi</pre>

然后新建一个`cygwin`分支，并新建`.cygwin_profile`文件：

<pre class="lang:sh decode:true"># 解决tmux在cygwin下的问题
alias tmux='rm -rf /tmp/tmux* && tmux'

# 解决ohmyzsh在cygwin中不兼容autojump的问题
[[ -s $HOME/.autojump/etc/profile.d/autojump.sh ]] && source $HOME/.autojump/etc/profile.d/autojump.sh
autoload -U compinit && compinit -u</pre>

这几行脚本只有在`cygwin`中才需要，而其他平台并不需要。

&nbsp;

第四步：全局配置变更

将来有全局的配置变更，直接在`master`分支提交一下，再`merge`到各个平台即可。

&nbsp;

第五步：环境变量

上面的配置中还有一个`.env\_profile`文件，我的设计中，这个文件是用来放环境变量的，因为这个通用性非常差，例如`JAVA\_HOME`，就算是都是 Mac 也会有不同的版本。

总之策略是你自己设定的，根据自己的习惯来就行了。

&nbsp;

### <span id="i-2">自动化脚本</span>

目标完成，基本策略也很清晰，还差什么呢？好像还有点不方便！

能不能自动`merge`？能不能一键在新电脑上初始化？

这些都不是问题，待我写几个脚本~

&nbsp;

最后贴上我的配置：<a href="https://github.com/dozer47528/home-config/tree/master" target="_blank">https://github.com/dozer47528/home-config/tree/master</a>
