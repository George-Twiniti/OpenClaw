---
name: startup-of-day
description: "Run the day‑start workflow when the user says “good morning” or “good afternoon,” or asks for a startup/standup/ops‑recap. Use to generate a morning continuity brief: where we left off, open loops, first actions, action‑required email + calendar summary, and schedule block suggestions for today. Also use when the user asks to “kickoff the day,” “start of day,” or “daily startup.”"
---

# Startup Of Day

## Overview
Provide MG’s day‑start brief on demand (good morning/afternoon). Pull from memory, Second‑Brain summaries, and run the startup brief script to surface action‑required email + calendar. Include schedule blocks and suggestions for the day.

## Workflow

### 1) Establish “today” context
- If you need current day/time, call `session_status` (timezone: Europe/London).
- Treat **good afternoon** the same as **good morning** (full startup flow).

### 2) Collect continuity inputs
Gather in this order:
1. **Memory**
   - `memory/YYYY-MM-DD.md` for today + yesterday
   - `MEMORY.md` (automation agreements + long‑term context)
2. **Second‑Brain** (if present)
   - `summaries/daily/YYYY-MM-DD.md` (yesterday)
   - `summaries/handoff/YYYY-MM-DD-next.md` (if available)
   - Recent `conv/ai/YYYY-MM-DD.md` if it exists
3. **Startup brief outputs**
   - Run the startup brief script on demand (see step 3) and capture **action‑required emails + calendar**

If a source is missing, proceed and note “not found.”

### 3) Execute startup brief (on demand)
- Run `startup_brief.py` to refresh the email + calendar snapshot for today.
- If it fails, report the error concisely and continue with available data.

### 4) Produce the day‑start brief
Return a single concise brief with the following sections:

1) **Where we left off** (1–4 bullets)
   - Use yesterday’s notes and handoff.

2) **Open loops / blockers** (bulleted list)
   - Include any unresolved decisions, pending approvals, missing info.

3) **First actions today** (top 3–5 actions)
   - Concrete, do‑next tasks.

4) **Action‑required inbox** (from startup brief)
   - List only emails that require action.

5) **Calendar & commitments** (next 24–48h)
   - Summarize upcoming events and constraints.

6) **Schedule blocks + suggestions**
   - Propose 2–4 time blocks (e.g., Deep work, Admin, Calls).
   - Include rationale (e.g., “before 11:00 is free for deep work”).

7) **Top priorities**
   - Explicitly rank the top 1–3 outcomes for today.

8) **Approvals / waiting‑on**
   - Anything blocked by someone else or awaiting a decision.

9) **Bills / finance watch‑outs**
   - Due dates or pending finance actions (if any).

10) **Daily KPI check**
   - A quick health snapshot if available (otherwise note “no KPI feed found”).

11) **Watch‑outs**
   - Risks, deadlines, or “don’t forget” items.

### 5) Ask one tight follow‑up (optional)
If critical info is missing, ask a single clarifying question (e.g., “Do you want me to prioritize X or Y first?”). Otherwise, do not ask questions.

## Style
- Concise, operational, no fluff.
- Use bullets; keep it scannable.
- Assume MG wants clear next actions and schedule guidance.
