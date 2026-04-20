#!/usr/bin/env python3
"""Create daily synthesis + handoff stubs for today."""
from datetime import datetime, timedelta
from pathlib import Path

root = Path.cwd()

today = datetime.now()
next_day = today + timedelta(days=1)

synth_dir = root / "summaries" / "daily"
handoff_dir = root / "summaries" / "handoff"

synth_dir.mkdir(parents=True, exist_ok=True)
handoff_dir.mkdir(parents=True, exist_ok=True)

synth_tpl = (Path(__file__).resolve().parent.parent / "templates" / "daily_synthesis.md").read_text()
handoff_tpl = (Path(__file__).resolve().parent.parent / "templates" / "handoff_next_day.md").read_text()

synth = synth_tpl.replace("{{YYYY-MM-DD}}", today.strftime("%Y-%m-%d"))
handoff = handoff_tpl.replace("{{YYYY-MM-DD}}", today.strftime("%Y-%m-%d")).replace("{{NEXT-DAY}}", next_day.strftime("%Y-%m-%d"))

synth_path = synth_dir / f"{today.strftime('%Y-%m-%d')}.md"
handoff_path = handoff_dir / f"{today.strftime('%Y-%m-%d')}-next.md"

if not synth_path.exists():
    synth_path.write_text(synth)
    print(synth_path)
else:
    print(f"Exists: {synth_path}")

if not handoff_path.exists():
    handoff_path.write_text(handoff)
    print(handoff_path)
else:
    print(f"Exists: {handoff_path}")
