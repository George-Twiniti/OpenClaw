#!/usr/bin/env node
import { readFile } from 'node:fs/promises';

const oracleUrl = process.env.ORACLE_BRIDGE_URL || 'http://vnic002.taild942c7.ts.net:8787';

async function jget(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status} ${await res.text()}`);
  return res.json();
}

async function jpost(url, body) {
  const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  if (!res.ok) throw new Error(`HTTP ${res.status} ${await res.text()}`);
  return res.json();
}

async function main() {
  const [,, cmd, ...args] = process.argv;
  if (cmd === 'enqueue') {
    const [url, title] = args;
    if (!url) throw new Error('Usage: oracle-transcript-bridge.mjs enqueue <url> [title]');
    return process.stdout.write(JSON.stringify(await jpost(`${oracleUrl}/seed`, { url, title: title ?? null }), null, 2) + '\n');
  }
  if (cmd === 'drain') return process.stdout.write(JSON.stringify(await jget(`${oracleUrl}/drain`), null, 2) + '\n');
  if (cmd === 'collect') {
    const raw = await readFile('/home/ubuntu/.openclaw/state/video-transcript-results.jsonl', 'utf8').catch(() => '');
    process.stdout.write(raw);
    return;
  }
  throw new Error('Usage: oracle-transcript-bridge.mjs <enqueue|collect|drain>');
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
