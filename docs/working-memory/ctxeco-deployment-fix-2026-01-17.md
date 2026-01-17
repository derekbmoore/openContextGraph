# ctxEco Deployment Fix - Working Memory

**Session:** 2026-01-17
**Status:** In Progress - Local Testing Phase

---

## Key Discovery: Two Backend Codebases

> [!IMPORTANT]
> The `ctxeco-api` container is deployed from **openContextGraph** repo, NOT ctxEco.
>
> - `ctxEco/backend/` - Development/experimental code
> - `openContextGraph/backend/` - Production code deployed to Azure

---

## Fixes Applied

### 1. LLM Endpoint Configuration (Phase 2)

**File:** `openContextGraph/backend/agents/elena.py`

**Problem:** Code defaulted to `api.openai.com` when `LLM_API_BASE` env var not set.

```python
# BEFORE (broken)
llm_api_base = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
```

**Fix:** Use Azure env vars from container configuration.

```python
# AFTER (fixed)
llm_api_base = os.getenv("AZURE_AI_ENDPOINT") or os.getenv("LLM_API_BASE", "")
llm_api_key = os.getenv("AZURE_AI_KEY") or os.getenv("LLM_API_KEY", "")
llm_model = os.getenv("AZURE_AI_DEPLOYMENT") or os.getenv("LLM_MODEL", "gpt-4o")
```

### 2. Zep Session Creation (Phase 1)

**File:** `ctxEco/backend/memory/client.py`

**Problem:** Zep OSS doesn't have `/api/v1/users` endpoint. Session creation failed because code required user to exist.

**Fix:** Track user creation success and omit `user_id` from session payload when user API unavailable.

---

## Container Environment Variables

The ctxeco-api container has these LLM-related env vars configured:

- `AZURE_AI_ENDPOINT` = `https://zimax-gw.azure-api.net/zimax/openai/v1`
- `AZURE_AI_KEY` = (Key Vault secret)
- `AZURE_AI_DEPLOYMENT` = `gpt-5.2-chat`
- `AZURE_AI_MODEL_ROUTER` = `model-router`

---

## Split Stream Architecture (Chat / Voice / Video)

The ctxeco-api has **three separate communication paths**:

| Stream | Handler | Endpoint | SDK/Protocol |
|--------|---------|----------|--------------|
| **Chat (Text)** | `ElenaAgent._call_llm()` | `AZURE_AI_ENDPOINT` (APIM gateway) | httpx REST |
| **Voice (Audio)** | VoiceLive SDK | `AZURE_VOICELIVE_ENDPOINT` (Azure AI Services) | WebSocket |
| **Avatar (Video)** | Direct to browser | Azure Speech Service | WebRTC |

**Key Finding:** The Elena agent LLM fix **only affects text chat**.  
Voice uses the VoiceLive SDK with a completely separate endpoint.

```python
# Voice router explicitly states this (line 27-28):
# Note: agent_chat and get_agent imports removed - not used in voice router
# Voice router uses VoiceLive SDK directly, not agent chat fallback
```

---

## Avatar Architecture Note

The avatar feature uses **split audio/video streams**:

- **VoiceLive WebSocket** for real-time audio (GPT Realtime API)
- **Separate video endpoint** for avatar rendering
- Both must be tested together when validating voice features

---

## Local Testing Results ✅

**Timestamp:** 2026-01-17 09:27 MST

All fixes verified locally:

| Fix | Status | Details |
|-----|--------|---------|
| AZURE_AI_ENDPOINT env var | ✅ PASSED | Code now uses Azure env vars instead of defaulting to api.openai.com |
| APIM headers | ✅ PASSED | Added Ocp-Apim-Subscription-Key and api-key headers |
| max_completion_tokens | ✅ PASSED | GPT-5.x requires this instead of max_tokens |
| Remove temperature | ✅ PASSED | GPT-5.x doesn't support custom temperature |

**Test Output:**

```
✅ SUCCESS: four
```

Elena agent successfully responded to "What is 2+2?" using Azure APIM → GPT-5.2-chat.

---

## Next Steps

- [x] Build local container from openContextGraph
- [x] Create local `.env` with Azure credentials
- [x] Test LLM call directly
- [x] Test Elena agent `_call_llm` method
- [ ] Commit and push fixes to openContextGraph
- [ ] Trigger Azure deployment
- [ ] Verify on ctxeco.com
