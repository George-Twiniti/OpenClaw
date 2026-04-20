---
name: daily-wrapup
description: Review, run, or audit the Second‑Brain daily wrap‑up workflow (daily synthesis, end‑of‑day summary, next‑day handoff). Trigger when the user says “wrap up today” or “end of day,” or asks for a daily wrap up, end‑of‑day recap, nightly synthesis, or to verify/repair the daily summary pipeline and its outputs in the Second‑Brain repo.
---

# Daily Wrapup

## Overview
Produce and validate the Second‑Brain daily wrap‑up outputs (daily synthesis + handoff), using the agreed workflow, paths, and tagging rules.

## Workflow

### 1) Load the spec
Read `references/daily-wrapup-spec.md` for the source‑of‑truth paths, schedule, and formatting rules.

### 2) Gather source material
- Prefer `second-brain/daily/YYYY-MM-DD*.md` if it exists (for the daily agent).
- Otherwise, use `second-brain/conv/ai/YYYY-MM-DD.md` for the requested day/week.
- Pull **email** inputs (Exchange + Gmail) from available daily/startup brief outputs.
- Pull **.specstory** notes from `C:/Users/George/source/<application>/.specstory` when relevant.
- If the user asks to “scan transcripts,” search recent `conv/ai/` files and extract relevant snippets.

### 3) Produce the wrap‑up
Create or update:
- Daily synthesis (`summaries/daily/YYYY-MM-DD.md`)
- **End‑of‑day wrap‑up** (`summaries/eod/YYYY-MM-DD.md`)
- Next‑day handoff (`summaries/handoff/YYYY-MM-DD-next.md`)

Follow the formatting rules from the spec, including **Tags** lines.

### 4) If automation is requested
Use `second-brain/scripts/daily-agent.js` when daily logs exist and the user wants the automated path. Note the script writes to `summaries/` (not `summaries/daily/`), so fix or move output if needed.

### 5) Validate & report
- Confirm files were written to the correct paths.
- Summarize what changed and any gaps (missing daily logs, missing tags, etc.).
