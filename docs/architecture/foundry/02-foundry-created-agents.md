---
layout: default
title: Foundry-Created Agents (Elena/Marcus/Sage)
parent: Foundry (Azure AI Foundry)
nav_order: 2
description: "How to run ctxEco agents as Foundry agents, and when to prefer hybrid mode."
---

# Foundry-Created Agents in ctxEco (Elena/Marcus/Sage)

> **Purpose**: document how to create agents in Foundry and use them in ctxEco, with clear trade-offs for the GTM MVP.

## Two approaches (what to ship vs. what to keep)

### 1) ctxEco-native agents (LangGraph)

- **Pros**: maximum flexibility, custom workflows, full control over tool execution and memory.
- **Cons**: more infrastructure/code to maintain.

### 2) Foundry agents (Foundry runtime)

- **Pros**: managed infra, built-in threads, built-in tool orchestration, agent catalog/discovery.
- **Cons**: less flexibility; tool execution model differs; migrations can be non-trivial.

### Recommendation (GTM MVP)

Use **hybrid** by default:

- Foundry for **agents + tool calling**
- ctxEco for **memory + ingestion + evidence + policy**
- keep LangGraph where we need complex multi-step reasoning

## Creating agents in Foundry (high level)

### Portal

1. Open Foundry project → **Agents**
2. Create agent (Elena/Marcus/Sage)
3. Set:
   - instructions (system prompt)
   - model (deployment)
   - tools (MCP tool + HTTP action group tools)

### API (illustrative)

```python
import httpx
from azure.identity import DefaultAzureCredential

async def create_foundry_agent(endpoint: str, project: str, payload: dict):
    token = DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default")
    headers = {"Authorization": f"Bearer {token.token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{endpoint}/api/projects/{project}/agents",
            headers=headers,
            json=payload,
            params={"api-version": "2024-10-01-preview"},
        )
        r.raise_for_status()
        return r.json()
```

## Tool integration: keep it simple

For GTM MVP, align tools around:

- **MCP server** (ctxEco): `tools/list`, `tools/call` (discoverable tool catalog)
- **HTTP tools** (ctxEco): `/api/v1/tools/*` endpoints for action-group compatibility

## Related docs

- [Foundry IQ + ctxEco Integration Master](../08-foundry-iq-ctxeco-integration-master.md)
- [Agent Service Integration](01-agent-service-integration.md)
- [Foundry Agent Integration Blueprint](../../research/foundry-agent-integration.md)

