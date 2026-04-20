# Mempalace × Second Brain Implementation Checklist

## Objective
Add a hybrid memory/navigation layer to Second Brain that keeps raw data canonical and adds palace-style retrieval over Postgres + pgvector + graph edges.

## Phase 0 — Scope and Decisions
- [ ] Confirm the initial source types to ingest
  - chat transcripts
  - notes/docs
  - meeting outputs
  - emails/captures
- [ ] Confirm the initial wing taxonomy
  - people
  - projects
  - systems
  - clients
  - research
  - decisions
  - operations
- [ ] Decide whether room creation is:
  - manual first
  - automatic from content
  - hybrid
- [ ] Define what counts as canonical vs derivative
  - raw capture = canonical
  - summary = derivative
  - palace nodes = navigation only

## Phase 1 — Schema
- [ ] Add `entities` table
  - [ ] id
  - [ ] type
  - [ ] name
  - [ ] slug
  - [ ] status
  - [ ] timestamps
- [ ] Add `memory_items` table for raw artifacts
  - [ ] id
  - [ ] entity_id nullable
  - [ ] source_type
  - [ ] source_uri
  - [ ] title
  - [ ] raw_text
  - [ ] checksum
  - [ ] captured_at
  - [ ] timestamps
- [ ] Add `memory_chunks` table
  - [ ] id
  - [ ] memory_item_id
  - [ ] chunk_index
  - [ ] chunk_text
  - [ ] embedding
  - [ ] token_count
  - [ ] timestamps
- [ ] Add `palace_nodes` table
  - [ ] id
  - [ ] parent_id nullable
  - [ ] node_type
  - [ ] label
  - [ ] entity_id nullable
  - [ ] sort_order
  - [ ] metadata jsonb
  - [ ] timestamps
- [ ] Add `graph_edges` table
  - [ ] id
  - [ ] from_node_id
  - [ ] to_node_id
  - [ ] edge_type
  - [ ] weight
  - [ ] evidence_memory_item_id nullable
  - [ ] timestamps
- [ ] Add `retrieval_logs` table
  - [ ] id
  - [ ] query_text
  - [ ] query_embedding
  - [ ] selected_node_ids jsonb
  - [ ] selected_memory_item_ids jsonb
  - [ ] mode
  - [ ] latency_ms
  - [ ] timestamps

## Phase 2 — Ingestion Pipeline
- [ ] Create canonical ingest entry point
  - [ ] accept raw text + source metadata
  - [ ] checksum de-duplication
  - [ ] preserve original text
- [ ] Chunk raw text into `memory_chunks`
- [ ] Generate embeddings for chunks
- [ ] Detect entities from content
- [ ] Assign or create wing candidates
- [ ] Assign or create room candidates
- [ ] Attach palace nodes to the raw item
- [ ] Create graph edges when explicit relationships exist
- [ ] Store derived summaries separately from raw items

## Phase 3 — Palace Model
- [ ] Define wing node rules
  - [ ] one wing per major namespace
  - [ ] stable slugs
  - [ ] human-readable labels
- [ ] Define room node rules
  - [ ] rooms represent subtopics/categories
  - [ ] rooms live under wings
  - [ ] support manual override
- [ ] Define drawer representation
  - [ ] raw memory item lives in a drawer
  - [ ] drawer links to original source URI
- [ ] Define hall/tunnel rules
  - [ ] hall = within-wing relation
  - [ ] tunnel = cross-wing relation
  - [ ] edge weights reflect confidence

## Phase 4 — Retrieval
- [ ] Build query normalization
  - [ ] entity extraction
  - [ ] keyword expansion
  - [ ] optional wing/room hints
- [ ] Implement palace-guided candidate selection
  - [ ] match wing names
  - [ ] match room names
  - [ ] traverse graph neighbors
- [ ] Run semantic search over chunks
- [ ] Merge lexical, semantic, and graph candidates
- [ ] Re-rank with weighted heuristic
  - [ ] semantic similarity
  - [ ] graph proximity
  - [ ] palace path match
  - [ ] recency
  - [ ] canonical source priority
- [ ] Return raw excerpts + palace path + source pointers
- [ ] Log retrieval decisions

## Phase 5 — Agent Context Bootstrap
- [ ] Create a compact wake-up bundle
  - [ ] active wings
  - [ ] active rooms
  - [ ] open loops
  - [ ] recent decisions
  - [ ] canonical source pointers
- [ ] Make the wake-up bundle deterministic and small
- [ ] Ensure raw source links remain available

## Phase 6 — API Surface
- [ ] Add search endpoint
  - [ ] query text
  - [ ] wing filter
  - [ ] room filter
  - [ ] source type filter
- [ ] Add node browsing endpoint
  - [ ] wing → room → drawer tree
- [ ] Add relationship endpoint
  - [ ] show graph edges around a node
- [ ] Add ingest endpoint or job
- [ ] Add retrieval log endpoint for debugging

## Phase 7 — UI
- [ ] Render wing navigation
- [ ] Render room navigation
- [ ] Render drawer/raw item view
- [ ] Show cross-links between nodes
- [ ] Show search results with rationale
- [ ] Show “why this result” explanation

## Phase 8 — Quality Guardrails
- [ ] Raw source must never be overwritten by summaries
- [ ] Summaries must be clearly labeled derivative
- [ ] Palace nodes must not become the only copy of truth
- [ ] Search must always be able to fall back to raw chunks
- [ ] Add tests for canonicality and de-duplication
- [ ] Add tests for retrieval ranking stability
- [ ] Add tests for graph edge creation

## Phase 9 — MVP Order
1. [ ] schema
2. [ ] raw ingest
3. [ ] chunk + embedding
4. [ ] palace node assignment
5. [ ] semantic search
6. [ ] graph edges
7. [ ] hybrid re-rank
8. [ ] UI browse tree
9. [ ] wake-up bundle

## Definition of Done
- [ ] A raw item can be ingested and preserved
- [ ] It gets chunked and embedded
- [ ] It is assigned a wing and room
- [ ] It can be retrieved by semantic search
- [ ] It can be found via palace navigation
- [ ] Graph links show related memory
- [ ] Summaries remain separate from raw source

## Suggested First Repo Tasks
- [ ] inspect the current DB schema in Second Brain
- [ ] map existing capture/summarization tables to the new model
- [ ] choose the minimum migration set
- [ ] implement `palace_nodes` and `graph_edges`
- [ ] wire ingest to create nodes and edges
- [ ] add a search endpoint that returns palace path + raw excerpt

## Notes
- Keep the implementation small and boring first.
- Don’t introduce compression as the primary store.
- The palace is a navigation layer, not a memory replacement.
