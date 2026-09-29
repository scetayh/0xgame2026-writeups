import zlib, struct

data = open('fat_Y1k@.png','rb').read()
# 按照笔记：
# 签名 0 ~ 7 bytes
# Length 8 ~ 11 bytes
# Type IHDR 12 ~ 15 bytes
# ! Width 16 ~ 19 bytes
# ! Height 20 ~ 23 bytes
#
# 要读 16 ~ 23 bytes
w, h = struct.unpack('>II', data[16:24])

# 收集所有 IDAT 的 Payload
idat = b''
pos = 8 # 跳过签名
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