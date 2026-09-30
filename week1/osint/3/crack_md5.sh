#!/usr/bin/env bash

target=fcfae8501b64417c529ba930fe683bb8
x_start=13374069
x_end=13375183
y_start=3516567
y_end=3518338

total=$(( ( x_end - x_start + 1 ) * ( y_end - y_start + 1 ) ))

count=0

for ((x=x_start; x<=x_end; x++)); do
    for ((y=y_start; y<=y_end; y++)); do
        printf -v flag '0xGame{%s,%s}' $x $y
        hash=$(printf '%s' "$flag" | md5sum | awk '{print $1}')

        echo "$flag $hash $count/$total"

        [[ $hash = "$target" ]] && \
            exit 0

        ((count++))
    done
done