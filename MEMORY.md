# MEMORY.md

## Automation agreements (rolling)
- OpenClaw config backed up to `~/.openclaw/workspace/backups/config/` after model fix (2026-03-30). Config switched from `ollama/qwen3:8b` to `ollama/qwen3:4b` as primary model; 8B was not installed despite being configured.
- Maintain an “ops recap” after each session and keep this automation-agreements list updated so context persists across sessions. (Agreed 2026-03-16)
- When Computer sends a video, use the `video-transcript-downloader` skill to process the transcript first. (2026-05-13)
- When Computer sends a video, extract the transcript and send the transcript-focused result back to Computer. (2026-05-21)
- Daily startup brief (08:00 Europe/Lisbon) runs `startup_brief.py` (email summary). (Corrected 2026-03-17)
- Daily routine includes: run the startup brief and report on **action‑required** emails + calendar to shape today’s agenda. (Confirmed 2026-03-17)
- Weekly bills scan (Fri 09:00 Europe/Lisbon) runs `bills_scan.py` for SIMAR water, EDP electric, Vodafone; applies to both Gmail accounts. (Confirmed 2026-03-16)
- Pending: set memory embeddings to Ollama (user wants Ollama to avoid OpenAI costs). Need provider+model+baseUrl and reindex. (From 2026-03-15 transcript)
- Second-Brain repo is managed at `/home/george/.openclaw/workspace/second-brain` via SSH; workflow doc defines capture paths and nightly synthesis at 23:00 Lisbon; commit conventions: `capture(ai): YYYY-MM-DD HH:mm`, `synthesis(daily): YYYY-MM-DD`. (From 2026-03-14 transcript)
- Default routing guidance: use local Qwen (Ollama) for quick/low‑stakes/privacy‑sensitive tasks; use cloud (OpenAI) for long‑context, high‑accuracy, complex reasoning, or polished outputs.
- Agent best practices (2026-03-19 video): emphasize agent loop (observe→think→act), define completion criteria in prompts, treat agents as goal→result systems, and start with low‑risk automations while scoping permissions tightly; agent harnesses are interchangeable once the loop is understood.
- OpenClaw backup/secret handling: SOPS+AGE encryption in OpenClaw repo (`George-Twiniti/OpenClaw`) with `.sops.yaml` and encrypted `secrets/*.env`; age private key stored by MG in Bitwarden. Startup-of-day and daily-wrapup skills packaged to `/home/george/.openclaw/workspace/skills/dist` (2026-03-20).
- Startup-of-day now reads calendar iCal URLs from Neon `second-brain.app_settings` (`gmail1_ical_url`, `gmail2_ical_url`) instead of the brittle secret/env chain; verified on 2026-04-09 that Gmail calendar feed entries show correctly, including `Hotel Checkout` and `Flight TP202: EWR to LIS`.
- Repo access note: `George-Twiniti/OpenClaw` is one of the two GitHub repos MG expects me to use (second repo: `George-Twiniti/Second-Brain`).
- Slack Lite integration: target workspace **Twiniti**, channel **#daily-log**; will require a public webhook URL (prefer Cloudflare Tunnel) once gateway is on a public server. Repo path confirmed: `/home/george/.openclaw/workspace/second-brain`. (2026-03-22)
- Best practices (from OpenClaw/Second‑Brain videos): treat the system as **memory + proactivity + tools**; build a **docs‑first support project** for troubleshooting; fully populate AGENTS/SOUL/IDENTITY/USER; maintain MEMORY.md + daily memory logs; enable compaction pre‑flush; use heartbeat + cron for proactivity; design architecture to be **portable across tools**; prefer **principles over rules**; let agents co‑build so they can maintain; treat the brain as **infrastructure** with Postgres as system of record + vector search + graph relationships; expose DB via MCP for agent access. (2026-03-23)
- Infrastructure direction: use the Oracle Ubuntu server (`129.159.181.219`) as the future **24x7 OpenClaw host**; keep Neon/Postgres as the active Second‑Brain operational store for now; Oracle host hardened with SSH key access, sudo password required, UFW enabled (SSH only), fail2ban active, and `~/.openclaw` permissions tightened. (2026-03-23)
- Second-Brain desktop admin app now uses local auth via `app/data/auth.json` or `SB_ADMIN_PASSWORD_HASH`; current dev login is `mg` and the password hash is generated with `npm run auth:hash`. Electron desktop app runs from `/home/george/.openclaw/workspace/second-brain/app` using `npm run dev` for dev mode and `npm start` after `npm run build:renderer`. (2026-04-10)
- Oracle Telegram export now mirrors canonical Second-Brain video paths under `/home/ubuntu/.openclaw/workspace/second-brain/conv/video/...` and `/home/ubuntu/.openclaw/workspace/second-brain/summaries/video/...`; next step is to verify the Oracle writer is saving there. (2026-04-16)
- Telegram video processing should treat the YouTube link as the task anchor and ignore sender metadata/timestamps in the reply; the Telegram reply should be summary-only with no metadata analysis or policy commentary. If warnings still appear, the Oracle Telegram router prompt needs patching. (2026-04-17)
- Two-way Tailnet bridge for transcript jobs was built on 2026-04-23. Oracle bridge base URL: `http://vnic002.taild942c7.ts.net:8787`; local bridge base URL: `http://gbroadbent5-1.taild942c7.ts.net:8788`. The local bridge needed a real `/jobs` API (not just `/status`) before the second claw could use it.
- vnic002.taild942c7.ts.net is the always-on central hub for the claws; Peggy is a node client of vnic002, not the hub.
- Gmail env files were copied to vnic002 on 2026-05-05 at `/home/ubuntu/.openclaw/workspace/secrets/gmail.env` and `/home/ubuntu/.openclaw/workspace/secrets/gmail_ical.env`.
- Session-closeout is the reliable pattern for preserving session state after resets; AEO / wiki / ai-landscape are set up on GitHub and use `dist/` as the production output convention.
- Orphaned OpenClaw transcripts live under `~/.openclaw/agents/main/sessions` as `.jsonl.reset.*` / `.jsonl.deleted.*`; most are heartbeat/no-op churn, but the durable ones carry infrastructure recoveries and should be distilled into memory immediately.
- GitHub push closeout on 2026-04-23 was left incomplete: OpenClaw push was blocked by a secret in history, and Second-Brain push needed a rebase before push.

## 2026-03-13
- Ollama on WSL2 can be installed without sudo by bootstrapping a user-space `zstd` (download `zstd` + `libzstd1` via `apt download`, extract with `dpkg-deb -x`), then extracting `https://ollama.com/download/ollama-linux-amd64.tar.zst` into `~/.local/ollama-user` using `tar --use-compress-program=...zstd -d`. The `.tgz` fallback returns 404. First run generates `~/.ollama/id_ed25519`.
- WSL background reliability: enable systemd via `/etc/wsl.conf` and restart WSL, then run Ollama as a user-level systemd service (`systemctl --user enable --now ollama`).

## 2026-03-15
- MG is CEO of **Twiniti**. Review of two years of AI conversation archives shows recurring focus on AI + digital engineering: digital twins/BIM/EAM, asset lifecycle, data governance, and AI productization (Praxis, Lexi, SignalDesk, Second‑Brain workflows). Also frequent work on marketing/SEO/LinkedIn content and client‑facing materials (pitches, BRDs, decks).
