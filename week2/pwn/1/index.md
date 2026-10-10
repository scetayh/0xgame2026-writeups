# 笼中鸟

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/1 $ nc nc1.ctfplus.cn 26454
hacker , do you know what is canary ?
Tell me what's your name?
scetayh
Hello , nice to meet you. scetayh
This time , I won't give you the backdoor.
 What can you do ?
nothing
Congratulations!
```

看看 IDA ：

```c
int __fastcall main(int argc, const char **argv, const char **envp)
{
  __int64 v4; // [rsp+8h] [rbp-18h] BYREF
  __int64 v5; // [rsp+10h] [rbp-10h]
  unsigned int seed[2]; // [rsp+18h] [rbp-8h]

  *(_QWORD *)seed = time(timer: nullptr);
  srand(seed: seed[0]);
  v5 = rand();
  v4 = 0;
  init(a1: &v4, a2: v5);
  vuln();
  return 0;
}
```

```c
__int64 __fastcall init(__int64 a1, __int64 a2)
{
  setvbuf(stream: stdin, buf: nullptr, modes: 2, n: 0);
  setvbuf(stream: stdout, buf: nullptr, modes: 2, n: 0);
  setvbuf(stream: stderr, buf: nullptr, modes: 2, n: 0);
  global_canary = a1 ^ a2;
  return a1 ^ a2;
}
```

伪代码显示构造了一个随机 canary 。

`vuln` ：

```c
int vuln()
{
  char s[40]; // [rsp+0h] [rbp-30h] BYREF
  __int64 v2; // [rsp+28h] [rbp-8h]

  v2 = global_canary;
  memset(s, c: 0, n: sizeof(s));
  puts(s: "hacker , do you know what is canary ?");
  puts(s: "Tell me what's your name?");
  read(fd: 0, buf: s, nbytes: 0x28u);           // 0x28 = 40 bytes
  printf(format: "Hello , nice to meet you. %s", s);
  puts(s: "This time , I won't give you the backdoor.\n What can you do ?");
  read(fd: 0, buf: s, nbytes: 0x40u);           // 0x40 = 64 bytes
  if ( v2 != global_canary )
  {
    puts(s: "All , you don't know what is canary.");
    puts(s: "YOU FAIL!!!");
    exit(status: -1);
  }
  return puts(s: "Congratulations!");
}
```

Stack 大概是：

- saved RBP
- `v2` (8 bytes)
- `s` (0x28 = 40 bytes)

它验证 `v2` 是否与 `global_canary` 相同，阻碍攻击者使用栈溢出。利用这两句：

```c
  read(fd: 0, buf: s, nbytes: 0x28u);           // 0x28 = 40 bytes
  printf(format: "Hello , nice to meet you. %s", s);
```

由于 `read` 不会在字符串末尾补 `\0` ，如果将 40 bytes 末尾填充为 `A` ，`printf` 就有可能越过 40 bytes 读到 `v2` canary ，从而泄露 canary 内容。

如果覆盖多了就会……

```bash
(sage) scetayh@yuprae-gentoo ~/Projects/0xgame2026-writeups/week2/pwn/1 $ nc nc1.ctfplus.cn 26454
hacker , do you know what is canary ?
Tell me what's your name?
ScetayhChan's_Edenic_Territory_Arouse_Yearning_Hearts
Hello , nice to meet you. ScetayhChan's_Edenic_Territory_Arouse_Ye�g�j�This time , I won't give you the backdoor.
 What can you do ?
Congratulations!
```

所以必须发送 40 bytes 。接下来第二次 `read` ：

```c
  read(fd: 0, buf: s, nbytes: 0x40u);           // 0x40 = 64 bytes
```

只要保证第 41 至 48 字节仍然写原来的 canary ，canary 检查就会通过。接下来就能够布置 ROP 。

脚本如下：

```python

```