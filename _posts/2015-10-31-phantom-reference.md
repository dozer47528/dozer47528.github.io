---
title: 利用 PhantomReference 替代 finalize
author: Dozer
layout: post
permalink: /2015/10/phantom-reference.html
categories:
  - 编程技术
tags:
  - Java
---

### 问题来源

之前的一篇文章讲了 [利用 WeakReference 关闭守护线程](/2014/10/weakreference-exit-in-java.html) ，守护线程一旦发现守护的对象不在了，就把自己清理掉。

这次的问题更棘手一些，假如一个对象有一些资源需要被关闭，那怎么处理？

很多人会说，这个简单啊！用 Java 的`finalize`！

但在 Java 中的`finalize`真的设计得不好，一不小心就会引发很多问题。

<!--more-->

&nbsp;

### Java 中的`finalize`有哪些问题？

1. 影响 GC 性能，可能会引发`OutOfMemoryException`
2. `finalize`方法中对异常处理不当会影响 GC
3. 子类中未调用`super.finalize`会导致父类的`finalize`得不到执行

总结一下就是：实现`finalize`对代码的质量要求非常高，一旦使用不当，就容易引发各种问题。

&nbsp;

### PhantomReference

Java 中的各种引用的区别就不说了，网上一搜一大堆。
直接上代码吧。

假设我有这样一个类，内部有一个`InputStream`并且需要自动`close`掉它。你只需要这么用就行了：

	public class CleanUpExample {
	    private InputStream input;
	
	    public CleanUpExample() {
	        //todo:init input
	        CleanUpHelper.register(this, new CleanUpImpl(input));
	    }
	
	    static class CleanUpImpl implements CleanUp {
	        private final InputStream input;
	
	        public CleanUpImpl(InputStream input) {
	            this.input = input;
	        }
	
	        @Override
	        public void cleanUp() {
	            try {
	                if (input != null) {
	                    input.close();
	                }
	            } catch (IOException e) {
	                e.printStackTrace();
	            }
	
	            System.out.println("Success!");
	        }
	    }
	}

看完了业务代码就来看看底层实现吧，先看一下最简单的`CleanUp`接口：

	public interface CleanUp {
	    void cleanUp();
	}

然后看一下略复杂的`CleanUpHelper`

	public final class CleanUpHelper {
	
	    private CleanUpHelper(){}
	
	    private static volatile boolean started = false;
	
	    private static final int SLEEP_TIME = 10;
	
	    private static final Thread CLEAN_UP_THREAD = new Thread(new Runnable() {
	        @Override
	        public void run() {
	            while (!Thread.currentThread().isInterrupted()) {
	                try {
	                    Reference target = REFERENCE_QUEUE.poll();
	                    if (target != null) {
	                        CleanUp cleanUp = MAPS.remove(target);
	                        if (cleanUp != null) {
	                            cleanUp.cleanUp();
	                            continue;
	                        }
	                    }
	                } catch (RuntimeException ignore) {
	                    //add logs
	                }
	
	                try {
	                    Thread.sleep(SLEEP_TIME);
	                } catch (InterruptedException e) {
	                    Thread.currentThread().interrupt();
	                }
	            }
	        }
	    });
	
	    private static final Map<Reference<Object>, CleanUp> MAPS = new ConcurrentHashMap<Reference<Object>, CleanUp>();
	
	    private static final ReferenceQueue<Object> REFERENCE_QUEUE = new ReferenceQueue<Object>();
	
	    public static void register(Object watcher, CleanUp cleanUp) {
	        init();
	        MAPS.put(new PhantomReference<Object>(watcher, REFERENCE_QUEUE), cleanUp);
	    }
	
	    private static void init() {
	        if (!started) {
	            synchronized (CleanUpHelper.class) {
	                if (!started) {
	                    CLEAN_UP_THREAD.setName("CleanUpThread");
	                    CLEAN_UP_THREAD.setDaemon(true);
	                    CLEAN_UP_THREAD.start();
	                    started = true;
	                }
	            }
	        }
	    }
	}

最后跑一下测试代码，看看是否能被清理掉：

	CleanUpExample item = new CleanUpExample();
	item = null;
	System.gc();
	Thread.sleep(2000);

&nbsp;

### 使用过程中的一个坑
`CleanUpExample` 在使用过程中只要实现一下`CleanUp`接口并且注册一下即可。

看似简单但这里有一个大坑，创建内部类的时候，一定要用静态内部类，而不要使用匿名内部类、成员内部类和局部内部类。

因为只有静态内部类才不会依赖外围类，其它的内部类在编译完成后会隐含地保存着一个引用，该引用是指向创建它的外围内。

这样你的代码又把`CleanUpImpl`注册到了`CleanUpHelper`中，最终导致`CleanUpExample`无法被 GC。

来一个错误的例子：

	public class CleanUpExample {
	    private InputStream input;
	
	    public CleanUpExample() {
	        //todo:init input
	        
	        CleanUpHelper.register(this, new CleanUp() {
	            @Override
	            public void cleanUp() {
	                try {
	                    if (input != null) {
	                        input.close();
	                    }
	                } catch (IOException e) {
	                    e.printStackTrace();
	                }
	
	                System.out.println("Success!");
	            }
	        });
	    }
	}

我第一次用自己写的`CleanUpHelper`就是这么写的，匿名内部类多简洁啊，但是，这样写后就无法生效了，一定要注意！

&nbsp;

### 为什么不用`close`方法来解决。

之前提到的守护进程和这次的资源清理，其实只要加一个`close`方法，在销毁的时候调一下就行了。

但是我们现在做的都是给全公司用的 Java 中间件。用户是不爱看文档的，我以前用别人的中间件也不看；用户也很少回去完整地在`finally`中去调用`close`方法。我自己也不喜欢，懒癌发作。