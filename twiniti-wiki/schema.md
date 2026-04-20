# Schema & conventions

## Purpose

Define how this wiki is organized and maintained.

## Directory layout

- `index.md` — entry point and navigation
- `log.md` — chronological record of edits, ingests, and decisions
- `wiki/` — maintained knowledge pages
- `raw/` — immutable source material and excerpts

## Page conventions

- Use one page per concept when the topic is reusable.
- Prefer clear, short filenames with hyphens.
- Each page should open with a direct definition.
- End with practical takeaways or next steps where relevant.
- Cross-link related pages instead of duplicating content.

## Writing style

- Evergreen, implementation-oriented, and vendor-neutral.
- Use concise headings and bullets for scanability.
- Distinguish between:
  - what the concept is
  - why it matters
  - how to implement it
  - common failure modes

## Maintenance rules

- Keep raw sources immutable.
- Synthesize into the wiki pages; do not copy large blocks verbatim.
- Update the index whenever a major page is added.
- Record significant changes in `log.md`.
- When content overlaps, create a canonical page and link to it.

## Quality bar

A good page answers:
1. What is it?
2. Why does it matter?
3. How does it work in practice?
4. What are the failure modes?
5. What should I do next?
