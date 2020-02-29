---
title: 深入研究 UCenter API 之 加密与解密
author: Dozer
layout: post
permalink: /2011/01/ucenter-api-in-depth-3rd.html
categories:
  - 编程技术
tags:
  - AspDotNet
---

<div>
  <blockquote>
    <p>
      <strong>目录：</strong>
    </p>

    <ol>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-1st.html" target="_blank"><strong>开篇</strong></a>
      </li>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-2nd.html" target="_blank"><strong>通讯原理：UCenter API 与子站之间的通讯原理和单点登陆原理</strong></a>
      </li>
      <li>
        <a href="/2011/01/ucenter-api-in-depth-3rd.html" target="_blank"><strong>加密与解密：AuthCode详解 & AuthCode函数翻译过程中的注意点</strong></a>
      </li>
      <li>
        <strong><a href="/2011/02/ucenter-api-in-depth-4th.html" target="_blank">网站搭建： 康盛旗下网站 & Asp.net 网站搭建</a></strong>
      </li>
      <li>
        <strong><a href="/2011/04/ucenter-api-in-depth-5th.html" target="_blank">MVC 网站下的用法：在 MVC 下的使用方法</a></strong>
      </li>
      <li>
        <strong><a href="/2011/05/ucenter-api-for-net-on-codeplex.html" target="_blank">下载地址：UCenter API For .Net 在 CodePlex 上发布啦！</a></strong>
      </li>
    </ol>
  </blockquote>
</div>

&nbsp;

### AuthCode

UCenter API 中的加密解密函数，被称为 php 领域的经典之作，也是康盛公司为 php 做的一大贡献

这个函数，可以通过一个 KEY ，生成动态的密文，并可以再通过这个 KEY 来解密

我没有研究过什么加密算法，所以对这个的基础知识也不是很了解，或许在 C# 中会有更强大的算法，但是这个函数在做 UCenter API 的时候是必需的。

也是 UCenter API php 版翻译成 C# 版本中最难的一个部分。

<!--more-->

&nbsp;

### PHP 版详解

    // $string： 明文 或 密文
    // $operation：DECODE表示解密,其它表示加密
    // $key： 密匙
    // $expiry：密文有效期
    //字符串解密加密
    function authcode($string, $operation = 'DECODE', $key = '', $expiry = 0) {
         // 动态密匙长度，相同的明文会生成不同密文就是依靠动态密匙
        $ckey_length = 4;   // 随机密钥长度 取值 0-32;
                    // 加入随机密钥，可以令密文无任何规律，即便是原文和密钥完全相同，加密结果也会每次不同，增大破解难度。
                    // 取值越大，密文变动规律越大，密文变化 = 16 的 $ckey_length 次方
                    // 当此值为 0 时，则不产生随机密钥
        // 密匙
        $key = md5($key ? $key : UC_KEY);
        // 密匙a会参与加解密
        $keya = md5(substr($key, 0, 16));
        // 密匙b会用来做数据完整性验证
        $keyb = md5(substr($key, 16, 16));
        // 密匙c用于变化生成的密文
        $keyc = $ckey_length ? ($operation == 'DECODE' ? substr($string, 0, $ckey_length): substr(md5(microtime()), -$ckey_length)) : '';
        // 参与运算的密匙
        $cryptkey = $keya.md5($keya.$keyc);
        $key_length = strlen($cryptkey);

        // 明文，前10位用来保存时间戳，解密时验证数据有效性，10到26位用来保存$keyb(密匙b)，解密时会通过这个密匙验证数据完整性
        // 如果是解码的话，会从第$ckey_length位开始，因为密文前$ckey_length位保存 动态密匙，以保证解密正确
        $string = $operation == 'DECODE' ? base64_decode(substr($string, $ckey_length)) : sprintf('%010d', $expiry ? $expiry + time() : 0).substr(md5($string.$keyb), 0, 16).$string;
        $string_length = strlen($string);

        $result = '';
        $box = range(0, 255);

        $rndkey = array();
        // 产生密匙簿
        for($i = 0; $i <= 255; $i++) {
            $rndkey[$i] = ord($cryptkey[$i % $key_length]);
         }
         // 用固定的算法，打乱密匙簿，增加随机性，好像很复杂，实际上对并不会增加密文的强度
        for($j = $i = 0; $i < 256; $i++) {
            $j = ($j + $box[$i] + $rndkey[$i]) % 256;
            $tmp = $box[$i];
            $box[$i] = $box[$j];
            $box[$j] = $tmp;
         }
        // 核心加解密部分
        for($a = $j = $i = 0; $i < $string_length; $i++) {
            $a = ($a + 1) % 256;
            $j = ($j + $box[$a]) % 256;
            $tmp = $box[$a];
            $box[$a] = $box[$j];
            $box[$j] = $tmp;
            // 从密匙簿得出密匙进行异或，再转成字符
            $result .= chr(ord($string[$i]) ^ ($box[($box[$a] + $box[$j]) % 256]));
         }

        if($operation == 'DECODE') {
            // 验证数据有效性，请看未加密明文的格式
            if((substr($result, 0, 10) == 0 || substr($result, 0, 10) - time() > 0) && substr($result, 10, 16) == substr(md5(substr($result, 26).$keyb), 0, 16)) {
                return substr($result, 26);
             } else {
                return '';
             }
         } else {
             // 把动态密匙保存在密文里，这也是为什么同样的明文，生产不同密文后能解密的原因
             // 因为加密后的密文可能是一些特殊字符，复制过程可能会丢失，所以用base64编码
            return $keyc.str_replace('=', '', base64_encode($result));
         }
    }

