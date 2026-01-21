---
layout: default
title: Foundry Threads (Feature Flag)
parent: Foundry (Azure AI Foundry)
nav_order: 3
description: "How ctxEco uses Foundry threads for persistence and why it matters."
---

# Foundry Threads (Feature Flag)

> **Status**: documented as implemented in prior iterations; ctxEco keeps this as a feature-flagged capability.  
> **Feature flag**: `USE_FOUNDRY_THREADS` (default `false`)

## What threads are for

Threads provide **managed, durable conversation persistence** so:

- sessions survive restarts
- “golden thread” demos can replay deterministically
- project-based isolation can be attached at the thread level

## Desired behavior in ctxEco

- When `USE_FOUNDRY_THREADS=false`:
  - ctxEco uses in-memory session behavior only (fast path)
- When `USE_FOUNDRY_THREADS=true`:
  - ctxEco creates/loads Foundry threads for persistence
  - ctxEco still persists memory to Zep (long-term memory)
  - failures degrade gracefully back to in-memory behavior

## Data flow (conceptual)

```text
User request
  ↓
get_or_create_session()
  ├─ cache hit → return
  └─ cache miss
      ├─ Foundry threads enabled → load/create thread → build context → cache → return
      └─ Foundry unavailable → fallback to in-memory session
```

## Configuration

```bash
AZURE_FOUNDRY_AGENT_ENDPOINT=https://<account>.services.ai.azure.com
AZURE_FOUNDRY_AGENT_PROJECT=<project-name>
USE_FOUNDRY_THREADS=true
```

## Related docs

- [Agent Service Integration](01-agent-service-integration.md)
- [Foundry IQ + ctxEco Integration Master](../08-foundry-iq-ctxeco-integration-master.md)

