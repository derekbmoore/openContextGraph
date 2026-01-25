---
layout: default
title: Diagram Specs (Nano Banana)
parent: Architecture
nav_exclude: true
---

## Diagram Specs (Nano Banana)

This folder contains **diagram specifications** used to generate visual diagrams (for the wiki and social collateral).

### Canonical “Nano Banana” JSON schema (v1)

For new wiki diagrams, we standardize on the simple spec (as documented in `backend/llm/gemini_client.py`):

```json
{
  "title": "string",
  "type": "architecture | flowchart | mindmap",
  "nodes": [
    { "id": "string", "label": "string", "type": "string", "color": "#rrggbb" }
  ],
  "edges": [
    { "source": "string", "target": "string", "label": "string" }
  ]
}
```

### Notes

- **Existing legacy specs** in this repo may use richer or alternate shapes (`connections`, `metadata`, layout hints, prompts). Those are kept as-is.
- New wiki specs should live under `docs/assets/diagrams/wiki/` and follow the canonical schema above.

