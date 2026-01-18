# CtxEco Azure Deployment Architecture

**Last Updated:** 2026-01-17  
**Status:** PoC Running  
**Resource Group:** `ctxeco-rg`  
**Region:** `eastus2`

---

## Executive Summary

This document describes the current Azure infrastructure for CtxEco (OpenContextGraph) and serves as a blueprint for customer tenant deployments.

---

## Architecture Overview

```text
                          ┌─────────────────────────────────────┐
                          │        ctxeco.com (SWA)             │
                          │     Azure Static Web Apps           │
                          │   happy-meadow-0d77a0d0f.azureswa   │
                          └──────────────┬──────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
│   api.ctxeco.com    │    │   zep.ctxeco.com    │    │  Temporal (internal)│
│    ctxeco-api       │    │     ctxeco-zep      │    │  ctxeco-temporal-*  │
│    Port: 8082       │    │    Port: 8000       │    │    Port: 7233       │
└─────────────────────┘    └─────────────────────┘    └─────────────────────┘
              │                          │                          │
              └──────────────────────────┴──────────────────────────┘
                                         │
                          ┌──────────────┴──────────────┐
                          │   ctxeco-aca (Environment)  │
                          │ whitecliff-aa751815.eastus2 │
                          └─────────────────────────────┘
```

---

## Resource Inventory

### Container Apps Environment

| Property | Value |
| :--- | :--- |
| **Name** | `ctxeco-aca` |
| **Default Domain** | `whitecliff-aa751815.eastus2.azurecontainerapps.io` |
| **Region** | `eastus2` |

### Container Apps

| App | Custom Domain | Internal FQDN | Port | External |
| :--- | :--- | :--- | :--- | :--- |
| `ctxeco-api` | `api.ctxeco.com` | `ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io` | 8082 | ✅ |
| `ctxeco-zep` | `zep.ctxeco.com` | `ctxeco-zep.whitecliff-aa751815.eastus2.azurecontainerapps.io` | 8000 | ✅ |
| `ctxeco-temporal-server` | - | `ctxeco-temporal-server.whitecliff-aa751815.eastus2.azurecontainerapps.io` | 7233 | ✅ |
| `ctxeco-temporal-ui` | - | `ctxeco-temporal-ui.whitecliff-aa751815.eastus2.azurecontainerapps.io` | 8080 | ✅ |
| `ctxeco-worker` | - | - | - | ❌ (internal) |

### Static Web App (Frontend)

| Property | Value |
| :--- | :--- |
| **Name** | `ctxeco-web` |
| **Custom Domain** | `ctxeco.com` |
| **Default Hostname** | `happy-meadow-0d77a0d0f.1.azurestaticapps.net` |
| **Staging** | Enabled |

### Data Services

| Service | Endpoint |
| :--- | :--- |
| **PostgreSQL** | `ctxeco-db.postgres.database.azure.com` (v16, Ready) |
| **Key Vault** | `https://ctxecokv.vault.azure.net/` |
| **Blob Storage** | `https://ctxecostore.blob.core.windows.net/` |
| **File Storage** | `https://ctxecostore.file.core.windows.net/` |

### Identity

| Resource | Purpose |
| :--- | :--- |
| `ctxeco-backend-id` | Backend API managed identity |
| `ctxeco-worker-id` | Worker managed identity |
| `ctxeco.onmicrosoft.com` | Azure AD B2C tenant |

---

## API Endpoints

### Production Endpoints

| Service | URL | Auth |
| :--- | :--- | :--- |
| **Frontend** | `https://ctxeco.com` | Azure AD B2C |
| **API** | `https://api.ctxeco.com` | Bearer token |
| **MCP Server** | `https://api.ctxeco.com/mcp` | `x-api-key` header |
| **Zep Memory** | `https://zep.ctxeco.com` | API key |
| **Temporal UI** | Internal only | - |

### MCP Server (Foundry Agents)

