---
layout: default
title: Foundry IQ Implementation Notes (POC → Production)
parent: Knowledge
nav_order: 4
description: "Detailed implementation checklist for integrating Foundry IQ into ctxEco Tri-Search™."
---

# Foundry IQ Implementation Notes (POC → Production)

This is the **detailed checklist** for implementing Foundry IQ knowledge-base retrieval and fusing it with ctxEco Tri-Search™.

## Target behavior

```text
1. Semantic/vector retrieval (ctxEco memory)
2. Keyword retrieval (ctxEco memory)
3. Foundry IQ retrieval (enterprise KB)
4. Fuse with RRF
5. Return results with evidence + gating metadata
```

## Required configuration

ctxEco already defines feature flags in:
- [`backend/core/config.py`](https://github.com/derekbmoore/openContextGraph/blob/main/backend/core/config.py)

### Environment variables

```bash
# Enable Foundry IQ
USE_FOUNDRY_IQ=true

# Knowledge Base ID (from Foundry portal)
FOUNDRY_IQ_KB_ID=kb-...

# Foundry project endpoint context (already used elsewhere)
AZURE_FOUNDRY_AGENT_ENDPOINT=https://<account>.services.ai.azure.com
AZURE_FOUNDRY_AGENT_PROJECT=<project-name>
```

## Implementation steps

### 1) Add a Foundry IQ client

Create a small client wrapper (recommended path: `backend/integrations/foundry_iq.py`) that supports:

- `search(query, limit, filters, project_id)`
- `list_knowledge_bases()` (optional)
- `get_knowledge_base(kb_id)` (optional)

Auth preference order:

1. **Managed Identity / Entra (OBO where needed)**
2. API key only for constrained POC environments

### 2) Integrate into `search_memory`

Update the retrieval pipeline (implementation lives in `backend/memory/client.py`) to:

- call Foundry IQ when `USE_FOUNDRY_IQ=true` and `FOUNDRY_IQ_KB_ID` is set
- normalize Foundry IQ hits into the same internal result schema used by Tri-Search™
- fuse rankings with RRF

### 3) Evidence-first output

For each Foundry IQ hit, store:

- KB id + document/source URL
- chunk ids (if available)
- permission trimming context (what user/tenant/group the result was returned under)
- the fused score contribution (optional but recommended for debugging)

### 4) Tests (“golden thread”)

Add deterministic tests that verify:

- Foundry IQ disabled → Tri-Search works unchanged
- Foundry IQ enabled but unreachable → graceful fallback (no 500s)
- Foundry IQ enabled and reachable → results include Foundry IQ sources and are fused correctly

## Related docs

- [Foundry IQ Hybrid Search](02-foundry-iq-hybrid-search.md)
- [Foundry IQ + ctxEco Integration Master](../architecture/08-foundry-iq-ctxeco-integration-master.md)

