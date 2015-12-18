---
title: 禁用 RestTemplate 的自动重定向功能
author: Dozer
layout: post
permalink: /2014/05/disable-resttemplate-redirect.html
categories:
  - 编程技术
tags:
  - CORS
  - Java
  - Spring
---
### Cors Proxy 该不该自动重定向

**<a title="利用 Spring MVC 和 RestTemplate 实现 CorsProxy" href="/2014/03/use-spring-mvc-and-resttemplate-impl-corsproxy.html" target="_blank">上篇文章</a> **我用 RestTemplate 实现了 CorsProxy 功能，项目上线后在实际使用的时候遇到了一个很坑爹的问题。

*   Client 通过 CorsProxy 请求了一个页面
*   CorsProxy 收到请求后，自己去重新请求目标页面
*   目标页面返回了 302 重定向
*   CorsProxy 收到后自动消化了这个重定向
*   但是在处理 Location 的时候，这个 Location 的 URL 包含一个空格
*   CorsProxy 抛错

场景是这样的，那么这里有2个问题。

<!--more-->

&nbsp;

1) 为什么 CorsProxy 自动跳转的时候会抛错，而浏览器自动跳转的时候不会抛错？

这个和框架实现原理有关。严格的来说，URL 里是不允许有空格的，但是如果对空格解码，解码出来的还是空格。

浏览器在这方面的要求不是很严格，而 RestTemplate 对这个要求很严格。

坑爹的是，RestTemplate 只会抛一个 400 bad request 错误。

后来我尝试着用别的框架去调用这个地址才看到了详细的错误内容，然后才意识到是 Location 里的 URL 里包含一个空格！

&nbsp;

2) 为什么 RestTemplate 会自动去做重定向？该不该做？

其实在大部分场景中，框架和浏览器自动处理重定向是有好处的。难不成你 Javascript 的 Ajax 请求中每次都要手动处理重定向？这个太麻烦了！

可我的这个 CorsProxy 和一般的 Web 接口不同，我不应该内部消化，我只是一个转发者，我要把数据原封不动地抛回去！

所以我标题中的答案就很清楚了，CorsProxy 不该内部消化重定向。

&nbsp;

### RestTemplate 怎么禁用自动重定向？

这个问题看似简单，我本来以为只要设一个属性就行了，结果发现，RestTemplate 的调用层次太深了…

网上找了很多教程都失败，后来在 Spring 论坛发现了一个帖子（<a href="http://forum.spring.io/forum/spring-projects/web/99054-disabling-followredirect-in-resttemplate" target="_blank"><strong>传送门</strong></a>），但回答的人只是简单地说了一下原理，没有代码。

&nbsp;

所以我就自己实现一下吧！代码量非常少。

我们先来看一下  RestTemplate 的第二个构造函数：

	/**
	 * Create a new instance of the {@link RestTemplate} based on the given {@link ClientHttpRequestFactory}.
	 * @param requestFactory HTTP request factory to use
	 * @see org.springframework.http.client.SimpleClientHttpRequestFactory
	 * @see org.springframework.http.client.HttpComponentsClientHttpRequestFactory
	 */
	public RestTemplate(ClientHttpRequestFactory requestFactory) {
		this();
		setRequestFactory(requestFactory);
	}

切入点就在这里了！ 上面提到了两种 `ClientHttpRequestFactory`，网上很多教程是按照`HttpComponentsClientHttpRequestFactory`做的，但是实现起来机器复杂，而且我试了一下失败了…

&nbsp;

后来看了一下上面文章中提到的`SimpleClientHttpRequestFactory`中的一个方法：

	protected void prepareConnection(HttpURLConnection connection, String httpMethod) throws IOException {
		if (this.connectTimeout >= 0) {
			connection.setConnectTimeout(this.connectTimeout);
		}
		if (this.readTimeout >= 0) {
			connection.setReadTimeout(this.readTimeout);
		}
		connection.setDoInput(true);
		if ("GET".equals(httpMethod)) {
			connection.setInstanceFollowRedirects(true);
		}
		else {
			connection.setInstanceFollowRedirects(false);
		}
		if ("PUT".equals(httpMethod) || "POST".equals(httpMethod) || "PATCH".equals(httpMethod)) {
			connection.setDoOutput(true);
		}
		else {
			connection.setDoOutput(false);
		}
		connection.setRequestMethod(httpMethod);
	}

看到玄机了吗？这里发现是 GET 请求的话，就自动`setInstanceFollowRedirects`为`true`了。

&nbsp;

看完了源代码，改造起来就很简单了，自己继承一个新的类就行了：

	public class NoRedirectClientHttpRequestFactory extends
			SimpleClientHttpRequestFactory {
	
		@Override
		protected void prepareConnection(HttpURLConnection connection,
				String httpMethod) throws IOException {
			super.prepareConnection(connection, httpMethod);
			connection.setInstanceFollowRedirects(false);
		}
	}

每次执行完`super.prepareConnection`后，我再把`setInstanceFollowRedirects`强制设置成`false`。

&nbsp;

最后是`bean`配置：

	<bean id="proxyRestTemplate" class="org.springframework.web.client.RestTemplate">
		<constructor-arg>
			<bean
				class="com.dianping.ba.crm.mobile.utils.NoRedirectClientHttpRequestFactory">
				<property name="connectTimeout" value="6000" />
				<property name="readTimeout" value="60000" />
			</bean>
		</constructor-arg>
	</bean>

注入你自己的`ClientHttpRequestFactory`就行了！

对了，这里也可以设置连接时间和超时时间。
