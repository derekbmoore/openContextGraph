---
layout: default
title: Foundry Integration Impact Analysis (Non-Breaking)
parent: Foundry (Azure AI Foundry)
nav_order: 8
description: "What Foundry adds vs what ctxEco keeps unchanged for the GTM MVP."
---

# Foundry Integration Impact Analysis (Non-Breaking)

> **Principle**: Foundry integration should be **additive** for the GTM MVP.  
> We use Foundry where it accelerates delivery, and keep ctxEco where we differentiate (governed memory, ingestion, evidence).

## What stays unchanged (core differentiation)

### 1) Tri-Search™ (keyword + vector + graph) remains the knowledge substrate

- Retrieval stays centered on ctxEco memory and graph.
- Foundry IQ is treated as an *additional* enterprise-doc retrieval plane (hybrid), not a replacement.

See:
- [Tri-Search™](../../architecture/04-tri-search.md)
- [Graph Knowledge (Gk) + Tri-Search™](../../knowledge/01-graph-knowledge-tri-search.md)

### 2) Antigravity Router (A/B/C truth classes) remains the ingestion strategy

Foundry can store files; ctxEco still owns **classification + extraction routing + metadata invariants**.

See:
- [Antigravity Router](../../architecture/03-antigravity-router.md)

### 3) Tool governance remains a ctxEco responsibility

Even when tools are invoked via Foundry or MCP, ctxEco is where we enforce:

- tenant/project isolation
- allowlists / policy checks
- evidence bundles and audit trails

See:
- [Tools](../../tools/index.md)

## What Foundry adds (where we leverage it)

### 1) Threads (P0)

Thread persistence improves reliability and demo repeatability.

- Feature flag: `USE_FOUNDRY_THREADS`
- Intent: durable conversation storage without changing agent logic.

See:
- [Foundry Threads](03-foundry-threads.md)

### 2) Knowledge bases (P0/P1)

Foundry IQ knowledge bases are the fastest route to “enterprise docs grounding” for customers who live in M365/OneLake.

See:
- [Foundry IQ (Enterprise Knowledge Bases)](05-foundry-iq.md)

### 3) Orchestration (P1)

Foundry orchestration helps us deliver “single prompt → multi-agent outcome” workflows.

See:
- [Multi-Agent Orchestration (Foundry)](04-multi-agent-orchestration.md)

