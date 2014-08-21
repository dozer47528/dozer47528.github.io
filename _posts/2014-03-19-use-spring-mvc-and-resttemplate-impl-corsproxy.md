---
title: 利用 Spring MVC 和 RestTemplate 实现 CorsProxy
author: Dozer
layout: post
permalink: /2014/03/use-spring-mvc-and-resttemplate-impl-corsproxy/
posturl_add_url:
  - yes
duoshuo_thread_id:
  - 1171159103985658384
categories:
  - 编程技术
tags:
  - CORS
  - java
  - Spring
---

### <span id="CORS_PROXY">CORS PROXY 是什么</span>

跨域的问题大家应该都知道了，ajax 请求是不能直接调用另一个域名下的接口的，虽然 jsonp 可以解决一定的问题，但是对于 Post、PUT、DELETE 等高级功能的支持上就无能为力了。

&nbsp;

为了解决这个问题，高级浏览器中都开始支持 CORS 了，CORS 在 headers 中定义了相关参数，告诉浏览器我的接口是否允许被外部站定请求，允许哪些 Method，等等…

具体的用法可以看看相关文档：<a href="https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS" target="_blank">https://developer.mozilla.org/en-US/docs/HTTP/Access_control_CORS</a>

<!--more-->

&nbsp;

有了 CORS ，下一个问题又来了，CORS 必须在服务端加上相关的 headers 才可以进行，那么第三方接口没有启用 CORS 怎么办？

不是他们来不及实现，而是他们为了安全性，根本就不想去实现。因为 CORS 是有一定的危险性的：<a href="http://www.freebuf.com/articles/web/18493.html" target="_blank">http://www.freebuf.com/articles/web/18493.html</a>

