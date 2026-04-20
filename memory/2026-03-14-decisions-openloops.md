# 2026-03-14 — Decisions & Open Loops

## Decisions / Agreements
- Second‑Brain repo is managed from `/home/george/.openclaw/workspace/second-brain` (SSH access confirmed).
- Workflow doc (AI_WORKFLOW_OPENCLAW.md) governs capture paths, nightly synthesis target (23:00 Lisbon), and commit conventions.
- OpenClaw should provide morning continuity: where we left off, top open loops, today’s first actions.

## Open Loops / To‑decide
- Auto‑capture of OpenClaw conversations into `conv/ai/YYYY-MM-DD.md` — confirm behavior/implementation.
- Nightly summaries at 23:00 Lisbon — confirm cron + which outputs (daily/category/handoff).
- Auto‑commit + push cadence — confirm per‑capture vs nightly batching.
- Telegram setup continuation — clarify what channel/account is desired and finalize config.
- Memory embeddings via Ollama — finalize model/baseUrl and reindex (now configured to mxbai-embed-large on 127.0.0.1:11434; verify runtime OK).

## Notes
- WSL could not access `C:\Users\george\Documents\second-brain`; repo was pulled from GitHub instead.
