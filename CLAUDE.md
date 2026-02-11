# CLAUDE.md — ctxEco (OpenContextGraph)

> **This is the memory backbone of the Context Ecology.**
> ctxEco provides Tri-Search™, agent orchestration, and persistent memory for the entire workspace.

## Project Identity

**ctxEco** (OpenContextGraph) is the Brain + Spine architecture that powers context engineering for the zimax.workspace ecosystem.

## Core Capabilities

### Tri-Search™

Three search modalities with Reciprocal Rank Fusion:

```
                    ┌─────────────────────────────────────┐
                    │           TRI-SEARCH™               │
                    │   Reciprocal Rank Fusion (RRF)      │
                    └─────────────────────────────────────┘
                                    │
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
           ▼                        ▼                        ▼
    ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
    │  KEYWORD    │         │   VECTOR    │         │   GRAPH     │
    │   (BM25)    │         │  (pgvector) │         │ (Graphiti)  │
    │             │         │             │         │             │
    │ Exact match │         │  Semantic   │         │ Provenance  │
    │ IDs, errors │         │  Concepts   │         │ Relations   │
    └─────────────┘         └─────────────┘         └─────────────┘
           │                        │                        │
           └────────────────────────┼────────────────────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────────────┐
                    │    RRF Score = Σ 1/(k + rank_i)     │
                    │         k = 60 (constant)           │
                    └─────────────────────────────────────┘
```

### Memory Types

| Type | Storage | Purpose |
|------|---------|---------|
| **Episodic** | Sessions + Messages | Conversation history |
| **Semantic** | Facts + Entities | Knowledge with provenance |
| **Domain** | `.ctxeco/domain-memory.md` | Project patterns |
| **Working** | `docs/working-memory/` | Journey records |

### Agent Personas

| Agent | System Prompt | Tools |
|-------|---------------|-------|
| **Marcus** | Technical Lead | Code analysis, debugging, architecture |
| **Elena** | Business Analyst | Requirements, strategy, stakeholder comms |
| **Sage** | Storyteller | Narrative generation, visuals, synthesis |

## Azure Deployment (Production)

ctxEco runs in Azure Container Apps (resource group: `ctxeco-rg`):

| Service | URL | Purpose |
|---------|-----|--------|
| **ctxEco API** | `https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io` | Main API, Tri-Search |
| **Zep Memory** | `https://ctxeco-zep.whitecliff-aa751815.eastus2.azurecontainerapps.io` | Vector memory |
| **Temporal Server** | `https://ctxeco-temporal-server.whitecliff-aa751815.eastus2.azurecontainerapps.io` | Workflow orchestration |
| **Temporal UI** | `https://ctxeco-temporal-ui.whitecliff-aa751815.eastus2.azurecontainerapps.io` | Workflow dashboard |
| **Worker** | Internal | Background processing |

**Azure Portal**: [ctxeco-rg](https://portal.azure.com/#@zimax.net/resource/subscriptions/23f4e2c5-0667-4514-8e2e-f02ca7880c95/resourceGroups/ctxeco-rg/overview)

## API Endpoints

### Memory Operations

```bash
# Add messages to session
POST /api/v1/sessions/{session_id}/memory
{
  "messages": [{"role_type": "assistant", "content": "...", "metadata": {...}}]
}

# Search memories (Tri-Search)
POST /api/v1/search
{
  "query": "...",
  "search_type": "hybrid",  # keyword | similarity | hybrid
  "user_id": "...",
  "tenant_id": "...",
  "limit": 10
}

# Add fact (semantic memory)
POST /api/v1/users/{user_id}/facts
{
  "fact": "...",
  "metadata": {"classification": "Class_A", "tags": [...]}
}

# Graph search (provenance)
GET /api/v1/graph/search?query=...&limit=20
```

### MCP Tools

```python
# Available MCP tools
[
  "search_memory",       # Tri-Search across all memory
  "add_memory",          # Add to episodic memory
  "add_fact",            # Add semantic fact
  "read_domain_memory",  # Read project patterns
  "update_domain_memory", # Update project patterns
  "generate_story",      # Sage narrative generation
  "generate_diagram",    # Sage visual generation
]
```

## Architecture

```
ctxEco/
├── backend/
│   ├── agents/          # Marcus, Elena, Sage
│   ├── api/             # FastAPI endpoints
│   ├── memory/          # Zep client, access policies
│   ├── llm/             # Claude, Gemini clients
│   ├── orchestration/   # Temporal workflows
│   └── etl/             # Data ingestion pipelines
├── frontend/            # React 19 + Vite
├── docs/
│   ├── working-memory/  # Episodic journey records
│   ├── stories/         # Sage-generated narratives
│   ├── knowledge/       # Knowledge base articles
│   └── operations/      # Runbooks, guides
└── .ctxeco/
    └── domain-memory.md # Project patterns (auto-ingested)
```

## Database

ctxEco owns these databases on the shared PostgreSQL:

| Database | Purpose |
|----------|---------|
| `zep` | Zep memory service (pgvector) |
| `ctxEco` | Backend application data |
| `temporal` | Workflow orchestration |
| `temporal_visibility` | Workflow search/visibility |

## Writing Memories from This Project

### For Architectural Decisions

Update `.ctxeco/domain-memory.md`:

```markdown
## Architectural Patterns

### New Pattern: [Name]
- **Decision**: What we decided
- **Rationale**: Why we decided it
- **Date**: When
```

### For Journey Records

Create `docs/working-memory/{topic}-{date}.md`:

```yaml
---
title: "Descriptive Title"
summary: "Brief summary for Tri-Search"
date: 2026-01-30
classification: Class A
tags: [tag1, tag2]
---
```

### For Stories

Create `docs/stories/story-request-{topic}.md` with context for Sage.

## Integration with Workspace

ctxEco provides memory services to:
- **secai-radar**: Trust scoring context, daily brief memory
- **zimax-web**: User session context, personalization
- **All AI assistants**: Shared memory via Tri-Search

## Development

### Local Development
```bash
# Start backend
cd backend && source .venv/bin/activate
uvicorn api.main:app --reload --port 8000

# Start frontend
cd frontend && npm run dev

# Run tests
cd backend && pytest tests/ -v
```

### Using Production API
```bash
# Set environment to use Azure
export ZEP_API_URL=https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io

# Test connection
curl $ZEP_API_URL/
```

## Key Environment Variables

```bash
# Production (Azure)
ZEP_API_URL=https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io

# Local development
ZEP_API_URL=http://localhost:8000

# Common
ZEP_API_KEY=                        # if authentication enabled
DATABASE_URL=postgresql://...       # PostgreSQL connection
ANTHROPIC_API_KEY=                  # Claude for Sage
GEMINI_API_KEY=                     # Gemini for visuals
```

---

*ctxEco is the memory backbone. Every improvement to this system enriches the entire workspace's context.*
