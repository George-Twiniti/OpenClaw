#!/usr/bin/env node
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const bridgeUrl = process.env.BRIDGE_URL || 'http://127.0.0.1:8788';
const ytdlp = process.env.YTDLP_PATH || '/home/george/.local/bin/yt-dlp';
const pollDelayMs = Number(process.env.WORKER_POLL_DELAY_MS || 3000);

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

async function extractTranscript(url) {
  const out = await execFileAsync(ytdlp, ['--write-auto-sub', '--sub-lang', 'en', '--sub-format', 'vtt', '--skip-download', '-o', '/tmp/%(title)s.%(ext)s', url], { maxBuffer: 10 * 1024 * 1024 });
  return { title: null, transcript: out.stdout || out.stderr || '' };
}

async function getNextJob() {
  const next = await jget(`${bridgeUrl}/jobs/next`);
  return next?.job ?? null;
}

async function getJobById(id) {
  const payload = await jget(`${bridgeUrl}/jobs/${id}`);
  return payload?.job ?? null;
}

async function processJob(job) {
  if (!job?.id) throw new Error('Bridge returned a job without an id');
  const current = (await getJobById(job.id)) || job;
  const result = {
    jobId: current.id,
    url: current.url,
    title: current.title ?? null,
    transcript: current.transcript ?? null,
    status: 'failed',
    notes: current.notes ?? null,
  };
  try {
    const extracted = await extractTranscript(current.url);
    result.title = extracted.title ?? current.title ?? null;
    result.transcript = extracted.transcript;
    result.status = 'completed';
    result.notes = null;
  } catch (error) {
    result.notes = error?.message ?? String(error);
  }
  await jpost(`${bridgeUrl}/jobs/${current.id}/result`, result);
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

async function main() {
  while (true) {
    const job = await getNextJob();
    if (!job) break;
    await processJob(job);
  }
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
