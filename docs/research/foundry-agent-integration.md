# Blueprint: Azure AI Foundry Agent Integration

**Status:** ✅ Phase 2 Complete (MCP + Temporal Integration)  
**Target Service:** Azure AI Foundry Agent Service  
**Endpoint:** `zimax` (Azure OpenAI Service)  
**MCP Server:** `ctxeco.com/mcp`

---

## Executive Summary

We have successfully integrated Elena, Marcus, and Sage as **Azure AI Foundry Agents** using a **Hybrid Tooling Architecture**:

- **Orchestrator Model:** gpt-5.2-chat (all three agents)
- **Tool Protocol:** MCP (Model Context Protocol)
- **Specialist Models:** Claude (stories), Gemini (diagrams)
- **Workflow Engine:** Temporal (durable execution)

---

## What Has Been Achieved ✅

### 1. Agent Provisioning

| Agent | Foundry ID | MCP Connected | Status |
| :--- | :--- | :--- | :--- |
| **Elena** | `asst_4kAvh0iYARDkEfH2NygdLlUp` | ✅ | Ready |
| **Marcus** | `asst_pGd3gsS2ujEAIkKfkIm1JRep` | ✅ | Ready |
| **Sage** | `asst_ab78FfxxCy4uziyHBB4fPr2l` | ✅ | Ready |

### 2. MCP Server Implementation

**Files Created:**

- `backend/api/routes/mcp.py` - JSON-RPC 2.0 router
- `backend/api/mcp_tools.py` - Tool registry (8 tools)
- `backend/api/middleware/auth.py` - Added `get_optional_user`

**Tools Exposed via MCP:**

| Tool | Handler | Status |
| :--- | :--- | :--- |
| `search_memory` | Zep Tri-Search | ✅ Live |
| `list_episodes` | Zep Sessions | ✅ Live |
| `generate_story` | Temporal → Claude | ✅ Live |
| `generate_diagram` | Gemini Activity | ✅ Live |
| `search_codebase` | Placeholder | ⏳ Pending |
| `get_project_status` | Placeholder | ⏳ Pending |
| `create_github_issue` | Placeholder | ⏳ Pending |
| `trigger_ingestion` | Placeholder | ⏳ Pending |

### 3. Multi-Model Pipeline

```text
Foundry Agent (gpt-5.2) → MCP → Temporal Workflow
                                    ├── Claude (story generation)
                                    ├── Gemini (diagram generation)
                                    └── Zep (memory enrichment)
```

### 4. Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                Azure AI Foundry (Agent Orchestration)           │
│                Elena / Marcus / Sage (gpt-5.2-chat)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │ MCP Protocol (JSON-RPC)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ctxeco.com/mcp                               │
│                    (FastAPI Router)                             │
├─────────────────────────────────────────────────────────────────┤
│  initialize   → Server info + capabilities                      │
│  tools/list   → Tool manifest (8 tools)                         │
│  tools/call   → Dispatch to handlers                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Zep Memory    │  │ Temporal      │  │ GitHub API    │
│ (Tri-Search)  │  │ (Workflows)   │  │ (Pending)     │
└───────────────┘  └───────────────┘  └───────────────┘
```

---

## What Still Needs to Be Done ⏳

### Phase 2.5: Deployment & Verification (Current)

| Task | Owner | Dependency | Status |
| :--- | :--- | :--- | :--- |
| Fix `azure-ai-projects` version in requirements.txt | - | - | ✅ Done |
| Deploy backend to ctxeco.com | DevOps | CI/CD | 🔄 In Progress |
| Verify MCP endpoint responds to `tools/list` | QA | Deployment | ⏳ Blocked |
| Test Sage → `generate_story` → Claude | QA | Temporal online | ⏳ Blocked |
| Enrich memory with Foundry integration episode | Sage | Backend online | ⏳ Blocked |

**Acceptance Criteria:**

```bash
curl -X POST https://ctxeco.com/mcp \
  -H "Content-Type: application/json" \
  -H "x-api-key: mcp_sage_..." \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
# Returns: {"result":{"tools":[...8 tools...]}}
```

---

### Phase 3: Built-in Tools & M365 Integration

| Task | Description | Files to Modify |
| :--- | :--- | :--- |
| **3.1 Elena SharePoint** | Add Foundry built-in SharePoint tool to Elena agent definition | Foundry Portal |
| **3.2 Marcus ripgrep** | Implement real `search_codebase` using subprocess ripgrep | `mcp.py` dispatch |
| **3.3 Marcus GitHub Issues** | Implement `create_github_issue` via GitHub App API | `mcp.py` + GitHub App |
| **3.4 Marcus Project Status** | Implement `get_project_status` via GitHub Projects API | `mcp.py` |
| **3.5 Elena trigger_ingestion** | Wire `trigger_ingestion` to ETL router | `mcp.py` → `etl.ingest()` |

**Implementation Details:**

```python
# 3.2 search_codebase - Real implementation
import subprocess
result = subprocess.run(
    ["rg", "--json", query, "--max-count", "20"],
    capture_output=True, text=True, cwd="/app"
)
return json.loads(result.stdout)

