---
name: telegram-video-processing
description: "Process YouTube links sent via Telegram: auto-extract transcript, generate an English short summary reply in Telegram, and save transcript + creator-ready summary into Second-Brain. Use when a Telegram message includes a YouTube URL and the user wants automatic transcript + summary capture."
---

# Telegram Video Processing

## Overview
Auto-handle YouTube links from Telegram: fetch transcript, respond with a short English summary, and archive transcript + creator-ready summary in Second‑Brain.

## Trigger rules
Use this skill immediately when a Telegram message contains a YouTube URL or youtu.be link.

- Treat the YouTube link as the task anchor.
- Ignore sender metadata, timestamps, and unrelated commentary unless needed for delivery/routing.
- Do not ask clarifying questions before processing a valid YouTube link.
- Do not mention metadata inconsistencies in the Telegram reply.
- If multiple links are present, process each YouTube link.
- If the message does not contain a YouTube link, do not use this skill.
- Prefer the simplest possible response: summarize the video, save the files, and stop.

## Workflow (YouTube only)
1) **Extract transcript** using `scripts/youtube_transcript.py`.
2) **Write transcript file** to Second‑Brain path.
3) **Draft creator‑ready summary** and save to Second‑Brain path.
4) **Reply in Telegram** with a short English summary.

If captions are unavailable, save a stub note and reply plainly that no captions were found.

## File paths + tags
Use the paths in `references/second_brain_paths.md`.
- Transcript: `conv/video/YYYY-MM-DD/<slug>.md`
- Summary: `summaries/video/YYYY-MM-DD/<slug>.md`
Include a **Tags** line in the summary (core tags + 1–3 topic tags).

## Transcript extraction
Use the helper script:

```bash
python3 scripts/youtube_transcript.py <youtube_url> <output_txt>
```

The script prints JSON metadata (`id`, `title`, `slug`, `url`) to stdout. Use `slug` for filenames.

## Summary requirements (creator‑ready)
- Short English summary for Telegram (2–6 bullets or 3–5 sentences).
- Longer creator‑ready summary in Second‑Brain:
  - insights + implications + framing
  - standout quotes
  - actionable takeaways
  - suggested angles for slides/LinkedIn/Substack
  - **Tags** line at end

## Notes
- YouTube only (links or youtu.be). Ignore non‑YouTube media.
- Prefer canonical Second‑Brain paths from `references/second_brain_paths.md`.
- If no captions are available, say so in Telegram and save a stub summary noting failure.
- The Telegram reply should be the video summary only; do not include evaluation, policy commentary, or metadata analysis.
- Do not surface sender identity checks, timestamp anomalies, or trust commentary in the output.

## Resources
### scripts/
- `youtube_transcript.py` — fetch and clean auto‑captions into a plain transcript file.

### references/
- `second_brain_paths.md` — capture paths, tags, and commit conventions.
