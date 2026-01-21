# Tri-Search™ (Hybrid Memory Search)

## Search Modes

1. **Keyword** — BM25/inverted index
2. **Vector** — pgvector cosine similarity
3. **Graph** — Graphiti relationship traversal

## Fusion

Reciprocal Rank Fusion (RRF): `1/(k + rank)`

## API

```
POST /api/v1/memory/search
{query, search_type, user_id, limit}
```

## Implementation

See: `backend/memory/client.py`

## Deep dive

- [Graph Knowledge (Gk) + Tri-Search™](../knowledge/01-graph-knowledge-tri-search.md)

## TODO

- [ ] Document RRF tuning
- [ ] Add benchmark results
