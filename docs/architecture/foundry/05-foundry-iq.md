---
layout: default
title: Foundry IQ (Enterprise Knowledge Bases)
parent: Foundry (Azure AI Foundry)
nav_order: 5
description: "How Foundry IQ knowledge bases fit into ctxEco DIKW and hybrid retrieval."
---

# Foundry IQ (Enterprise Knowledge Bases)

Foundry IQ is the Foundry-native **knowledge base** layer (multi-source retrieval). In ctxEco, it complements (not replaces) our **Tri-Search™ + Gk** memory substrate.

## Where this fits (DIKW)

- **Foundry IQ**: enterprise documents (SharePoint / OneLake / web, etc.)
- **ctxEco**: episodic + semantic + operational memory, governed with provenance + policy

## Recommended GTM MVP pattern

1. Configure **Foundry IQ KB-1 (M365 Knowledge)** for SharePoint / OneLake
2. Attach ctxEco **MCP server** to the Foundry agents for:
   - cross-source retrieval when KB coverage is incomplete
   - evidence bundles + policy checks
   - ingestion triggers and source status
3. Fuse at the agent layer: “KB grounding + ctxEco memory”

## Status in this repo

ctxEco already defines feature flags for Foundry IQ:

- `USE_FOUNDRY_IQ`
- `FOUNDRY_IQ_KB_ID`

See: [`backend/core/config.py`](https://github.com/derekbmoore/openContextGraph/blob/main/backend/core/config.py)

Implementation note: the **hybrid retrieval** wiring (calling Foundry IQ, normalizing hits, fusing with RRF) is documented in:

- [Foundry IQ Hybrid Search](../../knowledge/02-foundry-iq-hybrid-search.md)
- [Foundry IQ Implementation Notes (POC → Production)](../../knowledge/04-foundry-iq-implementation-notes.md)

## What to build next (minimum)

- A small Foundry IQ client wrapper
- A hybrid search fusion step that preserves:
  - provenance (KB id + source URL)
  - gating context (tenant/project/groups)
  - evidence bundle output (what was used and why)

## Links

- [Foundry IQ + ctxEco Integration Master](../08-foundry-iq-ctxeco-integration-master.md)

