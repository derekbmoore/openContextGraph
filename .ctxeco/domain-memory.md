# ctxEco Domain Memory

> **Purpose:** This file stores project-specific knowledge that agents need to remember across sessions.  
> **How it works:** Agents read this file in the Research phase, update it after making decisions, and it's automatically ingested into Zep for long-term memory.

## Project Evolution (from Git Logs)

*This section is automatically populated by agents when they make architectural decisions or fix bugs.*

## Architectural Patterns

### Code Style
- **Database columns:** Always use `snake_case`
- **Python classes:** Use `PascalCase`
- **API routes:** RESTful, `/api/v1/{resource}/{id}`
- **Error handling:** Always include CORS headers in exception handlers

### Integration Patterns
- **Foundry agents:** Always attach ctxEco MCP server for cross-source retrieval
- **Memory search:** Always include `tenant_id` + `acl_groups` in filters
- **Tool calls:** Always attribute to authenticated user (Entra OID)

### Anti-Patterns (What NOT to Do)
- ❌ Don't use `api.openai.com` as default endpoint (use Azure env vars)
- ❌ Don't commit secrets to Key Vault (use Managed Identity)
- ❌ Don't make multiple commits within 14 minutes (deployment conflicts)

## Known Issues & Solutions

*This section documents recurring problems and their solutions.*

## Project-Specific Knowledge

### Key Technologies
- **Backend:** FastAPI, Python 3.11+
- **Frontend:** React 19, Vite, TypeScript
- **Memory:** Zep (Tri-Search™), PostgreSQL + pgvector
- **Orchestration:** Temporal workflows
- **Deployment:** Azure Container Apps, Static Web Apps

### Critical Configurations
- `AZURE_FOUNDRY_AGENT_ENDPOINT` must be `openai.azure.com` (not `cognitiveservices`)
- `AZURE_FOUNDRY_AGENT_API_VERSION` must be `2024-05-01-preview` (not `2025-xx`)
- `AZURE_SPEECH_REGION` must be `westus2` for Avatar (hard requirement)

---

*Last updated: 2026-01-21*  
*This file is automatically ingested into Zep for agent retrieval.*
