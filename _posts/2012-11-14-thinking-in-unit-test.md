---
title: 单元测试有感
author: Dozer
layout: post
permalink: /2012/11/thinking-in-unit-test/
categories:
  - 编程技术
tags:
  - Mock
  - 单元测试
---

### 你为什么不写单元测试？

前一段时间，部门有两位同事给大家进行了 Unit Test 的分享。

其中一位的主题是：<a href="http://zh.wikipedia.org/wiki/%E6%A8%A1%E6%8B%9F%E5%AF%B9%E8%B1%A1" target="_blank"><strong>Mock</strong></a> 技术

主要介绍了如何用 Mock 技术辅助单元测试。

另一位的主题是：单元测试之分割复杂业务逻辑

主要是以一个案例，介绍了复杂的业务逻辑应该怎么进行单元测试。

<!--more-->

听完两次分享后，我们团队正好在开展单元测试专项整治行动，我是负责人，所以当然要带带头啦。也顺便思考了很多问题。

1.  为什么要单元测试
2.  怎么有效地进行单元测试
3.  单元测试的技巧

&nbsp;

第一点就不用过多地阐述了，大家都知道做这件事有什么好处。但是大家为什么不做呢？

再仔细回顾一下，两位同事的关注点都在第三个问题上，第三个问题是一个平铺开来的问题，答案有许许多多，大部分人也知道很多点。

可是，你为什么还是不写单元测试？因为你没有把最本质的问题搞清楚。那就是“**怎么有效地进行单元测试”**。

&nbsp;

如果不搞清楚第二点，你就好象处于这样一种状态：

知道减肥的好处，知道运动可以减肥。但是你为什么执行了却没效果？

因为你不知道减肥的核心是消耗脂肪，你不知道运动还分有氧运动和无氧运动，你不知道如果一直进行无氧运动你不仅不会减肥，反而会满身肌肉。如果你是一个女生，你岂不是悲剧了…？

所以很多人知道把复杂函数分割成小函数有助于简化测试，但是他并不明白如何分割，因为他不知道测试的核心目的是什么。所以最后导致不仅没有提高测试效率，反而让自己的代码变得乱七八糟。

&nbsp;

### 思考

有了上面三个问题，也就有了我下面的思考：

&nbsp;

#### 为什么要单元测试？

答案有很多，大部分都是围绕着：确保功能正确、提升质量等几个方面的。

第一个问题有了答案，那就有了第二个问题：

&nbsp;

#### 如何确保功能正确、提升质量？

有一次我写了一个作业（控制台应用程序），<a href="http://zh.wikipedia.org/wiki/Scrum" target="_blank"><strong>Scrum Master</strong></a> 要求我写单元测试，我心中的第一反应是：这个让我怎么写啊？这不就是一个简单的作业吗？跑一下不就知道正不正确了吗？

于是我写了一个单元测试：把这个项目的 Main 函数调用了一下… Over 了…

后来它经常出错…

为什么我测试了，但是没有确保它功能的正确性？没有提升它的质量？简单的来说就是：测了等于白测…

好了，下一个问题又引出来了：

&nbsp;

#### 为什么有时候测了等于白测？

这个问题很简单，为什么测了等于白测？因为我的程序是读取数据库数据的，内部还有很多分支。而我每次 Run 的时候一般只会跑其中一条分支。而具体跑哪条分支和数据库里的数据有关。

所以，为什么我测了等于白测？为什么它不是一个有效的测试？

因为我没有测试到所有情况（有时候也不一定要所有，起码要覆盖到重要的、大部分的情况）。

因此想要让测试更有效的话，你往往需要覆盖到所有情况：

&nbsp;

#### 如何覆盖到所有的情况？

这里又来一个案例了，这个案例就是同事分享中的案例：一个复杂的函数，包含许多分支，怎么覆盖到所有情况？

考虑如下情况：

    public class TestClass
        {
            public int Method1(int a, bool b)
            {
                int result = 0;
                if (b)
                {
                    if (a &gt; 10)
                    {
                        result = 2;
                    }
                    else if (a &gt; 5)
                    {
                        result = 3;
                    }
                }
                else
                {
                    if (a &lt; 3)
                    {
                        result = 4;
                    }
                    else if (a &lt; 4)
                    {
                        result = 5;
                    }
                }
                return result;
            }
        }

你说这个怎么测？

有N个分支，会根据 a 和 b 的值跑不同的分支。你是不是想要把所有的可能性全部测一遍？

b:true    a:11

b:true    a:7

b:true    a:4

b:false    a:1

…

你这是在复习数学里的排列组合吗？

