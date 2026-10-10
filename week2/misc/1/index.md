# 小伊卡...不胖...不胖...（已黑化）

用 Okteta 截了一下前 26 字节：

```
89 50 4E 47 ← 签名
0D 0A 1A 0A ←
00 00 00 0D ← Chunk 1 长度：(D)_16 = (13)_10
49 48 44 52 ← Chunk 1 类型：IHDR
00 00 00 00 ← Chunk 1 数据：IHDR 记录图像宽度：0
00 00 00 00 ← Chunk 1 数据：IHDR 记录图像高度：0
08 02       ← 位深 8，颜色类型 2（8 位 RGB）
```

宽高都不对。提取 IDAT raw ，算一下究竟多少个像素：

```python
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
```

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/misc/1 $ python3 calc.py 
1229440
```

用 Sage 分解质因数：

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/misc/1 $ sage <<EOF
> factor(1229440)
> EOF
┌────────────────────────────────────────────────────────────────────┐
│ SageMath version 10.9, Release Date: 2026-05-04                    │
│ Using Python 3.12.14. Type "help()" for help.                      │
└────────────────────────────────────────────────────────────────────┘
Ctrl click to launch VS Code Native REPL (https://aka.ms/python-native-repl)
sage: 2^7 * 5 * 17 * 113
```

1229440 = 2^7 * 5 * 17 * 113 。8 位 RGB ，每像素 3 bytes。设宽 w 高 h ，则每行字节数为 1 + 3w（ 1 是 filter）。约束条件：

- h * (1 + 3w) = 1229440

即：

- h * (1 + 3w) = 2^7 * 5 * 17 * 113

如果不乱裁剪，宽高往往都是偶数，那么 w 为偶数，3w 为偶数，(1 + 3w) 为奇数。根据质因数分解，(1 + 3w) 可能等于：

- 5 → w 非整数
- 17 → w 非整数
- 113 → w 非整数
- 5 * 17 → w = 28, h = 14464
- 17 * 113 → w = 640, h = 640
- 113 * 5 → w = 188, h = 2716
- 5 * 17 * 113 → w = 3201, h = 128

只有 640 * 640（0x280 * 0x280）正常。用 Week 1 脚本修回来：

```python
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
```

![](fixed.png)

得到 flag 为 `0xGame{d0_yOu_tru1y_underst@nd_(Rc?}` 。