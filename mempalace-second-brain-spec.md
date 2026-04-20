# Mempalace × Second Brain Spec

## Goal
Create a hybrid memory/retrieval layer for Second Brain that keeps raw source material canonical while adding a palace-style navigation model on top.

## Core Principle
- **Raw source is truth**
- **Palace structure is navigation**
- **Embeddings are fuzzy recall**
- **Graph edges are relationships**

Do not replace original captures with summaries.

## Design Summary
Mempalace contributes a useful metaphor and retrieval pattern:
- wings = top-level namespaces
- rooms = grouped memory categories within a wing
- drawers = raw documents, transcripts, source captures
- hall/tunnel links = cross-room / cross-wing relationships

Second Brain already has the right system-of-record shape:
- Postgres as source of truth
- pgvector for semantic search
- graph relationships for explicit links
- raw artifacts stored separately from derived views

The hybrid approach is to layer a palace-style index and navigation API over the existing database.

## Data Model

### 1) entities
Canonical things in the world: people, projects, systems, sources, topics, places.

Suggested fields:
- id
- type
- name
- slug
- status
- created_at
- updated_at

### 2) memory_items
Raw source artifacts.

Examples:
- chat transcript
- meeting notes
- email capture
- imported doc
- summary derivative

Suggested fields:
- id
- entity_id (optional)
- source_type
- source_uri
- title
- raw_text
- checksum
- captured_at
- created_at
- updated_at

### 3) memory_chunks
Chunked text for search and retrieval.

Suggested fields:
- id
- memory_item_id
- chunk_index
- chunk_text
- embedding
- token_count
- created_at

### 4) palace_nodes
Navigation nodes for the palace structure.

Types:
- wing
- room
- drawer
- hall
- tunnel

Suggested fields:
- id
- parent_id (nullable)
- node_type
- label
- entity_id (optional)
- sort_order
- metadata jsonb
- created_at
- updated_at

### 5) graph_edges
Explicit relationships.

Suggested fields:
- id
- from_node_id
- to_node_id
- edge_type
- weight
- evidence_memory_item_id (optional)
- created_at

### 6) retrieval_logs
Track what was searched and what won.

Suggested fields:
- id
- query_text
- query_embedding
- selected_node_ids jsonb
- selected_memory_item_ids jsonb
- mode
- latency_ms
- created_at

## Navigation Model

### Wing
Top-level bucket for a major namespace:
- person
- project
- client
- system
- topic

Example wings:
- MG
- Oracle server
- Second Brain
- OpenClaw
- mempalace

### Room
A sub-area inside a wing.

Examples:
- decisions
- tasks
- architecture
- bugs
- notes
- references
- timelines

### Drawer
The raw item.

Examples:
- a Telegram thread
- a GitHub issue
- a daily log
- a meeting transcript
- a note imported from a source

### Hall / Tunnel
Cross-links.
- hall: within-wing relationship
- tunnel: cross-wing relationship

Examples:
- “Telegram onboarding” hall within Oracle wing
- “memory embeddings” tunnel between OpenClaw and Second Brain

## Retrieval Flow

### Step 1: Normalize Query
- detect entities
- infer likely wing/room candidates
- keep the original text

### Step 2: Palace-Guided Candidate Selection
Search first by:
- entity matches
- wing/room names
- explicit graph neighbors

### Step 3: Semantic Search
Run vector search over memory_chunks and rank by similarity.

### Step 4: Hybrid Re-rank
Combine:
- lexical match
- graph proximity
- palace node relevance
- recency
- embedding similarity

### Step 5: Return
Return:
- best memory items
- path through palace nodes
- supporting raw excerpts

## Ranking Heuristic
Suggested scoring weights:
- 40% semantic similarity
- 25% explicit graph proximity
- 15% palace path match
- 10% recency
- 10% source authority / canonicality

Authority rules:
- raw capture beats summary
- source artifact beats derivative note
- direct evidence beats inferred link

## Write Path
When new content arrives:
1. Store raw item
2. Chunk it
3. Embed chunks
4. Detect or update entities
5. Attach to wing/room nodes
6. Create graph edges when evidence exists
7. Optionally create summary derivatives, but keep them separate

## How to Apply MemPalace Concepts

### Keep
- verbatim storage
- semantic search
- structure-first navigation
- local/offline operation
- raw data preservation

### Adapt
- wings/rooms/drawers become DB-backed navigation nodes
- halls/tunnels become graph edges
- wake-up context becomes a compact retrieval bootstrap

### Skip or Limit
- lossy compression as default storage
- any claim that structure replaces search
- any summarization that overwrites source text

## Second Brain Integration Points

### 1) Ingestion pipeline
- import chat logs, docs, transcripts, notes
- assign wing/room candidates
- insert raw + chunks + embeddings

### 2) Search API
- query text
- optional wing/room filters
- return ranked raw items + palace path

### 3) Timeline / memory views
- show decisions and recurring topics per wing
- show how a topic moved across rooms over time

### 4) Agent context bootstrap
- provide a short wake-up bundle:
  - current wings
  - active rooms
  - top open loops
  - recent decisions
  - canonical source pointers

## Suggested Initial Wings for Second Brain
- People
- Clients
- Projects
- Systems
- Decisions
- Research
- Operations
- Archive

## Suggested Initial Rooms Under Projects
- goals
- architecture
- implementation
- blockers
- notes
- decisions
- references

## Minimal MVP
Build these first:
1. palace_nodes table
2. graph_edges table
3. entity tagging on ingest
4. hybrid retrieval API
5. UI showing wing → room → drawer path

## Success Criteria
- user can ask vague questions and get the right source
- agent can navigate from a wing into a room quickly
- raw source remains accessible
- summaries never replace originals
- retrieval works both semantically and structurally

## Open Questions
- Should wings map to people/projects only, or include topics and systems too?
- Do we want automatic room creation from content, or manual curation?
- Should palace paths be stable IDs or human-readable slugs?
- How much summary is safe before it starts distorting the raw memory?

## Recommendation
Use the mempalace pattern as a **navigation layer** and keep Second Brain as the **authoritative memory store**.

That gives you:
- human-friendly structure
- machine-friendly retrieval
- raw fidelity
- graph-aware context
- no forced summarization loss
