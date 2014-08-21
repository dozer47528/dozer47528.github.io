---
title: git 环境搭建进阶
author: Dozer
layout: post
permalink: /2013/05/git-extras/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658365
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
categories:
  - 编程技术
tags:
  - cygwin
  - git
  - msysgit
  - shell
---

### <span id="_git">各种 git 工具</span>

最新在 mac 和 windows 下用了各种 git 工具；有 shell 的，也有 GUI 的，并尝试着使用它们来进行工作。

经过一番实践后，给大家推荐一套我最喜欢的 git 工具。

另外也给大家推荐一些基本配置，可以让你的工作效率大大提升。

&nbsp;

### <span id="i">公共配置</span>

先给大家看一下我 .gitconfig 文件里的一些配置（mac & windows 都适用）：

<pre>[color]
#开启着色功能
	status = auto
	diff = auto
	branch = auto
	interactive = auto
[merge]
#默认 merge 都加上 --no-ff
	ff = false
[alias]
#别名
	st = status
	ci = "commit -m"
	br = branch
	co = checkout
	cia = "commit -am"
	df = diff
	dt = difftool
	mg = merge
	mt = mergetool
	ll = "log --oneline"</pre>

<!--more-->

开启颜色后会让你的 shell 非常漂亮：

[<img class="alignnone size-medium wp-image-1287" alt="git-color" src="/uploads/2013/05/git-color-245x300.png" width="245" height="300" />][1]

最后一块是 git 的别名功能，你可以直接在配置文件里写，也可以用命令下，具体写法网上搜一下就有了。

之前我认为是 GUI 更快，因为每次打一大堆命令，实在是太烦了。用了别名后，你的效率会大大提升。

&nbsp;

### <span id="mac_os">mac os</span>

mac 上的 git 就不用怎么纠结了，直接是官方的标准 git 即可。

但是有两个问题：

1.  shell 颜色不够好看，命令不友好（就算开启了上面说的自动着色后还是不够漂亮，不友好指的是不能显示分支名）；
2.  gitk 看分支图很乱。

&nbsp;

#### <span id="oh_my_zsh">oh my zsh</span>

zsh 是一个替代 mac shell 的东西，在 shell 上拓展了很多东西。

oh my zsh 是一个开元框架可以让你方便地配置 zsh。

下载地址：<a href="https://github.com/robbyrussell/oh-my-zsh" target="_blank">https://github.com/robbyrussell/oh-my-zsh</a>

一行命令就可以安装了，上面的教程非常完成，配置完成后你的 bash 会变的非常漂亮。

&nbsp;

另外它还支持很多主题， 尝试着替换一下？会让你有更意外的收获：

<a href="https://github.com/robbyrussell/oh-my-zsh/wiki/themes" target="_blank">https://github.com/robbyrussell/oh-my-zsh/wiki/themes</a>

至此，shell 的问题解决了。对了，别忘了尝试一下 zsh 的 tab auto complete，会有惊喜哦！

效果如下：

[<img class="alignnone size-medium wp-image-1294" alt="bash" src="/uploads/2013/05/bash-300x57.png" width="300" height="57" />][2]

&nbsp;

#### <span id="git-extras">git-extras</span>

git-extras 包含了很多扩展的 git 命令，有的人喜欢，有的人不喜欢，各取所好吧。

项目地址：<a href="https://github.com/visionmedia/git-extras" target="_blank">https://github.com/visionmedia/git-extras</a>

mac 下更建议从 brew 中安装。

[<img class="alignnone size-medium wp-image-1295" alt="summary" src="/uploads/2013/05/summary.png" width="297" height="176" />][3]

&nbsp;

#### <span id="SourceTree">SourceTree</span>

SourceTree 支持 windows 平台和 mac 平台，它展示出来的分支图非常漂亮！

gitk 下的分支图，同一个分支一直会乱窜…

但是在 SourceTree 下却非常清楚！

