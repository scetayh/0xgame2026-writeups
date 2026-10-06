import zlib, struct

data = open('fat_Y1k@_ERROR！.png','rb').read()

w, h = struct.unpack('>II', data[16:24])

idat = b''
pos = 8
while pos < len(data):
    ln, typ = struct.unpack('>I4s', data[pos:pos+8])
    if typ == b'IDAT':
        idat += data[pos+8:pos+8+ln]
    pos += 12 + ln

raw = zlib.decompress(idat)

print('bytes:', len(raw))
print('IHDR height:', h)
print('bytes per line:', 1 + w*3)
print('factual lines:', len(raw) // (1 + w*3))

import binascii

with open("fat_Y1k@_ERROR！.png","rb") as f:
    buf = bytearray(f.read())

buf[16] = 0x00
buf[17] = 0x00
buf[18] = 0x02
buf[19] = 0x80

buf[20] = 0x00
buf[21] = 0x00
buf[22] = 0x02
buf[23] = 0x80

# 又按照笔记：
# 签名 0 ~ 7 bytes
# Length 8 ~ 11 bytes
# ! Type IHDR 12 ~ 15 bytes
# ! Payload 16 ~ 28 bytes
# CRC 29 ~ 32 bytes
new_crc = binascii.crc32(buf[12 : 29]) & 0xFFFFFFFF
buf[29:33] = new_crc.to_bytes(4, byteorder='big')

with open("fixed.png","wb") as out:
    out.write(buf)
