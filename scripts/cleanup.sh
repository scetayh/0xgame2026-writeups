#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT_DIR="$PROJECT_ROOT/dist"

rm -f -- \
    "$OUTPUT_DIR/0xgame2026-writeup.md" \
    "$OUTPUT_DIR/0xgame2026-writeup.html" \
    "$OUTPUT_DIR/0xgame2026-writeup.pdf" \
    "$OUTPUT_DIR/0xgame2026-writeup-week1.md" \
    "$OUTPUT_DIR/0xgame2026-writeup-week1.html" \
    "$OUTPUT_DIR/0xgame2026-writeup-week1.pdf" \
    "$OUTPUT_DIR/0xgame2026-writeup-week2.md" \
    "$OUTPUT_DIR/0xgame2026-writeup-week2.html" \
    "$OUTPUT_DIR/0xgame2026-writeup-week2.pdf"