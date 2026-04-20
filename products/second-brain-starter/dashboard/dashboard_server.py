#!/usr/bin/env python3
import argparse, json, subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

NEON_KEY_FILE = Path('/home/george/.openclaw/keys/Neon_Key.txt')


def read_file(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception:
        return ""


def neon_url():
    raw = NEON_KEY_FILE.read_text().strip()
    if raw.startswith('psql '):
        raw = raw.replace('psql ', '', 1).strip()
    return raw.strip("'\r\n")


def db_query(sql):
    try:
        res = subprocess.run([
            'psql', neon_url(), '-t', '-A', '-c', sql
        ], check=True, capture_output=True, text=True)
        return res.stdout.strip()
    except Exception:
        return ''


def latest_file(dirpath, suffix=".md"):
    p = Path(dirpath)
    if not p.exists():
        return None
    files = sorted([f for f in p.glob(f"*{suffix}")], reverse=True)
    return files[0] if files else None


def recent_files(dirpath, limit=5):
    p = Path(dirpath)
    if not p.exists():
        return []
    files = sorted([f for f in p.glob("*.md")], reverse=True)
    return files[:limit]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            html = """
<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <title>Second‑Brain Dashboard</title>
  <style>
    body { font-family: Arial, sans-serif; background:#0b0f14; color:#eaeaea; padding:20px; }
    h1,h2 { color:#58a6ff; }
    pre { background:#111; padding:12px; border-radius:8px; white-space:pre-wrap; }
    .grid { display:grid; grid-template-columns:1fr; gap:20px; }
  </style>
</head>
<body>
  <h1>Second‑Brain Dashboard</h1>
  <div class="grid">
    <section><h2>Latest Daily Summary</h2><pre id="daily"></pre></section>
    <section><h2>Latest Handoff</h2><pre id="handoff"></pre></section>
    <section><h2>Recent Captures (Files)</h2><pre id="captures"></pre></section>
    <section><h2>Recent Captures (DB)</h2><pre id="db_captures"></pre></section>
    <section><h2>Graph Overview</h2><pre id="graph"></pre></section>
  </div>
<script>
fetch('/data').then(r=>r.json()).then(data=>{
  document.getElementById('daily').textContent = data.daily || 'No summary found.';
  document.getElementById('handoff').textContent = data.handoff || 'No handoff found.';
  document.getElementById('captures').textContent = data.captures || 'No captures found.';
  document.getElementById('db_captures').textContent = data.db_captures || 'No DB captures found.';
  document.getElementById('graph').textContent = data.graph || 'No graph data.';
});
</script>
</body>
</html>
"""
            self.wfile.write(html.encode("utf-8"))
            return

        if self.path == "/data":
            repo = Path(self.server.repo)
            daily = latest_file(repo / "summaries" / "daily")
            handoff = latest_file(repo / "summaries" / "handoff")
            captures = recent_files(repo / "daily", limit=5)

            db_caps = db_query("SELECT created_at::text || ' | ' || left(content, 200) FROM captures ORDER BY created_at DESC LIMIT 5;")
            graph = db_query("SELECT node_type || ': ' || count(*) FROM graph_nodes GROUP BY node_type ORDER BY count(*) DESC;")

            data = {
                "daily": read_file(daily) if daily else "",
                "handoff": read_file(handoff) if handoff else "",
                "captures": "\n\n".join([read_file(f) for f in captures]),
                "db_captures": db_caps,
                "graph": graph
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
            return

        self.send_response(404)
        self.end_headers()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to second-brain repo")
    ap.add_argument("--port", type=int, default=8788)
    args = ap.parse_args()

    server = HTTPServer(("0.0.0.0", args.port), Handler)
    server.repo = args.repo
    print(f"Dashboard on :{args.port} -> {args.repo}")
    server.serve_forever()
