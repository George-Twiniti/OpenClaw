#!/usr/bin/env bash
set -euo pipefail
msg=${1:-"capture: $(date '+%Y-%m-%d %H:%M')"}

git add .
git commit -m "$msg"
git push
