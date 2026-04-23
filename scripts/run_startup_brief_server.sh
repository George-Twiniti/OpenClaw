#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${WORKSPACE:-$HOME/.openclaw/workspace}"
RUNTIME_DIR="${RUNTIME_DIR:-$HOME/.openclaw/state/startup-brief}"
TMP_DIR="$RUNTIME_DIR/tmp"
OUTPUT_JSON="${STARTUP_BRIEF_OUTPUT:-$RUNTIME_DIR/latest.json}"
AGE_KEY_FILE="${SOPS_AGE_KEY_FILE:-$HOME/.openclaw/keys/age.key}"
SECRETE_FILE="${STARTUP_BRIEF_SECRETE_FILE:-$WORKSPACE/secrets/Secrete.txt}"
OVERRIDE_ENV="$TMP_DIR/startup-brief-overrides.env"

mkdir -p "$TMP_DIR" "$(dirname "$OUTPUT_JSON")"
chmod 700 "$RUNTIME_DIR" "$TMP_DIR"

if [[ ! -f "$AGE_KEY_FILE" ]]; then
  echo "Missing AGE key: $AGE_KEY_FILE" >&2
  exit 1
fi

for secret in gmail.env exchange.env gmail_ical.env; do
  if [[ ! -f "$WORKSPACE/secrets/$secret" ]]; then
    echo "Missing encrypted secret: $WORKSPACE/secrets/$secret" >&2
    exit 1
  fi
done

if [[ ! -f "$SECRETE_FILE" ]]; then
  echo "Missing override file: $SECRETE_FILE" >&2
  exit 1
fi

if ! command -v sops >/dev/null 2>&1; then
  echo "sops is required but not installed" >&2
  exit 1
fi

export SOPS_AGE_KEY_FILE="$AGE_KEY_FILE"
export SOPS_CONFIG="$WORKSPACE/.sops.yaml"
export STARTUP_BRIEF_RUNTIME_DIR="$RUNTIME_DIR"
export STARTUP_BRIEF_SECRETE_FILE="$SECRETE_FILE"

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
content.append('GMAIL1_EMAIL=georgebroadbent67@gmail.com')
content.append('GMAIL1_APP_PASSWORD=exleeeapffivwqri')
content.append('GMAIL2_EMAIL=xbr350@gmail.com')
content.append('GMAIL2_APP_PASSWORD=vhszuarvdjmfveov')
out.write_text('\n'.join(content) + '\n')
out.chmod(0o600)
PY

export GMAIL1_EMAIL=georgebroadbent67@gmail.com
export GMAIL1_APP_PASSWORD=exleeeapffivwqri
export GMAIL2_EMAIL=xbr350@gmail.com
export GMAIL2_APP_PASSWORD=vhszuarvdjmfveov
export GMAIL1_ICAL_URL="https://calendar.google.com/calendar/ical/xbr350%40gmail.com/private-f10c3f0c11fd696021bc1364c5d3ce25/basic.ics"
export GMAIL2_ICAL_URL="https://calendar.google.com/calendar/ical/georgebroadbent67%40gmail.com/private-79ba5515b899207d72190cb7963b69f2/basic.ics"
export GMAIL_ENV="$WORKSPACE/secrets/gmail.env"
export EXCHANGE_ENV="$WORKSPACE/secrets/exchange.env"
export GMAIL_ICAL_ENV="$WORKSPACE/secrets/gmail_ical.env"
export GMAIL_IMAP_ENV="$OVERRIDE_ENV"
python3 "$WORKSPACE/scripts/bills_scan.py"

export STARTUP_BRIEF_OUTPUT="$OUTPUT_JSON"
export STARTUP_BRIEF_RUNTIME_DIR="$RUNTIME_DIR"
python3 "$WORKSPACE/scripts/startup_brief.py"

if [[ -x "$WORKSPACE/scripts/oracle-bridge-sync.mjs" ]]; then
  node "$WORKSPACE/scripts/oracle-bridge-sync.mjs" status >/dev/null || true
fi
if [[ -x "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" ]]; then
  node "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" drain >/dev/null || true
  node "$WORKSPACE/scripts/oracle-transcript-bridge.mjs" collect >/dev/null || true
fi

echo "Wrote startup brief to $OUTPUT_JSON"
