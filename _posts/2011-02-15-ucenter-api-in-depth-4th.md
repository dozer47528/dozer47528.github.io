---
title: 深入研究 UCenter API 之 网站搭建
author: Dozer
layout: post
permalink: /2011/02/ucenter-api-in-depth-4th.html
categories:
  - 编程技术
tags:
  - AspDotNet
  - Discuz
  - Ucenter
---

<div>
  <blockquote>
    <p>
      <strong>目录：</strong>
    </p>

    <ol>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-1st/" target="_blank"><strong>开篇</strong></a>
      </li>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-2nd/" target="_blank"><strong>通讯原理：UCenter API 与子站之间的通讯原理和单点登陆原理</strong></a>
      </li>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-3rd/" target="_blank"><strong>加密与解密：AuthCode详解 & AuthCode函数翻译过程中的注意点</strong></a>
      </li>
      <li>
        <strong><a href="/2011/02/ucenter-api-in-depth-4th/" target="_blank">网站搭建： 康盛旗下网站 & Asp.net 网站搭建</a></strong>
      </li>
      <li>
        <strong><a href="/2011/04/ucenter-api-in-depth-5th/" target="_blank">MVC 网站下的用法：在 MVC 下的使用方法</a></strong>
      </li>
      <li>
        <strong><a href="/2011/05/ucenter-api-for-net-on-codeplex/" target="_blank">下载地址：UCenter API For .Net 在 CodePlex 上发布啦！</a></strong>
      </li>
    </ol>
  </blockquote>
</div>

&nbsp;

### 康盛旗下产品的搭建

**1、UCenter**

这个当然是最基本的东西，安装起来也很简单，官方就有教程

<http://faq.comsenz.com/userguide/x/install.html>

[<img title="ucenter_success" alt="ucenter_success" src="/uploads/2011/01/ucenter_success.png" width="474" height="330" />][1]

安装完成后，因为还没有安装别的应用，所以应用数量是：0

<!--more-->

**2、Discuz**

如果仅仅是为了用 UCenter，那有点得不偿失了，一般都会配上论坛

这里采用的是 Discuz! 7.2

<http://faq.comsenz.com/userguide/discuz/install.html>

[<img title="connection" alt="connection" src="/uploads/2011/01/connection.png" width="547" height="266" />][2]

这里没有什么难度，网上有许多教程

&nbsp;

&nbsp;

### Asp.net 测试网站的搭建

**新建网站**

既然是 UCenter 和 Asp.net 通讯，那肯定要搭建一个 Asp.net 的网站了

为了 方便测试，我们最好把网站直接在 IIS 中调试

新建网站应用程序 — 打开属性页面

[<img title="ucentertest" alt="ucentertest" src="/uploads/2011/01/ucentertest-300x172.png" width="300" height="172" />][3]

这步非不要操作，但是可以模拟真实的场景，并且还可以在 IIS 里调试

&nbsp;

设置完后我们看一下 IIS 里的情况（我把 UCenter 和 Discuz 挂在 IIS 下了）

&nbsp;

**在 UCenter 下新建应用程序**

登录后点添加新应用

[<img title="add_app" alt="add_app" src="/uploads/2011/01/add_app-300x126.png" width="300" height="126" />][4]

&nbsp;

按照这张图配置一下

[<img title="apps_settings" alt="apps_settings" src="/uploads/2011/01/apps_settings-200x300.png" width="200" height="300" />][5]

这里就一个地方和配置 php 的网站不同，就是“应用接口文件名称”

当然你也可以用 .php 然后配置 IIS，但是这个多麻烦？用 ashx 是最方便的，在后面会有详解，到时候你就知道为什么了

&nbsp;

提交后复制一下配置信息，后面有用

[<img title="app_info" alt="app_info" src="/uploads/2011/01/app_info-300x208.png" width="300" height="208" />][6]

&nbsp;

**配置Asp.net网站**

接下来我们需要把配置文件写入 Asp.net 的网站的 Web.config 中

乍一看，这配置是 php 格式的！

但这里有一份完整的配置信息，只要替换对应的地方就行：

