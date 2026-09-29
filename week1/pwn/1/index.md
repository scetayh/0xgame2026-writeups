# 亦步亦趋

**这道题想得有点简单了。**

在 [**废案**](old/index.md) 的探索基础上，把 `pwn` 拖进 IDA 看看：

![](1.png)

![](2.png)

函数区已经列出了 Level 1 和 Level 2 两个层级的同名函数：

![](3.png)

实际上 Level 1 通过多次 `nc` 都被发现两个地址之间的距离恒为 28 字节，所以不算棘手，用废案里的方法还是能过。下面要解决的是 Level 2 的问题。先双击 `level2` 函数看看：

```asm
; Attributes: bp-based frame

public level2
level2 proc near

var_20= byte ptr -20h

; __unwind {
endbr64
push    rbp
mov     rbp, rsp
sub     rsp, 20h
lea     rax, asc_2048   ; "\n====================================="...
mov     rdi, rax        ; s
call    _puts
lea     rax, aLevel2TheRealC ; "[Level 2] The real challenge: control f"...
mov     rdi, rax        ; s
call    _puts
lea     rax, asc_20B0   ; "======================================="...
mov     rdi, rax        ; s
call    _puts
lea     rax, aThisTimeYouNee ; "This time , you need to change the retu"...
mov     rdi, rax        ; s
call    _puts
lea     rax, win
mov     rsi, rax
lea     rax, format     ; "I have prepared backdoor for you. 'win'"...
mov     rdi, rax        ; format
mov     eax, 0
call    _printf
lea     rax, aNowInputYourFi ; "Now input your final Payload:\n> "
mov     rdi, rax        ; format
mov     eax, 0
call    _printf
lea     rax, [rbp+var_20]
mov     rdi, rax
mov     eax, 0
call    _gets
nop
leave
retn
; } // starts at 1232
level2 endp
```

![](4.png)

按 F5 查看伪代码：

```c
__int64 level2()
{
  _BYTE v1[32]; // [rsp+0h] [rbp-20h] BYREF

  puts(s: "\n==============================================");
  puts(s: "[Level 2] The real challenge: control flow! (Ret2Text)");
  puts(s: "==============================================");
  puts(s: "This time , you need to change the return address");
  printf(format: "I have prepared backdoor for you. 'win', It's addr about: %p\n", win);
  printf(format: "Now input your final Payload:\n> ");
  return gets(a1: v1);
}
```

![](5.png)

这里确实是要打印 `win` 的地址。但是随后要做什么呢？看看 `win` ：

```
; Attributes: bp-based frame

; int win()
public win
win proc near
; __unwind {
endbr64
push    rbp
mov     rbp, rsp
lea     rax, s          ; "Congratulations! You have hijacked the "...
mov     rdi, rax        ; s
call    _puts
lea     rax, command    ; "/bin/sh"
mov     rdi, rax        ; command
call    _system
nop
pop     rbp
retn
; } // starts at 1209
win endp
```

![](6.png)

注释已经证明了系统调用：

```
lea     rax, command    ; "/bin/sh"
```

伪代码也这样显示：

```c
int win()
{
  puts(s: "Congratulations! You have hijacked the control flow!");
  return system(command: "/bin/sh");
}
```

![](7.png)

思路已经明确了，首先更正 [**废案**](old/index.md) 错误，然后拿到 Shell 环境，最后扫盘获取 flag 。

脚本具体编写过程看 [send.sh](send.sh) 。