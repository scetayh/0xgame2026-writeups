#!/usr/bin/env bash

python3 build_week1.py

i=1
for md_file in *.md; do
    [[ "$md_file" = "README.md" ]] && \
        break
    printf '%s\n\n%s\n\n%s' "---" "![](rank-week$i-1.png)" "![](rank-week$i-2.png)" >> "$md_file"

    pandoc "$md_file" \
        --standalone \
        --toc \
        --number-sections \
        --highlight-style=tango \
        --css=style.css \
        -o "${md_file%.md}.html"
    ((i++))
done

for html_file in *.html; do
    weasyprint \
        "$html_file" \
        "${html_file%.html}.pdf"
done