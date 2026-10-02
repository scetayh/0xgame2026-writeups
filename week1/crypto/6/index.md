# 深具传统的ECC之诞生

```bash
(base) scetayh@yuprae-gentoo ~ $ nc nc1.ctfplus.cn 11800
[+] Invalid Touch
[+] p = 380025560263444925282186340357451425457046895363401263284043
[+] E: y^2 = x^3 + 3*x + 0 mod p
[+] A pair of points was randomly selected.
[+] G = (89416635389252243162818482998273067753365476637225933437342, 246277781258250668709138589808946483685012465285148814183503)
[+] Q = (329460413071651533403262472631632126805896556373758724864455, 299273891016902567464505544081763716760408274149519169100436)
[+] Q = bytes_to_long(flag) * G
```

打开 SageMath ：

```bash
(base) scetayh@yuprae-gentoo ~ $ conda activate sage
(sage) scetayh@yuprae-gentoo ~ $ sage
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 10.9, Release Date: 2026-05-04                    │
│ Using Python 3.12.14. Type "help()" for help.                      │
└────────────────────────────────────────────────────────────────────┘
sage: 
```

依次定义模数、曲线和两个点：

```python
p = 380025560263444925282186340357451425457046895363401263284043
E = EllipticCurve(GF(p), [3, 0])
G = E(89416635389252243162818482998273067753365476637225933437342, 246277781258250668709138589808946483685012465285148814183503)
Q = E(329460413071651533403262472631632126805896556373758724864455, 299273891016902567464505544081763716760408274149519169100436)
```

然后暴力算：

```python
discrete_log?
k = discrete_log(Q, G, G.order(), operation='+')
print(k)
```

得到：

```
18134719827048627907749248473909097355496002454513789
```

按照 `nc` 的提示使用 `long_to_bytes`：

```python
(sage) scetayh@yuprae-gentoo ~ $ python3
Python 3.12.14 (main, Sep  2 2026, 23:29:55) [GCC 15.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from Crypto.Util.number import long_to_bytes as ltb
>>> print(ltb(18134719827048627907749248473909097355496002454513789))
b"0xGame{master's touch}"
>>> 
```

拿到 flag `0xGame{master's touch}` 。