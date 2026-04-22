#!/usr/bin/env bash
set -euo pipefail

ORACLE_SSH="ubuntu@132.145.195.174"
SSH_KEY="$HOME/.ssh/ssh-key-2026-04-10.key"
REMOTE_BASE="/home/ubuntu/.openclaw"
LOCAL_BASE="$HOME/.openclaw/workspace"
TARGET_REPO="$LOCAL_BASE/second-brain"
REMOTE_REPO="$REMOTE_BASE/workspace/second-brain"

# Canonical Oracle output locations we want to mirror into Second-Brain.
REMOTE_FILES=(
  "$REMOTE_REPO/conv/video/**/*.md"
  "$REMOTE_REPO/summaries/video/**/*.md"
  "$REMOTE_REPO/conv/video/**/*.vtt"
)

TMPDIR=$(mktemp -d)
cleanup(){ rm -rf "$TMPDIR"; }
trap cleanup EXIT

# Pull canonical outputs from Oracle.
for pattern in "${REMOTE_FILES[@]}"; do
  ssh -i "$SSH_KEY" "$ORACLE_SSH" "sh -lc 'for f in $pattern; do [ -f \"\$f\" ] && printf \"%s\\n\" \"\$f\"; done'" \
    | while IFS= read -r remote_file; do
        [ -z "$remote_file" ] && continue
        rel="${remote_file#$REMOTE_REPO/}"
        mkdir -p "$TMPDIR/$(dirname "$rel")"
        scp -i "$SSH_KEY" "$ORACLE_SSH:$remote_file" "$TMPDIR/$rel"
      done
done

# If nothing was found, exit quietly.
if ! find "$TMPDIR" -type f | grep -q .; then
  exit 0
fi

cd "$TARGET_REPO"
find "$TMPDIR" -type f | while IFS= read -r f; do
  rel="${f#$TMPDIR/}"
  mkdir -p "$(dirname "$rel")"
  cp "$f" "$rel"
done

git add .
if ! git diff --cached --quiet; then
  git commit -m "capture(ai): oracle telegram export"
  git push
fi
