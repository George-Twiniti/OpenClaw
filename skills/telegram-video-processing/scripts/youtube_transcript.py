#!/usr/bin/env python3
"""Fetch YouTube auto-captions and output cleaned transcript text.

Usage:
  youtube_transcript.py <youtube_url> <output_txt>

Requires: yt-dlp available in PATH.
"""
import re
import sys
import json
import subprocess
from pathlib import Path


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def sanitize_slug(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-\s]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text[:80] or "video"


def vtt_to_text(vtt_path: Path) -> str:
    text = vtt_path.read_text(encoding="utf-8", errors="ignore")
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or re.match(r"\d+:\d+:\d+\.\d+ -->", line):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        lines.append(line)
    # de-duplicate consecutive lines
    out = []
    prev = None
    for l in lines:
        if l != prev:
            out.append(l)
        prev = l
    clean = " ".join(out)
    # split into readable paragraphs
    sentences = re.split(r"(?<=[.!?])\s+", clean)
    paras = []
    buf = []
    for s in sentences:
        if not s:
            continue
        buf.append(s)
        if len(buf) >= 2:
            paras.append(" ".join(buf))
            buf = []
    if buf:
        paras.append(" ".join(buf))
    return "\n\n".join(paras)


def main():
    if len(sys.argv) != 3:
        print("Usage: youtube_transcript.py <youtube_url> <output_txt>")
        sys.exit(1)
    url = sys.argv[1]
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Get video id + title
    vid = run(["yt-dlp", "--print", "id", url])
    title = run(["yt-dlp", "--print", "title", url])
    slug = sanitize_slug(title)

    tmp_dir = out_path.parent / ".tmp_transcript"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    vtt_path = tmp_dir / f"{vid}.en.vtt"

    # Download auto-subs (English)
    subprocess.check_call([
        "yt-dlp",
        "--write-auto-subs",
        "--sub-lang", "en",
        "--sub-format", "vtt",
        "--skip-download",
        "-o", str(tmp_dir / "%(id)s.%(ext)s"),
        url,
    ])

    if not vtt_path.exists():
        raise SystemExit("No English auto-captions found.")

    transcript = vtt_to_text(vtt_path)
    meta = {
        "id": vid,
        "title": title,
        "slug": slug,
        "url": url,
    }

    out_path.write_text(
        f"# {title}\n\n"
        f"URL: {url}\n"
        f"Video ID: {vid}\n\n"
        f"---\n\n"
        f"{transcript}\n",
        encoding="utf-8",
    )

    # Print JSON metadata for caller use
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