&nbsp;

    <!--客户端版本-->
    <add key="UC_CLIENT_VERSION" value="1.5.2"/>
    <!--发行时间-->
    <add key="UC_CLIENT_RELEASE" value="20101001"/>

    <!--API 开关（value类型：True False 默认值：True）-->
    <!--是否允许删除用户-->
    <add key="API_DELETEUSER" value="True"/>
    <!--是否允许重命名用户-->
    <add key="API_RENAMEUSER" value="True"/>
    <!--是否允许得到标签-->
    <add key="API_GETTAG" value="True"/>
    <!--是否允许同步登录-->
    <add key="API_SYNLOGIN" value="True"/>
    <!--是否允许同步登出-->
    <add key="API_SYNLOGOUT" value="True"/>
    <!--是否允许更改密码-->
    <add key="API_UPDATEPW" value="True"/>
    <!--是否允许更新关键字-->
    <add key="API_UPDATEBADWORDS" value="True"/>
    <!--是否允许更新域名解析缓存-->
    <add key="API_UPDATEHOSTS" value="True"/>
    <!--是否允许更新应用列表-->
    <add key="API_UPDATEAPPS" value="True"/>
    <!--是否允许更新客户端缓存-->
    <add key="API_UPDATECLIENT" value="True"/>
    <!--是否允许更新用户积分-->
    <add key="API_UPDATECREDIT" value="True"/>
    <!--是否允许向UCenter提供积分设置-->
    <add key="API_GETCREDITSETTINGS" value="True"/>
    <!--是否允许获取用户的某项积分-->
    <add key="API_GETCREDIT" value="True"/>
    <!--是否允许更新应用积分设置-->
    <add key="API_UPDATECREDITSETTINGS" value="True"/>
    <!--API 开关结束-->

    <!--返回值设置-->
    <!--返回成功（默认：1）-->
    <add key="API_RETURN_SUCCEED" value="1"/>
    <!--返回失败（默认：-1）-->
    <add key="API_RETURN_FAILED" value="-1"/>
    <!--返回禁用（默认：-2）-->
    <add key="API_RETURN_FORBIDDEN" value="-2"/>
    <!--返回值设置结束-->

    <!--[必填]通信密钥-->
    <add key="UC_KEY" value="FD144298AF7E4797A66ACC0C18C97EA3"/>
    <!--[必填]UCenter地址-->
    <add key="UC_API" value="http://localhost/ucenter"/>
    <!--[必填]默认编码-->
    <add key="UC_CHARSET" value="utf-8"/>
    <!--[非必填]UCenter IP-->
    <add key="UC_IP" value=""/>
    <!--[必填]应用ID-->
    <add key="UC_APPID" value="2"/>

其中，除了标记必填的，别的都可以不填，默认值就是这个

Asp.net 网站算是搭建成功了，但是现在还没有用到那个类库呢！

&nbsp;

&nbsp;

### 类库的使用方法

**类库概况**

[<img class="alignnone size-full wp-image-217" title="solution" alt="solution" src="/uploads/2011/02/solution.png" width="220" height="189" />][7]

&nbsp;

**类库分为以下几个部分**

1.  Api 用于提供给 UCenter 调用的结构
2.  Client 用于调用 UCenter 的接口
3.  Model 调用过程中的一些数据封装
4.  UcConfig 静态类，读取上面的配置文件信息
5.  UcUtility 一些常用函数
6.  App.config 配置文件示例

&nbsp;

&nbsp;

**调用 UCenter API**

这步非常简单，只要配置好前面的东西，然后简单地调用一个类就行了。

&nbsp;

    IUcClient client = new UcClient();
    var user = client.UserLogin("admin", "admin");//登陆
    if (user.Success)//判断是否登陆成功
    {
        client.PmSend(0, 0, "公告", "测试公告", user.Uid);//给该用户发送系统消息
    }

&nbsp;

那具体有哪些函数可以被调用呢？可以看一下IUcClient接口

