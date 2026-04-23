#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';

const base = process.env.ORACLE_OPENCLAW_HOME || '/home/ubuntu/.openclaw';
const oracleUrl = process.env.ORACLE_BRIDGE_URL || 'http://100.85.189.47:8787';
const stateDir = path.join(base, 'state');
const queuePath = path.join(stateDir, 'video-transcript-queue.json');
const resultsPath = path.join(stateDir, 'video-transcript-results.jsonl');

async function readJson(file, fallback) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); } catch { return fallback; }
}

async function writeJson(file, value) {
  await fs.mkdir(path.dirname(file), { recursive: true });
  await fs.writeFile(file, JSON.stringify(value, null, 2) + '\n');
}

async function main() {
  // Placeholder for future HTTP transport; current behavior stays file-based.
  void oracleUrl;
  const [,, cmd, ...args] = process.argv;
  if (cmd === 'status') {
    const queue = await readJson(queuePath, { jobs: [] });
    const jobs = Array.isArray(queue) ? queue : (queue.jobs ?? []);
    const results = await fs.readFile(resultsPath, 'utf8').then(t => t.trim().split('\n').filter(Boolean).length).catch(() => 0);
    process.stdout.write(JSON.stringify({ queued: jobs.filter(j => j?.status === 'queued').length, total: jobs.length, results }, null, 2) + '\n');
    return;
  }
  if (cmd === 'seed') {
    const [url, title] = args;
    if (!url) throw new Error('Usage: oracle-bridge-sync.mjs seed <url> [title]');
    const queue = await readJson(queuePath, { jobs: [] });
    const jobs = Array.isArray(queue) ? queue : (queue.jobs ?? []);
    const id = `job_${Date.now()}_${Math.random().toString(16).slice(2, 8)}`;
    jobs.push({ id, url, title: title ?? null, status: 'queued', claimedAt: null, completedAt: null, failedAt: null, notes: null, transcript: null });
    await writeJson(queuePath, { jobs });
    process.stdout.write(JSON.stringify({ jobId: id, url, title: title ?? null, status: 'queued' }, null, 2) + '\n');
    return;
  }
  throw new Error('Usage: oracle-bridge-sync.mjs <status|seed>');
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
