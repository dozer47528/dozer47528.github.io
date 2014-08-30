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

### 为什么是 git

工作的时候，常常在 Mac, Linux 和 Windows(Cygwin) 之间切换，它们都是 *nix，很多配置都是可以共享的。

例如`.zshrc`, `.gitconfig`, `.tmux.conf` 等等。

公司回家后用 Windows(Cygwin) 办公，很多配置和 Mac 不一样，非常不顺手，但是又怎么同步能？

最难的是，它们虽然大致相同，但还是有一些不同的！

<!--more-->

&nbsp;

现在各种云都上T了，而且也都跨平台了，那为什么需要用 git 来实现 Home 目录下的各种配置同步呢？

主要原因是三个：

1.  各种云很难选择仅仅同步个别文件，它们都是按文件夹级别的
2.  git 在出现冲突的时候解决起来更简单
3.  git 通过分支策略，可以有继承关系（一般情况不需要用到）

&nbsp;

### 实现步骤

&nbsp;

#### 第一步：在 github 或者 bitbucket 上新建一个项目

bitbucket 可以新建私有项目，我的配置里没什么敏感信息，所以就放 github 了。

&nbsp;

#### 第二步：立刻建一个`.gitignore`文件，并手动添加你需要同步的文件

在`.gitignore`中直接忽略所有文件`*`。

为什么这么做？Home 目录里大部分是不需要同步的，需要同步的文件你可以强制加入 git 中：

`git add -f [yourfile]`

&nbsp;

#### 第三步：整理各种配置的关系并编写脚本

我用的是`ohmyzsh`，所以主要的配置都在`.zshrc`中，最关键的一段脚本如下：

    # Include
    if [ -f ~/.env_profile ]; then
        . ~/.env_profile
    fi
    if [ -f ~/.alias_profile ]; then
        . ~/.alias_profile
    fi
    
    if [[ $('uname') == 'Linux' && -f ~/.linux_profile ]]; then
        . ~/.linux_profile
    fi
    if [[ $('uname') == 'Darwin' && -f ~/.mac_profile ]]; then
        . ~/.mac_profile
    fi
    if [[ $('uname') == 'CYGWIN_NT-6.2' && -f ~/.cygwin_profile ]]; then
        . ~/.cygwin_profile
    fi

&nbsp;

这段脚本会自动读取一下公用的配置，这个根据自己的习惯去配置，例如`.env_profile`和`.alias_profile`。

然后再根据当前的操作系统去加载不同的配置。

你可以把所有的文件全部放在`master`分支上，因为会根据系统自动加载，所以不会有冲突。

而我不会把`.env_profile`签入，因为里面都是环境变量，每个电脑都不太一样，签入没有什么意义。

&nbsp;

#### 第四步：如果有特殊需求，就拉新的分支

例如你有一个树莓派，不希望加载那么多的`ohmyzsh`插件，那么你可以新拉一个分支把相关功能注释掉。但大部分情况下不需要弄这个。

&nbsp;

### 如何在新的电脑加载这份配置

这里有些技巧，因为如果你的电脑本来就包含这些文件了，而你想全部替换掉的话，需要如下操作：

    cd ~ #到根目录
    git init #初始化git
    git remote add origin [your url] #帮顶远程分支
    git fetch origin #拉一下远程代码
    git reset --hard origin/master #强制把本地文件还原成和远程一致
    git branch --set-upstream master origin/master #绑定本地和远程的分支

&nbsp;

### 我的配置

最后贴上我的配置：<a href="https://github.com/dozer47528/home-config/tree/master" target="_blank">https://github.com/dozer47528/home-config/tree/master</a>
