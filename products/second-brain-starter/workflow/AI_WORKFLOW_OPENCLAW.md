# OpenClaw + Second Brain Workflow

## Agreed Operating Model

1. Slack remains the ad-hoc capture inbox.
2. Existing n8n Slack processing continues unchanged.
3. OpenClaw captures AI conversations into daily markdown files.
4. OpenClaw prepares category summaries daily.
5. OpenClaw prepares end-of-day summary + tomorrow plan.

## Capture Paths

- Raw AI conversations: `conv/ai/YYYY-MM-DD.md`
- Daily synthesis: `summaries/daily/YYYY-MM-DD.md`
- Category summaries: `summaries/categories/YYYY-MM-DD/<category>.md`
- Next-day handoff: `summaries/handoff/YYYY-MM-DD-next.md`
- Video transcripts: `conv/video/YYYY-MM-DD/<slug>.md`
- Video summaries: `summaries/video/YYYY-MM-DD/<slug>.md`

## Nightly Schedule

- Nightly synthesis target time: **23:00 Europe/Lisbon** (when online)

## Daily Capture Cadence (when 23:00 is offline)

- **Start-of-day catch-up**: on first interaction each day, capture *yesterday’s* conversation blocks.
- **End-of-day closeout**: on last interaction (or on request), capture *today’s* blocks.

## Morning Continuity

At first interaction the next day, OpenClaw should provide:

1. Where we left off yesterday
2. Top open loops
3. Today's first actions

## Video → Transcript → Summary (Telegram)

Workflow:
1. MG sends a video to OpenClaw via Telegram.
2. OpenClaw extracts the transcript and saves it in Second‑Brain.
3. OpenClaw produces a **creator‑ready summary** optimized for:
   - PowerPoint slide creation
   - LinkedIn/Substack posts
   - Cross‑video synthesis and thematic aggregation

Summary requirements:
- Not just facts; include insights, implications, and framing that support writing and slide‑building.
- Highlight standout quotes, actionable takeaways, and suggested angles.

## Data Contract (per captured conversation block)

```markdown
### [2026-02-18T23:01:00+00:00] source=openclaw channel=webchat session=agent:main:main id=<id>
**User**
...

**Assistant**
...

**Tags**: #ai #workflow
```

## Tagging Rules

- Always include a **Tags** line in daily summaries, video summaries, and captured conversation blocks.
- Use short, consistent tags to enable retrieval. Core tags:
  - `#ai` `#video` `#workflow` `#research` `#product` `#strategy` `#book` `#writing`
- Add 1–3 topic‑specific tags when obvious (e.g., `#autores`, `#ollama`, `#openclaw`).

## Commit Convention

- Capture commits: `capture(ai): YYYY-MM-DD HH:mm`
- Synthesis commits: `synthesis(daily): YYYY-MM-DD`
