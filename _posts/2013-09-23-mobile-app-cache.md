---
title: Mobile App 缓存设计逻辑
author: Dozer
layout: post
permalink: /2013/09/mobile-app-cache/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658374
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  - 
categories:
  - 编程技术
tags:
  - HTML5
  - PhoneGap
  - 缓存
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 出了什么问题？</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 慢不是你的错</a>
    </li>
    <li>
      <a href="#i-3"><span class="toc_number toc_depth_1">3</span> 缓存设计逻辑</a><ul>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">3.1</span> 如果第一次打开</a>
        </li>
        <li>
          <a href="#App"><span class="toc_number toc_depth_2">3.2</span> 曾经打开过，App 关闭后重新打开</a>
        </li>
        <li>
          <a href="#i-5"><span class="toc_number toc_depth_2">3.3</span> 下拉刷新</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-6"><span class="toc_number toc_depth_1">4</span> 进阶优化</a><ul>
        <li>
          <a href="#i-7"><span class="toc_number toc_depth_2">4.1</span> 加载失败的处理</a>
        </li>
        <li>
          <a href="#i-8"><span class="toc_number toc_depth_2">4.2</span> 超时自动加载</a>
        </li>
        <li>
          <a href="#i-9"><span class="toc_number toc_depth_2">4.3</span> 考虑在后台异步检查是否有新数据</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#DOM"><span class="toc_number toc_depth_1">5</span> DOM元素优化</a>
    </li>
    <li>
      <a href="#i-10"><span class="toc_number toc_depth_1">6</span> 其他性能问题</a>
    </li>
  </ul>
</div>

### <span id="i">出了什么问题？</span>

最近在用 PhoneGap 做手机端 App，第一个版本出来后，给人的整体感觉就是：卡！慢！非常卡！非常慢！

每次切换 tab 都要5秒左右，这个实在是无法接受啊。

&nbsp;

### <span id="i-2">慢不是你的错</span>

本来，用 PhoneGap 就会让人产生质疑，它会不会很慢？

所以一出现慢的问题，大部分人一开始都会怪到 PhoneGap 头上吧？我一开始也在质疑自己，用 PhoneGap 是正确的选择吗？

<!--more-->

&nbsp;

但当我仔细思考后我发现，我们真的是错怪 PhoneGap 了，这个慢，真不是你的错！

&nbsp;

为什么呢？

大家有没有数过手机上的新浪微博刷新一次要多久？

我家是 20M 电信，手机连 wifi，手机端新浪微博刷新一次要 3s 以上。

可… 我们的接口都在 3s 一下，却不如人家慢呢？

因为它做了很多优化！最关键的就是在缓存和分页的应用上了。

&nbsp;

### <span id="i-3">缓存设计逻辑</span>

在参考了新浪微博的体验后，我觉得良好的体验应该是这样的：

&nbsp;

#### <span id="i-4">如果第一次打开</span>

这种场景就不用说了，肯定是要去调用接口的。

&nbsp;

#### <span id="App">曾经打开过，App 关闭后重新打开</span>

如下图：

[<img class="alignnone size-medium wp-image-1369" alt="reopen" src="/uploads/2013/09/reopen-200x300.png" width="200" height="300" />][1]

最新的一条记录是在9月21日，打开 App 后直接显示上次加载的内容，App 没有自动请求数据。

这时候如果在下面  tab 中切换，也不会请求数据，所以速度非常快。

&nbsp;

#### <span id="i-5">下拉刷新</span>

[<img class="alignnone size-medium wp-image-1370" alt="reload" src="/uploads/2013/09/reload-200x300.png" width="200" height="300" />][2]

有了缓存以后，用户需要对自己的数据可控，所以加下拉刷新以后，就可以让用户自己来控制何时刷新了。

网络没了，就不刷新；急着看新数据，就多刷几次。

&nbsp;

缓存 + 上拉刷新是标配，有了这个功能后，整体的体验会非常棒！

&nbsp;

### <span id="i-6">进阶优化</span>

说完了标配，就要说说可以让体验更上一层楼的进阶优化了。

&nbsp;

#### <span id="i-7">加载失败的处理</span>

手机App数据加载失败是一件很常见的事情，坐地铁遇到死角网络就断了。

如果这是用户正好在刷新数据怎么办？

第一个关键点：如果失败千万别把缓存的老数据清空了，好歹还可以看看以前的数据嘛。

第二个关键点：如果失败，给一个友好的提示，例如：“网络不佳，请重试…”。总之就是要告诉用户，他应该怎么做。

&nbsp;

#### <span id="i-8">超时自动加载</span>

如果缓存的数据放了很久了，其实重新打开 App 的时候可以考虑自动帮用户刷新的。

这里又要提到上面的一点了，加载失败别把老数据清空了！

&nbsp;

#### <span id="i-9">考虑在后台异步检查是否有新数据</span>

大家如果在看微博，50条看了你半个多小时，这半个多小时里，一定发生了很多很多事情…

微博客户端会在后台定时检查有多少心数据，然后会在左下角显示。

这样用户就知道他有没有必要去刷新一下数据了。

另外就算网络状况不佳，检查失败了，也不会影响用户当前的操作。

&nbsp;

### <span id="DOM">DOM元素优化</span>

从性能上来看，Native App 肯定比 Html 的性能更好。

同样是一个 list，Html 可能在有 20 个 item 的时候就卡了，而 Native 可能要到 50 个 item才卡。

&nbsp;

但是我依然不认为这是 PhoneGap 架构的严重问题。

是的，它不如 Native，但是就算你用 Native ，你也必须面对这个问题！

Native 的解决思路可能是复用 list 中的 item，那 Html 中为什么就不能这么做呢？

&nbsp;

另外还有上拉加载更多，等等，这些不都是在解决 list 中元素过多的问题吗？

无论是 Native 还是 Html ，都会有同样的问题，你都要去解决，解决的思路也都很类似。

&nbsp;

### <span id="i-10">其他性能问题</span>

虽说展示一个 list 页面，PhoneGap + Html 的性能问题可以克服靠代码克服，而且这个问题在 Native 里也有；

但如果你想在切换多页面的时候有切换动画，用 Html5 的效果还是会差许许多多的。

这时候，你可能就需要考虑一部分 Native 代码，一部分 Html 代码了。而实现这个的成本，不亚于直接用 Native 开发。

&nbsp;

 [1]: /uploads/2013/09/reopen.png
 [2]: /uploads/2013/09/reload.png