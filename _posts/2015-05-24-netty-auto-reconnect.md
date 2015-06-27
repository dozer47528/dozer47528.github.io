---
title: Netty 自动重连
author: Dozer
layout: post
permalink: /2015/05/netty-auto-reconnect.html
categories:
  - 编程技术
tags:
  - Netty
---

### 自动重连

用 Netty 写 Client 和 Server 的时候必须要去处理自动重连。

Server 端启动时的错误，要去不断重试。

Client 端不仅要处理启动时的错误，还要处理中途断开连接。

<!--more-->

&nbsp;

### Server 端的处理

和常规的代码相比，Server 端只要处理一个地方即可：

    public final class TcpServer {
   
        private volatile EventLoopGroup bossGroup;
    
        private volatile EventLoopGroup workerGroup;
    
        private volatile ServerBootstrap bootstrap;
    
        private volatile boolean closed = false;
    
        private final int localPort;
    
        public TcpServer(int localPort) {
            this.localPort = localPort;
        }
    
        public void close() {
            closed = true;
    
            bossGroup.shutdownGracefully();
            workerGroup.shutdownGracefully();
    
            System.out.println("Stopped Tcp Server: " + localPort);
        }
    
        public void init() {
            closed = false;
    
            bossGroup = new NioEventLoopGroup();
            workerGroup = new NioEventLoopGroup();
            bootstrap = new ServerBootstrap();
            bootstrap.group(bossGroup, workerGroup);
    
            bootstrap.channel(NioServerSocketChannel.class);
    
            bootstrap.childHandler(new ChannelInitializer<SocketChannel>() {
                @Override
                protected void initChannel(SocketChannel ch) throws Exception {
                    //todo: add more handler
                }
            });
    
            doBind();
        }
    
        protected void doBind() {
            if (closed) {
                return;
            }
    
            bootstrap.bind(localPort).addListener(new ChannelFutureListener() {
                @Override
                public void operationComplete(ChannelFuture f) throws Exception {
                    if (f.isSuccess()) {
                        System.out.println("Started Tcp Server: " + localPort);
                    } else {
                        System.out.println("Started Tcp Server Failed: " + localPort);
    
                        f.channel().eventLoop().schedule(() -> doBind(), 1, TimeUnit.SECONDS);
                    }
                }
            });
        }
    }
    
我们把整个初始化分成了两个部分，第一部分是初始化相关 class，第二部分做真正的监听端口。

这里最特殊的地方就是在调用`bind`方法后，添加一个`listener`检查是否成功，如果失败的话，需要调用`.channel().eventLoop().schedule()`方法，创建一个任务，我这代码设置的是1秒后尝试重新连接。

另外考虑到 server 可以被人为关闭，所以还需要检查当前时候已经关闭。如果不检查的话，你的 server 可能就永远也关不掉了。

&nbsp;

### Client 端的处理

client 端启动流程差不多，但是需要加一个 handler 来处理连接断开。

    public class TcpClient {
    
        private volatile EventLoopGroup workerGroup;
    
        private volatile Bootstrap bootstrap;
    
        private volatile boolean closed = false;
    
        private final String remoteHost;
    
        private final int remotePort;
    
        public TcpClient(String remoteHost, int remotePort) {
            this.remoteHost = remoteHost;
            this.remotePort = remotePort;
        }
    
        public void close() {
            closed = true;
            workerGroup.shutdownGracefully();
            System.out.println("Stopped Tcp Client: " + getServerInfo());
        }
    
        public void init() {
            closed = false;
    
            workerGroup = new NioEventLoopGroup();
            bootstrap = new Bootstrap();
            bootstrap.group(workerGroup);
            bootstrap.channel(NioSocketChannel.class);
    
            bootstrap.handler(new ChannelInitializer<SocketChannel>() {
                @Override
                public void initChannel(SocketChannel ch) throws Exception {
                    ChannelPipeline pipeline = ch.pipeline();
                    pipeline.addFirst(new ChannelInboundHandlerAdapter() {
                        @Override
                        public void channelInactive(ChannelHandlerContext ctx) throws Exception {
                            super.channelInactive(ctx);
                            ctx.channel().eventLoop().schedule(() -> doConnect(), 1, TimeUnit.SECONDS);
                        }
                    });
    
                    //todo: add more handler
                }
            });
    
            doConnect();
        }
    
        private void doConnect() {
            if (closed) {
                return;
            }
    
            ChannelFuture future = bootstrap.connect(new InetSocketAddress(remoteHost, remotePort));
    
            future.addListener(new ChannelFutureListener() {
                public void operationComplete(ChannelFuture f) throws Exception {
                    if (f.isSuccess()) {
                        System.out.println("Started Tcp Client: " + getServerInfo());
                    } else {
                        System.out.println("Started Tcp Client Failed: " + getServerInfo());
                        f.channel().eventLoop().schedule(() -> doConnect(), 1, TimeUnit.SECONDS);
                    }
                }
            });
        }
    
        private String getServerInfo() {
            return String.format("RemoteHost=%s RemotePort=%d",
                    remotePort,
                    remotePort);
        }
    }
    
可以看到，我们在`channelInactive`事件中，也创建了一个任务，在1秒后重新连接。

&nbsp;

### 示例代码

大家可以自己跑跑看：

[https://github.com/dozer47528/AutoReconnectNettyExample](https://github.com/dozer47528/AutoReconnectNettyExample)