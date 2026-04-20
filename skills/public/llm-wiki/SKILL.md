---
name: llm-wiki
description: Build and maintain a persistent LLM-maintained markdown wiki from source materials and an index/log structure. Use when creating or updating a wiki-style knowledge base, designing ingest/query/lint workflows, or working from ideas like Karpathy’s llm-wiki gist where raw sources remain canonical and the wiki is the maintained synthesis layer.
---

# LLM Wiki

## Goal

Create a durable markdown wiki that compiles knowledge once, keeps it current, and preserves raw sources as truth.

## Core structure

- `raw/` for immutable source material
- `wiki/` for LLM-maintained markdown pages
- `index.md` for content navigation
- `log.md` for chronological operations
- a schema file that defines conventions and workflows

## Operating rules

- Keep raw sources immutable.
- Let the wiki be the maintained synthesis layer.
- Update cross-references when adding or revising pages.
- Record ingests, queries, and lint passes in `log.md`.
- Read `index.md` first when searching the wiki.
- Use the schema file to keep the agent disciplined.

## Typical tasks

- Design the wiki directory layout.
- Draft the schema/conventions file.
- Create or revise `index.md` and `log.md`.
- Define ingest, query, and lint workflows.
- Add a small search tool only when the wiki outgrows simple file navigation.

## Keep it minimal

Start with the smallest useful wiki system. Add automation only when manual markdown maintenance becomes tedious.
