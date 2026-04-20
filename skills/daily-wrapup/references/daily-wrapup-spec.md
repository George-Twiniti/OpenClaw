# Daily Wrapup — Second‑Brain Spec (OpenClaw)

## Source of truth
Primary workflow doc: `/home/george/.openclaw/workspace/second-brain/AI_WORKFLOW_OPENCLAW.md`

## Capture paths
- Raw AI conversations: `second-brain/conv/ai/YYYY-MM-DD.md`
- Daily synthesis: `second-brain/summaries/daily/YYYY-MM-DD.md`
- **End‑of‑day wrap‑up**: `second-brain/summaries/eod/YYYY-MM-DD.md`
- Next‑day handoff: `second-brain/summaries/handoff/YYYY-MM-DD-next.md`
- Category summaries: `second-brain/summaries/categories/YYYY-MM-DD/<category>.md`
- Video transcripts: `second-brain/conv/video/YYYY-MM-DD/<slug>.md`
- Video summaries: `second-brain/summaries/video/YYYY-MM-DD/<slug>.md`

## Schedule & cadence
- Nightly synthesis target: **23:00 Europe/Lisbon** when online.
- If 23:00 was offline:
  - Start‑of‑day catch‑up: capture *yesterday’s* conversation blocks on first interaction.
  - End‑of‑day closeout: capture *today’s* blocks on last interaction or on request.

## Morning continuity
At first interaction the next day, include:
1. Where we left off yesterday
2. Top open loops
3. Today’s first actions
4. Reference yesterday’s **end‑of‑day wrap‑up** (`summaries/eod/YYYY-MM-DD.md`)

## Daily summary generator (script)
`second-brain/scripts/daily-agent.js` (Node v18+). Usage:
```
node daily-agent.js --repo "/home/george/.openclaw/workspace/second-brain" --model "gpt-4o-mini" --commit
```
- Reads `second-brain/daily/YYYY-MM-DD*.md`
- Writes `second-brain/summaries/YYYY-MM-DD.md` (note: script writes to `summaries/`, not `summaries/daily/`)
- Can create stub files in `entities/`, `projects/`, `ideas/`, `reference/`

## End‑of‑day wrap‑up content (minimum)
Include at least:
1. What happened today (3–7 bullets)
2. Decisions
3. Open loops / blockers
4. Progress by project
5. Tomorrow’s first actions (1–3)
6. Notable inputs (emails, calendar, .specstory notes, convo snippets)
7. Tags

If `.specstory` is present, summarize the newest relevant development log(s) per project into the wrap-up, even when the file timestamp rolls past midnight. This is mandatory for the daily wrap-up.

## Sources to include
- `second-brain/conv/ai/YYYY-MM-DD.md`
- `second-brain/daily/YYYY-MM-DD*.md` (if present)
- **.specstory** notes from `C:/Users/George/source/<application>/.specstory` (capture the latest per-project development log so second-brain reflects work done; this is a required part of the daily wrap-up, not an optional extra)
- **Email**: Exchange + Gmail **action‑required summaries only** (subject + next step), from startup brief / mail scan outputs

## Output formatting rules
- Include **Tags** line in daily summaries, end‑of‑day wrap‑ups, and captured conversation blocks.
- Core tags: `#ai` `#video` `#workflow` `#research` `#product` `#strategy` `#book` `#writing`
- Add 1–3 topic‑specific tags when obvious.

## Commit conventions
- Capture commits: `capture(ai): YYYY-MM-DD HH:mm`
- Synthesis commits: `synthesis(daily): YYYY-MM-DD`
