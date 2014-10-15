---
title: 利用 WeakReference 关闭守护线程
author: Dozer
layout: post
permalink: /2014/10/weakreference-exit-in-java/
categories:
  - 编程技术
tags:
  - java
  - 多线程
---

### 不要让 this 在构造期间逸出

《Java 并发编程实战》中有这么一段：

> 不要让`this`在构造期间逸出。

原因很简单，因为如果在构造期间创建了一个新线程并把`this`传递给新线程，`this`还没有准备完毕，新线程如果提前使用调用一些数据的话可能会有未知的错误。具体的错误和`JVM`的实现有关，可能大部分情况下没问题，但是一旦有了问题，你恐怕找都找不到。

参考：

+ [Don't publish the "this" reference during construction](http://www.ibm.com/developerworks/library/j-jtp0618/#2)
+ 《Java 并发编程实战》

<!--more-->

&nbsp;

### 守护线程

很多`class`需要守护线程，根据上面的提醒，守护线程不应该在构造函数中创建。

常见的做法就是使用`init`函数了，然后在内部记录一个变量，标记是否已经`init`。如果没有初始化就进行后续操作了，可以报错也可以自动帮它`init`一下。

配合`Spring`的话可以把`init`函数加到`init-method`中：

	<bean id="hello" class="cc.dozer.Hello" init-method="init" />

第一个坑来了！

如果你的`class`是一个单例那没有问题，如果你的`class`可能会被销毁并创建新的实例，那么这时候就有问题了！因为老的实例一直在被一个守护线程持有，所以 GC 的时候永远也不会被回收！

可能你会说加一个`close`方法就行了。恩，这是必须要加的，但是这还不够，如果是做框架，没办法用这个来约束用户的不良行为。`init`可以有办法启动调用，那如果用户忘记调用`close`了怎么办？

&nbsp;

### 弱引用

弱引用要登场了！守护线程不应该对被守护的实例有强依赖，如果被守护的线程被GC了，那么守护线程应该自己停下来。

那么这里就可以用到弱引用了：

	public class Hello {
		private Thread thread;
		
		private boolean inited;
	
		public void close() {
			if (this.thread != null) {
				thread.interrupt();
			}
		}
	
		public synchronized void init() {
			if(inited){
				return;
			}
			Monitor monitor = new Monitor(this);
			thread = new Thread(monitor);
			thread.setDaemon(true);
			thread.start();
			inited = true;
		}
	
		static class Monitor implements Runnable {
			private WeakReference<Hello> ref;
	
			public Monitor(Hello hello) {
				this.ref = new WeakReference<Hello>(hello);
			}
	
			private Hello getHello() throws WeakReferenceGCException {
				Hello weak = ref.get();
				if (weak == null) {
					throw new WeakReferenceGCException();
				}
				return weak;
			}
	
			@Override
			public void run() {
				while (!Thread.interrupted()) {
					try {
						Thread.sleep(100);
						Hello hello = getHello();
						//todo: ...
					} catch (WeakReferenceGCException e) {
						System.out.println("Hello has be GC");
						break;
					} catch (InterruptedException ignore) {
						break;
					}
				}
			}
		}
	}
	
	public class WeakReferenceGCException extends RuntimeException {}

妈妈再也不用担心用户忘记调用`close`方法了！这里创建了一个新的`RuntimeException`，在`getHello`的时候只要实例被 GC 就抛出这个异常，守护线程捕捉到后自己停止即可。

其实，不仅在这里，只要在逻辑上非强依赖的引用最好都改写成弱引用，防止内存溢出。