# 3.3 create_github_issue - GitHub App
from github import Github
gh = Github(os.getenv("GITHUB_APP_TOKEN"))
repo = gh.get_repo("derekbmoore/openContextGraph")
issue = repo.create_issue(title=args["title"], body=args["body"])
return {"issue_number": issue.number, "url": issue.html_url}
```

---

### Phase 4: Enterprise Governance

| Task | Description | Priority |
| :--- | :--- | :--- |
| **4.1 Key Vault Integration** | Move MCP keys from code to Azure Key Vault references | P0 |
| **4.2 Audit Logging** | Log all `tools/call` to `tool_invocations` table | P1 |
| **4.3 Retention Policy** | Daily job to purge threads older than 30 days | P2 |
| **4.4 APIM Gateway** | Route MCP through Azure API Management V2 | P2 |

**4.1 Key Vault Implementation:**

```python
# Replace hardcoded keys with:
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

client = SecretClient(vault_url="https://ctxeco-kv.vault.azure.net/", credential=DefaultAzureCredential())
MCP_KEY_MARCUS = client.get_secret("mcp-key-marcus").value
```

**4.2 Audit Schema:**

```sql
INSERT INTO tool_invocations (
    run_id, tool_call_id, tenant_id, actor_object_id,
    actor_type, tool_name, decision, inputs_hash, created_at
) VALUES (
    :run_id, :tool_call_id, :tenant_id, :agent_id,
    'autonomous', :tool_name, 'ALLOW', :hash, NOW()
);
```

---

### Phase 5: Identity Boundary (BYOI)

| Task | Description | Validation |
| :--- | :--- | :--- |
| **5.1 Publish Agents** | Convert agents from Draft to Published with Service Principals | Portal check |
| **5.2 Elena OBO Test** | Elena reads user's OneDrive file via delegated token | File content returned |
| **5.3 RBAC Deny Test** | Marcus attempts M365 access → Denied | 403 response |
| **5.4 Elena GitHub Deny** | Elena attempts GitHub issue creation → Denied | 403 response |

**Test Script:**

```bash
# 5.2 - Elena OBO (should succeed)
curl -X POST https://ctxeco.com/mcp \
  -H "x-api-key: mcp_elena_..." \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"read_onedrive","arguments":{"path":"/Documents/test.txt"}},"id":1}'

# 5.3 - Marcus M365 (should fail)
curl -X POST https://ctxeco.com/mcp \
  -H "x-api-key: mcp_marcus_..." \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"read_onedrive","arguments":{"path":"/Documents/test.txt"}},"id":1}'
# Expected: {"error":{"code":-32603,"message":"RBAC: Marcus denied access to M365 tools"}}
```

---

## Configuration Reference

### MCP Server Endpoint

```text
URL: https://api.ctxeco.com/mcp
Method: POST
Content-Type: application/json
```

### API Key Authentication

```text
Header: x-api-key
Values: (stored in Azure Key Vault - use env vars)
  - Elena: $MCP_KEY_ELENA
  - Marcus: $MCP_KEY_MARCUS
  - Sage:   $MCP_KEY_SAGE
```

### Environment Variables (Production)

```bash
MCP_KEY_ELENA=mcp_elena_...  # From Key Vault
MCP_KEY_MARCUS=mcp_marcus_...
MCP_KEY_SAGE=mcp_sage_...
```

---

## Files Modified/Created

| File | Change |
| :--- | :--- |
| `backend/api/routes/mcp.py` | NEW - MCP JSON-RPC router |
| `backend/api/mcp_tools.py` | NEW - Tool registry |
| `backend/api/main.py` | Added MCP router at `/mcp` |
| `backend/api/middleware/auth.py` | Added `get_optional_user` |
| `docs/agents/marcus.yaml` | NEW - Agent definition reference |
| `docs/agents/sage.yaml` | NEW - Agent definition reference |

---

## References

- [Azure AI Foundry Agents](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/)
- [MCP Best Practices](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/tool-best-practice)
- [MCP Memory](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/concepts/what-is-memory)
- [Model Context Protocol Spec](https://spec.modelcontextprotocol.io/)
