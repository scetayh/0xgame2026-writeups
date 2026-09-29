# Treasure_island

服务器先登进去 `ls` 一圈：

```bash
scetayh@yuprae-gentoo ~ $ ssh player@nc1.ctfplus.cn -p15491
The authenticity of host '[nc1.ctfplus.cn]:15491 ([43.248.116.26]:15491)' can't be established.
ED25519 key fingerprint is: SHA256:IrZ+OtxHi2Cm+EdHLU1Hzxx9P4lH2izPNFVKIxJy3PE
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:4: [nc1.ctfplus.cn]:15968
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[nc1.ctfplus.cn]:15491' (ED25519) to the list of known hosts.
player@nc1.ctfplus.cn's password: 
Welcome to Ubuntu 24.04.5 LTS (GNU/Linux 5.15.0-117-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.

🏝  Welcome to Treasure Island! cd treasure_island to start.
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ls -al
total 40
drwxr-x--- 1 player player 4096 Sep 29 07:28 .
drwxr-xr-x 1 root   root   4096 Sep 27 08:31 ..
-rw-r--r-- 1 player player  220 Mar 31  2024 .bash_logout
-rw-r--r-- 1 player player 3844 Sep 27 08:31 .bashrc
drwx------ 2 player player 4096 Sep 29 07:28 .cache
-rw-r--r-- 1 player player  807 Mar 31  2024 .profile
drwxr-xr-x 1 player player 4096 Sep 29 07:28 treasure_island
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ls -al treasure_island/
total 56
drwxr-xr-x 1 player player  4096 Sep 29 07:28 .
drwxr-x--- 1 player player  4096 Sep 29 07:28 ..
drwxr-xr-x 1 player player  4096 Sep 27 08:43 chest
-rwxr-xr-x 1 player player   215 Sep 27 08:28 clue.txt
-rw-r--r-- 1 player player 25024 Sep 29 07:28 real_map.txt
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ls -al /
total 64
drwxr-xr-x    1 root root 4096 Sep 29 07:28 .
drwxr-xr-x    1 root root 4096 Sep 29 07:28 ..
lrwxrwxrwx    1 root root    7 Apr 22  2024 bin -> usr/bin
drwxr-xr-x    2 root root 4096 Apr 22  2024 boot
drwxr-xr-x    5 root root  360 Sep 29 07:28 dev
drwxr-xr-x    1 root root 4096 Sep 27 08:43 etc
drwxr-xr-x    1 root root 4096 Sep 27 08:31 home
lrwxrwxrwx    1 root root    7 Apr 22  2024 lib -> usr/lib
lrwxrwxrwx    1 root root    9 Apr 22  2024 lib64 -> usr/lib64
drwxr-xr-x    2 root root 4096 Sep 11 02:03 media
drwxr-xr-x    2 root root 4096 Sep 11 02:03 mnt
drwxr-xr-x    1 root root 4096 Sep 27 08:43 opt
dr-xr-xr-x 1793 root root    0 Sep 29 07:28 proc
drwx------    2 root root 4096 Sep 11 02:10 root
drwxr-xr-x    1 root root 4096 Sep 29 07:28 run
lrwxrwxrwx    1 root root    8 Apr 22  2024 sbin -> usr/sbin
drwxr-xr-x    2 root root 4096 Sep 11 02:03 srv
dr-xr-xr-x   13 root root    0 Oct  3  2025 sys
drwxrwxrwt    1 root root 4096 Sep 29 07:28 tmp
drwxr-xr-x    1 root root 4096 Sep 11 02:03 usr
drwxr-xr-x    1 root root 4096 Sep 11 02:10 var
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ 
```

根目录底下没有什么奇形怪状的东西。看看给的两个文件，一个是 `treasure_island/clue.txt` ：

```
The old captain trusted no locks, only numbers.

He spread a thousand chests across the sand,
and left the chart to remember what his chest is called.

Count what the chart keeps, and the count will name the chest.
```

另一个是 `treasure_island/real_map.txt` ： 

```
GOLD cave: 12 paces to the mark
GOLD parrot: 81 paces to the mark
GOLD mast: 98 paces to the mark
GOLD skull: 62 paces to the mark
GOLD mast: 29 paces to the mark
...
GOLD coins: 36 paces to the mark
```

每一行的格式都是：

```
GOLD <ITEM>: <COUNT> paces to the mark
```

此外再 `ls treasure_island/chest/` ：

```
box_000.txt  box_063.txt  box_126.txt  box_189.txt  box_252.txt  box_315.txt  box_378.txt  box_441.txt  box_504.txt  box_567.txt  box_630.txt  box_693.txt  box_756.txt  box_819.txt  box_882.txt  box_945.txt
box_001.txt  box_064.txt  box_127.txt  box_190.txt  box_253.txt  box_316.txt  box_379.txt  box_442.txt  box_505.txt  box_568.txt  box_631.txt  box_694.txt  box_757.txt  box_820.txt  box_883.txt  box_946.txt
box_002.txt  box_065.txt  box_128.txt  box_191.txt  box_254.txt  box_317.txt  box_380.txt  box_443.txt  box_506.txt  box_569.txt  box_632.txt  box_695.txt  box_758.txt  box_821.txt  box_884.txt  box_947.txt
box_003.txt  box_066.txt  box_129.txt  box_192.txt  box_255.txt  box_318.txt  box_381.txt  box_444.txt  box_507.txt  box_570.txt  box_633.txt  box_696.txt  box_759.txt  box_822.txt  box_885.txt  box_948.txt
box_004.txt  box_067.txt  box_130.txt  box_193.txt  box_256.txt  box_319.txt  box_382.txt  box_445.txt  box_508.txt  box_571.txt  box_634.txt  box_697.txt  box_760.txt  box_823.txt  box_886.txt  box_949.txt
box_005.txt  box_068.txt  box_131.txt  box_194.txt  box_257.txt  box_320.txt  box_383.txt  box_446.txt  box_509.txt  box_572.txt  box_635.txt  box_698.txt  box_761.txt  box_824.txt  box_887.txt  box_950.txt
box_006.txt  box_069.txt  box_132.txt  box_195.txt  box_258.txt  box_321.txt  box_384.txt  box_447.txt  box_510.txt  box_573.txt  box_636.txt  box_699.txt  box_762.txt  box_825.txt  box_888.txt  box_951.txt
...
box_062.txt  box_125.txt  box_188.txt  box_251.txt  box_314.txt  box_377.txt  box_440.txt  box_503.txt  box_566.txt  box_629.txt  box_692.txt  box_755.txt  box_818.txt  box_881.txt  box_944.txt
```