CORS 中有一个定义 \`Access-Control-Allow-Origin\` 用来表示允许哪些来源进行跨域请求，像上面提到的第三方公共接口如果开放了 CORS，那么来源是不确定的，所以如果在这里配置成允许所有的来源就非常危险了。

黑客很有可能会利用 <a href="http://en.wikipedia.org/wiki/Cross-site_scripting" target="_blank"><strong>XSS</strong></a> 来进行相关的攻击。

&nbsp;

所以怎么对付这种第三方的接口了？

终于引出 CORS Proxy 了！

CORS Proxy 就是 client 和第三方 server 中间的一个代理服务器，而且这个服务器只能你自己使用（把 \`Access-Control-Allow-Origin\` 设置成 client 的地址）。

CORS Proxy 内部再用 Http Client 来请求第三方服务器。

注意！用代码写的 Http Client 是不存在跨域问题的，因为跨域限制是浏览器加的安全防护措施，而不是 server 端的限制。

&nbsp;

### <span id="CORS_PROXY-2">CORS PROXY 实现原理</span>

CORS Proxy 的原理其实很简单，主要就做三件事情：

1.  身份验证
2.  转发请求
3.  带上 CORS 相关的 headers

那在 java 中怎么实现了？

我们用 Spring MVC 和 Spring 的 RestTemplate 来实现了一个 CORS Proxy：

<pre class="lang:java decode:true">@Controller
@RequestMapping(value = "/corsproxy")
public class CorsProxyController {
    private Logger logger = LoggerFactory.getLogger(getClass());

    private RestTemplate restTemplate;
    private HeaderFilter headerFilter;
    private TargetUrlFilter targetUrlFilter;
    private final String CORS_PREFIX = "corsproxy/";
    private final String HTTP_PREFIX = "http/";
    private final String HTTPS_PREFIX = "https/";

    @RequestMapping(value = "/**")
    public ResponseEntity&lt;byte[]&gt; proxy(HttpServletRequest request, @RequestBody byte[] body, @RequestHeader MultiValueMap&lt;String, String&gt; headers) throws UnsupportedEncodingException {

        String url = request.getRequestURI();
        String queryString = request.getQueryString();

        if (queryString != null && queryString != "") {
            url = url + "?" + queryString;
        }

        String targetUrl = getTargetUrl(url);

        if (!targetUrlFilter.checkUrl(targetUrl)) {
            return new ResponseEntity&lt;byte[]&gt;(HttpStatus.FORBIDDEN);
        }

        ResponseEntity&lt;byte[]&gt; result = null;
        try {
            result = restTemplate.exchange(new URI(targetUrl), HttpMethod.valueOf(request.getMethod()), new HttpEntity&lt;byte[]&gt;(body, headers), byte[].class);
        } catch (HttpClientErrorException exp) {
            return new ResponseEntity&lt;byte[]&gt;(exp.getResponseBodyAsByteArray(), getResponseHeaders(exp.getResponseHeaders()), exp.getStatusCode());
        } catch (HttpServerErrorException exp) {
            return new ResponseEntity&lt;byte[]&gt;(exp.getResponseBodyAsByteArray(), getResponseHeaders(exp.getResponseHeaders()), exp.getStatusCode());
        } catch (Exception exp) {
            return new ResponseEntity&lt;byte[]&gt;(exp.getMessage().getBytes("utf-8"), getResponseHeaders(new HttpHeaders()), HttpStatus.INTERNAL_SERVER_ERROR);
        }

        return new ResponseEntity&lt;byte[]&gt;(result.getBody(), getResponseHeaders(result.getHeaders()), result.getStatusCode());
    }

    @Resource(name = "restTemplate")
    public void setRestTemplate(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    @Resource(name = "headerFilter")
    public void setHeaderFilter(HeaderFilter headerFilter) {
        this.headerFilter = headerFilter;
    }

    @Resource(name = "targetUrlFilter")
    public void setTargetUrlFilter(TargetUrlFilter targetUrlFilter) {
        this.targetUrlFilter = targetUrlFilter;
    }

    private String getTargetUrl(String url) {
        String targetUrl = url.substring(url.indexOf(CORS_PREFIX) + CORS_PREFIX.length());
        if (targetUrl.indexOf(HTTP_PREFIX) == 0) {
            targetUrl = "http://" + targetUrl.substring(HTTP_PREFIX.length());
        } else if (targetUrl.indexOf(HTTPS_PREFIX) == 0) {
            targetUrl = "https://" + targetUrl.substring(HTTPS_PREFIX.length());
        }
        return targetUrl;
    }

    private HttpHeaders getResponseHeaders(HttpHeaders originHeaders) {
        HttpHeaders header = new HttpHeaders();
        for (Entry&lt;String, List&lt;String&gt;&gt; item : originHeaders.entrySet()) {
            if (headerFilter.needRemoveHeader(item.getKey(), item.getValue().toString())) {
                continue;
            }
            header.put(item.getKey(), item.getValue());
        }

        return header;
    }

}</pre>

代码不是很复杂，这里是 Controller，另外还有一个 Filter：

<pre class="lang:java decode:true">public class CorsFilter extends OncePerRequestFilter  implements Filter{
    private HeaderHelper headerHelper;

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        for(Map.Entry&lt;? extends String, ? extends List&lt;String&gt;&gt; header: headerHelper.getHeadersMap().entrySet()){
            Joiner joiner = Joiner.on("; ").skipNulls();
            String value = joiner.join(header.getValue());
            response.addHeader(header.getKey(),value);
        }
        filterChain.doFilter(request, response);
    }

    @Resource(name = "headerHelper")
    public void setHeaderHelper(HeaderHelper headerHelper) {
        this.headerHelper = headerHelper;
    }
}</pre>

代码中的 \`HeaderHelper \`，\`HeaderFilter\` 和 \`TargetUrlFilter\` 没什么逻辑，只是读取了一下配置而已。

&nbsp;

### <span id="i">一些注意事项</span>

这个实现没有难度，但是其中有一个部分算是一个大坑。

#### <span id="i-2">编码问题</span>

一开始我的 CORS Proxy 接受的\`RequestBody\`是\`String\`，用\`RestTemplate\`请求的返回值也是\`String\`，但是后来发现其中会有很多问题。client 和 server 的编码规范不一定标准，其实你作为代理服务器，根本不需要去进行编码，client 端给你的是什么，你就原封不动传给 server 就行了，所以我们编写的时候全部用了\`byte[]\`，从此就再无问题了。

&nbsp;

还有一个是\`GET\`的\`QueryString\`，这里很坑！如果是中文的话，从\`Request\`里获得的是被编码过的内容，不会自动解码成中文。而\`RestTemplate\`会自动对它进行编码，所以客户端收到的就是2次编码的内容了，如果只解码一次，是得不到中文的。

怎么解决？调用\`RestTemplate\`的时候不要吧\`String\`类型的 url 传过去，而是传一个\`URI\`对象，这样\`RestTemplate\`就不会去自动编码了。

&nbsp;

#### <span id="Transfer-Encoding">Transfer-Encoding</span>

一开始做的时候，我把 server 端返回的 body 和 headers 原封不动地给了 client，但是 client 一直会中断连接！完全收不到数据。

直觉让我觉得是 headers 中的一些东西有问题。于是用排除法一个个尝试，最后发现问题出在了\`Transfer-Encoding\`身上。

原来这是一个<a href="http://zh.wikipedia.org/wiki/%E5%88%86%E5%9D%97%E4%BC%A0%E8%BE%93%E7%BC%96%E7%A0%81" target="_blank"><strong>分块传输编码</strong></a>，那为什么加上了这个 header 就有问题了呢？

因为我的代理已经和 server 端把所有的数据传输完了，我把所有的数据返回给了 client，但是代理却又告诉 client 说自己是分块传输的… client 就无法理解了…

最后我又写了一个\`HeaderFilter\`，然后把一些不需要传输的 header 给过滤掉了。

&nbsp;

#### <span id="Content-Length">Content-Length</span>

\`Content-Length\`也是一个坑，为什么呢？因为 server 端传过来的\`Content-Length\`是不能直接传给 client 的。

有这么一个场景，client 和 proxy 之间有 gzip，server 和 proxy 之间没有 gzip。

这是 proxy 传给 client 的\`Content-Length\`就是未压缩前的长度，就出现问题了。

怎么解决？同样用上面的\`HeaderFilter\`，过滤掉后，proxy 所在的服务端会自动为\`Response\`加上\`Content-Length\`的，根本不需要手动指定。

&nbsp;

#### <span id="Access-Control-Allow-Origin">Access-Control-Allow-Origin</span>

CORS 标准中有几个 header，其中一个就是\`Access-Control-Allow-Origin\`，它代表着你可以让哪个域名跨域请求你的地址。

我上面的\`HeaderHelper\`会自动加上这个 header，但后来遇到了一个奇葩的 case！

原始的地址已经加上了\`Access-Control-Allow-Origin\`，然后我的\`HeaderHelper\`会再给它加上一个。

然后\`Access-Control-Allow-Origin\`这个 header 是很坑爹的，它可以是\`*\`，也可以是\`http://www.dozer.cc\`，但是它不可以是\`http://www.dozer.cc, http://www.baidu.com\`。

就是说要么是通配符，要么就只能允许一个域名！

我上面加了两次，就被解析成了\`\*,\*\`，然后浏览器就不认识了…

&nbsp;

所以如果有多个域名怎么办？那只能动态生成这个 header。

但是从安全性的考虑，强烈建议独立部署自己的 CorsPorxy，而不要混用！

&nbsp;

#### <span id="i-3">重定向的问题</span>

这个话题设计的东西比较多，已经自成文章：<a href="/2014/05/disable-resttemplate-redirect/" target="_blank"><strong>禁用 RestTemplate 的自动重定向功能</strong></a>

&nbsp;

&nbsp;

后面还有哪些坑呢？我们目前也还没遇到，但我们把很多东西写成了配置，将来再发现有问题就改配置好了。实现逻辑就那么点，可配置的地方也就那么点，万变不离其宗。