如果你不想这么写，那么请考虑如下写法：

    public class TestClass
        {
            public int Method1(int a, bool b)
            {
                int result = 0;
                if (b)
                {
                    result = Method2(a, result);
                }
                else
                {
                    result = Method3(a, result);
                }
                return result;
            }

            private int Method3(int a, int result)
            {
                if (a &lt; 3)
                {
                    result = 4;
                }
                else if (a &lt; 4)
                {
                    result = 5;
                }
                return result;
            }

            private int Method2(int a, int result)
            {
                if (a &gt; 10)
                {
                    result = 2;
                }
                else if (a &gt; 5)
                {
                    result = 3;
                }
                return result;
            }
        }

先想一下这个命题是否正确：如果一个函数中每块功能是正确的，那么它整体也是正确的。

如果这个命题没错，那么如果把一个函数中的模块拆分后，变成三个函数，如果三个函数的功能都是正确的，那么它整体也是正确的。

好了，再回归主题：如何覆盖到所有的情况？

上面的第二种写法，<span style="background-color: #eeeeee;">Method2</span> 和 <span style="background-color: #eeeeee;">Method3</span> 已经非常好测了，大家都会写。

那 <span style="background-color: #eeeeee;">Method1</span> 怎么测呢？如果 <span style="background-color: #eeeeee;">Method2</span> 和 <span style="background-color: #eeeeee;">Method3</span> 已经正确了，那我应该只测 <span style="background-color: #eeeeee;">Method1</span> 中的逻辑代码就行了。

那我怎么能去掉变量 <span style="background-color: #eeeeee;">a</span> 对 <span style="background-color: #eeeeee;">Method1</span> 的影响呢？因为 <span style="background-color: #eeeeee;">Method1</span> 中的逻辑只关心变量 <span style="background-color: #eeeeee;">b</span> 的值。

有经验的同学肯定想到解决方案了：

    public class TestClassMock : TestClass
        {
            protected override int Method2(int a, int result)
            {
                return 1;
            }
            protected override int Method3(int a, int result)
            {
                return 2;
            }
        }

Mock 一个 <span style="background-color: #eeeeee;">TestClass</span> ，并把它的两个方法覆盖掉（记得把原来的两个方法加上 <span style="background-color: #eeeeee;">virtual</span> 关键字）。

*这里的方案其实并不好，如果你是面向接口的编程的话，想要覆盖、替代一些方法会非常简单。*

我把这两个函数的结果写死了，我就可以安心的测 <span style="background-color: #eeeeee;">Method1</span> 了！

当它们三个函数都测试通过了，那么它们整体也不会有问题了。

&nbsp;

#### 各种测试技巧到底是为了什么？

上面的案例中，我提到到了分割复杂函数、面向接口的编程、Mock。

那我为什么要用这些？

因为我想要让我的测试能覆盖到各种情况、能变得更有效。

那这些技巧都在做什么事情？

让我可以解耦，能够有针对性地测试一块代码。

所以，第二个问题“怎么有效地进行单元测试”好像有一点眉目了。

&nbsp;

### 怎么有效地进行单元测试？

前面的思考过程中，至上而下又自下而上，最终回归到我们要解决的问题上。

经过这番思考后，我有了一个答案：**针对单一职责，进行有针对性的测试。**

&nbsp;

首先如果是多层架构，单元测试不应该跨越多层，因为每一层都有自己的职责！千万别在一个单元测试里测试多个职责。

例如业务逻辑层调用了数据库访问层，先取出数据然后再进行简单处理？你是不是觉得在业务逻辑层写一个测试就够了？

可是它们各自有各自的职责，如果剥离后再进行测试，就会非常简单了。

这里往往会用到面向接口的编程和 Mock 技术。

&nbsp;

如果一个函数有很复杂的逻辑，对它写一个单元测试的话，其实也违背了上面的原则了。因为它并不是单一职责。

它一会儿要做这个，一会儿要做那么。所以需要理清思路，把这个复杂的函数分割成几个有单一职责的小函数。

这里主要考验对业务的理解和一些编码技巧了。

顺便附上之前写的一篇文章：<a title="短函数的优点" href="/2012/01/the-advantages-of-short-function/" target="_blank"><strong>《短函数的优点》</strong></a>

&nbsp;

### 后续工作

最后，我想这应该是测试的核心目标了吧？各种测试技巧不都是围绕这个目标进行的吗？

现在终于明白减肥的核心目标是什么了，下面各种行动就可以围绕这个核心开展了。

记住，不要以为运动了就可以减肥！不要以为分割了函数就方便测试了！
