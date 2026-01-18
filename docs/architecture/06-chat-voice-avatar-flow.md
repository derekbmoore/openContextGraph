# Chat → Voice (Voice live WS) → Realtime (WebRTC) → Avatar → Foundry → MCP → Memory (Tri-Search™ + Gk)

This document consolidates end-to-end flow for **chat**, **voice**, and **avatar video** from the UI through Foundry agents/tools, back to ctxeco via MCP or HTTP action groups, and into Tri-Search™ memory (keyword + semantic + Gk/graph). It captures auth boundaries, WebSocket vs WebRTC paths, and regional constraints.

## 1) System Overview (High-Level)

```text
User (Browser)
    ├─ Chat UI → ctxeco API → Foundry Agent → (Action Groups) ctxeco Tools → Memory (Tri-Search™)
    │                                     └─ MCP (optional) → ctxeco Tool Registry
    ├─ Voice (Voice live, WS proxy)
    │    Browser → ctxeco Voice WS → Voice live API (WS/events) → ctxeco → Memory
    ├─ Voice (Azure OpenAI Realtime, WebRTC direct)
    │    Browser ↔ Azure OpenAI Realtime (WebRTC) ← token from ctxeco → transcripts/events → Memory
    └─ Avatar Video (Speech Avatar Relay, WebRTC)
               Browser ↔ Azure Speech Avatar Relay (WebRTC; region-limited) ← ICE creds from ctxeco
```

**Transport reality check**

* **Voice live** is **WebSocket transport**.
* **Azure OpenAI Realtime** supports **WebRTC** (recommended for low-latency audio) and also WebSockets.

Key modules:

* **Chat API**: [backend/api/routes/chat.py](backend/api/routes/chat.py)
* **Voice Router**: [backend/api/routes/voice.py](backend/api/routes/voice.py)
* **Voice Service**: [backend/voice/voicelive_service.py](backend/voice/voicelive_service.py)
* **MCP Server**: [backend/api/routes/mcp.py](backend/api/routes/mcp.py)
* **MCP Tool Registry**: [backend/api/mcp_tools.py](backend/api/mcp_tools.py)
* **Tri-Search™ client**: [backend/memory/client.py](backend/memory/client.py)
* **UI Voice (WS proxy)**: [frontend/src/components/VoiceChat/VoiceChat.tsx](frontend/src/components/VoiceChat/VoiceChat.tsx)
* **UI Voice (WebRTC direct)**: [frontend/src/components/VoiceChat/VoiceChatV2.tsx](frontend/src/components/VoiceChat/VoiceChatV2.tsx)
* **WebRTC hook**: [frontend/src/hooks/useAzureRealtime.ts](frontend/src/hooks/useAzureRealtime.ts)

Related Engram SOPs:

* [engram/docs/operations/webrtc-avatar-sop.md](../../engram/docs/operations/webrtc-avatar-sop.md)
* [engram/docs/05-knowledge-base/azure-ai-configuration.md](../../engram/docs/05-knowledge-base/azure-ai-configuration.md)

---

## 2) Chat Flow (Foundry-First)

**Entry:** `POST /api/v1/chat`

### Sequence

1. **Auth**: `get_current_user()` builds `SecurityContext` (tenant/user/roles).
2. **Context Build**: `EnterpriseContext` assembled (episodic/semantic/operational).
3. **Tri-Search™ Enrichment**: `memory_client.enrich_context(...)` injects facts into context.
4. **Foundry Routing**: if `ELENA_FOUNDRY_AGENT_ID` (or Marcus/Sage) and Foundry project endpoint are configured, call `chat_via_foundry(...)`.
5. **Tooling**:

    * **Preferred**: HTTP Action Groups (server-to-server; easiest to network-isolate).
    * **Optional**: MCP (JSON-RPC) for tool discovery/invocation.
6. **Persist Memory**: `memory_client.add_memory(...)` writes user + assistant turns.

### Foundry endpoint note (Project endpoint form)

Foundry “Project endpoint” is of the form:

* `https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}`
   (or `.../api/projects/_project` for default).

### Auth note (enterprise default)

Plan for **Microsoft Entra ID** (RBAC-driven). For production, Microsoft guidance emphasizes Entra-based auth rather than static keys.

---

## 3) Voice Flow A — Voice live via WS Proxy

**Entry:** `WebSocket /api/v1/voice/voicelive/{session_id}`

### Sequence

1. **Auth + SecurityContext**: user identity mapped for tenant scoping.
2. **Ensure User/Session in memory store**: `memory_client.get_or_create_user` + `get_or_create_session`.
3. **Enrichment**: fetch facts via Tri-Search and inject into session bootstrap (see caveat below).
4. **Voice live connect**: backend connects to Voice live WebSocket and bridges audio/events.
5. **Audio Stream**: browser sends PCM16 chunks; backend forwards; responses stream back.
6. **Persistence**: transcripts/turns written into memory (Tri-Search) async.

