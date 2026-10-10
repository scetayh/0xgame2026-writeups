import zlib, struct

data = open('fat_Y1k@_ERROR！.png','rb').read()

idat = b''
pos = 8
while pos < len(data):
    ln, typ = struct.unpack('>I4s', data[pos:pos+8])
    if typ == b'IDAT':
        idat += data[pos+8:pos+8+ln]
    pos += 12 + ln

raw = zlib.decompress(idat)

print(len(raw))