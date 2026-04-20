# Repo Notes: karpathy/autoresearch

## Core idea
Autonomous research loop over a small but real LLM training setup.

## Operating model
- Single mutable target file: `train.py`
- Supporting files are mostly fixed:
  - `prepare.py` for one-time data prep and runtime utilities
  - `program.md` for agent instructions / experiment policy
- Fixed wall-clock budget per experiment: ~5 minutes
- Primary evaluation metric: `val_bpb` (lower is better)

## Typical workflow
1. Verify baseline setup works.
2. Read `program.md`.
3. Modify only the allowed experiment surface.
4. Run a short training experiment.
5. Compare metric to baseline.
6. Keep the change only if it improves the metric or clearly advances the objective.

## Practical constraints
- Assumes a single NVIDIA GPU in the upstream repo.
- The repo is intentionally small.
- Keep experiments short, isolated, and reviewable.
- Prefer one clear change per run.

## What to preserve in a skill
- The autonomous loop
- The decision rule: keep or discard based on measurable improvement
- The distinction between human-authored program instructions and agent-edited code
- Minimal context and minimal moving parts
