---
title: API Blueprint Docker
author: Dozer
layout: post
permalink: /2016/03/api-blueprint-docker.html
categories:
  - 编程技术
tags:
  - 团队
  - Docker
---

### API Blueprint

上次介绍的 [API Blueprint 解决方案](/2016/01/api-blueprint.html) 虽然不错，但是有一些问题：

1. 部署麻烦，需要装不少东西
2. 文档更新后不支持自动部署
3. 没有权限控制

以至于我们团队最后没有用这个方案，所以我想了下解决方案。

1. 通过 Docker 镜像，解决部署问题
2. 通过 Docker 镜像中的脚本，配合 Github Webhook 来实现自动化部署
3. 还未实现

正好顺便学习一下 Docker，Docker 的书看过几本了，之前同事也做过分享，但还是那句话：实践出真知。

之前虽然了解各种概念，但是自己捣鼓后，才算是真正的理解。

<!--more-->

&nbsp;

### 实现方案

#### Dockerfile

`Dockerfile` 非常简单，直接贴出来就行了：

    FROM centos

    RUN yum install -y epel-release && yum update -y && yum install -y node npm make nginx git
    RUN npm install -g aglio drakov

    COPY scripts/startup.sh /usr/local/bin/
    COPY scripts/deploy.sh /usr/local/bin/
    COPY scripts/webhook.js /usr/local/bin/

    RUN chmod -R 755 /usr/local/bin/*

    CMD /usr/local/bin/deploy.sh && /usr/local/bin/startup.sh


这里主要依赖了`nodejs`和`nginx`。

`aglio`只能把文档渲染成`html`，但是不包括 server，所以需要配合`nginx`。

而`drakov`自己会启动一个 server。

然后这里最关键的就是3个脚本了，继续详解一下这三个脚本。

&nbsp;

#### startup.sh

这里是启动脚本，看`Dockerfile`最后一行，定义了默认启动脚本。

    nginx
    nohup drakov -f "/opt/api-blueprint/*.apib" --public > /dev/null &
    node /usr/local/bin/webhook.js

三行命令对应3个服务。

&nbsp;

#### deploy.sh
这个脚本负责拉取新的文档，并调用`aglio`渲染成`html`，然后复制到`nginx`根目录。

    if [ -d /opt/api-blueprint ]
    then
            cd /opt/api-blueprint
            git checkout -f
            git clean -f
            git pull
    else
            git clone $repository /opt/api-blueprint
            cd /opt/api-blueprint
    fi

    find . -name "*.apib" | sed 's/.apib//' | xargs -i -t aglio -i {}.apib --theme-template triple -o {}.html
    rm -rf /usr/share/nginx/html/*
    cp -R * /usr/share/nginx/html/

&nbsp;

#### webhook.js
这个脚本负责监听 `webhook`，启动部署。

    var http = require('http');
    var exec = require('child_process').exec;

    var cmdStr = 'bash -c /usr/local/bin/deploy.sh';

    setInterval(function() {
      console.log("Start auto reload.")
      exec(cmdStr, function(err, stdout, stderr) {
        if (err) {
          console.error(err);
        } else {
          console.log("Update success!");
          console.log(stdout);
        }
      });
    }, 5 * 60 * 1000);

    http.createServer(function(req, res) {
      console.log("Start webhook reload.")
      exec(cmdStr, function(err, stdout, stderr) {
        if (err) {
          console.error(err);
        } else {
          console.log("Update success!");
          console.log(stdout);
        }
      });
      res.writeHead(200, {
        'Content-Type': 'text/plain'
      });
      res.end("");

    }).listen(8080);

收到请求就重新调用一下`deploy.sh`。

Github 上可以这么设置：

![webhook](/uploads/2016/03/webhook.png)

如果你在内网，不方便暴露到公网，可以忽略这个功能，脚本内部也是自动刷新，5分钟一次。

&nbsp;

### 如何使用？

这个项目已经放到了 Github 和 Docker Hub 上。

源代码：[https://github.com/dozer47528/api-blueprint-docker](https://github.com/dozer47528/api-blueprint-docker)

Docker 镜像：[https://hub.docker.com/r/dozer47528/api-blueprint-docker/](https://hub.docker.com/r/dozer47528/api-blueprint-docker/)

使用起来非常简单：

    docker run --name test \
    -e "repository=https://github.com/dozer47528/api-blueprint-test.git" \
    -p 80:80 -p 8080:8080 -p 3000:3000 \
    -d dozer47528/api-blueprint-docker

把其中的`repository`替换成你们自己的地址即可。

内部端口需要映射一下：

* 80: 文档
* 8080: webhook
* 3000: Mock 服务器

&nbsp;

#### 如何支持私有仓库？

首先在宿主机上配置完`ssh`，然后在启动的时候隐射一下文件`-v ~/.ssh:/root/.ssh`。

完整的命令类似于这样：

    docker run --name test \
    -v ~/.ssh:/root/.ssh \
    -e "repository=https://github.com/dozer47528/api-blueprint-test.git" \
    -p 80:80 -p 8080:8080 -p 3000:3000 \
    -d dozer47528/api-blueprint-docker

&nbsp;

#### 如何修改`aglio`的启动参数？

启动的时候加上这个参数：`-e "aglio=--theme-template triple"`

完整的命令类似于这样：

    docker run --name test \
    -e "aglio=--theme-template triple" \
    -e "repository=https://github.com/dozer47528/api-blueprint-test.git" \
    -p 80:80 -p 8080:8080 -p 3000:3000 \
    -d dozer47528/api-blueprint-docker

&nbsp;

### 文档怎么写？

自己的文档怎么写？首先，我这边只会转换`apib`结尾的文档，这是 API Blueprint 的标准后缀名。

然后你也可以在里面直接扔`html`文件。

所有文档文件夹随便放，我会递归所有文件。

最后建议放一个`index.html`，自己做一个导航，这样自己用起来方便一点。

我这边有一个例子：

[https://github.com/dozer47528/api-blueprint-test](https://github.com/dozer47528/api-blueprint-test)

&nbsp;

### 下一步是什么？

还有一些不完善的地方需要改进：

* 支持私有仓库，例如 Bitbucket（已完成）
* 支持自定义`aglio`样式，我现在在脚本里写死了一个我自己比较喜欢的样式，最好可以在`docker run`的时候把样式传进去（已完成）
* 有些服务部署在内网，不方便设置 webhook，要支持自动刷新数据（已完成）
