# ctxEco Domain Memory

> **Purpose:** This file stores project-specific knowledge that agents need to remember across sessions.  
> **How it works:** Agents read this file in the Research phase, update it after making decisions, and it's automatically ingested into Zep for long-term memory.

## Context Ecology Awareness (2026-01-30)

**CRITICAL**: This workspace is a **Context Ecology with Recursive Self-Awareness**.

All AI assistants (VS Code, Cursor, Antigravity) must:
1. **Search memories BEFORE making changes** — Use Tri-Search (keyword, vector, graph)
2. **Write memories AFTER significant improvements** — Persist learnings
3. **Use graph search for provenance** — Understand entity relationships
4. **Update this file for architectural decisions** — This is auto-ingested

### Workspace Components
| Project | Role | Memory Integration |
|---------|------|-------------------|
| ctxEco | Memory backbone, Tri-Search, agents | Primary |
| secai-radar | MCP trust scoring, daily briefs | Consumer |
| zimax-web | Corporate frontend | Consumer |

### Memory Writing Patterns
- **Working Memory**: Create `docs/working-memory/{topic}-{date}.md` with YAML frontmatter
- **Domain Memory**: Update this file for architectural decisions
- **Stories**: Create `docs/stories/story-request-*.md` for Sage generation

### Ingestion Command
```bash
# Uses Azure production API by default
python scripts/ingest_memory.py --all

# Or specify local for development
ZEP_API_URL=http://localhost:8000 python scripts/ingest_memory.py --all
```

### Azure Deployment
All services run in Azure Container Apps (`ctxeco-rg`):
- **ctxEco API**: `https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io`
- **Zep Memory**: `https://ctxeco-zep.whitecliff-aa751815.eastus2.azurecontainerapps.io`
- **Temporal**: `https://ctxeco-temporal-ui.whitecliff-aa751815.eastus2.azurecontainerapps.io`

## Project Evolution (from Git Logs)

### 2026-01-30: Database Credential Unification
- **Decision**: Azure Key Vault as single source of truth for all credentials
- **Rationale**: Multiple services were failing due to fragmented credential stores
- **Documentation**: Created comprehensive guide suite (DATABASE-*.md)

### 2026-01-30: Context Ecology Awareness
- **Decision**: All AI assistants must read/write memories as part of their workflow
- **Rationale**: The system exists to provide recursive self-awareness; this must be explicit
- **Files Created**: Workspace CLAUDE.md, .cursorrules, ingest_memory.py

### 2026-01-30: Azure Production Endpoints Established
- **ctxEco API**: `https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io`
- **Zep Memory**: `https://ctxeco-zep.whitecliff-aa751815.eastus2.azurecontainerapps.io`
- **Temporal UI**: `https://ctxeco-temporal-ui.whitecliff-aa751815.eastus2.azurecontainerapps.io`
- **Azure Portal**: [ctxeco-rg](https://portal.azure.com/#@zimax.net/resource/subscriptions/23f4e2c5-0667-4514-8e2e-f02ca7880c95/resourceGroups/ctxeco-rg/overview)

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

### Shared Database Architecture
- **Server**: `ctxeco-db.postgres.database.azure.com`
- **Databases**: zep, ctxEco, temporal, temporal_visibility, secairadar
- **Credentials**: Azure Key Vault `ctxecokv` is source of truth
- **Connection Format**: `postgresql://ctxecoadmin:PASSWORD@ctxeco-db...5432/DATABASE?sslmode=require`

---

*Last updated: 2026-01-30*  
*This file is automatically ingested into Zep for agent retrieval.*
