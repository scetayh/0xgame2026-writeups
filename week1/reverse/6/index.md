# z3_solver

`main()` 里边其他的都是一些打印提示和 I/O 操作，重点看缩进最多的主分支：

```c
      if ( (unsigned int)sub_401550(a1: (__int64)Buffer) != 0 )
      {
        puts(Buffer: "Correct! Constraints solved.");
        return 0;
      }
```

真正决定对错的就是 `sub_401550()` 函数，其他的不用管。反编译：

```c
__int64 __fastcall sub_401550(__int64 a1)
{
  int i; // [rsp+Ch] [rbp-4h]

  for ( i = 0; i <= 22; ++i )
  {
    if ( *(_BYTE *)(a1 + i) <= 0x1Fu || *(_BYTE *)(a1 + i) > 0x7Eu )
      return 0;
    if ( 5 * *(unsigned __int8 *)(a1 + (i + 1) % 23)
       + 3 * *(unsigned __int8 *)(a1 + i)
       + 11 * *(unsigned __int8 *)(a1 + (i + 7) % 23)
       + 7 * *(unsigned __int8 *)(a1 + (i + 4) % 23) != word_404000[i] )
      return 0;
  }
  return 1;
}
```

查看 `word_404000` ：

```
.rdata:0000000000404000 word_404000     dw 0B21h, 7BFh, 0A2Ch, 0A2Bh, 8FCh, 860h, 0AC7h, 0A21h
.rdata:0000000000404000                                         ; DATA XREF: sub_401550+13F↑o
.rdata:0000000000404010                 dw 7EEh, 0A0Eh, 0B55h, 0A05h, 0ABBh, 902h, 0BC8h, 0BCBh
.rdata:0000000000404020                 dw 6FFh, 0C4Eh, 0A48h, 7E3h, 0AEFh, 0A27h, 0A57h
```

数一数有23个元素，和 `i = 0; i <= 22` 吻合，所以这就是数组。IDA 导出得到：

```c
unsigned __int16 word_404000[23] = {2849u, 1983u, 2604u, 2603u, 2300u, 2144u,
                                    2759u, 2593u, 2030u, 2574u, 2901u, 2565u,
                                    2747u, 2306u, 3016u, 3019u, 1791u, 3150u,
                                    2632u, 2019u, 2799u, 2599u, 2647u};
```

上边那个函数 `__int64 a1` 是形参，`(__int64)Buffer` 是实参，看一下 `Buffer` 是什么：

```c
char Buffer[128]; // [rsp+20h] [rbp-80h] BYREF
```

长 128 的字符数组，到函数里退化成指针，用 `a1` 表示。把函数改写一下（等价变量类型、转换进制、格式化）：

```c
#include <stdint.h>

uint16_t word_404000[23] = {2849u, 1983u, 2604u, 2603u, 2300u, 2144u,
                            2759u, 2593u, 2030u, 2574u, 2901u, 2565u,
                            2747u, 2306u, 3016u, 3019u, 1791u, 3150u,
                            2632u, 2019u, 2799u, 2599u, 2647u};

int64_t sub_401550(int64_t a1) {
    for (int i = 0; i <= 22; ++i) {
        if (*(unsigned char *)(a1 + i) <= 31u ||
            *(unsigned char *)(a1 + i) > 126u) {
            return 0;
        }

        if (5 * *(uint8_t *)(a1 + (i + 1) % 23) + 3 * *(uint8_t *)(a1 + i) +
                11 * *(uint8_t *)(a1 + (i + 7) % 23) +
                7 * *(uint8_t *)(a1 + (i + 4) % 23) !=
            word_404000[i]) {
            return 0;
        }
    }
    return 1;
}
```

然后拆解第二个判断逻辑：

```c
uint8_t n1 = *(uint8_t *)(a1 + (i + 1) % 23),
        n2 = *(uint8_t *)(a1 + i),
        n3 = *(uint8_t *)(a1 + (i + 7) % 23),
        n4 = *(uint8_t *)(a1 + (i + 4) % 23);

if (5 * n1 + 3 * n2 + 11 * n3 + 7 * n4 != word_404000[i]) {
    return 0;
}
```

`Buffer` 的指针每一 `i` 行都做一次加法，循环后移，`*` 解引用后得到待验证的 23 个根中的某一个（编号取决于 `i` ），存进 `n1` 等等；这样每一行都会因为指针的移动而取到不同的根，这些根分别与 5 、3 、11 、7 做乘法再加起来，验证是否等于预期。那么方程组大概长这样：

```
5x_1 + 3x_0 + 11x_7 + 7x_4 = 2849
5x_2 + 3x_1 + 11x_8 + 7x_5 = 1983
5x_3 + 3x_2 + 11x_9 + 7x_6 = 2604
...
5x_0 + 3x_22 + 11x_6 + 7x_3 = 2647
```

想象一下，把每一行等式里没有出现的根补上，乘以 0 ，这就是线性方程组。

把这个约束题复刻到 Python 里用矩阵做：

```python
import numpy

constraints = numpy.array([
    2849, 1983, 2604, 2603, 2300, 2144,
    2759, 2593, 2030, 2574, 2901, 2565,
    2747, 2306, 3016, 3019, 1791, 3150,
    2632, 2019, 2799, 2599, 2647,
]) # 等式右边 23 行

matrix_order = 23

matrix = numpy.zeros((matrix_order, matrix_order)) # 等式左边 23 阶矩阵

for i in range(matrix_order): # 矩阵第 i 行
    matrix[i][(i + 1) % matrix_order] = 5 # 第多少列取决于伪代码，分别赋那四个值
    matrix[i][i] = 3
    matrix[i][(i + 7) % matrix_order] = 11
    matrix[i][(i + 4) % matrix_order] = 7

solutions = numpy.linalg.solve(matrix, constraints)
rounded_solutions = numpy.round(solutions).astype(int)

flag = ''.join(chr(c) for c in rounded_solutions)

print(flag)
```

得到 flag 为 `0xGame{z3_Se3ms_ezzz2z}` 。