&nbsp;

这份详解不是我写的，网上有很多，找不到原作者了

&nbsp;

&nbsp;

### C# 版

    /// <summary>
    /// AuthCode解码&编码
    /// </summary>
    /// <param name="sourceStr">原始字符串</param>
    /// <param name="operation">操作类型</param>
    /// <param name="keyStr">API KEY</param>
    /// <param name="expiry">过期时间 0代表永不过期</param>
    /// <returns></returns>
    private static string AuthCode(string sourceStr, AuthCodeMethod operation, string keyStr, int expiry = 0)
    {
        var ckeyLength = 4;
        var source = Encode.GetBytes(sourceStr);
        var key = Encode.GetBytes(keyStr);

        key = Md5(key);

        var keya = Md5(SubBytes(key, 0, 0x10));
        var keyb = Md5(SubBytes(key, 0x10, 0x10));
        var keyc = (ckeyLength > 0)
                        ? ((operation == AuthCodeMethod.Decode)
                                ? SubBytes(source, 0, ckeyLength)
                                : RandomBytes(ckeyLength))
                        : new byte[0];

        var cryptkey = AddBytes(keya, Md5(AddBytes(keya, keyc)));
        var keyLength = cryptkey.Length;

        if (operation == AuthCodeMethod.Decode)
        {
            while (source.Length % 4 != 0)
            {
                source = AddBytes(source, Encode.GetBytes("="));
            }
            source = Convert.FromBase64String(BytesToString(SubBytes(source, ckeyLength)));
        }
        else
        {
            source =
                AddBytes(
                    (expiry != 0
                            ? Encode.GetBytes((expiry + PhpTimeNow()).ToString())
                            : Encode.GetBytes("0000000000")),
                    SubBytes(Md5(AddBytes(source, keyb)), 0, 0x10), source);
        }

        var sourceLength = source.Length;

        var box = new int[256];
        for (var k = 0; k < 256; k++)
        {
            box[k] = k;
        }

        var rndkey = new int[256];
        for (var i = 0; i < 256; i++)
        {
            rndkey[i] = cryptkey[i % keyLength];
        }

        for (int j = 0, i = 0; i < 256; i++)
        {
            j = (j + box[i] + rndkey[i]) % 256;
            var tmp = box[i];
            box[i] = box[j];
            box[j] = tmp;
        }

        var result = new byte[sourceLength];
        for (int a = 0, j = 0, i = 0; i < sourceLength; i++)
        {
            a = (a + 1) % 256;
            j = (j + box[a]) % 256;
            var tmp = box[a];
            box[a] = box[j];
            box[j] = tmp;

            result[i] = (byte)(source[i] ^ (box[(box[a] + box[j]) % 256]));
        }

        if (operation == AuthCodeMethod.Decode)
        {
            var time = long.Parse(BytesToString(SubBytes(result, 0, 10)));
            if ((time == 0 ||
                    time - PhpTimeNow() > 0) &&
                BytesToString(SubBytes(result, 10, 16)) == BytesToString(SubBytes(Md5(AddBytes(SubBytes(result, 26), keyb)), 0, 16)))
            {
                return BytesToString(SubBytes(result, 26));
            }
            return "";
        }
        return BytesToString(keyc) + Convert.ToBase64String(result).Replace("=", "");
    }

    /// <summary>
    /// Byte数组转字符串
    /// </summary>
    /// <param name="b">数组</param>
    /// <returns></returns>
    public static string BytesToString(byte[] b)
    {
        return new string(Encode.GetChars(b));
    }

    /// <summary>
    /// 计算Md5
    /// </summary>
    /// <param name="b">byte数组</param>
    /// <returns>计算好的字符串</returns>
    public static byte[] Md5(byte[] b)
    {
        var cryptHandler = new MD5CryptoServiceProvider();
        var hash = cryptHandler.ComputeHash(b);
        var ret = "";
        foreach (var a in hash)
        {
            if (a < 16)
            { ret += "0" + a.ToString("x"); }
            else
            { ret += a.ToString("x"); }
        }
        return Encode.GetBytes(ret);
    }

    /// <summary>
    /// Byte数组相加
    /// </summary>
    /// <param name="bytes">数组</param>
    /// <returns></returns>
    public static byte[] AddBytes(params byte[][] bytes)
    {
        var index = 0;
        var length = 0;
        foreach(var b in bytes)
        {
            length += b.Length;
        }
        var result = new byte[length];

        foreach(var bs in bytes)
        {
            foreach (var b in bs)
            {
                result[index++] = b;
            }
        }
        return result;
    }

    /// <summary>
    /// Byte数组分割
    /// </summary>
    /// <param name="b">数组</param>
    /// <param name="start">开始</param>
    /// <param name="length">结束</param>
    /// <returns></returns>
    public static byte[] SubBytes(byte[] b, int start, int length = int.MaxValue)
    {
        if (start >= b.Length) return new byte[0];
        if (start < 0) start = 0;
        if (length < 0) length = 0;
        if (length>b.Length || start + length > b.Length) length = b.Length - start;
        var result = new byte[length];
        var index = 0;
        for(var k = start;k< start + length;k++)
        {
            result[index++] = b[k];
        }
        return result;
    }

    /// <summary>
    /// 计算Php格式的当前时间
    /// </summary>
    /// <returns>Php格式的时间</returns>
    public static long PhpTimeNow()
    {
        return DateTimeToPhpTime(DateTime.UtcNow);
    }

    /// <summary>
    /// PhpTime转DataTime
    /// </summary>
    /// <returns></returns>
    public static DateTime PhpTimeToDateTime(long time)
    {
        var timeStamp = new DateTime(1970, 1, 1); //得到1970年的时间戳
        var t = (time + 8 * 60 * 60) * 10000000 + timeStamp.Ticks;
        return new DateTime(t);
    }

    /// <summary>
    /// DataTime转PhpTime
    /// </summary>
    /// <param name="datetime">时间</param>
    /// <returns></returns>
    public static long DateTimeToPhpTime(DateTime datetime)
    {
        var timeStamp = new DateTime(1970, 1, 1);  //得到1970年的时间戳
        return (datetime.Ticks - timeStamp.Ticks) / 10000000;  //注意这里有时区问题，用now就要减掉8个小时
    }

    /// <summary>
    /// 随机字符串
    /// </summary>
    /// <param name="lens">长度</param>
    /// <returns></returns>
    public static byte[] RandomBytes(int lens)
    {
        var chArray = new[]
                            {
                                'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G',
                                'H', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                                'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
                            };
        var length = chArray.Length;
        var result = new byte[lens];
        var random = new Random();
        for (var i = 0; i < lens; i++)
        {
            result[i] = (byte) chArray[random.Next(length)];
        }
        return result;
    }

    /// <summary>
    /// 操作类型
    /// </summary>
    enum AuthCodeMethod
    {
        Encode,
        Decode,
    }

C# 版是一行一行按照原版本翻译的，增加了一些 C# 中没有的函数

&nbsp;

**1、string -> byte[] 的问题**

在这段算法中，经常会用到 Base64 算法，C# 中的 Base64 要求输入的是 byte[] 数组

在 php 程序中，都是直接用字符串的，而且也没有问题。

那在 C# 版中自然想到了 Encoding.Default.GetBytes() 函数

但这个函数有个很奇怪的问题：

Encoding.UTF8.GetBytes(((char) 200).ToString())[0].ToString() //最后的值是多少？

运行一下后发现它不是200，因为这个函数涉及到了编码问题

所以上述的操作，如果直接对字符串操作，那会出现很多问题，因为 php 和 C# 对字符串使用的默认编码不同。

所以就改成了对 byte[] 进行操作
