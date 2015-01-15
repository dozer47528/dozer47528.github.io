---
title: Java 中的 URL编码
author: Dozer
layout: post
permalink: /2014/03/url-encoding-in-java/
categories:
  - 编程技术
tags:
  - java
---

### URL编码

概念就不啰嗦了，直接上维基百科：<a href="http://zh.wikipedia.org/wiki/%E7%99%BE%E5%88%86%E5%8F%B7%E7%BC%96%E7%A0%81" target="_blank"><strong>传送门</strong></a>

简单的来说，当你提交 POST 请求，并且 RequestBody 的类型是 application/x-www-form-urlencoded 时，就需要用URL编码了。

而这个工作一般不需要你手动做，常见的Web框架都帮你处理好了。

<!--more-->

&nbsp;

### encodeURI 和 encodeURIComponent

JavaScript 中常常会见到这两个函数，发 POST 请求的时候，同样也是不需要你做任何事情的，但是如果是 GET 请求的话，就会需要用到这两个函数了。

那它们具体有什么区别？怎么用呢？

这里有一篇文章就讲的非常好：<a href="http://stackoverflow.com/questions/75980/best-practice-escape-or-encodeuri-encodeuricomponent" target="_blank">http://stackoverflow.com/questions/75980/best-practice-escape-or-encodeuri-encodeuricomponent</a>

总结一下就是：

如果你的URL是这样的：

那你的处理方式就应该是这样的：

`encodeURI('http://www.test.com/?.html') + '?' + encodeURIComponent('q') + '=' + encodeURIComponent('select count(*) from user where date>='2014')`

&nbsp;

当然这是最完整的写法，如果有些地方你自己知道没有特殊字幕，那么就没必要写那么复杂了。

那 encodeURI 和 encodeURIComponent 跟 URL编码比有什么区别呢？

主要区别就是它少编了一些符号，因为完整的URI，前半部分的 URL 和后半部分的 QueryString 中的特殊字符是不一样的，所以处理起来也不一样。

MDN文档：

<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURI" target="_blank">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURI</a>

<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent" target="_blank">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/encodeURIComponent</a>

&nbsp;

### Java 中遇到的问题

如果你的 Java 程序作为服务端，不管客户端用了哪种编码方式，你只要一个方法就搞定了。

那就是`URLDecoder.decode`。

&nbsp;

但是当把 Java 作为客户端去调其他地址的时候就出问题了！

我这里有一个需求：

用 Spring 的 RestTemplate 去掉一个 RestFul 接口，URL 是这样的：`http://www.test.com/?q=select count(*) from user where date >= 2014`。

和明显我不能直接把这个 URL 传给 RestTemplate ，所以我先用`URLEncoder.encode`对后面那串 SQL 进行了编码，然后再传给了 RestTemplate。

&nbsp;

第一个问题来了，理论上这里是对 QueryString 进行编码，所以需要用 encodeURIComponent，但是 Java 中竟然没有。。。

还好在网上找到了实现方法：

    public static String encodeURIComponent(String s)
    {
        String result = null;

        try
        {
            result = URLEncoder.encode(s, "utf-8")
                    .replaceAll("\\+", "%20")
                    .replaceAll("\\%21", "!")
                    .replaceAll("\\%27", "'")
                    .replaceAll("\\%28", "(")
                    .replaceAll("\\%29", ")")
                    .replaceAll("\\%7E", "~");
        }

        // This exception should never occur.
        catch (UnsupportedEncodingException e)
        {
            result = s;
        }

        return result;
    }

&nbsp;

第一个问题解决后，第二个问题来了：

`RestTemplate`对我的 URL 又进行了一个`URLEncoder.encode` ，可我的 URL 是已经编码过的，再编码一次明显就出错了。

这个问题纠结了好久，后来发现可以这么解决：

先创建一个`URI` 对象，然后不要传`String`类型的 URL，而是传一个对象，这样`RestTemplate`就不会对此一举了。

&nbsp;

至此，问题解决。但是，复杂参数还是尽量不要放在 QueryString 里，不然坑很多…

&nbsp;
