# ！？数学基础？！

`nc` 出来的东西长这个样子：

```bash
scetayh@yuprae-gentoo ~ $ nc nc1.ctfplus.cn 43364
==================================================
                   (Scripting 101)                
==================================================
系统提示：连续答对 100 道随机四则运算题，即可获得 Flag！
[round:1/100 ]
calculate: 549 一 231 = ?
Input your answer: 
[!] Timeout ! ! !
```

先打个死循环看一看究竟问题格式大概长什么样：

```bash
scetayh@yuprae-gentoo ~ $ while true; do nc nc1.ctfplus.cn 43364 | grep calculate; done
calculate: 552 ＋ 364 = ?
calculate: 573 ＋ 660 = ?
calculate: 848 一 718 = ?
calculate: 843 ＋ 826 = ?
calculate: 630 ÷ 30 = ?
calculate: 989 一 805 = ?
calculate: 955 一 796 = ?
calculate: 87 x 62 = ?
calculate: 12 x 39 = ?
calculate: 92 x 86 = ?
calculate: 176 ＋ 680 = ?
calculate: 843 一 789 = ?
calculate: 95 x 86 = ?
calculate: 987 一 206 = ?
calculate: 520 ＋ 305 = ?
calculate: 3328 ÷ 52 = ?
calculate: 752 ＋ 254 = ?
calculate: 54 x 74 = ?
calculate: 361 一 251 = ?
calculate: 447 ＋ 882 = ?
calculate: 546 一 295 = ?
calculate: 599 一 388 = ?
calculate: 817 ＋ 250 = ?
calculate: 323 一 164 = ?
calculate: 44 x 92 = ?
calculate: 79 x 22 = ?
calculate: 389 ＋ 395 = ?
calculate: 55 x 38 = ?
calculate: 946 ＋ 195 = ?
calculate: 28 x 92 = ?
calculate: 1440 ÷ 24 = ?
calculate: 728 ÷ 13 = ?
calculate: 79 x 22 = ?
^C
```

可以看到共性还是比较明显的，想到可以用 `bash` 截取字符串，利用 FIFO 传递给 `bc` 计算，最后发送出去。

脚本具体编写过程看 [auto_calculate.sh](auto_calculate.sh) 。

运行：

```bash
scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week1/pwn/2 $ ./auto_calculate.sh 43364
==================================================
                   (Scripting 101)                
==================================================
系统提示：连续答对 100 道随机四则运算题，即可获得 Flag！
[round:1/100 ]
calculate: 523 ＋ 320 = ?
>>> 523 + 320 = 843 # 注意这一行并没有通过 FIFO 发送出去，它是为了给人看的；发送出去的已经走 FD 3 了
Input your answer: [√] Correct!

[round:2/100 ]
calculate: 333 ＋ 887 = ?
>>> 333 + 887 = 1220
Input your answer: [√] Correct!

[round:3/100 ]
calculate: 55 x 85 = ?
>>> 55 * 85 = 4675
Input your answer: [√] Correct!

[round:4/100 ]
calculate: 728 一 668 = ?
>>> 728 - 668 = 60
Input your answer: [√] Correct!

[round:5/100 ]
calculate: 999 一 415 = ?
>>> 999 - 415 = 584
Input your answer: [√] Correct!

...

[round:100/100 ]
calculate: 461 ＋ 294 = ?
>>> 461 + 294 = 755
Input your answer: [√] Correct!

==================================================
Flag: 0xGame{Y0u_4r3_7h3_PY7h0n_m4st3r}

==================================================
```