```bash
# Test MCP tools/list
curl -X POST "https://api.ctxeco.com/mcp" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MCP_KEY_SAGE" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'

# Returns 8 tools:
# - search_memory, list_episodes
# - generate_story, generate_diagram
# - search_codebase, trigger_ingestion
# - get_project_status, create_github_issue
```

---

## Issues Identified (PoC Blockers)

### P0 - Critical

| Issue | Status | Resolution |
| :--- | :--- | :--- |
| MCP keys hardcoded in source | 🔧 Fixed | Now reads from env vars |
| `azure-ai-projects` version error | 🔧 Fixed | Changed to `>=1.0.0` |
| `search_memory` syntax error | 🔧 Fixed | Restored function definition |

### P1 - High

| Issue | Status | Resolution |
| :--- | :--- | :--- |
| MCP tools are placeholders | ⏳ Pending | Implement real handlers |
| Keys not in Key Vault | ⏳ Pending | Move to `ctxecokv` |
| No audit logging | ⏳ Pending | Add `tool_invocations` table |

### P2 - Medium

| Issue | Status | Resolution |
| :--- | :--- | :--- |
| Thread retention not enforced | ⏳ Pending | Add daily purge job |
| Missing APIM gateway | ⏳ Pending | Route MCP through APIM |
| Temporal UI exposed | ⏳ Pending | Restrict to internal |

---

## Customer Deployment Checklist

### Prerequisites

- [ ] Azure Subscription with Owner access
- [ ] Custom domain with DNS control
- [ ] Azure AD B2C tenant (or External ID)
- [ ] GitHub repository with CI/CD secrets

### Infrastructure (Bicep/ARM)

```bash
# 1. Create Resource Group
az group create --name $CUSTOMER-rg --location eastus2

# 2. Deploy Container Apps Environment
az containerapp env create --name $CUSTOMER-aca \
  --resource-group $CUSTOMER-rg \
  --location eastus2

# 3. Deploy Container Apps (API, Worker, Zep, Temporal)
# See: infra/main.bicep

# 4. Deploy Static Web App
# See: .github/workflows/frontend.yml

# 5. Configure Custom Domains
# See: infra/dns.bicep
```

### Configuration

| Variable | Description | Example |
| :--- | :--- | :--- |
| `AZURE_TENANT_ID` | Customer Azure AD tenant | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_CLIENT_ID` | App registration client ID | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | `https://customer.openai.azure.com/` |
| `ZEP_API_KEY` | Zep Cloud API key | `zep_...` |
| `TEMPORAL_HOST` | Temporal server address | `ctxeco-temporal-server:7233` |
| `MCP_KEY_*` | Agent MCP keys | From Key Vault |

### DNS Records

| Record | Type | Value |
| :--- | :--- | :--- |
| `@` | A | Static Web App IP |
| `api` | CNAME | `$CUSTOMER-api.azurecontainerapps.io` |
| `zep` | CNAME | `$CUSTOMER-zep.azurecontainerapps.io` |

---

## Security Considerations

### Identity & Access

- **User Auth:** Azure AD B2C / External ID
- **Agent Auth:** API keys (move to Key Vault for production)
- **Service-to-Service:** Managed Identity

### Network

- **Frontend:** Public (SWA)
- **API:** Public with TLS
- **Temporal:** Should be internal-only
- **PostgreSQL:** Private endpoint recommended

### Secrets Rotation

| Secret | Location | Rotation |
| :--- | :--- | :--- |
| MCP agent keys | Key Vault | 90 days |
| Database password | Key Vault | 90 days |
| OpenAI API key | Key Vault | On-demand |
| Zep API key | Key Vault | On-demand |

---

## Files Reference

| File | Purpose |
| :--- | :--- |
| `infra/main.bicep` | Infrastructure as Code |
| `.github/workflows/backend.yml` | Backend CI/CD |
| `.github/workflows/frontend.yml` | Frontend CI/CD |
| `backend/api/routes/mcp.py` | MCP JSON-RPC router |
| `backend/api/mcp_tools.py` | Tool registry |
| `docs/research/foundry-agent-integration.md` | Integration plan |
