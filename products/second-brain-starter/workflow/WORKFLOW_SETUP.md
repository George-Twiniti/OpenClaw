# Workflow Setup Guide

This package includes **three workflows**:

1) **Daily Summary (GitHub Action)**
   - File: `daily-agent.yml`
   - Runs on a schedule to generate `summaries/daily/YYYY-MM-DD.md`

2) **Daily Category Summary Agent**
   - File: `daily-agent.js`
   - Node script run by the GitHub Action

3) **Slack → Second‑Brain (n8n)**
   - File: `Slack-SignalDesk-Github.sanitized.json`
   - Captures Slack messages into your Second‑Brain (daily logs), routes high‑value items to SignalDesk, and creates Notion entries.

---

## A) Daily Summary + Category Summary (GitHub Actions)

1. Copy `daily-agent.yml` into your repo: `.github/workflows/`
2. Copy `daily-agent.js` into your repo: `scripts/`
3. Add repo secret: `OPENAI_API_KEY`
4. Trigger the workflow (manual or scheduled)

**Output:**
- `summaries/daily/YYYY-MM-DD.md`

---

## B) Slack → Second‑Brain (n8n)

1. Import the sanitized JSON into n8n:
   - Settings → Import Workflow
   - Select `Slack-SignalDesk-Github.sanitized.json`

2. Replace placeholders with your credentials:
   - Slack OAuth
   - Notion API key
   - SignalDesk token
   - GitHub OAuth

3. Update database IDs and channel IDs:
   - Replace the Notion DB IDs in the “Config” node
   - Update the Slack channel ID in the Slack Trigger

4. Activate the workflow

**Notes:**
- The export has been sanitized: all secrets are placeholders.
- You must configure credentials in your own n8n instance.

---

If you want a fully OpenClaw‑native Slack capture workflow, we can provide an OpenClaw variant in a future update.
