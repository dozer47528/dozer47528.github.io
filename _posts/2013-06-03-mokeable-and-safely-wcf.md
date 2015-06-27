---
title: WCF 调用的那些事
author: Dozer
layout: post
permalink: /2013/06/mokeable-and-safely-wcf.html
wpzoom_post_title:
  - Yes
wpzoom_post_readmore:
  - Yes
wpzoom_post_url:
  -
categories:
  - 编程技术
tags:
  - DotNet
  - Mock
  - WCF
---

### WCF 的问题和 using 语句块

WCF 这个问题已经纠结了很久了：

介绍：<a href="http://kb.cnblogs.com/page/88739/" target="_blank">http://kb.cnblogs.com/page/88739/</a>

各种解决方案：<a href="http://stackoverflow.com/questions/573872/what-is-the-best-workaround-for-the-wcf-client-using-block-issue" target="_blank">http://stackoverflow.com/questions/573872/what-is-the-best-workaround-for-the-wcf-client-using-block-issue</a>

<!--more-->

&nbsp;

### WCF 与 Mock

WCF 太让人纠结了！不仅用 using 会有问题， Mock 这方面设计的也很糟糕！

假设忽略 using 的问题（大部分情况下用 using 不会有什么问题），

如果想要 Mock 就需要掉接口了，用一个接口来引用对象。但是 WCF 的接口没有记承 IDispose …

我也不知道它是怎么设计的，总之很蛋疼。

&nbsp;

### 改良版

网上的改进方案很多，但是只针对 using 进行了改善，另外需求可能也和我有所不同，所以自己弄了一种实现方案：

    public static class Wcf
    {
        public static void Use<T>(T proxy, Action<T> codeBlock)
        where T : class
        {
            try
            {
                codeBlock(proxy);

                if (proxy is ClientBase<T>)
                {
                    (proxy as ClientBase<T>).Close();
                }
            }
            catch
            {
                if (proxy is ClientBase<T>)
                {
                    (proxy as ClientBase<T>).Abort();
                }
                throw;
            }
        }
    }

&nbsp;

具体用法：

    protected void Test()
    {
        Wcf.Use(GetClient(), client =>
            {
                client.Call();
            });
    }

    protected virtual ICient GetClient()
    {
        return new Client();
    }

&nbsp;

代码中我没有进行泛型约束，因为 WCF 的接口不继承于任何接口，那么还约束什么呢？

然后我会检测具体实现类的类型，如果可以 Close，就调用。

如果你的类是 Mock 的，并没有 Close 方法，那么就直接忽略了。

所以，这个方案即可以解决 using 的问题，又可以实现 Mock~

&nbsp;

最后如果有不好的地方，大家可以拍砖，我觉得会有更好的方案。
