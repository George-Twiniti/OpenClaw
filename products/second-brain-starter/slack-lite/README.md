# Slack Lite (No n8n)

A minimal Slack → Second‑Brain capture workflow without n8n.

## What it does
- Accepts a Slack webhook (JSON)
- Writes each message to `daily/YYYY-MM-DD-HHMM.md`

## How to use
1) Start the webhook server:

```bash
python3 slack_webhook_server.py --repo /path/to/second-brain --port 8787
```

2) In Slack, create a Workflow:
- Trigger: “Shortcut” or “Message posted”
- Step: “Send a web request”
- URL: `http://<your-ip>:8787/slack`
- Method: POST
- Body: JSON

Suggested JSON body:
```json
{
  "text": "{{message_text}}",
  "user": "{{user_name}}",
  "channel": "{{channel_name}}",
  "ts": "{{message_ts}}"
}
```

## Notes
- Run on a trusted network only. This is a simple local receiver.
- For production, put it behind a private tunnel/VPN.
