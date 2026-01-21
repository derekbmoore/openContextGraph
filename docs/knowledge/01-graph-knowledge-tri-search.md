---
layout: default
title: Graph Knowledge (Gk) + Tri-Search™
parent: Knowledge
nav_order: 1
description: "How ctxEco combines keyword + vector + graph retrieval with RRF."
---

# Graph Knowledge (Gk) + Tri-Search™

> **Why it matters**: ctxEco retrieval is not “just RAG.” We combine **keyword**, **vector**, and **graph** signals (plus provenance) so agents can do relationship-based reasoning with citations and strong security boundaries.

## Tri-Search™ Architecture

ctxEco memory retrieval uses **three complementary search layers**, fused via **Reciprocal Rank Fusion (RRF)**:

### 1) Keyword search (lexical)

- **Purpose**: exact phrases, acronyms, terminology, titles.
- **Backing store (this repo)**: Zep sessions + metadata; fallback keyword scan is implemented for resilience.

### 2) Vector search (semantic)

- **Purpose**: paraphrase matching, “meaning” retrieval.
- **Backing store (this repo)**: Zep similarity search (vector-backed), with optional enterprise variants where embeddings live in dedicated stores.

### 3) Graph search (Gk) — relationship retrieval

- **Purpose**: traverse relationships (multi-hop), connect entities/topics/episodes/facts.
- **Backing store (this repo)**: derived from memory (facts + sessions) and rendered as a dynamic graph at query time.

## Fusion: Reciprocal Rank Fusion (RRF)

Tri-Search combines rankings from multiple retrieval methods using:

```text
RRF Score = Σ (1 / (k + rank_i))
```

Where:
- \(k = 60\) (standard constant)
- `rank_i` is the rank of the candidate in each retrieval list

## Knowledge Graph (Gk): what’s in it

### Node types (typical)

- **User** (central node)
- **Episodes** (sessions)
- **Facts** (extracted / curated semantic statements)

### Edge types (typical)

- **participated_in**: User → Episode
- **established**: Episode → Fact
- **knows**: User → Fact (fallback when source episode isn’t present)

> Implementation note: the graph is generated in [`backend/api/routes/graph.py`](https://github.com/derekbmoore/openContextGraph/blob/main/backend/api/routes/graph.py).

## Using the Knowledge Graph UI

- **UI**: Memory → Graph (Gk)
- **Local dev**: `http://localhost:5173/` (navigate to the Memory / Graph page)
- **Production**: `https://ctxeco.com/` (if enabled for the tenant)

## APIs

### Graph endpoint

```text
GET /api/v1/memory/graph?query=<optional>
```

### Tri-Search endpoint

```text
POST /api/v1/memory/search
```

See implementation in [`backend/memory/client.py`](https://github.com/derekbmoore/openContextGraph/blob/main/backend/memory/client.py).

## Diagram: Gk inside Tri-Search™

```mermaid
flowchart TB
  U[User Query] --> FE[Frontend: Memory pages]
  FE -->|POST /api/v1/memory/search| API1[Memory API]
  FE -->|GET /api/v1/memory/graph| API2[Graph API]

  API1 --> RRF[Reciprocal Rank Fusion]
  RRF --> K[Keyword Search]
  RRF --> V[Vector Search]
  RRF --> GK[Graph Knowledge (Gk)]

  GK --> Z[Zep facts + sessions]
  K --> Z
  V --> Z

  Z --> OUT[Ranked context + provenance]
```

## Related docs (ctxEco)

- [Tri-Search™ (overview)](../architecture/04-tri-search.md)
- [Antigravity Router (ingestion)](../architecture/03-antigravity-router.md)
- [System overview](../architecture/01-system-overview.md)