船长不信锁新数字；散布了一千个箱子；统计图表 (`real_map.txt`) 里的东西，统计结果就是箱子编号。

我试着直接打开所有箱子内容，看看能不能速通：

```
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ cat treasure_island/chest/box_000.txt 
Empty... just sand and disappointment. (box 000)
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ cat treasure_island/chest/box_001.txt 
Empty... just sand and disappointment. (box 001)
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ cat treasure_island/chest/box_*.txt 
Empty... just sand and disappointment. (box 000)
Empty... just sand and disappointment. (box 001)
Empty... just sand and disappointment. (box 002)
Empty... just sand and disappointment. (box 003)
Empty... just sand and disappointment. (box 004)
...
Empty... just sand and disappointment. (box 728)
Empty... just sand and disappointment. (box 729)
Empty... just sand and disappointment. (box 730)
Empty... just sand and disappointment. (box 731)
Empty... just sand and disappointment. (box 732)
🏆 You found the real treasure chest!

The chest is empty. The gold was moved to /tmp/flag —
but a keeper's heartbeat seals it.

Somewhere on this island a heart keeps beating,
re-locking /tmp/flag with every beat.
Silence the heart, and erase its mark,
or it will never let the gold go.

(ps: the watcher below shows no mercy to half-done work.)
Empty... just sand and disappointment. (box 734)
Empty... just sand and disappointment. (box 735)
Empty... just sand and disappointment. (box 736)
Empty... just sand and disappointment. (box 737)
Empty... just sand and disappointment. (box 738)
...
Empty... just sand and disappointment. (box 999)
```

好像没什么技术含量……

按照 733 号箱子的说法，flag 就在 `/tmp/flag` ，但是有一个什么 heartbeat 一直锁着它。用 `ls -ld` 看看：

```bash
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ls -ld /tmp/flag 
---------- 1 root root 45 Sep 29 07:28 /tmp/flag
```

不仅 `000` 还 `root:root` 。找一下进程：

```bash
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ps aux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.0  0.0   4460  3588 ?        Ss   07:28   0:00 /bin/bash /etc/.flagd/entrypoint.sh
root          15  0.0  0.0   4328  3368 ?        S    07:28   0:00 /bin/bash /etc/.flagd/respawn.sh
root          16  0.1  0.0   4328  3456 ?        S    07:28   0:01 /bin/bash /etc/.flagd/watchdog.sh
root          20  0.0  0.0   4312  2772 ?        S    07:28   0:00 runuser -u player -- env -i /bin/bash /opt/.whisper/heartbeat.sh
player        24  0.0  0.0   4328  3420 ?        S    07:28   0:00 /bin/bash /opt/.whisper/heartbeat.sh
root          27  0.0  0.0  12020  3036 ?        Ss   07:28   0:00 sshd: /usr/sbin/sshd [listener] 0 of 10-100 startups
root         127  0.0  0.0  12524  8952 ?        Ss   07:28   0:00 sshd: player [priv]
player       162  0.0  0.0  12924  6304 ?        S    07:28   0:00 sshd: player@pts/0
player       163  0.0  0.0   5256  4436 pts/0    Ss   07:28   0:00 -bash
root        4500  0.0  0.0   2700  1052 ?        S    07:49   0:00 sleep 60
player      4560  0.0  0.0   2700  1024 ?        S    07:49   0:00 sleep 2
root        4563  0.0  0.0   2700  1176 ?        S    07:49   0:00 sleep 1
player      4564  0.0  0.0   8288  4224 pts/0    R+   07:49   0:00 ps aux
```

可以看到有以下几个关键的 process ：

- `entrypoint.sh`
- `respawn.sh`
- `watchdog.sh`
- `heartbeat.sh`

考虑从源头上消灭 process 的话，`kill` 真的不如 `rm` ，除非有某个进程一直不断地创建脚本（但那是其次才应该该考虑的事情）。所以先删掉有权限的文件 `/opt/.whisper/heartbeat.sh` ：

```bash
rm /opt/.whisper/heartbeat.sh
```

同时杀死我有权限的进程：

```bash
kill 24
```

这个时候看一下 `/tmp/flag` 文件：

```bash
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ ls -ld /tmp/flag 
-r--r--r-- 1 root root 45 Sep 29 07:28 /tmp/flag
```

有权限了，直接读：

```bash
player@dep-7b059bfd-f16a-4d46-8d54-f976d48e73ca-68f74498c6-qmwcg:~$ cat /tmp/flag 
0xGame{82421a06-fab2-4f0d-a9f4-92745953f1e0}
```

所以 flag 就是 `0xGame{82421a06-fab2-4f0d-a9f4-92745953f1e0}` 。