---
title: 知乎用户屏蔽插件
author: Dozer
layout: post
permalink: /2016/08/zhihu-block-chrome-extension.html
categories:
  - 互联网
tags:
  - Chrome
---

### 脑子是个好东西，希望人人都能拥有它

知乎是个很有意思的地方，而人与人之间有不同的观点是很正常的事情。

但有的人就很奇怪，一言不和就开始人身攻击了。

这两天就遇到一个奇葩的人。

<!--more-->
![Zhihu Comment](/uploads/2016/08/zhihu-comment.png)

问题是：高速遇到紧急情况应该紧急刹车还是紧急变道？

“让速不让道”这个原则是流淌着很多血的，高速遇到紧急情况进行紧急变道简直是找死。

但有些人的观点是：大家应该去尝试了解车辆的极限，只要多多观察紧急变线是安全的。

具体谁对谁错其实本来就没有一个最终的答案，车不同，驾驶技术不同，处理的方式也会有不同。

&nbsp;

那大家相互辩论一下，真像总是越辩越明的。但这个人就奇葩了，所有和他不意见不一致的人都变成了“傻子”、“中二少年”、“技术差”。

我和他辩到一半，最后他把我屏蔽了，还振振有词地说到：我不想和你们这种喷子争什么了。

&nbsp;

😂  我竟无言以对，最无语的是，我本来以为知乎不应该是这样的一个地方。

我平时从来不看别的网站上的新闻，因为下面的评论惨不忍睹。

但知乎也出现了这样的人，怎么办？

于是这个插件出现了！

&nbsp;

### 知乎本身的缺陷

我很喜欢 V2EX 的屏蔽功能，因为只要屏蔽了一个人后，就不会看到任何和他相关的东西了，眼不见为净。但知乎不行，知乎屏蔽后只是对方无法再给你留言。

但是对方的回答、评论你还是会看到。

其实，自己写个插件来实现这个其实是非常简单的一件事情。

&nbsp;

#### 源代码

    (function () {
        'use strict';

        var main = function () {
            var blockedUserLinks = [];
            var blockedUserNames = [];

            var blockUser = function () {
                $.each(blockedUserLinks, function (index, item) {
                    var links = [item, "http://www.zhihu.com" + item, "http://www.zhihu.com" + item];
                    $.each(links, function (index, link) {
                        $('div.zm-item-answer:has(a.author-link[href="' + link + '"])').remove();
                    });
                });

                $.each(blockedUserNames, function (index, item) {
                    $('div.comment-app-holder div[aria-label="' + item + "的评论" + '"]').remove();
                });

            };

            // load blocked user
            $.get("/settings/filter").done(function (html) {
                var page = $(html);
                $.each(page.find('.blocked-users a.avatar-link'), function (index, item) {
                    blockedUserLinks.push($(item).attr("href"));
                });

                $.each(page.find('.blocked-users div.body a'), function (index, item) {
                    blockedUserNames.push($(item).text());
                });

                blockUser();
            });


            $(document).ajaxComplete(function (event, request, settings) {
                blockUser();
            });
        };

        var injectedScript = document.createElement('script');
        injectedScript.type = 'text/javascript';
        injectedScript.text = '(' + main + ')("");';
        (document.body || document.head).appendChild(injectedScript);
    })();

这里主要就是自动读取你屏蔽的用户清单，然后在页面上找到这些用户的回答、评论即可。

&nbsp;

#### 两个关键点

第一个难点是知乎会有很多 ajax 请求，所以脚本不能只在页面加载完成后执行，还需要在没次 ajax 请求后执行。知乎用的是 jQyery，直接用`$(document).ajaxComplete`就可以了。

接下来一个难点是，Chrome 插件的 Javascript 默认是和页面隔离的，坐上面的操作。网上找到的解决方案也很简单，把 Javascript 代码插入原页面，这样就可以执行了。

&nbsp;

### 下载地址

最后是下载地址：

Chrome Web Store: [https://chrome.google.com/webstore/detail/知乎用户屏蔽插件/ahdjhhjbjfhoohjgaddgpbhkccbfmbpn](https://chrome.google.com/webstore/detail/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E5%B1%8F%E8%94%BD%E6%8F%92%E4%BB%B6/ahdjhhjbjfhoohjgaddgpbhkccbfmbpn)

Github: [https://github.com/dozer47528/zhihu-block-chrome-extension](https://github.com/dozer47528/zhihu-block-chrome-extension)

好用的话就打赏一下呗！为了上传这个插件，我也是花了5刀的。