&nbsp;

    using System.Collections.Generic;

    namespace DS.Web.UCenter.Client
    {
        ///<summary>
        /// UcApi客户端
        ///</summary>
        public interface IUcClient
        {
            /// <summary>
            /// 用户注册
            /// </summary>
            /// <param name="userName">用户名</param>
            /// <param name="passWord">密码</param>
            /// <param name="email">Email</param>
            /// <param name="questionId">登陆问题</param>
            /// <param name="answer">答案</param>
            /// <returns></returns>
            UcUserRegister UserRegister(string userName, string passWord, string email, int questionId = 0, string answer = "");

            /// <summary>
            /// 用户登陆
            /// </summary>
            /// <param name="userName">用户名/Uid/Email</param>
            /// <param name="passWord">密码</param>
            /// <param name="loginMethod">登录方式</param>
            /// <param name="checkques">需要登陆问题</param>
            /// <param name="questionId">问题ID</param>
            /// <param name="answer">答案</param>
            /// <returns></returns>
            UcUserLogin UserLogin(string userName, string passWord, LoginMethod loginMethod = LoginMethod.UserName, bool checkques = false, int questionId = 0, string answer = "");

            /// <summary>
            /// 得到用户信息
            /// </summary>
            /// <param name="userName">用户名</param>
            /// <returns></returns>
            UcUserInfo UserInfo(string userName);

            /// <summary>
            /// 得到用户信息
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            UcUserInfo UserInfo(int uid);

            /// <summary>
            /// 更新用户信息
            /// 更新资料需验证用户的原密码是否正确，除非指定 ignoreoldpw 为 1。
            /// 如果只修改 Email 不修改密码，可让 newpw 为空；
            /// 同理如果只修改密码不修改 Email，可让 email 为空。
            /// </summary>
            /// <returns></returns>
            UcUserEdit UserEdit(string userName, string oldPw, string newPw, string email, bool ignoreOldPw = false, int questionId = 0, string answer = "");

            /// <summary>
            /// 删除用户
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            bool UserDelete(params int[] uid);

            /// <summary>
            /// 删除用户头像
            /// </summary>
            /// <param name="uid">Uid</param>
            void UserDeleteAvatar(params int[] uid);

            /// <summary>
            /// 同步登陆
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns>同步登陆的 Html 代码</returns>
            string UserSynlogin(int uid);

            /// <summary>
            /// 同步登出
            /// </summary>
            /// <returns>同步登出的 Html 代码</returns>
            string UserSynLogout();

            /// <summary>
            /// 检查 Email 格式
            /// </summary>
            /// <param name="email">Email</param>
            /// <returns></returns>
            UcUserCheckEmail UserCheckEmail(string email);

            /// <summary>
            /// 增加受保护用户
            /// </summary>
            /// <param name="admin">操作管理员</param>
            /// <param name="userName">用户名</param>
            /// <returns></returns>
            bool UserAddProtected(string admin, params string[] userName);

            /// <summary>
            /// 删除受保护用户
            /// </summary>
            /// <param name="admin">操作管理员</param>
            /// <param name="userName">用户名</param>
            /// <returns></returns>
            bool UserDeleteProtected(string admin, params string[] userName);

            /// <summary>
            /// 得到受保护用户
            /// </summary>
            /// <returns></returns>
            UcUserProtecteds UserGetProtected();

            /// <summary>
            /// 合并用户
            /// </summary>
            /// <param name="oldUserName">老用户名</param>
            /// <param name="newUserName">新用户名</param>
            /// <param name="uid">Uid</param>
            /// <param name="passWord">密码</param>
            /// <param name="email">Email</param>
            /// <returns></returns>
            UcUserMerge UserMerge(string oldUserName, string newUserName, int uid, string passWord, string email);

            /// <summary>
            /// 移除重名用户记录
            /// </summary>
            /// <param name="userName">用户名</param>
            void UserMergeRemove(string userName);

            /// <summary>
            /// 得到用户积分
            /// </summary>
            /// <param name="appId">应用程序Id</param>
            /// <param name="uid">Uid</param>
            /// <param name="credit">积分编号</param>
            /// <returns></returns>
            int UserGetCredit(int appId, int uid, int credit);

            /// <summary>
            /// 检查新消息
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            UcPmCheckNew PmCheckNew(int uid);

            /// <summary>
            /// 发送短消息
            /// </summary>
            /// <param name="fromUid">发件人用户 ID，0 为系统消息</param>
            /// <param name="replyPmId">回复的消息 ID，0:发送新的短消息，大于 0:回复指定的短消息</param>
            /// <param name="subject">消息标题</param>
            /// <param name="message">消息内容</param>
            /// <param name="msgTo">收件人ID</param>
            /// <returns></returns>
            UcPmSend PmSend(int fromUid, int replyPmId, string subject, string message, params int[] msgTo);

            /// <summary>
            /// 发送短消息
            /// </summary>
            /// <param name="fromUid">发件人用户 ID，0 为系统消息</param>
            /// <param name="replyPmId">回复的消息 ID，0:发送新的短消息，大于 0:回复指定的短消息</param>
            /// <param name="subject">消息标题</param>
            /// <param name="message">消息内容</param>
            /// <param name="msgTo">收件人用户名</param>
            /// <returns></returns>
            UcPmSend PmSend(int fromUid, int replyPmId, string subject, string message, params string[] msgTo);

            /// <summary>
            /// 删除短消息
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="folder">文件夹</param>
            /// <param name="pmIds">短消息ID</param>
            /// <returns>删除的数量</returns>
            int PmDelete(int uid, PmDeleteFolder folder, params int[] pmIds);

            /// <summary>
            /// 删除会话
            /// </summary>
            /// <param name="uid">发件人</param>
            /// <param name="toUids">收件人</param>
            /// <returns>删除的数量</returns>
            int PmDelete(int uid, params int[] toUids);

            /// <summary>
            /// 修改阅读状态
            /// </summary>
            /// <param name="uid">发件人</param>
            /// <param name="toUids">收件人</param>
            /// <param name="pmIds">短消息ID</param>
            /// <param name="readStatus">阅读状态</param>
            void PmReadStatus(int uid, int toUids, int pmIds = 0, ReadStatus readStatus = ReadStatus.Readed);

            /// <summary>
            /// 修改阅读状态
            /// </summary>
            /// <param name="uid">发件人</param>
            /// <param name="toUids">收件人数组</param>
            /// <param name="pmIds">短消息ID数组</param>
            /// <param name="readStatus">阅读状态</param>
            void PmReadStatus(int uid, IEnumerable<int> toUids, IEnumerable<int> pmIds, ReadStatus readStatus = ReadStatus.Readed);

            /// <summary>
            /// 获取短消息列表
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="page">当前页编号，默认值 1</param>
            /// <param name="pageSize">每页最大条目数，默认值 10</param>
            /// <param name="folder">短消息所在的文件夹</param>
            /// <param name="filter">过滤方式</param>
            /// <param name="msgLen">截取短消息内容文字的长度，0 为不截取，默认值 0</param>
            /// <returns></returns>
            UcPmList PmList(int uid, int page = 1, int pageSize = 10, PmReadFolder folder = PmReadFolder.NewBox, PmReadFilter filter = PmReadFilter.NewPm, int msgLen = 0);

            /// <summary>
            /// 获取短消息内容
            /// 本接口函数用于返回指定用户的指定消息 ID 的消息，返回的数据中包含针对这个消息的回复。
            /// 如果指定 touid 参数，那么短消息将列出所有 uid 和 touid 之间的短消息，daterange 可以指定返回消息的日期范围。
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="pmId">短消息ID</param>
            /// <param name="toUid">收件人ID</param>
            /// <param name="dateRange">日期范围</param>
            /// <returns></returns>
            UcPmView PmView(int uid, int pmId, int toUid = 0, DateRange dateRange = DateRange.Today);

            /// <summary>
            /// 获取单条短消息内容
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="type">类型</param>
            /// <param name="pmId">短消息ID</param>
            /// <returns></returns>
            UcPm PmViewNode(int uid, ViewType type = ViewType.Specified, int pmId = 0);

            /// <summary>
            /// 忽略未读消息提示
            /// </summary>
            /// <param name="uid">Uid</param>
            void PmIgnore(int uid);

            /// <summary>
            /// 得到黑名单
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            UcPmBlacklsGet PmBlacklsGet(int uid);

            /// <summary>
            /// 设置黑名单为禁止所有人（清空原数据）
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            bool PmBlacklsSetAll(int uid);

            /// <summary>
            /// 设置黑名单（清空原数据）
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="userName">黑名单用户名</param>
            /// <returns></returns>
            bool PmBlacklsSet(int uid, params string[] userName);

            /// <summary>
            /// 添加黑名单为禁止所有人
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            bool PmBlacklsAddAll(int uid);

            /// <summary>
            /// 增加黑名单
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="userName">黑名单用户名</param>
            /// <returns></returns>
            bool PmBlacklsAdd(int uid, params string[] userName);

            /// <summary>
            /// 删除黑名单中的禁止所有人
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <returns></returns>
            void PmBlacklsDeleteAll(int uid);

            /// <summary>
            /// 删除黑名单
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="userName">黑名单用户名</param>
            void PmBlacklsDelete(int uid, params string[] userName);

            /// <summary>
            /// 增加好友
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="friendId">好友ID</param>
            /// <param name="comment">备注</param>
            /// <returns></returns>
            bool UcFriendAdd(int uid, int friendId, string comment = "");

            /// <summary>
            /// 删除好友
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="friendIds">好友ID</param>
            /// <returns></returns>
            bool UcFriendDelete(int uid, params int[] friendIds);

            /// <summary>
            /// 获取好友总数
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="direction">方向</param>
            /// <returns>好友数目</returns>
            int UcFriendTotalNum(int uid, FriendDirection direction = FriendDirection.All);

            /// <summary>
            /// 好友列表
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="page">当前页编号</param>
            /// <param name="pageSize">每页最大条目数</param>
            /// <param name="totalNum">好友总数</param>
            /// <param name="direction">方向</param>
            /// <returns></returns>
            UcFriends UcFriendList(int uid, int page = 1, int pageSize = 10, int totalNum = 10, FriendDirection direction = FriendDirection.All);

            /// <summary>
            /// 积分兑换请求
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="from">原积分</param>
            /// <param name="to">目标积分</param>
            /// <param name="toAppId">目标应用ID</param>
            /// <param name="amount">积分数额</param>
            /// <returns></returns>
            bool UcCreditExchangeRequest(int uid, int from, int to, int toAppId, int amount);

            ///<summary>
            /// 修改头像
            ///</summary>
            ///<param name="uid">Uid</param>
            ///<param name="type"></param>
            ///<returns></returns>
            string Avatar(int uid, AvatarType type = AvatarType.Virtual);

            /// <summary>
            /// 得到头像地址
            /// </summary>
            /// <param name="uid">Uid</param>
            /// <param name="size">大小</param>
            /// <param name="type">类型</param>
            /// <returns></returns>
            string AvatarUrl(int uid,AvatarSize size,AvatarType type = AvatarType.Virtual);

            /// <summary>
            /// 检查头像是否存在
            /// </summary>
            /// <param name="uid"></param>
            /// <param name="size"></param>
            /// <param name="type"></param>
            /// <returns></returns>
            bool AvatarCheck(int uid, AvatarSize size = AvatarSize.Middle, AvatarType type = AvatarType.Virtual);

            /// <summary>
            /// 获取标签数据
            /// </summary>
            /// <param name="tagName">标签名</param>
            /// <param name="number">应用程序ID对应的数量</param>
            /// <returns></returns>
            UcTags TagGet(string tagName, IEnumerable<KeyValuePair<string, string>> number);

            /// <summary>
            /// 添加事件
            /// </summary>
            /// <param name="icon">图标类型，如：thread、post、video、goods、reward、debate、blog、album、comment、wall、friend</param>
            /// <param name="uid">Uid</param>
            /// <param name="userName">用户名</param>
            /// <param name="titleTemplate">标题模板</param>
            /// <param name="titleData">标题数据数组</param>
            /// <param name="bodyTemplate">内容模板</param>
            /// <param name="bodyData">模板数据</param>
            /// <param name="bodyGeneral">相同事件合并时用到的数据：特定的数组，只有两项：name、link，保留</param>
            /// <param name="targetIds">保留</param>
            /// <param name="images">相关图片的 URL 和链接地址。一个图片地址，一个链接地址</param>
            /// <returns></returns>
            int FeedAdd(FeedIcon icon, int uid, string userName, string titleTemplate, string titleData, string bodyTemplate, string bodyData, string bodyGeneral, string targetIds, params string[] images);

            /// <summary>
            /// 得到Feed
            /// </summary>
            /// <param name="limit">数量限制</param>
            /// <returns></returns>
            UcFeeds FeedGet(int limit);

            /// <summary>
            /// 得到应用列表
            /// </summary>
            /// <returns></returns>
            UcApps AppList();

            /// <summary>
            /// 添加邮件到队列
            /// </summary>
            /// <param name="subject">标题</param>
            /// <param name="message">内容</param>
            /// <param name="uids">Uid</param>
            /// <returns></returns>
            UcMailQueue MailQueue(string subject, string message,params int[] uids);

            /// <summary>
            /// 添加邮件到队列
            /// </summary>
            /// <param name="subject">标题</param>
            /// <param name="message">内容</param>
            /// <param name="emails">目标Email</param>
            /// <returns></returns>
            UcMailQueue MailQueue(string subject, string message, params string[] emails);

            /// <summary>
            /// 添加邮件到队列
            /// </summary>
            /// <param name="subject">标题</param>
            /// <param name="message">内容</param>
            /// <param name="uids">Uid</param>
            /// <param name="emails">目标email</param>
            /// <returns></returns>
            UcMailQueue MailQueue(string subject, string message, int[] uids, string[] emails);

            /// <summary>
            /// 添加邮件到队列
            /// </summary>
            /// <param name="subject">标题</param>
            /// <param name="message">内容</param>
            /// <param name="fromMail">发信人，可选参数，默认为空，uc后台设置的邮件来源作为发信人地址</param>
            /// <param name="charset">邮件字符集，可选参数，默认为gbk</param>
            /// <param name="htmlOn">是否是html格式的邮件，可选参数，默认为FALSE，即文本邮件</param>
            /// <param name="level">邮件级别，可选参数，默认为1，数字大的优先发送，取值为0的时候立即发送，邮件不入队列</param>
            /// <param name="uids">Uid</param>
            /// <param name="emails">目标email</param>
            /// <returns></returns>
            UcMailQueue MailQueue(string subject,string message,string fromMail,string charset,bool htmlOn,int level,int[] uids,string[] emails);
        }
    }