### Voice live endpoint + auth (important)

Voice live uses a WS URL shaped like:

* `wss://{resource}.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01&model=gpt-realtime`

Auth options:

* **Entra** via `Authorization: Bearer <token>` with scope `https://ai.azure.com/.default` (legacy `https://cognitiveservices.azure.com/.default`).
* **api-key** via header or querystring.

**Why the proxy matters**: browsers can’t reliably set WS headers before the handshake; backend proxy can.

### Audio format requirement (don’t hand-wave)

Voice live supports **16 kHz or 24 kHz PCM16** audio inputs (mono).

### Audio Capture (Current)

The UI uses **AudioWorkletNode** for mic capture with a fallback to `ScriptProcessorNode` if the worklet cannot be loaded.

### Instruction Caveat (model vs agent sessions)

* If you run **model-based sessions**, you can bootstrap memory via `session.update.instructions`.
* If you run **custom agent sessions**, `instructions` is not supported; inject memory via conversation items/tooling patterns instead.

---

## 4) Voice Flow B — Azure OpenAI Realtime via WebRTC (Direct Browser)

**Entry (token):** `POST /api/v1/voice/realtime/token`

### Sequence

1. Browser requests an ephemeral token from backend.
2. Backend mints token via:

    * `POST https://{resource}.openai.azure.com/openai/v1/realtime/client_secrets`
    * The backend uses `AZURE_OPENAI_REALTIME_ENDPOINT` + `AZURE_OPENAI_REALTIME_KEY`.
    * Endpoint must be `openai.azure.com` (not `services.ai.azure.com`).
3. Browser establishes direct WebRTC connection to:

    * `https://{resource}.openai.azure.com/openai/v1/realtime/calls` (from `calls_url` in token response)
4. Audio flows direct browser ↔ Realtime.
5. Transcripts/events forwarded to backend for memory enrichment and persistence.

**Example token response** (from `/api/v1/voice/realtime/token`):

* `token_type`: `ephemeral_key`
* `access_token`: `...`
* `expires_in`: `60`
* `calls_url`: `https://{resource}.openai.azure.com/openai/v1/realtime/calls`

### Realtime regional guidance (global deployments)

As of current model availability guidance, GPT Realtime “global deployments” are listed in:

* **East US 2** and **Sweden Central**.

### Security note (higher posture option)

You can proxy SDP negotiation through the same token service so the browser never sees the ephemeral token.

---

## 5) Avatar Video — Speech Avatar Relay (WebRTC)

**Entry:** `POST /api/v1/voice/avatar/ice-credentials`

### Sequence

1. Browser asks for ICE/TURN credentials.
2. Backend requests ICE/TURN from Azure Speech (regional).
3. Browser builds `RTCPeerConnection` and negotiates SDP via backend signaling.

### Region requirement (Speech avatar voice sync)

Speech avatar voice sync regions include:

* `westus2`, `westeurope`, `southeastasia` (choose based on tenant/customer constraints).

### Operational gotcha (timeouts)

The avatar real-time API can disconnect after **~5 minutes idle** and has a **~30 minute connection duration limit** (plan keepalives / UX accordingly).

### Data residency note (compliance-friendly)

Speech processing is tied to the Speech resource region (document which region(s) you deploy).

---

## 6) Memory Tri-Search™ (keyword + semantic + Gk)

Tri-Search is implemented in [backend/memory/client.py](backend/memory/client.py):

* **Keyword**: BM25
* **Semantic**: Vector search
* **Gk (Graph Knowledge)**: graph traversal
* **Fusion**: RRF hybrid

Memory endpoints:

* `POST /api/v1/memory/search` (Tri-Search)
* `GET /api/v1/memory/facts/{user_id}`
* `GET /api/v1/memory/episodes`
* `POST /api/v1/memory/enrich`

UI:

* Search page: [frontend/src/pages/Memory/Search.tsx](frontend/src/pages/Memory/Search.tsx)
* Graph (Gk): [frontend/src/pages/Memory/KnowledgeGraph.tsx](frontend/src/pages/Memory/KnowledgeGraph.tsx)

### Tenant Isolation & Authorization

* Tenant scoping is enforced in memory queries via `tenant_id` in `SecurityContext` (see [backend/api/routes/memory.py](backend/api/routes/memory.py)).
* Tool endpoints enforce auth via JWT or agent API keys: [backend/api/routes/tools.py](backend/api/routes/tools.py), [backend/api/agent_keys.py](backend/api/agent_keys.py).

---

## 7) Auth Boundaries (tightened)

