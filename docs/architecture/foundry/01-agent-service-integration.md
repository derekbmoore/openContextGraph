---
layout: default
title: Agent Service Integration (Threads, Files, Tools)
parent: Foundry (Azure AI Foundry)
nav_order: 1
description: "How ctxEco uses Azure AI Foundry Agent Service features with a hybrid approach."
---

# Azure AI Foundry Agent Service Integration (ctxEco)

> **Status**: Analysis + migration roadmap (kept current to Jan 2026)  
> **Strategy**: hybrid (keep LangGraph “Brain”; use Foundry-managed “Spine” capabilities)

## Why this matters for the GTM MVP

Foundry Agent Service helps us ship a credible enterprise MVP faster by providing:

- **Threads**: managed conversation persistence
- **Files**: managed file storage (agent-friendly)
- **Vector stores**: optional managed vector infrastructure (we keep Zep initially)
- **Tool calling infra**: strongly-typed tool execution surfaces
- **Project isolation**: aligns with ctxEco tenant/project boundaries

## Current state in ctxEco

We already have feature flags in settings (see `backend/core/config.py`):

- `USE_FOUNDRY_THREADS`
- `USE_FOUNDRY_FILES`
- `USE_FOUNDRY_VECTORS`
- `USE_FOUNDRY_TOOLS`
- `USE_FOUNDRY_IQ` (see Knowledge section)

## Integration architecture (recommended)

**Hybrid model**: Foundry provides managed infrastructure, ctxEco keeps agent logic.

```text
Browser / UI
  ↓
ctxEco API (FastAPI)
  ├─ LangGraph agent logic (Brain)
  └─ Foundry Agent Service client (Spine)
        ├─ Threads (persistence)
        ├─ Files (uploads / artifacts)
        ├─ Vector stores (optional)
        └─ Tool execution (optional)
```

## Configuration (baseline)

```bash
# Foundry Agent Service context
AZURE_FOUNDRY_AGENT_ENDPOINT=https://<account>.services.ai.azure.com
AZURE_FOUNDRY_AGENT_PROJECT=<project-name>
AZURE_FOUNDRY_AGENT_KEY=<optional-if-not-using-managed-identity>

# Feature flags
USE_FOUNDRY_THREADS=true
USE_FOUNDRY_FILES=false
USE_FOUNDRY_VECTORS=false
USE_FOUNDRY_TOOLS=false
```

## Practical phased plan (MVP-first)

### Phase 1: Threads (P0)

- Turn on `USE_FOUNDRY_THREADS` for persistence/replay
- Keep Zep as long-term memory
- Keep tool calling via ctxEco MCP + HTTP tools

### Phase 2: Files (P1)

- Use Foundry file storage for uploads and agent artifacts (where it simplifies ops)

### Phase 3: Tools + vector stores (P2)

- Only after we have strong governance + evidence bundles
- Avoid premature migration away from Zep until we have metrics that justify it

## References

- Foundry agents: `https://learn.microsoft.com/en-us/azure/ai-foundry/agents/`
- Master integration doc: [Foundry IQ + ctxEco Integration Master](../08-foundry-iq-ctxeco-integration-master.md)

