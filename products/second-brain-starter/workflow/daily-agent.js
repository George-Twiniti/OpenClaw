// daily-agent.js
// Node v18+
// Usage:
//   node daily-agent.js --repo "/path/to/second-brain" --model "gpt-4o-mini" --commit
//
// Requires:
//   export OPENAI_API_KEY="..."
// Optional:
//   export TZ="Europe/Lisbon"  (recommended)

import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY  
});


// ---- args ----
const args = process.argv.slice(2);
const getArg = (k, d = null) => {
  const i = args.indexOf(k);
  return i >= 0 ? args[i + 1] : d;
};
const REPO = getArg("--repo", process.cwd());
const MODEL = getArg("--model", "gpt-4o-mini");
const DO_COMMIT = args.includes("--commit");

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY) {
  console.error("Missing OPENAI_API_KEY env var");
  process.exit(1);
}

// ---- helpers ----
const ensureDir = (p) => fs.mkdirSync(p, { recursive: true });
const readIfExists = (p) => (fs.existsSync(p) ? fs.readFileSync(p, "utf8") : "");
const writeFileSafe = (p, content) => {
  ensureDir(path.dirname(p));
  fs.writeFileSync(p, content, "utf8");
};

const listMdBasenames = (dir) => {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.toLowerCase().endsWith(".md"))
    .map((f) => f.toLowerCase());
};

const todayLisbon = () => {
  // Compute YYYY-MM-DD in Europe/Lisbon without external deps
  const dtf = new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Lisbon" });
  return dtf.format(new Date()); // YYYY-MM-DD
};

// Read daily logs for today (supports one file or many, like YYYY-MM-DD-*.md)
const DATE = todayLisbon();
const DAILY_DIR = path.join(REPO, "daily");
const SUMMARY_DIR = path.join(REPO, "summaries");

const dailyFiles = fs.existsSync(DAILY_DIR)
  ? fs
      .readdirSync(DAILY_DIR)
      .filter((f) => f.startsWith(DATE) && f.toLowerCase().endsWith(".md"))
      .map((f) => path.join(DAILY_DIR, f))
  : [];

if (dailyFiles.length === 0) {
  console.log(`No daily files found for ${DATE} in ${DAILY_DIR}`);
  process.exit(0);
}

const dailyText = dailyFiles
  .map((fp) => `# FILE: ${path.basename(fp)}\n\n${readIfExists(fp)}`)
  .join("\n\n---\n\n");

// existing file indices (for stub creation guard)
const existing = {
  entities: listMdBasenames(path.join(REPO, "entities")),
  projects: listMdBasenames(path.join(REPO, "projects")),
  ideas: listMdBasenames(path.join(REPO, "ideas")),
  reference: listMdBasenames(path.join(REPO, "reference")),
};

// ---- OpenAI call (no SDK) ----
async function openaiChat({ model, system, user }) {
  const res = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model,
      temperature: 0.2,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
    }),
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`OpenAI error ${res.status}: ${txt}`);
  }
  const json = await res.json();
  return json.choices?.[0]?.message?.content ?? "";
}

// ---- prompt ----
const SYSTEM = `You are my daily-review agent for a markdown-based second brain.

Goal:
- Generate a concise daily summary in markdown for today's captured thoughts.
- Create NEW stub files only when clearly named and only if they don't already exist.
- Do not modify existing entity/project/idea/reference files; only create missing stubs.

Output MUST be strict JSON:
{
  "summary_md": "string",
  "create_files": [
    { "path": "entities/<file>.md|projects/<file>.md|ideas/<file>.md|reference/<file>.md", "content": "string" }
  ]
}

Rules:
- summary_md should be markdown with these sections:
  - Themes (top 5)
  - Open loops / follow-ups
  - Decisions (if any)
  - People mentioned
  - Projects mentioned
  - Ideas / references
  - Suggested next actions (1–3)
- create_files: keep to <= 10 total. Prefer none unless high confidence.
- Filenames must be lowercase, hyphenated, ascii only, ending .md. Example: "muhammad.md", "expo-city-proposal.md".
- Stub template:
  - include a YAML frontmatter with: type, name, created (YYYY-MM-DD), tags (array)
  - include headings: Mentions, Notes (and Next actions for projects)
- Do not include any text outside the JSON.`;

const USER = `Today (Lisbon): ${DATE}

Existing files (lowercase basenames):
entities: ${JSON.stringify(existing.entities)}
projects: ${JSON.stringify(existing.projects)}
ideas: ${JSON.stringify(existing.ideas)}
reference: ${JSON.stringify(existing.reference)}

Daily log content:
${dailyText}

Return JSON only.`;

// ---- run ----
const raw = await openaiChat({ model: MODEL, system: SYSTEM, user: USER });

// strict JSON parse with minimal cleanup
let out;
try {
  out = JSON.parse(raw);
} catch (e) {
  // try to salvage if model wrapped in code fences
  const m = raw.match(/```json\s*([\s\S]*?)\s*```/i) || raw.match(/```([\s\S]*?)```/);
  if (m) out = JSON.parse(m[1]);
  else throw new Error(`Failed to parse JSON. Model output:\n${raw}`);
}

// write summary
ensureDir(SUMMARY_DIR);
const summaryPath = path.join(SUMMARY_DIR, `${DATE}.md`);
writeFileSafe(summaryPath, out.summary_md || `# ${DATE}\n\n(no summary)\n`);
console.log(`Wrote summary: ${summaryPath}`);

// create stub files (skip if exists)
const created = [];
for (const f of Array.isArray(out.create_files) ? out.create_files : []) {
  if (!f?.path || !f?.content) continue;

  const rel = f.path.replace(/^\/+/, "");
  const abs = path.join(REPO, rel);

  if (fs.existsSync(abs)) continue;

  writeFileSafe(abs, f.content);
  created.push(rel);
}
if (created.length) console.log(`Created stubs:\n- ${created.join("\n- ")}`);

// optional git commit
if (DO_COMMIT) {
  try {
    execSync(`git -C "${REPO}" add summaries "${created.map((p) => `"${p}"`).join(" ")}"`, {
      stdio: "inherit",
    });
    execSync(`git -C "${REPO}" commit -m "Daily summary ${DATE}"`, { stdio: "inherit" });
    console.log("Committed.");
  } catch (e) {
    console.log("Git commit skipped/failed (repo not initialized or nothing to commit).");
  }
}
