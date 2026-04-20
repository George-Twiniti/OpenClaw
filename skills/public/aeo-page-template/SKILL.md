---
name: aeo-page-template
description: Build AI-search-optimized Twiniti AEO pages using a standard structured template and content schema. Use when creating, rewriting, or scaling Twiniti public pages for search engines and AI retrieval. Focus on concise answer-first sections, defined headings, metadata, and internal link structure.
---

# AEO Page Template

## Goal
Create a repeatable page format for Twiniti AEO pages that is easy for search engines and AI systems to parse.

## Core principles
- Answer first, details second.
- Keep sections short and explicit.
- Prefer definitions, relationships, and outcomes over marketing prose.
- Use Twiniti-owned content first; fill gaps with web research.
- Make pages semantically distinct.

## Standard page structure
1. **Hero / definition**
   - Page title
   - One-sentence definition
   - Short supporting sentence

2. **Why it matters**
   - Problem statement
   - Operational impact
   - Who it affects

3. **What it is**
   - Define the concept, product, or service
   - Clarify what it is not, if useful

4. **How it works**
   - 3–5 short steps or components
   - Keep language concrete

5. **Benefits / outcomes**
   - 3–5 direct benefits
   - Tie each benefit to a practical result

6. **Use cases / audience**
   - Industries, roles, or scenarios

7. **Related Twiniti pages**
   - Internal links to the most relevant supporting pages

8. **Metadata**
   - title tag
   - meta description
   - canonical
   - Open Graph / Twitter basics
   - Google tag if required by site template

## Suggested content schema
For each page, define:
- `slug`
- `title`
- `summary`
- `definition`
- `problem`
- `howItWorks[]`
- `benefits[]`
- `audience[]`
- `relatedPages[]`
- `metadata` (title, description, canonical)
- `sources[]`
- `lastUpdated`

## Writing rules
- 1 idea per paragraph.
- 2–4 lines per paragraph max.
- Use explicit nouns instead of vague pronouns.
- Avoid fluff like “revolutionary” unless it is a quoted claim.
- Prefer plain English over abstract brand language.
- If a page has sub-modules, give each module a short definition and 2–3 outcomes.

## Build workflow
1. Inventory candidate AEO pages.
2. Map each page to a schema.
3. Draft content from Twiniti docs.
4. Fill factual gaps from the web.
5. Write page files.
6. Verify metadata and internal links.

## Validation checklist
- Does the page answer the core question in the first screen?
- Can an AI summarize the page in one sentence?
- Is the page distinct from nearby pages?
- Is the metadata consistent with the content?
- Are the internal links relevant and sparse?
