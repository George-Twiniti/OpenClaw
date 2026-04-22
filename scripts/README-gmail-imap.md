# Gmail IMAP (App Password) — Read‑only setup

This is a custom Gmail reader using IMAP + app passwords.

## 1) Enable IMAP in Gmail
Gmail → Settings → Forwarding and POP/IMAP → **Enable IMAP**.

## 2) Create app passwords
Google Account → Security → App passwords.

## 3) Store secrets locally (do not paste in chat)
Create a local secrets file:

```
mkdir -p /home/george/.openclaw/workspace/secrets
chmod 700 /home/george/.openclaw/workspace/secrets

cat > /home/george/.openclaw/workspace/secrets/gmail.env <<'EOF'
GMAIL1_EMAIL=georgebroadbent67@gmail.com
GMAIL1_APP_PASSWORD=PASTE_APP_PASSWORD_1
GMAIL2_EMAIL=xbr350@gmail.com
GMAIL2_APP_PASSWORD=PASTE_APP_PASSWORD_2
GMAIL_LABEL=INBOX
GMAIL_QUERY=UNSEEN
GMAIL_LIMIT=20
EOF

chmod 600 /home/george/.openclaw/workspace/secrets/gmail.env
```

## 4) Run
```
set -a; source /home/george/.openclaw/workspace/secrets/gmail.env; set +a
python3 /home/george/.openclaw/workspace/scripts/gmail_imap.py
```

Outputs a JSON-ish summary of unread messages.

## Notes
- Read‑only; does not send or modify mail.
- Adjust GMAIL_QUERY for other searches (e.g., ALL, FROM "foo", SUBJECT "bar").
