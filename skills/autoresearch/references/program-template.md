# Program Template

Use this as the baseline `program.md` guidance for an AutoResearch run.

## Goal
Improve the target metric with short, measurable experiments.

## Rules
- Make one meaningful change per iteration.
- Keep experiments short and comparable.
- Prefer simple hypotheses over speculative rewrites.
- Record the before/after metric for every run.
- Keep a change only if the result improves the metric or clearly justifies further exploration.
- Revert changes that fail to help.

## Agent behavior
- Inspect the repo first.
- Respect the current scope and constraints.
- Do not modify fixed support files unless the task explicitly allows it.
- Summarize the hypothesis, change, metric, and decision after each run.

## Suggested output
- Hypothesis
- Change made
- Result
- Keep/discard
- Next experiment
