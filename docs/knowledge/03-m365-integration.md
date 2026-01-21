---
layout: default
title: Microsoft 365 (Teams + Outlook + SharePoint + OneDrive)
parent: Knowledge
nav_order: 3
description: "M365 integration research and implementation plan for ctxEco (Foundry-first)."
---

# Microsoft 365 Integration (Teams + Outlook + SharePoint + OneDrive)

> **Status**: Research complete; implementation is staged for GTM MVP.  
> **Primary agent owner**: Elena (knowledge + sources).

## Executive summary

Azure AI Foundry enables **native Microsoft 365 integration** so ctxEco agents can meet users where they work:

- **Teams**: publish an agent as a Teams bot
- **Outlook**: add-in experience for summarization + drafting
- **SharePoint**: document access + search + grounding (Foundry IQ + connectors)
- **OneDrive**: requires careful handling (not always available via “remote SharePoint” pathways)

## Integration architecture (target)

```text
Microsoft 365 (Teams / Outlook / SharePoint)
            │
            ▼
Azure AI Foundry Agent Service (Elena / Marcus / Sage)
            │
            ├── Foundry IQ (knowledge bases, multi-source grounding)
            │
            └── ctxEco MCP + Tools (governed memory, ingestion, evidence, policy)
                    │
                    ▼
           Tri-Search™ + Gk + Operational memory
```

## Recommended MVP sequence

### Phase 1 (MVP): SharePoint + Foundry IQ KB

- Connect 1–2 SharePoint sites/libraries.
- Stand up KB-1 (“M365 Knowledge”) in Foundry IQ.
- Ensure permission trimming works and is documented.

### Phase 2: Teams bot for Elena

- Publish Elena to Teams for “where users ask questions.”
- Keep tool surface minimal (search + cite + ingestion requests).

### Phase 3: Outlook add-in (optional for MVP)

- Drafting + summarization are high-value but UX is heavier; ship after Teams unless required by a launch customer.

## Key considerations (gating + safety)

- **Identity**: Entra ID is the boundary (tenant + user + groups).
- **Permission trimming**: enforce at source (SharePoint/Foundry IQ) and in ctxEco (tenant/project/groups).
- **Auditability**: store evidence bundles for every answer used in sales demos.

## Known platform gaps (design around)

- Some SharePoint “remote knowledge source” pathways explicitly **exclude OneDrive**; plan to:
  - ingest OneDrive into an indexable store (Blob/OneLake), or
  - implement OneDrive ingestion as a controlled MCP tool with delegated auth.

## Related docs

- [Foundry IQ Hybrid Search](02-foundry-iq-hybrid-search.md)
- [Foundry IQ + ctxEco Integration Master](../architecture/08-foundry-iq-ctxeco-integration-master.md)

