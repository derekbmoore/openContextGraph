# Chat Deployment Troubleshooting Guide

**Last Updated:** 2026-01-19
**Context:** OpenContextGraph / CtxEco Platform
**Component:** Chat Agent Service (Foundry & Local)

---

## 🚨 Quick Diagnosis

| Symptom | Error Code | Likely Cause | Fix |
| :--- | :--- | :--- | :--- |
| **Chat fails blindly** | 500 | Duplicate Config Fields OR Missing CORS | Check `config.py` for duplicates; Check `main.py` exception handlers. |
| **Values are `None`** | 500 | Pydantic Field Overrides | Remove duplicate fields in `config.py`. |
| **Agent Not Found** | 404 | Invalid API Version for Assistants | Set `AZURE_FOUNDRY_AGENT_API_VERSION` to `2024-05-01-preview`. |
| **Resource Not Found** | 404 | Invalid Endpoint for Threads | Set `AZURE_FOUNDRY_AGENT_ENDPOINT` to `https://zimax.openai.azure.com/`. |
| **Nested JSON** | 200 | Agent outputting JSON string | Ensure `chat.py` uses `_extract_content` helper. |
| **MCP 404** | 404 | Wrong URL Path | Use `/mcp` (Root level), NOT `/api/v1/mcp`. |

---

## 1. Configuration Reference (ACA)

Ensure these **Environment Variables** are set correctly in the Azure Container App.

### Critical: Foundry / OpenAI Settings

| Variable | Correct Value (Example) | Notes |
| :--- | :--- | :--- |
| `AZURE_FOUNDRY_AGENT_ENDPOINT` | `https://zimax.openai.azure.com/` | **DO NOT** use `cognitiveservices` endpoint for Assistants API. |
| `AZURE_FOUNDRY_AGENT_API_VERSION` | `2024-05-01-preview` | **DO NOT** use `2025-xx` (Future/Preview) versions yet. |
| `AZURE_FOUNDRY_AGENT_KEY` | `[Secret]` | Ensure this maps to the OpenAI resource, not the Hub. |

### Critical: Agent IDs

| Variable | Value |
| :--- | :--- |
| `ELENA_FOUNDRY_AGENT_ID` | `asst_...` |
| `MARCUS_FOUNDRY_AGENT_ID` | `asst_...` |

### Critical: Connectivity

| Variable | Value | Notes |
| :--- | :--- | :--- |
| `CORS_ORIGINS` | `https://ctxeco.com,https://api.ctxeco.com` | Must include frontend origin. |
| `AUTH_REQUIRED` | `true` (Prod) / `false` (Dev) | Affects `get_current_user`. |

---

## 2. Common Issues & Fixes

### Issue A: 500 Error with Generic Message

**Symptoms:** Browser console shows `500 Internal Server Error`, no response body, CORS error.
**Root Cause:** Unhandled exception in FastAPI bypassing middleware.
**Fix:**
Ensure `backend/api/main.py` has a generic exception handler:

```python
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # ... logic to add CORS headers ...
    return JSONResponse(status_code=500, content={"detail": f"{exc}"}, headers=headers)
```

### Issue B: "Missing Credentials" (OpenAIError)

**Symptoms:** Logs show `api_key` is None.
**Root Cause:** Duplicate fields in `backend/core/config.py`. Pydantic v2 overwrites the first definition with the last (which might be None).
**Fix:** Audit `config.py` and remove duplicate `Field(...)` definitions.

### Issue C: 404 Resource Not Found (Marcus/Sage)

**Symptoms:** Local Agent (Elena) works, but remote Foundry Agent (Marcus) fails with 404.
**Root Cause:**

1. **Wrong Endpoint:** Assistants API requires the *Inference* endpoint (`openai.azure.com`), not the *Management* endpoint (`cognitiveservices`).
2. **Wrong Version:** Some preview versions (`2025-11-15-preview`) in Hub might not support Threads on the inference endpoint.
**Fix:** Downgrade API version to `2024-05-01-preview` and correct the endpoint URL.

---

## 3. Verification Runbook

Use these commands to validate the deployment.

### A. Test Chat (Local & Foundry)

```bash
# Test Elena (Local Fallback usually)
curl -X POST 'https://api.ctxeco.com/api/v1/chat/' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://ctxeco.com' \
  -d '{"message":"hi","agent":"elena"}'

# Test Marcus (Foundry Native)
curl -X POST 'https://api.ctxeco.com/api/v1/chat/' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://ctxeco.com' \
  -d '{"message":"hi","agent":"marcus"}'
```

**Success:** JSON response with `{"response": "Hello..."}`.

### B. Test MCP Endpoint (Memory)

```bash
curl -X POST 'https://api.ctxeco.com/mcp' \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://ctxeco.com' \
  -d '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "search_memory", "arguments": {"query": "test"}}, "id": 1}'
```

**Success:** `200 OK` with `{"result": ...}`.
**Note:** Path is `/mcp`, **NOT** `/api/v1/mcp`.

### C. Check Logs

```bash
az containerapp logs show --name ctxeco-api --resource-group ctxeco-rg --type console --tail 50
```

Look for `Foundry run completed` or `chat to Foundry Agent`.
