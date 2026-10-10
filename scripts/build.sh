#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/dist"

cd "$PROJECT_ROOT"
mkdir -p "$OUTPUT_DIR"

python3 scripts/build_week1.py
python3 scripts/build_week2.py

: > "$OUTPUT_DIR/0xgame2026-writeup.md"

i=1
for md_file in "$OUTPUT_DIR"/0xgame2026-writeup-week*.md; do
    printf '\n\n%s\n\n%s\n\n%s\n' "---" "![](../assets/rank-week$i-1.jpg)" "![](../assets/rank-week$i-2.jpg)" >> "$md_file"

    pandoc "$md_file" \
        --standalone \
        --toc \
        --number-sections \
        --number-offset="$((i == 2 ? 1 : 0))" \
        --syntax-highlighting=tango \
        --css=../assets/style.css \
        -o "${md_file%.md}.html"

    weasyprint \
        "${md_file%.md}.html" \
        "${md_file%.md}.pdf"

    cat "$md_file" >> "$OUTPUT_DIR/0xgame2026-writeup.md"
    printf '\n\n' >> "$OUTPUT_DIR/0xgame2026-writeup.md"

    ((i++))
done

pandoc "$OUTPUT_DIR/0xgame2026-writeup.md" \
    --standalone \
    --toc \
    --number-sections \
    --syntax-highlighting=tango \
    --css=../assets/style.css \
    -o "$OUTPUT_DIR/0xgame2026-writeup.html"

weasyprint \
    "$OUTPUT_DIR/0xgame2026-writeup.html" \
    "$OUTPUT_DIR/0xgame2026-writeup.pdf"