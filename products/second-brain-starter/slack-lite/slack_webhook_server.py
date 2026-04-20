#!/usr/bin/env python3
"""Minimal Slack webhook receiver → Second‑Brain daily log."""
import argparse, json
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime
from pathlib import Path


def write_daily(repo, payload):
    repo = Path(repo)
    daily_dir = repo / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.utcnow()
    date = now.strftime("%Y-%m-%d")
    hhmm = now.strftime("%H%M")
    fname = daily_dir / f"{date}-{hhmm}.md"

    text = (payload.get("text") or "").strip()
    user = payload.get("user") or ""
    channel = payload.get("channel") or ""
    ts = payload.get("ts") or ""

    block = (
        "---\n"
        f"- ts: {now.isoformat()}\n"
        "  source: slack\n"
        f"  channel: {channel}\n"
        f"  user: {user}\n"
        f"  id: {ts}\n"
        "  text: |\n"
        + "    " + text.replace("\n", "\n    ") + "\n"
    )

    with open(fname, "a", encoding="utf-8") as f:
        f.write(block)

    return str(fname)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/slack":
            self.send_response(404)
            self.end_headers()
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            payload = {}

        fname = write_daily(self.server.repo, payload)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "file": fname}).encode("utf-8"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to second-brain repo")
    ap.add_argument("--port", type=int, default=8787)
    args = ap.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    server.repo = args.repo
    print(f"Slack Lite listening on :{args.port} -> {args.repo}")
    server.serve_forever()
