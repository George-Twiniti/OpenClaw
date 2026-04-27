#!/usr/bin/env node
import fs from 'node:fs/promises';

const oracleUrl = process.env.ORACLE_BRIDGE_URL || 'http://gbroadbent5.taild942c7.ts.net:8787';
const localUrl = process.env.LOCAL_BRIDGE_URL || 'http://gbroadbent5-1.taild942c7.ts.net:8788';

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
  if (cmd === 'status') return process.stdout.write(JSON.stringify(await jget(`${oracleUrl}/status`), null, 2) + '\n');
  if (cmd === 'seed') {
    const [url, title] = args;
    if (!url) throw new Error('Usage: oracle-bridge-sync.mjs seed <url> [title]');
    return process.stdout.write(JSON.stringify(await jpost(`${oracleUrl}/seed`, { url, title: title ?? null }), null, 2) + '\n');
  }
  if (cmd === 'drain') return process.stdout.write(JSON.stringify(await jget(`${oracleUrl}/drain`), null, 2) + '\n');
  if (cmd === 'collect') {
    const res = await fetch(`${localUrl}/status`).catch(() => null);
    const raw = await fs.readFile('/home/ubuntu/.openclaw/state/video-transcript-results.jsonl', 'utf8').catch(() => '');
    process.stdout.write(raw);
    return;
  }
  throw new Error('Usage: oracle-bridge-sync.mjs <status|seed|drain|collect>');
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
