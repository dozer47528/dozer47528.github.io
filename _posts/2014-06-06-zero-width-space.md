---
title: 零宽度空格
author: Dozer
layout: post
permalink: /2014/06/zero-width-space/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658388
categories:
  - 编程技术
tags:
  - java
---
<div id="toc_container" class="no_bullets">
  <p class="toc_title">
    文章导航
  </p>
  
  <ul class="toc_list">
    <li>
      <a href="#i"><span class="toc_number toc_depth_1">1</span> 看不见的空格</a>
    </li>
    <li>
      <a href="#i-2"><span class="toc_number toc_depth_1">2</span> 会有什么问题</a><ul>
        <li>
          <a href="#i-3"><span class="toc_number toc_depth_2">2.1</span> 源代码中包含零宽度空格</a>
        </li>
        <li>
          <a href="#i-4"><span class="toc_number toc_depth_2">2.2</span> 数据中的令宽度空格</a>
        </li>
      </ul>
    </li>
    
    <li>
      <a href="#i-5"><span class="toc_number toc_depth_1">3</span> 怎么避免</a>
    </li>
  </ul>
</div>

### <span id="i">看不见的空格</span>

空格看得见吗？空格本来就看不见… 但是一般的空格起码可以选中！

最近一个礼拜内竟然被这个零宽度空格坑了两次！

&nbsp;

什么是零宽度空格？

它是一个Unicode字符，它是一个空格，它没有宽度！

什么叫没有宽度？就是如果2个字母之间打了一个零宽度空格，你是看不见任何东西的…两个字母还是会挨在一起。

而且坑爹的是，就算你用的是等宽字体，它也看不见…

<!--more-->

&nbsp;

### <span id="i-2">会有什么问题</span>

我自己竟然会在短短的一周内被这个坑了两次：

&nbsp;

#### <span id="i-3">源代码中包含零宽度空格</span>

那天我正在写一个 java bean，需要用作序列化和反序列化。

在写单测的时候，自己手动写了一串\`json\`，然后传入后反序列化。

结果一直报错！java 中反序列化的时候如果字段名不一致就会报错，可是我的字段名没有写错啊！

然后我试着先序列化，然后把序列化出来的\`string\`反序列化，结果它成功了…

&nbsp;

我快崩溃了！两串\`string\`完全看不出任何区别！

到最后是怎么发现的呢？我保存到了文本文件后不小心用 VIM 打开了它，忽然发现了玄机所在！

[<img class="alignnone size-full wp-image-1509" src="http://www.dozer.cc/wp-content/uploads/2014/06/vim.png" alt="vim" width="272" height="119" />][1]

&nbsp;

#### <span id="i-4">数据中的令宽度空格</span>

另外一个坑是在业务中遇到的。用户在录入数据的时候输入了一个号码：\`ABC1234567\`。

从页面上看一切正常，但是在 SqlServer Management Studio 中看中间却有一个问号，\`ABC123?4567\`。

又崩溃了！如果你之前不知道令宽度空格的话，你能想到这是什么原因吗？编码问题？程序问题？数据库问题？

页面上看起来一切都是好的啊…

&nbsp;

### <span id="i-5">怎么避免</span>

吃一堑长一智，以后再有这样诡异的问题，我一定第一时间复制粘贴到 VIM 中查看。

高级编辑器中都是看不见这个符号的，只有 VIM 这种古老的编辑器才能看到。对了，git 的 diff 也可以看到！

另外，我也不知道我自己是怎么打出这个字符的，我们的用户我也不知道他是怎么打出这个字符的，太神奇了！

&nbsp;

如果你的程序对这种东西很敏感的话，建议把它过滤掉，但是经过我的实验，正则表达式的\`\s\`是无法过滤它的…

难怪编译器也把它当成源代码的一部分了…

 [1]: http://www.dozer.cc/wp-content/uploads/2014/06/vim.png