[<img alt="sourcetree" src="/uploads/2013/05/sourcetree.png" width="142" height="288" />][4]

仔细看了以后发现，SourceTree 的分支图能保证一个分支一直线，所以看起来非常清晰。

&nbsp;

### <span id="windows">windows</span>

windows 下的 git 选择太多了：

*   TortoiseGit ：<https://code.google.com/p/tortoisegit/>
*   SourceTree：<http://sourcetreeapp.com/>
*   cygwin + git：<http://www.cygwin.com/>
*   msysgit：<http://msysgit.github.io/>
*   GitHub for Windows：<http://windows.github.com/>

&nbsp;

我把它们都用了一遍了，所以给大家比较一下：

*   TortoiseGit ：免费图形化，适合新手，但是你将无法深入理解 git；另外它的分支图太烂了！
*   SourceTree：免费图形化工具，很好用，但是还是推荐用命令行，它适合用来看分支图。[  
    ][5]
*   cygwin + git：在 windows 上模拟 linux 环境，支持很多插件，很棒！
*   msysgit：搜索 git 默认会出来这个，普及率极高，不好好配置的话非常难用。[  
    ][6]
*   GitHub for Windows：对 msysgit 强化了一下，很好用。[  
    ][7]

&nbsp;

它们各有特色，如果结合起来用就会非常方便。

&nbsp;

#### <span id="SourceTree-2">SourceTree 适合看分支图</span>

windows 下也有 SoureceTree，体验一样棒！

&nbsp;

#### <span id="Github_for_Windows">Github for Windows</span>

如果你希望打开一个 shell ，可以操作 git ，也可以同时调用 windows 的命令，那这个会很适合你。

但是这个不是 Github 的吗？ 其实我用的是 Github for Windows 中的 Github Shell 功能。

它的 Shell 可以让你自由选择，你可以选择 cmd，也可以选择 Git Bash，最强大的是选择 PowerShell。

选择了 PowerShell 后，你的 Shell 上会显示当前分支、各种状态，而且 auto complete 也做的很好。

另外还可以同时操作 windows 里的东西哦~

&nbsp;

#### <span id="cygwin">cygwin</span>

最后强烈推荐的是 cygwin，让你在 windows 下有很棒的 linux(mac) 体验。

最最最强大的是，上面在 mac 篇中提到的 git-extras 和 zsh 它都可以支持！

&nbsp;

安装 zsh 很简单，运行 cygwin.exe 然后到安装包的步骤，搜索 zsh 即可。

最后还需要休要 cygwin 默认的 Shell。

把桌面上 cygwin termial 的路径改掉即可：

<pre class="lang:sh decode:true">#原始
C:\cygwin\bin\mintty.exe -i /Cygwin-Terminal.ico -
#改成
C:\cygwin\bin\mintty.exe -i /Cygwin-Terminal.ico /bin/zsh --login</pre>

&nbsp;

安装 git-extras 也很简单，按照官网的教程直接执行一条命令即可：

<pre class="lang:sh decode:true">(cd /tmp && git clone --depth 1 https://github.com/visionmedia/git-extras.git && cd git-extras && sudo make install)</pre>

如果无法识别 make 命令，打开 cygwin.exe 去搜索 make 并安装。

&nbsp;

对了，有没有觉得复制黏贴很不爽？还有字体也不顺？还有… 怎么没有半透明？

这些 cygwin 都支持，在标题栏右击，找到配置选项，里面有很多自定义的配置。

最后效果是不是和 mac 上很像？

[<img alt="cygwin" src="/uploads/2013/05/cygwin-300x156.png" width="300" height="156" />][8]

 [1]: /uploads/2013/05/git-color.png
 [2]: /uploads/2013/05/bash.png
 [3]: /uploads/2013/05/summary.png
 [4]: /uploads/2013/05/sourcetree.png
 [5]: http://sourcetreeapp.com/
 [6]: http://msysgit.github.io/
 [7]: http://windows.github.com/
 [8]: /uploads/2013/05/cygwin.png
