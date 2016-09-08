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

环形缓冲区：[https://zh.wikipedia.org/wiki/%E7%92%B0%E5%BD%A2%E7%B7%A9%E8%A1%9D%E5%8D%80](https://zh.wikipedia.org/wiki/%E7%92%B0%E5%BD%A2%E7%B7%A9%E8%A1%9D%E5%8D%80)

维基百科的解释是：它是一种用于表示一个固定尺寸、头尾相连的缓冲区的数据结构，适合缓存数据流。

底层数据结构非常简单，一个固定长度的数组加一个写指针和一个读指针。

![RingBuffer](/uploads/2016/09/ringbuffer.png)

只要像这张图一样，把这个数组辦弯，它就成了一个 RingBuffer。



<!--more-->
