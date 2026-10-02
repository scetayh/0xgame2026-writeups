# 四月是你的谎言

> 下一次听见告白时，就在回应里面在告白后面加上晚来的 TOO吧

```bash
scetayh@yuprae-gentoo ~/Projects $ nc nc1.ctfplus.cn 15880
message = YOU DID LIVE IN MY HEART
hash(key+message) = 46af62962126aa38e4f1680a6c64bc6b
please echo the mission in hash(key+message+response)

new longing: TOO
not matter,moon and sun have their next April

```

长 32 ，是 MD5 。因为 MD5 算法决定了 digest 保存了最后的计算状态，所以后加 `TOO` 的时候可以直接从末状态叠加。有一个工具叫 HashPump 专门处理长度拓展攻击，不过 [miekrr](https://github.com/miekrr) 的[仓库](https://github.com/miekrr/HashPump)已经吃灰很久了，在 GitHub 上搜到了一个“时光机器”仓库：

- https://github.com/timb-machine-mirrors/bwall-HashPump

（Owner 有两千七百多个仓库？）

这个仓库有 37 个提交 ahead of miekrr 的，并且使用 Make 组织项目，可以一键编译：

```bash
git clone git@github.com:timb-machine-mirrors/bwall-HashPump.git
cd bwall-HashPump
make -j8
sudo make install
```

看看用法：

```bash
(base) scetayh@yuprae-gentoo ~/Projects $ hashpump --help
HashPump [-h help] [-t test] [-s signature] [-d data] [-a additional] [-k keylength]
     HashPump generates strings to exploit signatures vulnerable to the Hash Length Extension Attack.
     -h --help          Display this message.
     -t --test          Run tests to verify each algorithm is operating properly.
     -s --signature     The signature from known message.
     -d --data          The data from the known message.
     -a --additional    The information you would like to add to the known message.
     -k --keylength     The length in bytes of the key being used to sign the original message with.
     Version 1.2.0 with CRC32, MD5, SHA1, SHA256 and SHA512 support.
     <Developed by bwall(@botnet_hunter)>

```

- `-s 46af62962126aa38e4f1680a6c64bc6b`
- `-d "YOU DID LIVE IN MY HEART"`
- `-a "TOO"`

问题是 key 多长不知道。虽然说可能会很长，把 padding 挤到下一个 block 里，但很大一个范围之内是不会多一个或几个 block 的。可以打一个 `for` 循环试试 1 到 64：

```bash
(base) scetayh@yuprae-gentoo ~/Projects $ for ((i=1; i<=64; i++)); do hashpump -s 46af62962126aa38e4f1680a6c64bc6b -d "YOU DID LIVE IN MY HEART" -a "TOO" -k $i; done
6c05458814ee4a67d990cf4142e755ba
YOU DID LIVE IN MY HEART\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x00TOO
6c05458814ee4a67d990cf4142e755ba
YOU DID LIVE IN MY HEART\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd0\x00\x00\x00\x00\x00\x00\x00TOO
6c05458814ee4a67d990cf4142e755ba
YOU DID LIVE IN MY HEART\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xd8\x00\x00\x00\x00\x00\x00\x00TOO
6c05458814ee4a67d990cf4142e755ba
# ...
```

看起来它会把 padding 也打印出来。`head -n 1` 过滤输出：

```bash
(base) scetayh@yuprae-gentoo ~/Projects $ for ((i=1; i<=64; i++)); do hashpump -s 46af62962126aa38e4f1680a6c64bc6b -d "YOU DID LIVE IN MY HEART" -a "TOO" -k $i | head -n 1; done
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
6c05458814ee4a67d990cf4142e755ba
# ...
6c05458814ee4a67d990cf4142e755ba
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
a211d4ec1611554cdf5231ff14a64263
# ...
a211d4ec1611554cdf5231ff14a64263
```

这两个试了一下都不对。题干里这么说：

> 在回应里面在告白后面加上晚来的 TOO吧

出题的时候并没有严格按照中英文之间加空格的规范写文本，所以这里的空格起到的应该不是视觉作用，而是英文单词分隔符，就是：

```
YOU DID LIVE IN MY HEART TOO
                        ^~~~
```

所以加上空格看看：

```bash
(base) scetayh@yuprae-gentoo ~/Projects $ for ((i=1; i<=64; i++)); do hashpump -s 46af62962126aa38e4f1680a6c64bc6b -d "YOU DID LIVE IN MY HEART" -a " TOO" -k $i | head -n 1; done
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
1577a52a3a88f80645a7e977801ae5d2
...
1577a52a3a88f80645a7e977801ae5d2
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
fb220a2afb2ab78f695678a42f3e30bc
...
fb220a2afb2ab78f695678a42f3e30bc
```

测试第一个就给过了：

```bash
(base) scetayh@yuprae-gentoo ~/Projects $ nc nc1.ctfplus.cn 15880
message = YOU DID LIVE IN MY HEART
hash(key+message) = 46af62962126aa38e4f1680a6c64bc6b
please echo the mission in hash(key+message+response)

new longing: 1577a52a3a88f80645a7e977801ae5d2
0xGame{you lie in April}
```

得到flag `0xGame{you lie in April}` 。