---
name: session-closeout
description: Create concise end-of-session handoff notes and durable memory updates after important work. Use when a session is ending, being reset, or needs to be preserved across sessions; when the user asks to save the previous session better; or when you need a repeatable closeout that writes key facts, open loops, and next steps into memory files.
---

# Session Closeout

Use this skill at the end of meaningful work so the next session can resume cleanly.

## Goal

Preserve durable facts, open loops, and the next action in files instead of relying on chat history.

## What to do

1. Identify durable facts worth keeping:
   - hosts, IPs, SSH aliases, key paths
   - deployed URLs and web roots
   - decisions, preferences, and recurring workflows
   - blockers and next actions

2. Write a short handoff note to today’s `memory/YYYY-MM-DD.md`.
   - Keep it factual and brief.
   - Capture only what the next session needs.

3. Promote long-lived truths to `MEMORY.md`.
   - Keep MEMORY.md for stable facts and recurring agreements.
   - Do not duplicate everything from the daily note.

4. If the work has a project-specific artifact, update it too.
   - e.g. `docs/<project>-plan.md`
   - Put exact paths/URLs there when useful.

## Suggested handoff format

- What was completed
- What was discovered
- What remains open
- Exact next step

## When to use this skill

Use it after:
- deployments
- server discoveries
- workflow changes
- long troubleshooting sessions
- anything that should survive a reset/new session

## Rules

- Be concrete. Include exact paths, URLs, and identifiers.
- Do not write speculative notes as facts.
- Update memory immediately after discovering important infrastructure facts.
- Keep the handoff short enough that a future session can scan it quickly.
