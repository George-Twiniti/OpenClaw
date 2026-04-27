#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
RUNTIME_DIR="${RUNTIME_DIR:-$HOME/.openclaw/state/startup-brief}"
TMP_DIR="$RUNTIME_DIR/tmp"
OUTPUT_JSON="${STARTUP_BRIEF_OUTPUT:-$RUNTIME_DIR/latest.json}"
SECRETE_FILE="${STARTUP_BRIEF_SECRETE_FILE:-$WORKSPACE/secrets/Secrete.txt}"
OVERRIDE_ENV="$TMP_DIR/startup-brief-overrides.env"
GMAIL_ENV_FILE="${GMAIL_ENV_FILE:-$WORKSPACE/secrets/gmail.env}"
EXCHANGE_ENV_FILE="${EXCHANGE_ENV_FILE:-$WORKSPACE/secrets/exchange.env}"
GMAIL_ICAL_ENV_FILE="${GMAIL_ICAL_ENV_FILE:-$WORKSPACE/secrets/gmail_ical.env}"
GMAIL_IMAP_ENV_FILE="${GMAIL_IMAP_ENV_FILE:-$WORKSPACE/secrets/gmail_imap.env}"

mkdir -p "$TMP_DIR" "$(dirname "$OUTPUT_JSON")"
chmod 700 "$RUNTIME_DIR" "$TMP_DIR"

for secret in "$GMAIL_ENV_FILE" "$EXCHANGE_ENV_FILE" "$GMAIL_ICAL_ENV_FILE"; do
  if [[ ! -f "$secret" ]]; then
    echo "Missing env file: $secret" >&2
    exit 1
  fi
done

if [[ ! -f "$SECRETE_FILE" ]]; then
  echo "Missing override file: $SECRETE_FILE" >&2
  exit 1
fi

export STARTUP_BRIEF_RUNTIME_DIR="$RUNTIME_DIR"
export STARTUP_BRIEF_SECRETE_FILE="$SECRETE_FILE"
export GMAIL_ENV="$GMAIL_ENV_FILE"
export EXCHANGE_ENV="$EXCHANGE_ENV_FILE"
export GMAIL_ICAL_ENV="$GMAIL_ICAL_ENV_FILE"
export GMAIL_IMAP_ENV="${GMAIL_IMAP_ENV_FILE:-$OVERRIDE_ENV}"

if [[ ! -f "$GMAIL_IMAP_ENV" ]]; then
  python3 - "$SECRETE_FILE" "$OVERRIDE_ENV" <<'PY'
import sys
from pathlib import Path
secrete = Path(sys.argv[1])
out = Path(sys.argv[2])
lines = secrete.read_text().splitlines()
content = []
for line in lines:
    if line.startswith('GMAIL1_ICAL_URL=') or line.startswith('GMAIL2_ICAL_URL='):
        content.append(line)
out.write_text('\n'.join(content) + '\n')
out.chmod(0o600)
PY
  export GMAIL_IMAP_ENV="$OVERRIDE_ENV"
fi

python3 "$WORKSPACE/scripts/bills_scan.py"

export STARTUP_BRIEF_OUTPUT="$OUTPUT_JSON"
export STARTUP_BRIEF_RUNTIME_DIR="$RUNTIME_DIR"
python3 "$WORKSPACE/scripts/startup_brief.py"

if [[ -x "$WORKSPACE/scripts/oracle-http-bridge.mjs" ]]; then
  if ! pgrep -f "oracle-http-bridge.mjs" >/dev/null 2>&1; then
    nohup node "$WORKSPACE/scripts/oracle-http-bridge.mjs" >/tmp/oracle-http-bridge.log 2>&1 &
  fi
fi
if [[ -x "$WORKSPACE/scripts/local-http-bridge.mjs" ]]; then
  if ! pgrep -f "local-http-bridge.mjs" >/dev/null 2>&1; then
    nohup node "$WORKSPACE/scripts/local-http-bridge.mjs" >/tmp/local-http-bridge.log 2>&1 &
  fi
fi

if [[ -x "$WORKSPACE/scripts/oracle-bridge-sync.mjs" ]]; then
  node "$WORKSPACE/scripts/oracle-bridge-sync.mjs" status >/dev/null || true
fi
if [[ -x "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" ]]; then
  node "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" drain >/dev/null || true
  node "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" collect >/dev/null || true
fi

echo "Wrote startup brief to $OUTPUT_JSON"
