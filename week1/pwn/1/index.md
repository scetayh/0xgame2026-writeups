# 亦步亦趋

**这道题想得有点简单了。**

在 [**废案**](old/index.md) 的探索基础上，把 `pwn` 拖进 IDA 看看：

![](1.png)

![](2.png)

函数区已经列出了 Level 1 和 Level 2 两个层级的同名函数：

![](3.png)

实际上 Level 1 我 `nc` 很多次都发现两个地址之间的距离恒为 28 字节，所以不算棘手，用废案里的方法还是能过。下面要解决的是 Level 2 的问题。先双击 `level2` 函数看看：

![](4.png)

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

