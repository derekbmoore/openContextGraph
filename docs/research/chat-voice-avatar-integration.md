# Chat, Voice, Avatar Integration Strategy

**Date:** 2026-01-17  
**Status:** NEEDS FIX  
**Priority:** P0

---

## Problem Statement

The current ctxeco.com deployment has broken chat, voice, and avatar features. The routing architecture needs clarification to work properly with Azure AI Foundry agents.

---

## Current Architecture (Broken)

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                              ctxeco.com SPA                              │
│                        (Static Web App - Frontend)                       │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────────────────┐
        ▼                          ▼                                      ▼
┌───────────────┐       ┌───────────────────┐              ┌──────────────────┐
│  /api/v1/chat │       │  /api/v1/voice/*  │              │   /api/v1/voice/ │
│  (POST)       │       │  (WebSocket)      │              │   avatar/*       │
│  BROKEN ❌     │       │  BROKEN ❌         │              │   BROKEN ❌       │
└───────────────┘       └───────────────────┘              └──────────────────┘
        │                          │                                      │
        └──────────────────────────┴──────────────────────────────────────┘
                                   │
                          api.ctxeco.com
                        Container App API
```

**Issues Identified:**

1. **Chat:** `/api/v1/chat` uses local `AgentRouter` which calls OpenAI directly
2. **Voice:** VoiceLive WebSocket expects Azure Realtime API endpoint
3. **Avatar:** WebRTC avatar needs Azure Speech API credentials

---

## Target Architecture Options

### Option A: Direct Azure (No Foundry)

Keep existing architecture - chat/voice/avatar talk directly to Azure AI services.

```text
Frontend → api.ctxeco.com → Azure OpenAI (chat) / Azure Realtime (voice) / Azure Speech (avatar)
```

**Pros:** Simpler, lower latency  
**Cons:** No Foundry orchestration, agents don't share MCP tools

---

### Option B: Foundry as Orchestrator (New)

All user interactions route through Foundry agents, which use MCP tools.

```text
Frontend → api.ctxeco.com → Azure AI Foundry → (MCP) → api.ctxeco.com → Claude/Gemini/Zep
```

**Pros:** Unified agent behavior, MCP tool sharing  
**Cons:** Higher latency, voice/avatar need special handling

---

### Option C: Hybrid (RECOMMENDED)

- **Chat:** Route through Foundry for orchestration
- **Voice:** Direct to Azure Realtime API (latency critical)
- **Avatar:** Direct to Azure Speech (WebRTC critical)

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                              ctxeco.com                                  │
└──────────────────────────────────┬──────────────────────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────────────────┐
        ▼                          ▼                                      ▼
┌───────────────┐       ┌───────────────────┐              ┌──────────────────┐
│  Chat (Foundry)│       │  Voice (Direct)   │              │  Avatar (Direct) │
│  gpt-5.2-chat │       │  Azure Realtime   │              │  Azure Speech    │
│  + MCP Tools  │       │  gpt-realtime     │              │  WebRTC          │
└───────────────┘       └───────────────────┘              └──────────────────┘
        │                          │                                      │
        ▼                          ▼                                      ▼
┌───────────────┐       ┌───────────────────┐              ┌──────────────────┐
│  MCP Server   │       │  Memory Enrich    │              │  Ice Credentials │
│  (Zep/Claude) │       │  (POST /enrich)   │              │  (Relay Tokens)  │
└───────────────┘       └───────────────────┘              └──────────────────┘
```

---

## Required Fixes

### 1. Chat Route (P0)

**Current:** Uses local `AgentRouter` → OpenAI
**Target:** Option depends on decision above

**If keeping direct (Option A/C chat-direct):**

- Verify `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_KEY` env vars
- Ensure `AgentRouter` can find and instantiate agents

**If using Foundry (Option C chat-foundry):**

- Chat endpoint calls Foundry agent via Assistants API
- Agent uses MCP tools via `api.ctxeco.com/mcp`
- Circular but controlled: chat → foundry → mcp → backend services

### 2. Voice Route (P0)

**Issue:** VoiceLive WebSocket needs these environment variables:

```bash
AZURE_AI_SERVICES_ENDPOINT=https://zimax.services.ai.azure.com
AZURE_AI_SERVICES_KEY=<key>
VOICELIVE_DEPLOYMENT=gpt-realtime
```

**Fix:**

- Confirm these are set in Container App environment
- The `/voice/status` shows `voicelive_configured: true` - verify actual connectivity

### 3. Avatar Route (P0)

**Issue:** WebRTC avatar needs Azure Speech credentials for ICE servers:

```bash
AZURE_SPEECH_KEY=<key>
AZURE_SPEECH_REGION=westus2
```

**Fix:**

- Confirm these are set in Container App environment
- `/avatar/ice-credentials` must return valid TURN/STUN credentials

---

## Environment Variables Checklist

| Variable | Service | Required |
| :--- | :--- | :--- |
| `AZURE_OPENAI_ENDPOINT` | Chat (direct) | ✅ |
| `AZURE_OPENAI_API_KEY` | Chat (direct) | ✅ |
| `AZURE_AI_SERVICES_ENDPOINT` | Voice | ✅ |
| `AZURE_AI_SERVICES_KEY` | Voice | ✅ |
| `VOICELIVE_DEPLOYMENT` | Voice | ✅ |
| `AZURE_SPEECH_KEY` | Avatar | ✅ |
| `AZURE_SPEECH_REGION` | Avatar | ✅ |
| `ZEP_API_URL` | Memory | ✅ |
| `ZEP_API_KEY` | Memory | ✅ |

---

## Verification Commands

```bash
# 1. Test Chat
curl -X POST "https://api.ctxeco.com/api/v1/chat/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"message": "Hello", "agent": "elena"}'

# 2. Test Voice Status
curl "https://api.ctxeco.com/api/v1/voice/status"

# 3. Test Avatar ICE
curl -X POST "https://api.ctxeco.com/api/v1/voice/avatar/ice-credentials" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "elena"}'

# 4. Test MCP (Foundry agents use this)
curl -X POST "https://api.ctxeco.com/mcp" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MCP_KEY_SAGE" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

---

## Decision Needed

**Which chat architecture do we want?**

- [ ] **Option A:** Keep existing direct Azure OpenAI (simplest, fast)
- [ ] **Option B:** Route all through Foundry (unified, slower)
- [ ] **Option C:** Hybrid - Chat via Foundry, Voice/Avatar direct (recommended)

Once decided, I can implement the fixes.
