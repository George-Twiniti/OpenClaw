#!/usr/bin/env python3
"""Create a new capture file from a template.
Usage: new_capture.py <type> <title>
Types: ai | meeting | idea | research
"""
import sys, os, re
from datetime import datetime
from pathlib import Path

type_map = {
    "ai": "capture_ai.md",
    "meeting": "capture_meeting.md",
    "idea": "capture_idea.md",
    "research": "capture_research.md",
}

if len(sys.argv) < 3:
    print("Usage: new_capture.py <type> <title>")
    sys.exit(1)

cap_type = sys.argv[1].lower()
if cap_type not in type_map:
    print(f"Unknown type: {cap_type}")
    sys.exit(1)

title = " ".join(sys.argv[2:]).strip()
slug = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-").lower()

today = datetime.now().strftime("%Y-%m-%d")

root = Path.cwd()

target_dir = {
    "ai": root / "conv" / "ai",
    "meeting": root / "conv" / "meetings",
    "idea": root / "conv" / "ideas",
    "research": root / "conv" / "research",
}[cap_type]

target_dir.mkdir(parents=True, exist_ok=True)

src = Path(__file__).resolve().parent.parent / "templates" / type_map[cap_type]
content = src.read_text()
content = content.replace("{{YYYY-MM-DD}}", today)
content = content.replace("{{short title}}", title)
content = content.replace("{{one‑line description}}", title)
content = content.replace("{{research question}}", title)

outfile = target_dir / f"{today}_{slug}.md"
if outfile.exists():
    print(f"File exists: {outfile}")
    sys.exit(1)

outfile.write_text(content)
print(outfile)
