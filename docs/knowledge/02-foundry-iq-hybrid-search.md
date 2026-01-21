---
layout: default
title: Foundry IQ Hybrid Search (ctxEco + Foundry IQ)
parent: Knowledge
nav_order: 2
description: "Hybrid retrieval strategy: ctxEco Tri-Search™ + Foundry IQ knowledge bases."
---

# Foundry IQ Hybrid Search (ctxEco + Foundry IQ)

> **Status**: Design + POC notes migrated; production implementation in ctxEco is **in progress**.  
> **Goal**: enterprise document grounding via **Foundry IQ**, fused with ctxEco **Tri-Search™** for episodic + graph context.

## Overview

Foundry IQ provides **multi-source knowledge bases** (ex: SharePoint + OneLake + web) for Foundry agents. ctxEco already provides:

- Tri-Search™ over durable memory (keyword + vector + graph signals)
- provenance + “evidence-first” answers
- policy and gating (tenant/project/groups + A/B/C truth class + sensitivity)

The hybrid strategy is:

1. Query ctxEco memory (Tri-Search™)
2. Query Foundry IQ KBs (enterprise documents)
3. Fuse results (RRF or weighted merge), preserving provenance + permission trimming

## What exists in this repo today

- **Feature flags** are already defined in settings:
  - `USE_FOUNDRY_IQ`
  - `FOUNDRY_IQ_KB_ID`
  - See [`backend/core/config.py`](https://github.com/derekbmoore/openContextGraph/blob/main/backend/core/config.py)

## Target integration shape (implementation plan)

### 1) Foundry IQ client

Add a small client wrapper (recommended location: `backend/integrations/foundry_iq.py`) that supports:

- search KB (query + filters + top/limit)
- list KBs (optional)
- get KB metadata (optional)
- auth: **Managed Identity / Entra** preferred; API keys only for controlled environments

### 2) Hybrid search plumbing

Integrate Foundry IQ as an additional retrieval phase (alongside keyword/vector/graph) and fuse:

- simplest: append Foundry IQ hits and re-rank with RRF
- enterprise: add policy-aware weighting by source trust level and sensitivity class

### 3) Gating + evidence

For every Foundry IQ result we keep:

- **provenance**: doc URL, KB id, chunk id
- **gating context**: tenant/project/groups (ctxEco) + permissions (Foundry IQ / source)
- **evidence bundle**: what was used and why

## Related docs

- [Foundry IQ + ctxEco Integration Master](../architecture/08-foundry-iq-ctxeco-integration-master.md)
- [Graph Knowledge (Gk) + Tri-Search™](01-graph-knowledge-tri-search.md)

