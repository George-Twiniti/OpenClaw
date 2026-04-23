#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';

const base = process.env.ORACLE_OPENCLAW_HOME || '/home/ubuntu/.openclaw';
const stateDir = path.join(base, 'state');
const queuePath = path.join(stateDir, 'video-transcript-queue.json');
const resultsPath = path.join(stateDir, 'video-transcript-results.jsonl');

async function readJson(file, fallback) {
  try {
    return JSON.parse(await fs.readFile(file, 'utf8'));
  } catch {
    return fallback;
  }
}

async function writeQueue(jobs) {
  await fs.mkdir(stateDir, { recursive: true });
  await fs.writeFile(queuePath, JSON.stringify({ jobs }, null, 2) + '\n');
}

async function enqueue(url, title = null) {
  const queue = await readJson(queuePath, { jobs: [] });
  const jobs = Array.isArray(queue) ? queue : (queue.jobs ?? []);
  const id = `job_${Date.now()}_${Math.random().toString(16).slice(2, 8)}`;
  jobs.push({ id, url, title, status: 'queued', claimedAt: null, completedAt: null, failedAt: null, notes: null, transcript: null });
  await writeQueue(jobs);
  return { jobId: id, url, title, status: 'queued' };
}

async function collect() {
  try {
    const raw = await fs.readFile(resultsPath, 'utf8');
    return raw.trim().split('\n').filter(Boolean).map((line) => JSON.parse(line));
  } catch {
    return [];
  }
}

async function drainQueue() {
  const queue = await readJson(queuePath, { jobs: [] });
  const jobs = Array.isArray(queue) ? queue : (queue.jobs ?? []);
  return jobs.filter((job) => job?.status === 'queued').map((job) => ({ id: job.id, url: job.url, title: job.title ?? null, status: job.status }));
}

async function main() {
  const [,, cmd, ...args] = process.argv;
  if (cmd === 'enqueue') {
    const [url, title] = args;
    if (!url) throw new Error('Usage: oracle-transcript-bridge.mjs enqueue <url> [title]');
    const result = await enqueue(url, title ?? null);
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
    return;
  }
  if (cmd === 'collect') {
    const results = await collect();
    process.stdout.write(JSON.stringify(results, null, 2) + '\n');
    return;
  }
  if (cmd === 'drain') {
    const jobs = await drainQueue();
    process.stdout.write(JSON.stringify(jobs, null, 2) + '\n');
    return;
  }
  throw new Error('Usage: oracle-transcript-bridge.mjs <enqueue|collect|drain>');
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
