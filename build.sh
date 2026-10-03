#!/usr/bin/env bash

python3 build_week1.py

for md_file in *.md; do
    [[ "$md_file" = "README.md" ]] && \
        break

    pandoc "$md_file" \
        --standalone \
        --toc \
        --number-sections \
        --highlight-style=tango \
        --css=style.css \
        -o "${md_file%.md}.html"
done

for html_file in *.html; do
    weasyprint \
        "$html_file" \
        "${html_file%.html}.pdf"
done