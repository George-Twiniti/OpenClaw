# Oracle Transcript Bridge

## Goal
Enable the Oracle main server and the local transcript worker to exchange transcript jobs and results safely through a simple file-based bridge.

## Files
- Request queue: `~/.openclaw/state/video-transcript-queue.json`
- Results inbox: `~/.openclaw/state/video-transcript-results.jsonl`

## Queue format
```json
{
  "jobs": [
    {
      "id": "job_123",
      "url": "https://www.youtube.com/watch?v=...",
      "title": null,
      "status": "queued",
      "claimedAt": null,
      "completedAt": null,
      "failedAt": null,
      "notes": null,
      "transcript": null
    }
  ]
}
```

## Result format
One JSON object per line in the results inbox:
```json
{
  "jobId": "job_123",
  "url": "https://www.youtube.com/watch?v=...",
  "title": "Video title",
  "transcript": "plain text transcript",
  "status": "completed",
  "notes": null
}
```

## Worker responsibilities
- read queue
- claim next queued job
- extract transcript locally
- append result to results inbox
- update queue status to completed/failed

## Main-server responsibilities
- discover pending YouTube URLs
- enqueue jobs
- watch results inbox
- archive transcript + summary into Second-Brain
- mark jobs archived

## Bridge helper commands
- `node scripts/oracle-transcript-bridge.mjs enqueue <url> [title]`
- `node scripts/oracle-transcript-bridge.mjs collect`

## Notes
- This is intentionally dumb and durable.
- If networking is later added, this contract can stay the same.
