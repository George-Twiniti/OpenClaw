#!/usr/bin/env python3
"""Fetch transcripts via Firecrawl and output transcript text.

Usage:
  youtube_transcript.py <video_url> <output_txt>

Requires: Firecrawl CLI available in PATH.
"""
import re
import sys
import json
import subprocess
import shutil
import tempfile
from pathlib import Path


def run(cmd):
    return subprocess.check_output(cmd, text=True).strip()


def resolve_firecrawl() -> str:
    exe = shutil.which("firecrawl")
    if not exe:
        raise SystemExit("missing Firecrawl CLI; install it and ensure `firecrawl` is on PATH")
    return exe


def sanitize_slug(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\-\s]", "", text)
    text = re.sub(r"\s+", "-", text).strip("-")
    return text[:80] or "video"


def extract_transcript(markdown: str) -> str:
    if not markdown:
        return ""
    patterns = [
        r"(?ms)^## Transcript\s*\n(?P<body>.*?)(?=\n##\s+|\Z)",
        r"(?ms)^### Transcript\s*\n(?P<body>.*?)(?=\n###\s+|\n##\s+|\Z)",
    ]
    for pattern in patterns:
        m = re.search(pattern, markdown)
        if m:
            body = m.group("body").strip()
            if body:
                return body
    return ""


def main():
    if len(sys.argv) != 3:
        print("Usage: youtube_transcript.py <youtube_url> <output_txt>")
        sys.exit(1)
    url = sys.argv[1]
    out_path = Path(sys.argv[2])
    out_path.parent.mkdir(parents=True, exist_ok=True)

    firecrawl = resolve_firecrawl()

    with tempfile.NamedTemporaryFile(prefix="firecrawl-transcript-", suffix=".json", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    actions = [
        {"type": "wait", "milliseconds": 7000},
        {
            "type": "executeJavascript",
            "script": "(()=>{ const b=[...document.querySelectorAll(\"button\")].find(el=>((el.getAttribute(\"aria-label\")||el.innerText||\"\").includes(\"Transcript\"))); if (b) { b.click(); return \"clicked\"; } return \"missing\"; })()",
        },
        {"type": "wait", "milliseconds": 5000},
    ]

    try:
        subprocess.run(
            [
                firecrawl,
                "scrape",
                url,
                "--actions",
                json.dumps(actions),
                "--format",
                "markdown",
                "--only-main-content",
                "--json",
                "-o",
                str(tmp_path),
            ],
            check=True,
            text=True,
        )

        payload = json.loads(tmp_path.read_text(encoding="utf-8"))
    finally:
        tmp_path.unlink(missing_ok=True)

    markdown = payload.get("markdown", "")
    metadata = payload.get("metadata", {}) if isinstance(payload.get("metadata", {}), dict) else {}
    title = metadata.get("title") or url
    slug = sanitize_slug(title)
    vid = metadata.get("identifier") or metadata.get("videoId") or metadata.get("id") or slug

    transcript = extract_transcript(markdown) or "No transcript found."

    meta = {"id": vid, "title": title, "slug": slug, "url": url}

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
