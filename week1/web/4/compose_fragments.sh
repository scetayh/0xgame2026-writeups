#!/usr/bin/env bash
set -Eeo pipefail
shopt -s inherit_errexit
IFS=$'\n\t'

readonly URL='http://8000-62a68483-e567-4b44-9923-adea1464e2d0.challenge.ctfplus.cn/page?id='

for ((i=1; i<=124; i++)); do
    lin_content="$(curl -sS "$URL"$i | grep '<span class="flag-fragment">')"
    rest=${lin_content#*>}
    fragment=${rest%%<*}
    printf '%s' "$fragment"
done
printf '\n'