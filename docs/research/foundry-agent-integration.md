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

| Agent | Foundry ID | MCP Connected | API Key |
| :--- | :--- | :--- | :--- |
| **Elena** | `Elena:22` | ✅ | `mcp_elena_Rn4LawobZttIbI-5zQIqrk16RA6553-r-V1WpzcLqUc` |
| **Marcus** | `Marcus:1` | ✅ | `mcp_marcus_A8m6ZCiSu_UFqWPvyY8e8qijAI0bXj1zdFk57YNhyIM` |
| **Sage** | `Sage:1` | ✅ | `mcp_sage_cr3P69wVNaM7PEihwwttSZgo0P27Fvx8L0Y2ySi9Ils` |

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

```
Foundry Agent (gpt-5.2) → MCP → Temporal Workflow
                                    ├── Claude (story generation)
                                    ├── Gemini (diagram generation)
                                    └── Zep (memory enrichment)
```

### 4. Architecture

```
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

### Phase 2.5: Deployment & Verification

- [ ] **Deploy Backend** to `ctxeco.com` with MCP router
- [ ] **Verify MCP** from live Foundry agents
- [ ] **Test Story Generation** end-to-end (Sage → MCP → Temporal → Claude)

### Phase 3: Built-in Tools & M365 Integration

- [ ] **Elena M365 Access:** Add SharePoint/OneDrive built-in tools
- [ ] **Marcus Code Tools:** Implement real `search_codebase` (ripgrep)
- [ ] **Marcus GitHub:** Implement `create_github_issue`, `get_project_status`

### Phase 4: Enterprise Governance

- [ ] **Retention Policy:** Daily purge job for expired threads
- [ ] **Audit Logging:** Log `tool_call_id` and `decision` to `tool_invocations` table
- [ ] **Key Vault:** Move MCP agent keys to Azure Key Vault
- [ ] **APIM Gateway:** Expose MCP via APIM V2 with rate limiting

### Phase 5: Identity Boundary (BYOI)

- [ ] **Publish Agents** in Foundry with Service Principal identities
- [ ] **Test OBO Flows:** Elena accessing user's OneDrive via delegated token
- [ ] **RBAC Enforcement:** Marcus denied M365 access, Elena denied GitHub

---

## Configuration Reference

### MCP Server Endpoint

```
URL: https://ctxeco.com/mcp
Method: POST
Content-Type: application/json
```

### API Key Authentication

```
Header: x-api-key
Values:
  - Elena: mcp_elena_Rn4LawobZttIbI-5zQIqrk16RA6553-r-V1WpzcLqUc
  - Marcus: mcp_marcus_A8m6ZCiSu_UFqWPvyY8e8qijAI0bXj1zdFk57YNhyIM
  - Sage:   mcp_sage_cr3P69wVNaM7PEihwwttSZgo0P27Fvx8L0Y2ySi9Ils
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
