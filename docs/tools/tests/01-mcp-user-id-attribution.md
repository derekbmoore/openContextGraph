---
layout: default
title: MCP User ID Attribution Test
parent: Tools
nav_order: 20
description: "How to validate user attribution and avoid cross-tenant leakage in MCP tool calls."
---

# MCP User ID Attribution Test

This page documents how to validate that tool calls invoked via **MCP** are **attributed to the correct user** and **scoped to the correct tenant/project**.

## Why this matters

- Prevents cross-tenant leakage
- Enables audit logging (“who did what”)
- Makes GTM demos credible (evidence-first + governance)

## What to verify (minimum)

1. **Tool calls are scoped** to `tenant_id` (and `project_id` when used).
2. **Tool calls are attributed** to the authenticated user identity (Entra OID preferred).
3. **No fallback identity** is used in production pathways.

## Smoke test (MCP tools/list)

```bash
curl -X POST https://api.ctxeco.com/mcp \
  -H "Content-Type: application/json" \
  -H "x-api-key: <agent-key>" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

## Tool call test (example: search_memory)

```bash
curl -X POST https://api.ctxeco.com/mcp \
  -H "Content-Type: application/json" \
  -H "x-api-key: <agent-key>" \
  -d '{
    "jsonrpc":"2.0",
    "method":"tools/call",
    "params":{"name":"search_memory","arguments":{"query":"tenant isolation","limit":5}},
    "id":2
  }'
```

## What to inspect in logs / telemetry

- user id / oid
- tenant id
- project id (if used)
- tool name + inputs hash
- decision (ALLOW/DENY) if policy checks are implemented

