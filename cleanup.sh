#!/usr/bin/env bash

rm -f -- *.html *.pdf

for md_file in *.md; do
    [[ "$md_file" = "README.md" ]] && \
        break

    rm "$md_file"
done