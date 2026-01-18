# PoC Readiness Checklist — Chat + Voice + Avatar + Tri‑Search™

Use this checklist to verify the solution is ready for a customer PoC deployment.

## 0) Reference Architecture
- End‑to‑end flow: [docs/architecture/06-chat-voice-avatar-flow.md](../architecture/06-chat-voice-avatar-flow.md)

## 1) Configuration Readiness

### 1.1 Frontend (Static Web App)
- `VITE_API_URL` points to **HTTPS** backend (no http://).
- `VITE_WS_URL` points to **wss://** or is unset (derived from `VITE_API_URL`).
- `VITE_API_SCOPE` matches Entra app (if auth required).

**Fail condition:** Mixed‑content errors in console.

### 1.2 Backend (Container App)
Ensure these are set:
- `AZURE_VOICELIVE_ENDPOINT=https://<account>.services.ai.azure.com`
- `AZURE_VOICELIVE_KEY=<Cognitive Services key>` (not APIM key)
- `AZURE_VOICELIVE_MODEL=gpt-realtime`
- `AZURE_VOICELIVE_API_VERSION=2025-10-01`
- `AZURE_OPENAI_REALTIME_ENDPOINT=https://<resource>.openai.azure.com`
- `AZURE_OPENAI_REALTIME_KEY=<Azure OpenAI key>`
- `AZURE_SPEECH_KEY=<Speech key>`
- `AZURE_SPEECH_REGION=westus2` (avatar relay)
- `AZURE_FOUNDRY_AGENT_ENDPOINT` / `AZURE_FOUNDRY_AGENT_PROJECT`
- `AZURE_FOUNDRY_AGENT_KEY` (or Managed Identity)
- `ELENA_FOUNDRY_AGENT_ID` (plus Marcus/Sage if enabled)

### 1.3 Key Vault
Verify secrets exist and match the target resource:
- `voicelive-api-key` **must** be the Cognitive Services key (not APIM key)
- `azure-speech-key` is valid and from **westus2** Speech resource
- `zep-api-key` matches the Zep instance for `ZEP_API_URL`

## 2) Auth Readiness
- Entra app redirect URIs include customer domain.
- Backend auth enabled: `AUTH_REQUIRED=true`.
- Test user can get token and call `/api/v1/chat`.

## 3) Chat (Foundry) Readiness
**Endpoint:** `POST /api/v1/chat`
- Foundry agent IDs set → Foundry path executes.
- If Foundry fails, local fallback still responds.

**Go/no‑go:** Chat returns `200` with response and writes memory.

## 4) Voice Readiness

### 4.1 VoiceLive v1 (WS proxy)
**Endpoint:** `WebSocket /api/v1/voice/voicelive/{session_id}`
- Connects and returns transcription/audio events.
- No 401 errors from VoiceLive.

### 4.2 Azure OpenAI Realtime (WebRTC direct)
**Endpoint:** `POST /api/v1/voice/realtime/token`
- Returns ephemeral token.
- Browser connects to Azure Realtime without 401.

**Go/no‑go:** Voice status OK and audio response received.

## 5) Avatar (WebRTC) Readiness
**Endpoint:** `POST /api/v1/voice/avatar/ice-credentials`
- Returns TURN credentials.
- Browser completes SDP negotiation and receives video track.

**Go/no‑go:** Avatar video stream plays in UI.

## 6) Tri‑Search™ + Gk Readiness
- `POST /api/v1/memory/search` returns ranked results.
- `POST /api/v1/memory/enrich` succeeds.
- Gk page renders: [frontend/src/pages/Memory/KnowledgeGraph.tsx](../../frontend/src/pages/Memory/KnowledgeGraph.tsx).

## 7) MCP + Tools Readiness
- `POST /mcp` with `tools/list` returns manifest.
- Tool endpoints respond:
  - `/api/v1/tools/search_memory`
  - `/api/v1/tools/enrich_memory`
  - `/api/v1/tools/create_episode`

## 8) Common Failure Modes & Fixes

### Mixed Content (HTTP API)
**Symptom:** `Mixed Content` error.
**Fix:** Update `VITE_API_URL` to https and redeploy frontend.

### VoiceLive 401
**Symptom:** WebSocket 401 or `Invalid response status`.
**Fix:** Ensure `voicelive-api-key` is **Cognitive Services** key and endpoint is `services.ai.azure.com`.

### Realtime 401/403
**Symptom:** `/api/v1/voice/realtime/token` fails or WebRTC connect rejected.
**Fix:** Ensure endpoint is `https://<resource>.openai.azure.com` and key is `AZURE_OPENAI_REALTIME_KEY`.

### Avatar ICE 401/500
**Symptom:** ICE request fails.
**Fix:** Set `AZURE_SPEECH_KEY` + `AZURE_SPEECH_REGION=westus2`.

### ScriptProcessorNode Deprecation
**Symptom:** Console warning.
**Fix:** Migrate to AudioWorkletNode in [frontend/src/components/VoiceChat/VoiceChat.tsx](../../frontend/src/components/VoiceChat/VoiceChat.tsx).

## 9) Go/No‑Go Criteria
**Go** if all are true:
- Chat returns response via Foundry or fallback.
- Voice WS or WebRTC path returns audio response.
- Avatar ICE returns and video stream plays.
- Tri‑Search returns results and enrich writes memory.
- No Mixed Content errors in browser.

**No‑Go** if any of:
- VoiceLive 401
- ICE credentials fail
- Chat cannot authenticate
- Memory search returns empty due to auth or config
