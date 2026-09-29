import binascii

with open("fat_Y1k@.png","rb") as f:
    buf = bytearray(f.read())

buf[20] = 0x00
buf[21] = 0x00
buf[22] = 0x05
buf[23] = 0xDC

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