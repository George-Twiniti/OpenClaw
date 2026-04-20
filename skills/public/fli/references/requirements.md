# Fli Requirements and Run Notes

## What Fli is
- Google Flights MCP and Python library
- Supports CLI flight search and MCP server modes

## What is needed to run it
- Python 3.10+ (practical target)
- `uv` recommended for dependency management and execution
- Network access to Google Flights endpoints
- For MCP use: either STDIO server (`fli-mcp`) or HTTP server (`fli-mcp-http`)

## Typical install
- `uv sync --all-extras`
- `uv run pytest`
- `uv run fli-mcp`
- `uv run fli-mcp-http`

## Typical CLI patterns
- `fli flights JFK LHR 2026-10-25`
- `fli dates JFK LHR --from 2026-01-01 --to 2026-02-01`

## Validation priorities for a skill
- confirm install commands
- identify runtime mode (CLI vs MCP)
- note required extras and example deps
- document the MCP configuration path for the target host
