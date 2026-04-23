#!/usr/bin/env node
import http from 'node:http';
import fs from 'node:fs/promises';
import path from 'node:path';

const base = process.env.ORACLE_OPENCLAW_HOME || '/home/ubuntu/.openclaw';
const stateDir = path.join(base, 'state');
const queuePath = path.join(stateDir, 'video-transcript-queue.json');
const resultsPath = path.join(stateDir, 'video-transcript-results.jsonl');
const port = Number(process.env.ORACLE_BRIDGE_PORT || 8787);
const host = process.env.ORACLE_BRIDGE_HOST || '127.0.0.1';

async function readJson(file, fallback) {
  try { return JSON.parse(await fs.readFile(file, 'utf8')); } catch { return fallback; }
}

async function writeQueue(jobs) {
  await fs.mkdir(stateDir, { recursive: true });
  await fs.writeFile(queuePath, JSON.stringify({ jobs }, null, 2) + '\n');
}

async function appendResult(result) {
  await fs.mkdir(stateDir, { recursive: true });
  await fs.appendFile(resultsPath, JSON.stringify(result) + '\n');
}

function json(res, code, body) {
  res.writeHead(code, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(body, null, 2) + '\n');
}

async function readJobs() {
  const queue = await readJson(queuePath, { jobs: [] });
  return Array.isArray(queue) ? queue : (queue.jobs ?? []);
}

async function handle(req, res) {
  const url = new URL(req.url, `http://${req.headers.host}`);
  if (req.method === 'GET' && url.pathname === '/status') {
    const jobs = await readJobs();
    const results = await fs.readFile(resultsPath, 'utf8').then(t => t.trim().split('\n').filter(Boolean).length).catch(() => 0);
    return json(res, 200, { queued: jobs.filter(j => j?.status === 'queued').length, total: jobs.length, results });
  }
  if (req.method === 'GET' && url.pathname === '/jobs') {
    const jobs = await readJobs();
    return json(res, 200, { jobs });
  }
  if (req.method === 'GET' && url.pathname === '/jobs/next') {
    const jobs = await readJobs();
    const next = jobs.find((job) => job?.status === 'queued') || null;
    if (!next) return json(res, 200, { job: null });
    next.status = 'claimed';
    next.claimedAt = new Date().toISOString();
    await writeQueue(jobs);
    return json(res, 200, { job: next });
  }
  if (req.method === 'POST' && url.pathname === '/jobs') {
    let body = '';
    for await (const chunk of req) body += chunk;
    const input = JSON.parse(body || '{}');
    const jobs = await readJobs();
    const id = input.id || `job_${Date.now()}_${Math.random().toString(16).slice(2, 8)}`;
    const job = { id, url: input.url, title: input.title ?? null, status: 'queued', claimedAt: null, completedAt: null, failedAt: null, notes: null, transcript: null };
    jobs.push(job);
    await writeQueue(jobs);
    return json(res, 200, { job });
  }
  if (req.method === 'POST' && /^\/jobs\/[^/]+\/result$/.test(url.pathname)) {
    let body = '';
    for await (const chunk of req) body += chunk;
    const result = JSON.parse(body || '{}');
    const jobs = await readJobs();
    const id = url.pathname.split('/')[2];
    const updated = jobs.map((item) => item.id === id ? { ...item, ...result, completedAt: result.status === 'completed' ? new Date().toISOString() : item.completedAt, failedAt: result.status === 'failed' ? new Date().toISOString() : item.failedAt } : item);
    await writeQueue(updated);
    await appendResult(result);
    return json(res, 200, { ok: true });
  }
  if (req.method === 'GET' && /^\/jobs\/[^/]+$/.test(url.pathname)) {
    const id = url.pathname.split('/')[2];
    const jobs = await readJobs();
    const job = jobs.find((item) => item.id === id) || null;
    return json(res, 200, { job });
  }
  if (req.method === 'GET' && /^\/results\/[^/]+$/.test(url.pathname)) {
    const id = url.pathname.split('/')[2];
    const raw = await fs.readFile(resultsPath, 'utf8').catch(() => '');
    const result = raw.split('\n').filter(Boolean).map((line) => JSON.parse(line)).find((item) => item.jobId === id) || null;
    return json(res, 200, { result });
  }
  res.writeHead(404);
  res.end('not found');
}

http.createServer((req, res) => {
  handle(req, res).catch((error) => json(res, 500, { error: error?.message ?? String(error) }));
}).listen(port, host, () => {
  console.log(`oracle-http-bridge listening on ${host}:${port}`);
});
