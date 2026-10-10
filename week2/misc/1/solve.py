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

new_crc = binascii.crc32(buf[12 : 29]) & 0xFFFFFFFF
buf[29:33] = new_crc.to_bytes(4, byteorder='big')

with open("fixed.png","wb") as out:
    out.write(buf)
