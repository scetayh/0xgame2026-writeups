#!/usr/bin/env bash
set -e

python3 build_week1.py
python3 build_week2.py

: > 0xgame2026-writeup.md

i=1
for md_file in 0xgame2026-writeup-week*.md; do
    printf '\n\n%s\n\n%s\n\n%s\n' "---" "![](rank-week$i-1.jpg)" "![](rank-week$i-2.jpg)" >> "$md_file"

    pandoc "$md_file" \
        --standalone \
        --toc \
        --number-sections \
        --number-offset="$((i == 2 ? 1 : 0))" \
        --syntax-highlighting=tango \
        --css=style.css \
        -o "${md_file%.md}.html"

    weasyprint \
        "${md_file%.md}.html" \
        "${md_file%.md}.pdf"

    cat "$md_file" >> 0xgame2026-writeup.md
    printf '\n\n' >> 0xgame2026-writeup.md

    ((i++))
done

pandoc 0xgame2026-writeup.md \
    --standalone \
    --toc \
    --number-sections \
    --syntax-highlighting=tango \
    --css=style.css \
    -o 0xgame2026-writeup.html

weasyprint \
    0xgame2026-writeup.html \
    0xgame2026-writeup.pdf