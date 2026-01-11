# Antigravity Router (Document Ingestion)

## Classification

| Class | Truth Value | Engine | Examples |
|-------|-------------|--------|----------|
| A | Immutable | Docling | PDFs, manuals, specs |
| B | Ephemeral | Unstructured | Emails, slides, docs |
| C | Operational | Pandas | CSV, JSON, logs |

## Metadata Fields

- `provenance_id` — source link
- `decay_rate` — 0.0 (permanent) to 1.0 (ephemeral)
- `classification` — A/B/C

## Implementation

See: `backend/etl/`

## TODO

- [ ] Document extraction engines
- [ ] Add classification heuristics
