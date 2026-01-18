# Customer Provisioning (PoC) — ctxeco

This runbook documents the full PoC provisioning path for customers so it can be repeated consistently. It covers Tri-Search™, Gk (Graph Knowledge) memory, Foundry agents, and demo tooling.

## Scope
- **Backend**: FastAPI API + memory + tools
- **Frontend**: ctxeco UI
- **Agents**: Foundry agents and action groups
- **Memory**: Tri-Search™ (keyword + vector + Gk fusion)
- **Voice/Avatar**: VoiceLive + Speech (if enabled)

## Prerequisites
- Azure subscription + resource group
- Azure Key Vault
- Azure AI Services account (Foundry/Unified endpoint)
- Azure Container Apps (API + worker)
- Azure Static Web Apps (frontend)
- Entra ID app registration for SPA

## Key Runtime Files
- Backend app: [backend/api/main.py](backend/api/main.py)
- Memory API: [backend/api/routes/memory.py](backend/api/routes/memory.py)
- Tools API: [backend/api/routes/tools.py](backend/api/routes/tools.py)
- MCP endpoint: [backend/api/routes/mcp.py](backend/api/routes/mcp.py)
- Tri-Search client: [backend/memory/client.py](backend/memory/client.py)
- Agent tool definitions: [docs/agents/marcus.yaml](docs/agents/marcus.yaml), [docs/agents/sage.yaml](docs/agents/sage.yaml)
- Feature flags: [config/features.json](config/features.json)

## Required Secrets (Key Vault)
Populate these secrets for each customer deployment (names are fixed):

- `azure-ai-key` — APIM subscription key or AI Services key
- `azure-ai-endpoint` — Foundry/AI Services endpoint (e.g., https://<account>.services.ai.azure.com)
- `azure-ai-project-name` — Foundry project name
- `azure-foundry-agent-endpoint` — Foundry Agent Service endpoint
- `azure-foundry-agent-project` — Foundry project
- `azure-foundry-agent-key` — Foundry Agent Service key (optional if using managed identity)
- `elena-foundry-agent-id` (and `marcus-foundry-agent-id`, `sage-foundry-agent-id` if used)
- `azure-speech-key` — Speech key for avatar
- `voicelive-api-key` — VoiceLive API key

> These are wired into the app by the Key Vault loader in [backend/core/config.py](backend/core/config.py) and the ACA secret references in [infra/modules/backend-aca.bicep](infra/modules/backend-aca.bicep).

## Environment Variables (App)
Set these on the API Container App:

- `AZURE_FOUNDRY_AGENT_ENDPOINT`
- `AZURE_FOUNDRY_AGENT_PROJECT`
- `AZURE_FOUNDRY_AGENT_KEY` (optional)
- `AZURE_FOUNDRY_AGENT_API_VERSION`
- `ELENA_FOUNDRY_AGENT_ID` (+ optional Marcus/Sage)
- `AZURE_VOICELIVE_ENDPOINT`
- `AZURE_VOICELIVE_KEY`
- `AZURE_VOICELIVE_PROJECT_NAME`
- `AZURE_VOICELIVE_API_VERSION`
- `AZURE_VOICELIVE_MODEL`
- `AZURE_SPEECH_KEY`
- `AUTH_REQUIRED` (true in prod)
- `OIDC_ISSUER_URL`, `OIDC_CLIENT_ID`, `OIDC_AUDIENCE` (or Entra fields)

Front-end Vite variables:
- `VITE_API_URL` (e.g., https://api.ctxeco.com)
- `VITE_WS_URL` (e.g., wss://api.ctxeco.com)
- `VITE_API_SCOPE` (optional)

## Tri-Search™ + Gk (Graph Knowledge)
Tri-Search is implemented in [backend/memory/client.py](backend/memory/client.py) and exposed via:

- **Search**: POST `/api/v1/memory/search`
- **Facts**: GET `/api/v1/memory/facts/{user_id}`
- **Episodes**: GET `/api/v1/memory/episodes`
- **Enrich**: POST `/api/v1/memory/enrich`

The Knowledge Graph UI is in [frontend/src/pages/Memory/KnowledgeGraph.tsx](frontend/src/pages/Memory/KnowledgeGraph.tsx).

### Demo Ingestion/Enrichment
For customer demos, use tool endpoints that map to Tri-Search and enrichment:

- POST `/api/v1/tools/search_memory`
- POST `/api/v1/tools/add_fact`
- POST `/api/v1/tools/enrich_memory`
- POST `/api/v1/tools/list_episodes`
- POST `/api/v1/tools/create_episode`

These are defined in [backend/api/routes/tools.py](backend/api/routes/tools.py).

## Foundry Agents + Tooling
Foundry agents can call ctxeco tools via HTTP endpoints:

- Marcus tool config: [docs/agents/marcus.yaml](docs/agents/marcus.yaml)
- Sage tool config: [docs/agents/sage.yaml](docs/agents/sage.yaml)

The MCP server is available at `/mcp` and tool definitions are registered in [backend/api/mcp_tools.py](backend/api/mcp_tools.py).

> Note: Tools are implemented twice (MCP and HTTP) for flexibility. Foundry action groups should point to the HTTP tools.

## Chat Flow (Foundry-first)
The chat route attempts Foundry first, then falls back to local routing:

- Route: POST `/api/v1/chat`
- Logic: [backend/api/routes/chat.py](backend/api/routes/chat.py)

Ensure Foundry agent IDs and endpoint settings are populated or chat will fall back to local routing.

## Voice/Avatar (Optional)
VoiceLive is configured via the environment variables listed above. Avatar requires Speech key.

Reference:
- Voice routes: [backend/api/routes/voice.py](backend/api/routes/voice.py)

## Smoke Test Checklist
1. **Health**: GET `/health`
2. **Chat**: POST `/api/v1/chat` with auth token
3. **Tri-Search**: POST `/api/v1/memory/search`
4. **Enrich**: POST `/api/v1/memory/enrich`
5. **Tools**: POST `/api/v1/tools/search_memory`
6. **UI**: open Memory → Search + Gk graph

## Rollback Notes
- All feature switches live in [config/features.json](config/features.json)
- If Foundry agents fail, chat will fall back to local routing
- If memory calls fail, the app continues with empty results

## Operator Notes
- Avoid “context graph” terminology in customer-facing docs; use **Gk**.
- Fc (Function Calls) refers to explicit tool calls surfaced to users.

## Next Steps for Each Customer
- Update Key Vault secrets with customer-specific keys
- Update Foundry agent action groups to use ctxeco tool URLs
- Confirm CORS origins include customer’s domain
- Run smoke test checklist
