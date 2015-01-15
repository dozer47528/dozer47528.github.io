---
title: Java 中拦截 System.exit
author: Dozer
layout: post
permalink: /2013/04/intercept-system-exit-in-java/
categories:
  - 编程技术
tags:
  - java
---

### 场景

有一个 jar 包，但是这个 jar 包是一个控制台应用程序，所以我想直接调用它的 main 函数来执行。

但是遇到一个很纠结的问题，这个 jar 包因为是一个控制台应用程序，所以遇到错误的时候，会直接执行 System.exit(-1)，我的程序用它的时候就会直接被退出了…

但我更希望它可以抛出异常。

<!--more-->

### 解决方案

解决方案其实很简单，通过了一种其他用途的手段实现了这个功能。

直接上代码，先创建一个类：

    public class MySecurityManager extends SecurityManager {
        @Override
        public void checkPermission(Permission perm) {
        }

        @Override
        public void checkPermission(Permission perm, Object context) {
        }

        @Override
        public void checkCreateClassLoader() {
        }

        @Override
        public void checkAccess(Thread t) {
        }

        @Override
        public void checkAccess(ThreadGroup g) {
        }

        @Override
        public void checkExit(int status) {
            throw new SecurityException("not allow to call System.exit");
        }

        @Override
        public void checkExec(String cmd) {
        }

        @Override
        public void checkLink(String lib) {
        }

        @Override
        public void checkRead(FileDescriptor fd) {
        }

        @Override
        public void checkRead(String file) {
        }

        @Override
        public void checkRead(String file, Object context) {
        }

        @Override
        public void checkWrite(FileDescriptor fd) {
        }

        @Override
        public void checkWrite(String file) {
        }

        @Override
        public void checkDelete(String file) {
        }

        @Override
        public void checkConnect(String host, int port) {
        }

        @Override
        public void checkConnect(String host, int port, Object context) {
        }

        @Override
        public void checkListen(int port) {
        }

        @Override
        public void checkAccept(String host, int port) {
        }

        @Override
        public void checkMulticast(InetAddress maddr) {
        }

        @Override
        public void checkPropertiesAccess() {
        }

        @Override
        public void checkPropertyAccess(String key) {
        }

        @Override
        public boolean checkTopLevelWindow(Object window) {
            return super.checkTopLevelWindow(window);
        }

        @Override
        public void checkPrintJobAccess() {
        }

        @Override
        public void checkSystemClipboardAccess() {
        }

        @Override
        public void checkAwtEventQueueAccess() {
        }

        @Override
        public void checkPackageAccess(String pkg) {
        }

        @Override
        public void checkPackageDefinition(String pkg) {
        }

        @Override
        public void checkSetFactory() {
        }

        @Override
        public void checkMemberAccess(Class<?> clazz, int which) {
        }

        @Override
        public void checkSecurityAccess(String target) {
        }
    }

&nbsp;

然后在程序启动的时候执行：

`System.setSecurityManager(new MySecurityManager());`

&nbsp;

### 原理

原理其实很简单，这个类可以对你所有的重要操作进行权限验证。所以当你对 exit 方法进行权限验证的时候，直接抛出异常就行了。

但是为什么要重写其它方法呢？因为这个类默认会让所有的操作抛出异常，所以如果你不把其它的方法重写并保持无代码的话，其它的所有操作也无法进行了，例如：读写文件等。
