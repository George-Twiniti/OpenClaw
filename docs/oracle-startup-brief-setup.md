# Oracle server startup brief setup

Goal: run the startup brief on the Oracle host, not locally, and persist a readable artifact for morning brief / heartbeat use.

## Files involved
- Wrapper: `scripts/run_startup_brief_server.sh`
- Core scripts:
  - `scripts/startup_brief.py`
  - `scripts/bills_scan.py`
- Secrets:
  - `secrets/gmail.env` (encrypted with SOPS)
  - `secrets/gmail_imap.env` (optional plaintext override)
  - `secrets/exchange.env`
  - `secrets/gmail_ical.env`
- AGE key on server:
  - `~/.openclaw/keys/age.key`

## Server-side output
- JSON artifact:
  - `~/.openclaw/state/startup-brief/latest.json`

## Expected server prerequisites
- OpenClaw workspace present at `~/.openclaw/workspace`
- `python3` installed
- `sops` installed
- AGE private key present at `~/.openclaw/keys/age.key`
- Secret files copied to `~/.openclaw/workspace/secrets/`

## Manual test on server
```bash
bash ~/.openclaw/workspace/scripts/run_startup_brief_server.sh
cat ~/.openclaw/state/startup-brief/latest.json
```

## Cron example on server
```cron
0 8 * * * TZ=Europe/Lisbon bash /home/ubuntu/.openclaw/workspace/scripts/run_startup_brief_server.sh >> /home/ubuntu/.openclaw/state/startup-brief/cron.log 2>&1
```

## Notes
- `startup_brief.py` now supports env overrides:
  - `GMAIL_ENV`
  - `GMAIL_IMAP_ENV`
  - `EXCHANGE_ENV`
  - `GMAIL_ICAL_ENV`
  - `STARTUP_BRIEF_OUTPUT`
- `bills_scan.py` now supports `GMAIL_ENV`, so the decrypted temp env path actually works.
- Once the artifact exists on the server, morning checks should prefer reading it instead of re-running the script interactively.
