---
name: autoresearch
description: Autonomous research loop skill for karpathy/autoresearch-style repositories. Use when the user asks to set up, run, or improve an AutoResearch-style experiment harness, create or refine a program.md, or coordinate short iterative research runs where an agent edits code, executes brief experiments, compares metrics, and keeps or discards changes based on measurable results.
---

# Autoresearch

Use this skill for compact autonomous research loops where a small codebase is iterated against a clear metric.

## Core workflow

1. Inspect the repository and identify the mutable experiment surface.
2. Confirm the baseline run and the evaluation metric.
3. Read the current `program.md` or equivalent agent instruction file.
4. Make one meaningful change per iteration.
5. Run a short experiment.
6. Compare the metric against baseline.
7. Keep the change only if it improves the metric or clearly advances the objective.
8. Summarize hypothesis, change, result, and decision.

## Use the bundled references

- `references/repo-notes.md` for the karpathy/autoresearch operating model and constraints.
- `references/program-template.md` for a compact baseline `program.md`.

## Design rules

- Keep the loop small and reviewable.
- Prefer short wall-clock experiments over long runs.
- Preserve the distinction between fixed support files and mutable experiment files.
- Avoid multi-change edits unless the task explicitly requires them.
- Treat the evaluation metric as the source of truth.
