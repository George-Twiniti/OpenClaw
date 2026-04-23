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

async function processOne() {
  const { job } = await jget(`${bridgeUrl}/jobs/next`);
  if (!job) return false;
  const result = { jobId: job.id, url: job.url, title: null, transcript: null, status: 'failed', notes: null };
  try {
    const extracted = await extractTranscript(job.url);
    result.title = extracted.title;
    result.transcript = extracted.transcript;
    result.status = 'completed';
  } catch (error) {
    result.notes = error?.message ?? String(error);
  }
  await jpost(`${bridgeUrl}/jobs/${job.id}/result`, result);
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  return true;
}

async function main() {
  while (true) {
    const worked = await processOne();
    if (!worked) break;
  }
}

main().catch((error) => {
  process.stderr.write((error?.stack ?? error?.message ?? String(error)) + '\n');
  process.exit(1);
});
