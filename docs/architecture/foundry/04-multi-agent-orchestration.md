---
layout: default
title: Multi-Agent Orchestration (Foundry)
parent: Foundry (Azure AI Foundry)
nav_order: 4
description: "How to use Foundry orchestration for Elena→Marcus→Sage workflows in the GTM MVP."
---

# Multi-Agent Orchestration (Foundry)

> **Goal**: enable “single request → complete deliverable” workflows by coordinating Elena, Marcus, and Sage.

## Why this matters for GTM MVP

Many buyers don’t want “chat”; they want outcomes:

- “Turn this request into requirements → plan → documentation”
- “Analyze this data → produce an executive narrative + evidence”

Orchestration is how we ship those outcomes without the user manually switching personas.

## Hybrid strategy (recommended)

- Use **Foundry orchestration** for multi-step, multi-agent workflows.
- Keep **ctxEco router** for simple, single-agent requests (fast, predictable).

## Target architecture (conceptual)

```text
User query
  ↓
Task analyzer (simple vs complex)
  ├─ Simple → ctxEco router → single agent
  └─ Complex → Foundry workflow orchestrator
              ├─ Elena (requirements/knowledge)
              ├─ Marcus (plan/execution)
              └─ Sage (narrative/diagrams)
```

## Canonical workflow: Requirements → Plan → Docs

```text
Elena: requirements + acceptance criteria
  ↓ (handoff)
Marcus: milestones + risks + timeline
  ↓ (handoff)
Sage: story + diagram + “what to ship” summary
```

## MVP success criteria

- One prompt produces:
  - a requirements artifact
  - a project plan artifact
  - a narrative + diagram artifact
- Each artifact has:
  - provenance links
  - tenant/project gating metadata
  - an evidence bundle (why these sources were used)

## Related docs

- [Foundry IQ + ctxEco Integration Master](../08-foundry-iq-ctxeco-integration-master.md)
- [Tools](../../tools/index.md)
- [Knowledge](../../knowledge/index.md)

