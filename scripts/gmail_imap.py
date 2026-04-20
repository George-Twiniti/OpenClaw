#!/usr/bin/env python3
"""Simple Gmail IMAP reader (app password). Read-only by default.

Env vars:
  GMAIL1_EMAIL, GMAIL1_APP_PASSWORD
  GMAIL2_EMAIL, GMAIL2_APP_PASSWORD
Optional:
  GMAIL_LABEL (default: INBOX)
  GMAIL_LIMIT (default: 20)
  GMAIL_QUERY (default: UNSEEN)

Outputs a JSON-ish summary to stdout.
"""
import os
import imaplib
import email
from email.header import decode_header
from datetime import datetime

LABEL = os.getenv("GMAIL_LABEL", "INBOX")
LIMIT = int(os.getenv("GMAIL_LIMIT", "20"))
QUERY = os.getenv("GMAIL_QUERY", "UNSEEN")

accounts = []
for i in (1, 2):
    addr = os.getenv(f"GMAIL{i}_EMAIL")
    pw = os.getenv(f"GMAIL{i}_APP_PASSWORD")
    if addr and pw:
        accounts.append((addr, pw))

if not accounts:
    raise SystemExit("No Gmail accounts configured. Set GMAIL1_EMAIL/GMAIL1_APP_PASSWORD (and optionally GMAIL2_...).")


def decode_header_value(raw):
    if not raw:
        return ""
    parts = decode_header(raw)
    out = []
    for val, enc in parts:
        if isinstance(val, bytes):
            out.append(val.decode(enc or "utf-8", errors="ignore"))
        else:
            out.append(val)
    return "".join(out)


def fetch_account(addr, pw):
    m = imaplib.IMAP4_SSL("imap.gmail.com")
    m.login(addr, pw)
    m.select(LABEL)
    typ, data = m.search(None, QUERY)
    if typ != "OK":
        m.logout()
        return []
    ids = data[0].split()[-LIMIT:]
    messages = []
    for msg_id in reversed(ids):
        typ, msg_data = m.fetch(msg_id, "(RFC822)")
        if typ != "OK":
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_header_value(msg.get("Subject"))
        from_ = decode_header_value(msg.get("From"))
        date_ = msg.get("Date")
        messages.append({
            "id": msg_id.decode(),
            "from": from_,
            "subject": subject,
            "date": date_,
        })
    m.logout()
    return messages


all_msgs = {}
for addr, pw in accounts:
    all_msgs[addr] = fetch_account(addr, pw)

print({
    "ts": datetime.utcnow().isoformat() + "Z",
    "label": LABEL,
    "query": QUERY,
    "accounts": all_msgs,
})
