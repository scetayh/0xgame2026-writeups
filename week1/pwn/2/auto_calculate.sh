#!/usr/bin/env bash

HOST=nc1.ctfplus.cn
PORT="$1"

TMP=$(mktemp -d)
IN="$TMP/in"
OUT="$TMP/out"

mkfifo "$IN" "$OUT"

cleanup() {
    kill "$nc_pid" 2>/dev/null
    wait "$nc_pid" 2>/dev/null
    rm -rf "$TMP"
}

trap cleanup EXIT

# FD 3 以读写方式打开 IN FIFO
exec 3<>"$IN"

# nc 的 stdin ← FD 3 ，stdout → OUT FIFO
nc "$HOST" "$PORT" <&3 >"$OUT" &
nc_pid=$!

# 读输入
while IFS= read -r line; do
    printf '%s\n' "$line"

    if [[ $line == calculate:* ]]; then
        # 斩头去尾留中间
        expr=${line#calculate: }
        expr=${expr%% =*}

        # 把不符合规范的运算符号改过来
        expr=${expr//＋/+}
        expr=${expr//一/-}
        expr=${expr//x/*}
        expr=${expr//÷//}

        # bc 计算
        answer=$(printf '%s\n' "$expr" | bc)

        # 输出结果
        printf 'tarikko: %s = %s\n' "$expr" "$answer" # 打印在终端上便于人阅读
        printf '%s\n' "$answer" >&3 # FIFO 传递给另一端提交
    fi
done <"$OUT"

# 善后
exec 3>&-
wait "$nc_pid"