* **User Auth (JWT)**: enforced on chat/memory/voice endpoints.
* **Agent/Tool Auth**:

   * Prefer **Entra** service-to-service for Foundry integrations.
   * MCP/API keys only for narrowly scoped, allow-listed agents/tools.

**Scopes cheat-sheet**

* Voice live (Entra): `https://ai.azure.com/.default` (legacy `https://cognitiveservices.azure.com/.default`).
* Azure OpenAI Realtime: API key is used by default in this code path (`AZURE_OPENAI_REALTIME_KEY`).

---

## 8) Config Checklist (Per Customer) — normalized

### Voice live (WS)

* `AZURE_VOICELIVE_WS_URL=wss://{resource}.services.ai.azure.com/voice-live/realtime?api-version=2025-10-01&model=gpt-realtime`
* Auth (recommended): Entra scope `https://ai.azure.com/.default` (legacy `https://cognitiveservices.azure.com/.default`).

### Azure OpenAI Realtime (WebRTC)

* `AZURE_OPENAI_REALTIME_ENDPOINT=https://{resource}.openai.azure.com`
* `AZURE_OPENAI_REALTIME_KEY=...`
* Token mint (server): `POST {AZURE_OPENAI_REALTIME_ENDPOINT}/openai/v1/realtime/client_secrets`
* WebRTC connect (client): `{calls_url}` from `/api/v1/voice/realtime/token`
* Supported regions (global deployments): East US 2, Sweden Central.

### Avatar (Speech / ICE)

* `AZURE_SPEECH_KEY`
* `AZURE_SPEECH_REGION` ∈ `{westus2, westeurope, southeastasia}`

### Foundry Agents (Chat)

* `AZURE_FOUNDRY_PROJECT_ENDPOINT=https://{ai-services-account-name}.services.ai.azure.com/api/projects/{project-name}`
* Auth: Entra-based (managed identity / service principal).
* `ELENA_FOUNDRY_AGENT_ID` (+ Marcus/Sage if used)

---

## 9) Enterprise Hardening Gaps (keep + expand slightly)

Your list is good; the only additions to track:

* **DLP/PII policy point**: confirm whether transcript redaction happens before memory write (tenant-configurable).
* **Key rotation + secret hygiene**: define rotation for agent/tool keys; avoid long-lived secrets where Entra works.
* **Egress controls**: WebRTC browser-direct is hard to private-link; document whether the customer accepts that, or requires proxy/relay patterns.

---

## 10) Common Errors & Fixes

### 10.1 Mixed Content

**Symptom:** `Mixed Content: ... https://ctxeco.com ... http://ctxeco-api...`
**Fix:** Use HTTPS endpoints and ensure `VITE_WS_URL` is `wss://` or derived from https.

### 10.2 Voice live 401/1011

**Root Cause:** wrong endpoint, wrong auth mode, or scope mismatch.
**Fix:**

* Use the proper `wss://.../voice-live/realtime?api-version=...` endpoint.
* If using Entra: ensure token scope `https://ai.azure.com/.default` (or legacy `https://cognitiveservices.azure.com/.default`).
* If using api-key: ensure it’s passed as a WS header (proxy) or querystring (direct).

### 10.3 “Why doesn’t my Voice live WebRTC work?”

Voice live is **WebSocket transport**. For WebRTC direct use **Azure OpenAI Realtime**.

### 10.4 Avatar ICE failures

Ensure Speech key + region alignment. If Managed Identity is flaky in a given account setup, use Speech key for the avatar relay path.

---

## 11) Flow Split Summary

* **Chat**: UI → ctxeco → Foundry Agent → Action Group tools → ctxeco memory.
* **Voice (Voice live WS)**: UI → ctxeco Voice WS → Voice live → ctxeco → memory.
* **Voice (OpenAI Realtime WebRTC)**: UI ↔ Azure OpenAI Realtime (token via ctxeco) → memory enrichment async.
* **Avatar video**: UI ↔ Azure Speech Avatar Relay (ICE from ctxeco). Region-limited.

---

## 12) Regional Guidance

* **Azure OpenAI Realtime (global deployments)**: currently centered on East US 2 and Sweden Central.
* **Speech Avatar voice sync**: Southeast Asia / West Europe / West US 2.
* **Voice live**: resource region constraints apply; document chosen region for compliance.

---

## 13) Verification Commands

* Voice status: `GET /api/v1/voice/status`
* ICE creds: `POST /api/v1/voice/avatar/ice-credentials`
* Token: `POST /api/v1/voice/realtime/token`
* Chat: `POST /api/v1/chat`
* Tri-Search: `POST /api/v1/memory/search`

See also [docs/research/chat-voice-avatar-integration.md](docs/research/chat-voice-avatar-integration.md).