这份 API 是根据 UCenter API **<a href="http://www.ucapi.com/api/" target="_blank">开发手册</a>**开发的

&nbsp;

&nbsp;

所有的API都在里面了，不用考虑实现细节，配置好以后直接调用即可！

&nbsp;

**供 UCenter 调用的接口**

这里，我们现在网站下新建一个叫 API 的文件夹（一定要叫 API）

然后再创建一个 ashx 文件（文件名和前面的配置对应即可，上面用的是 uc.ashx ，只要对应即刻，没必要用 uc.php）

&nbsp;

结构如下：

[<img class="alignnone size-full wp-image-218" title="ashx" alt="ashx" src="/uploads/2011/02/ashx.png" width="227" height="197" />][8]

uc.ashx 修改如下：

&nbsp;

    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Web;
    using DS.Web.UCenter.Api;

    namespace DS.Web.UCenter.Website.API
    {
        /// <summary>
        /// Summary description for uc
        /// </summary>
        public class uc:UcApiBase
        {
            public override ApiReturn DeleteUser(IEnumerable<int> ids)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn RenameUser(int uid, string oldUserName, string newUserName)
            {
                throw new NotImplementedException();
            }

            public override UcTagReturns GetTag(string tagName)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn SynLogin(int uid)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn SynLogout()
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdatePw(string userName, string passWord)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateBadWords(UcBadWords badWords)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateHosts(UcHosts hosts)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateApps(UcApps apps)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateClient(UcClientSetting client)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateCredit(int uid, int credit, int amount)
            {
                throw new NotImplementedException();
            }

            public override UcCreditSettingReturns GetCreditSettings()
            {
                throw new NotImplementedException();
            }

            public override ApiReturn GetCredit(int uid, int credit)
            {
                throw new NotImplementedException();
            }

            public override ApiReturn UpdateCreditSettings(UcCreditSettings creditSettings)
            {
                throw new NotImplementedException();
            }
        }
    }

本来呢，ashx 继承的是 IHttpHandler ，但是呢，我们需要修改一下，让它继承 UcApiBase

它是一个抽象类，重写抽象方法即可。

&nbsp;

但是具体怎么用呢？

这些函数不是给你调用的，是给 UCenter 调用的，你要做的就是写一些逻辑代码。比如 UCenter 告诉你 有人登陆了 (SynLogin函数)

那你应该做点什么呢？ 写 Cookie ？写 Session ？ 都行~

同样，当 UCenter 同步登出的时候，你也需要写一些逻辑代码，清理 Cookie 或者 Session

另外几个函数是干嘛的呢？ 参考 UCenter 接口**<a href="http://www.ucapi.com/api/" target="_blank">开发手册</a>**中的 API接口 这个章节即可

 [1]: /uploads/2011/01/ucenter_success.png
 [2]: /uploads/2011/01/connection.png
 [3]: /uploads/2011/01/ucentertest.png
 [4]: /uploads/2011/01/add_app.png
 [5]: /uploads/2011/01/apps_settings.png
 [6]: /uploads/2011/01/app_info.png
 [7]: /uploads/2011/02/solution.png
 [8]: /uploads/2011/02/ashx.png
