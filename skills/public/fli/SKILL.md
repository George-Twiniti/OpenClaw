---
name: fli
description: Google Flights MCP and Python library skill. Use when the user wants to install, run, configure, or integrate the punitarani/fli repo for flight search via CLI, MCP server, or Python API, including figuring out required dependencies, example commands, and how to wire it into an assistant workflow.
---

# Fli

Use this skill when working with the `punitarani/fli` repository.

## What to determine first

- Whether the user wants CLI usage, MCP server usage, or Python API usage.
- Whether the environment has `uv` available.
- Whether the target is STDIO MCP or HTTP MCP.

## Minimal run path

1. Read `references/requirements.md`.
2. Verify Python and `uv`.
3. Install dependencies with `uv sync --all-extras`.
4. Run a small smoke test:
   - `fli --help`
   - `fli flights JFK LHR 2026-10-25`
   - `fli-mcp`
5. If the MCP server is needed, document the config entry for the assistant runtime.

## Keep it practical

- Prefer the simplest runtime mode that satisfies the task.
- Use the examples in the repo only if the basic install or CLI smoke test needs confirmation.
- Keep configuration notes short and specific.
