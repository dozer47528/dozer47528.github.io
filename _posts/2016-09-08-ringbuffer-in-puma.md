---
title: RingBuffer 在 Puma 中的应用
author: Dozer
layout: post
permalink: /2016/09/ringbuffer-in-puma.html
categories:
  - 编程技术
tags:
  - RingBuffer
  - 设计模式
  - Puma
---

### 什么是 RingBuffer

环形缓冲区：[https://zh.wikipedia.org/wiki/環形緩衝區](https://zh.wikipedia.org/wiki/%E7%92%B0%E5%BD%A2%E7%B7%A9%E8%A1%9D%E5%8D%80)

维基百科的解释是：它是一种用于表示一个固定尺寸、头尾相连的缓冲区的数据结构，适合缓存数据流。

底层数据结构非常简单，一个固定长度的数组加一个写指针和一个读指针。

![RingBuffer](/uploads/2016/09/ringbuffer.png)

只要像这张图一样，把这个数组辦弯，它就成了一个 RingBuffer。

那它到底有什么精妙的地方呢？

我最近做的项目正好要用到类似的设计思路，所以翻出了以前在点评写的 [Puma](https://github.com/dianping/puma) 系统，看了看以前自己写的代码。顺便写个文章总结一下。

<!--more-->

&nbsp;

### Puma 是什么，为什么要用 RingBuffer

#### Puma 简介

[Puma](https://github.com/dianping/puma) 是一个 MySQL 数据库 Binlog 订阅消费系统。类似于阿里的 [Canel](https://github.com/alibaba/canal)。

Puma 会伪装成一个 MySQL Slave，然后消费 Binlog 数据，并缓存在本地。当有客户端连接上来的时候，就会从本地读取数据给客户端消费。

如果用很一般的设计，一个单独的线程会从 MySQL 消费数据，存到本地文件中。然后每个客户端的连接都会有一个线程，从本地文件中读取数据。

没错，第一版就是这么简单粗暴，当然，它是有效的。

&nbsp;

#### 利用缓存优化性能

不用做性能测试就知道，系统压力大了以后这里必定会是一个瓶颈。读写数据会有一点延时，如果多个客户端同时读取同一份数据又会造成很多的浪费。然后数据的编码解码还会有不少损耗。

所以这里当然要加一个缓存了。

一个线程写数据到磁盘，然后它可以同时把数据传递给各个客户端。

听起来像发布者订阅者模式？也有点像生产者消费者模式？

但是，它并不仅仅是发布者订阅者模式，因为这里的“发布者”和“订阅者”是完全异步的，而且每个“订阅者”的消费速度是不一样的。

它也不仅仅是生产者消费者模式，因为这里的“消费者”是同时消费所有数据，而不是把数据分发给各个“消费者”。

它们的消费速度不一样，还会出现缓存内的数据过新，“消费者”不得不去磁盘读取。

感觉这里的需求是两种设计模式的结合。

不仅如此，这是一套高并发的系统，怎么保证性能，怎么保证数据一致性？

所以，这个缓存看上去简单，其实它不简单。

&nbsp;

#### 常规解决思路

目标明确后，看看 Java 的并发集合中有什么能满足需求的吧。

第一个想到的就是`BlockingQueue`，为每一个客户端创建一个`BlockingQueue`，`BlockingQueue`内部是通过加锁来实现的，虽然锁冲突不会很多，但高并发的情况下，最好还是能做到无锁。

&nbsp;

#### Disruptor

当时正好看到了一系列介绍 Disruptor 的文章：[传送门](http://ifeve.com/disruptor/)

所以就在想能不能把 RingBuffer 用来解决我们的问题呢？

&nbsp;

### 对 RingBuffer 进行改进

看完了 RingBuffer 的基本原理后，就要开始用它来适应我们的系统了。这里遇到了几个问题：

1. 如何支持多个消费者
2. 如何判断当前有无新数据，如何判断当前数据是否已经被新数据覆盖
2. 如何保证数据一致性

&nbsp;

#### 第一个问题

这个问题简单，原始的 RingBuffer 只有一个写指针和一个读指针。

要支持多个消费者的话，只要为每个消费者创建一个读指针即可。

&nbsp;

#### 第二个问题

RingBuffer 的一个精髓就是，写指针和读指针的大小是会超过数组长度的，写入和读取数据的时候，是采用`writeIndex % CACHED_SIZE`这样的形式来读取的。

为什么要这么做？这就是为了解决判断有无新数据和数据是否已被覆盖的问题。

假设我内部2个指针，分别叫`nextWriteIndex`，`nextReadIndex`。

那么判断有无新数据的逻辑就是`if (nextReadIndex >= nextWriteIndex)`，返回`true`的话就是没有新数据了。

而判断数据是否被覆盖的逻辑就是`if (nextReadIndex < nextWriteIndex - CACHED_SIZE)`，返回`true`的话就是数据已经被覆盖了。

拿实际数据举个例子：

一个长度为10的 RingBuffer，内部是一个长度为10的数组。

此时`nextWriteIndex`=12，意味着它下一次写入的数据会在 12%10=2 上。此时，可读的有效范围是 2~11，对应的数组内的索引就是 2, 3, 4, 5, 6, 7, 8, 9, 0, 1。

所以，当`nextReadIndex`=12 的时候，会读到最老的数据2，这是老数据，不是新数据，此时表示没有行数据了。

当`nextReadIndex`＝1 的时候，是新数据，而不是想要的老数据，老数据已经被覆盖掉了，此时它没办法从缓存里读数据了。

&nbsp;

#### 第三个问题

最棘手的第三个问题来了，这个系统是要支持高并发的，如果是同步的操作，上面的代码没有任何问题。或者说，如果是同步的代码，干嘛还要用 RingBuffer 呢？

上面写入和读取，都有两步操作，更改数据和更改索引，按照逻辑上来讲，它们应该是强一致性的。只能加锁了？如果要加锁，为何不直接用`BlockingQueue`？

所以，是否可以通过什么方法，高并发和最终一致性呢？

&nbsp;

直接贴代码吧，根据代码一步步分析：

    public class CachedDataStorage {

        private static final int CACHED_SIZE = 5000;

        private final ChangedEventWithSequence[] data = new ChangedEventWithSequence[CACHED_SIZE];

        private volatile long nextWriteIndex = 0;

        public void append(Object dataValue) {
            data[(int) (nextWriteIndex % CACHED_SIZE)] = dataValue;
            nextWriteIndex++;
        }

        public Reader createReader() {
            return new Reader();
        }

        public class Reader {

            private Reader() {
            }

            private volatile long nextReadIndex = 0;

            public Object next() throws IOException {
                if (nextReadIndex >= nextWriteIndex) {
                    return null;
                }

                if (nextReadIndex <= nextWriteIndex - CACHED_SIZE) {
                    throw new IOException("data outdated");
                }

                Object dataValue = data[(int) (nextReadIndex % CACHED_SIZE)];

                if (nextReadIndex <= nextWriteIndex - CACHED_SIZE) {
                    throw new IOException("data outdated");
                } else {
                    nextReadIndex++;
                    return dataValue;
                }
            }
        }
    }

我们来一步步分析，先看内部的`Reader`和`createReader()`方法，每来一个客户端就会创建一个`Reader`，每个`Reader`会维护一个`nextReadIndex`。

然后看`append()`方法，可以说没有任何逻辑，直接写入数据，修改索引就结束了。但是，别小看了这两个步骤的操作顺序。

&nbsp;

好了，到了最复杂的`next()`方法了，这里可就大有讲究了。

一进来立刻执行`if (nextReadIndex >= nextWriteIndex)`，用来判断当前是否还有更新的数据。

因为写入的时候是先写数据再改索引，所以可能会出现明明有数据，但是这里认为没数据的情况。

但是并没有关系，我们更关注最终一致性，因为我们要的是确保这里一定不会读错数据，而不一定要确保这里有新数据就要立刻处理。就算这一轮没读到，下一轮也一定会读取到了。

&nbsp;

下一步是这一行`if (nextReadIndex <= nextWriteIndex - CACHED_SIZE)`，判断想要读取的数据有没有被新数据覆盖。等一下，这里为什么和上面介绍的不一样？

上面写的是`<`，而这里却是`<=`。上面提到，同步操作的情况下，用`<`是没有问题的，但是这里的异步的。

写入数据的时候，可能会出现数据已被覆盖，而索引未被更新的问题，所以这样子判断可以保证不会读错数据。

&nbsp;

既然上下边界都检查过了，那么就读取数据吧！就当这里准备读数据的时候，写数据的线程竟然又写入了好多数据，导致读出来的数据已经被覆盖了！

所以，一定要在读完数据后，再次检查数据是否被覆盖。

最终，整个过程实现了无锁，高并发和最终一致性。

在 Puma 系统中，启用缓存和关闭缓存，一写五读的情况下，性能整整提高了一倍。测试还是在我 SSD 上进行的，如果是传统硬盘，提升会更明显。

&nbsp;

### 高并发系统的设计思路

首先，这部分的代码可以在这里找到：[传送门](https://github.com/dianping/puma/tree/master/puma/src/main/java/com/dianping/puma/storage/cache)

完整的代码还包含了老数据被覆盖无数据可读时的数据源切换逻辑，还有当无消费者时关闭 RingBuffer 的逻辑。上面的代码已经被简化了很多，想看完整代码的话可以在上面的链接中看到。

&nbsp;

然后谈谈高并发系统的设计思路。

Java 并发编程的第一重境界是善用各种锁，尽量减少锁冲突，不能有死锁。

第二重境界就是善用 Java 的各种并发包，Java 的并发包里有的是无锁的，例如`AtomicLong`中用了`CAS`；有的是用了各种手段减少锁冲突，例如`ConcurrentHashMap`中就用了锁分段技术。整体效率都非常高，能熟练应用后也能写出很高效的程序。

再下一个境界就非常搞脑子了，往往是放弃了强一致性，而去追求最终一致性。其中会用到`AtomicLong`等无锁，或锁分段技术，并且常常会把它们结合起来用。就像上面那部分代码，看似简单，但实际上却要把各种边界条件思考地很全面，因为是最终一致性，所以中间的状态非常多。
