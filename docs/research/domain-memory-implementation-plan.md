# Domain Memory Implementation Plan

**Status:** Planning Phase  
**Target:** Multi-IDE support (Cursor, VS Code, Antigravity) + Developer Onboarding  
**Date:** 2026-01-21

---

## Executive Summary

This plan details how to integrate **Domain Memory** (Nate B. Jones pattern) into ctxEco to solve the "Green Intern" problem. The implementation must work seamlessly across **Cursor, VS Code, and Antigravity** IDEs and help developers get started quickly.

---

## Core Requirements

### 1. Multi-IDE Compatibility
- ✅ **File-based**: Domain Memory lives in `.ctxeco/domain-memory.md` (git-tracked)
- ✅ **IDE-agnostic tools**: MCP tools work from any IDE
- ✅ **No IDE-specific dependencies**: Pure Python/FastAPI implementation

### 2. Developer Onboarding
- ✅ **Seed file**: Initial `.ctxeco/domain-memory.md` template
- ✅ **Clear docs**: Quick start guide for developers
- ✅ **Examples**: Real-world usage examples
- ✅ **Discoverability**: Tools visible in MCP tool list

### 3. Integration Points
- ✅ **MCP Tools**: Three new tools (`read_domain_memory`, `update_domain_memory`, `scan_commit_history`)
- ✅ **Agent Prompts**: Update to use Domain Memory in Research phase
- ✅ **Antigravity Router**: Ingest Domain Memory as Class A
- ✅ **Tri-Search**: Boost Domain Memory results

---

## Implementation Phases

### Phase 1: Foundation (Week 1) — Developer Onboarding

**Goal:** Get developers started with Domain Memory immediately

#### 1.1 Create Domain Memory Directory Structure

```
openContextGraph/
├── .ctxeco/
│   ├── domain-memory.md          # Main file (git-tracked)
│   ├── README.md                  # Quick start guide
│   └── .gitkeep                   # Ensure directory is tracked
```

**Actions:**
- [ ] Create `.ctxeco/` directory
- [ ] Create `.ctxeco/domain-memory.md` with seed template
- [ ] Create `.ctxeco/README.md` with quick start
- [ ] Add `.ctxeco/.gitkeep` to ensure directory is tracked

#### 1.2 Seed Template Content

**File:** `.ctxeco/domain-memory.md`

```markdown
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
```

#### 1.3 Quick Start Guide

**File:** `.ctxeco/README.md`

```markdown
# Domain Memory Quick Start

## What is Domain Memory?

Domain Memory solves the "Green Intern" problem: AI agents that forget project context between sessions. This file (`.ctxeco/domain-memory.md`) stores project-specific knowledge that agents need to remember.

## How It Works

1. **Research Phase**: Agents read this file before making changes
2. **Implementation**: Agents make changes following established patterns
3. **Update Phase**: Agents update this file with new decisions/patterns
4. **Auto-Ingestion**: Updates are automatically ingested into Zep for long-term memory

## For Developers

### Reading Domain Memory

Agents automatically read this file via the `read_domain_memory` MCP tool. You can also:
- Open `.ctxeco/domain-memory.md` in any IDE (Cursor, VS Code, Antigravity)
- Search for patterns, decisions, or known issues
- Review project evolution

### Updating Domain Memory

**Option 1: Via Agent**
Ask an agent to update Domain Memory after making a decision:
> "After fixing the CORS issue, update Domain Memory with this solution."

**Option 2: Manual Edit**
Edit `.ctxeco/domain-memory.md` directly, then commit to git. The file will be ingested on next sync.

### MCP Tools Available

- `read_domain_memory` - Read current Domain Memory
- `update_domain_memory` - Update Domain Memory with new knowledge
- `scan_commit_history` - Analyze git logs for decisions/patterns

## Examples

See `docs/research/domain-memory-implementation-example.md` for complete workflow examples.

## Learn More

- [Domain Memory Integration Design](../research/domain-memory-integration.md)
- [Implementation Examples](../research/domain-memory-implementation-example.md)
```

---

### Phase 2: MCP Tools Implementation (Week 1-2)

**Goal:** Implement three MCP tools for Domain Memory

#### 2.1 Tool 1: `read_domain_memory`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

**Implementation:**
- Read `.ctxeco/domain-memory.md` from repo root
- Support optional section filtering
- Return structured JSON with content + metadata
- Handle missing file gracefully (return helpful error)

**Key Considerations:**
- **Multi-IDE**: Use `Path` relative to repo root (works in all IDEs)
- **Error handling**: If file doesn't exist, suggest creating it
- **Caching**: Optional in-memory cache (refresh on file change)

#### 2.2 Tool 2: `update_domain_memory`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

**Implementation:**
- Append new entries to `.ctxeco/domain-memory.md`
- Auto-format entries with date, decision, why, pattern
- Trigger Antigravity Router ingestion (Class A, decay: 0.01)
- Return Zep session ID for reference

**Key Considerations:**
- **File locking**: Handle concurrent updates (append-only reduces conflicts)
- **Format consistency**: Use consistent markdown structure
- **Auto-commit**: Optional git commit (or manual commit by developer)
- **Validation**: Ensure markdown is valid before writing

#### 2.3 Tool 3: `scan_commit_history`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

**Implementation:**
- Use `subprocess` to run `git log` commands
- Parse commit messages for decision keywords
- Extract patterns from commit diffs (optional, advanced)
- Return structured JSON for Domain Memory ingestion

**Key Considerations:**
- **Git availability**: Handle cases where git is not available
- **Performance**: Limit scan to recent commits (default: 30 days)
- **Security**: Read-only git operations (no writes)
- **Pattern extraction**: Use regex/LLM to identify decisions

---

### Phase 3: Agent Integration (Week 2)

**Goal:** Update agents to use Domain Memory in Research phase

#### 3.1 Update Agent System Prompts

**Files to update:**
- `docs/agents/elena.yaml`
- `docs/agents/marcus.yaml`
- `docs/agents/sage.yaml`

**Add to system prompt:**
```yaml
## Research Phase (Before Making Changes)

Before writing code or making decisions, you MUST:

1. **Read Domain Memory**: Use `read_domain_memory` to understand project patterns
2. **Scan Git History**: Use `scan_commit_history` to learn from recent changes
3. **Search Episodic Memory**: Use `search_memory` to find related past conversations

This ensures you:
- Follow established patterns
- Avoid known anti-patterns
- Understand "why" behind decisions
- Don't repeat past mistakes

## Implementation Phase (After Making Changes)

After fixing bugs or making architectural decisions:

1. **Update Domain Memory**: Use `update_domain_memory` to record the decision
2. **Enrich Memory**: The system will automatically ingest the update into Zep
3. **Reference**: Provide the Domain Memory entry date for future agents
```

#### 3.2 Register Tools in Agent Routers

**Files to update:**
- `backend/agents/elena.py` (if using local tool registration)
- `backend/agents/marcus.py`
- `backend/agents/sage.py`

**Action:** Ensure all three Domain Memory tools are available to agents via MCP.

---

### Phase 4: Antigravity Router Integration (Week 2)

**Goal:** Ensure Domain Memory files are ingested as Class A (immutable truth)

#### 4.1 Update Antigravity Router

**File:** `backend/etl/antigravity_router.py` (or equivalent)

**Changes:**
- Detect `.ctxeco/domain-memory.md` files
- Classify as **Class A (Immutable Truth)**
- Set decay rate to **0.01** (very low)
- Use Docling or direct markdown parsing

**Implementation:**
```python
def classify_document(file_path: str) -> str:
    """Classify document by truth value."""
    if ".ctxeco/domain-memory.md" in file_path:
        return "CLASS_A_TRUTH"  # Domain Memory is immutable truth
    # ... existing classification logic
```

#### 4.2 Auto-Ingestion on Update

**Integration point:** `update_domain_memory` handler

**Action:** After updating Domain Memory file, automatically trigger Antigravity Router ingestion.

```python
# In update_domain_memory handler
from api.routes.etl import trigger_ingestion

ingestion_result = await trigger_ingestion(
    source_type="file",
    source_path=str(domain_memory_path),
    data_class="CLASS_A_TRUTH",
    user=user
)
```

---

### Phase 5: Tri-Search Enhancement (Week 3)

**Goal:** Boost Domain Memory results in search

#### 5.1 Enhance `search_memory` Method

**File:** `backend/memory/client.py`

**Changes:**
- Add `include_domain_memory` parameter (default: `True`)
- Search Domain Memory file first (keyword matching or vector search)
- Apply +0.3 score boost to Domain Memory results
- Fuse with existing Tri-Search results using RRF

**Implementation:**
```python
async def search_memory_with_domain_boost(
    self,
    query: str,
    user_id: str,
    tenant_id: str,
    limit: int = 10,
    include_domain_memory: bool = True
) -> dict:
    """Search memory with Domain Memory boost."""
    # Step 1: Search Domain Memory (if enabled)
    domain_results = []
    if include_domain_memory:
        domain_memory_path = Path(".ctxeco/domain-memory.md")
        if domain_memory_path.exists():
            # Search Domain Memory file
            # Apply +0.3 boost
            domain_results = await self._search_domain_memory(query)
    
    # Step 2: Search Episodic Memory (existing)
    episodic_results = await self.search_episodes(query, limit=limit)
    
    # Step 3: Search Semantic Memory (existing)
    semantic_results = await self.search_memory(query, user_id, tenant_id, limit=limit)
    
    # Step 4: Fuse with RRF (Domain Memory gets boost)
    return self._fuse_results(domain_results, episodic_results, semantic_results, limit)
```

---

## File Structure

```
openContextGraph/
├── .ctxeco/
│   ├── domain-memory.md              # Main Domain Memory file (git-tracked)
│   ├── README.md                      # Quick start guide
│   └── .gitkeep                       # Ensure directory is tracked
├── backend/
│   ├── api/
│   │   ├── mcp_tools.py               # Add 3 new tool definitions
│   │   └── mcp_handlers.py            # Add 3 new handler implementations
│   ├── memory/
│   │   └── client.py                  # Enhance search_memory with Domain Memory boost
│   └── etl/
│       └── antigravity_router.py      # Classify Domain Memory as Class A
├── docs/
│   ├── agents/
│   │   ├── elena.yaml                 # Update system prompt
│   │   ├── marcus.yaml                # Update system prompt
│   │   └── sage.yaml                  # Update system prompt
│   └── research/
│       ├── domain-memory-integration.md           # Design doc (already created)
│       ├── domain-memory-implementation-example.md # Examples (already created)
│       └── domain-memory-implementation-plan.md    # This file
```

---

## Multi-IDE Considerations

### Cursor
- ✅ **MCP Tools**: Work via MCP server connection
- ✅ **File Access**: `.ctxeco/domain-memory.md` accessible via file system
- ✅ **Git Integration**: Standard git commands work

### VS Code
- ✅ **MCP Tools**: Work via MCP server connection (if MCP extension installed)
- ✅ **File Access**: `.ctxeco/domain-memory.md` accessible via file system
- ✅ **Git Integration**: Standard git commands work

### Antigravity
- ✅ **MCP Tools**: Work via MCP server connection
- ✅ **File Access**: `.ctxeco/domain-memory.md` accessible via file system
- ✅ **Git Integration**: Standard git commands work

**Key Point:** All tools are **IDE-agnostic** because they:
- Use file system paths (not IDE-specific APIs)
- Use standard git commands (not IDE git integrations)
- Work via MCP protocol (standardized)

---

## Developer Onboarding Checklist

### For New Developers

1. **Clone repo** → `.ctxeco/domain-memory.md` is automatically present
2. **Read `.ctxeco/README.md`** → Understand what Domain Memory is
3. **Open `.ctxeco/domain-memory.md`** → Review existing patterns/decisions
4. **Use agents** → Agents automatically use Domain Memory in Research phase
5. **Update Domain Memory** → Ask agents to update after making decisions

### For Existing Developers

1. **Review Domain Memory** → Check `.ctxeco/domain-memory.md` for new entries
2. **Update patterns** → Add new patterns/decisions as you discover them
3. **Use MCP tools** → Call `read_domain_memory` / `update_domain_memory` via agents
4. **Commit changes** → Domain Memory updates should be committed to git

---

## Testing Strategy

### Unit Tests

1. **`read_domain_memory`**
   - Test reading existing file
   - Test missing file (graceful error)
   - Test section filtering

2. **`update_domain_memory`**
   - Test appending new entry
   - Test markdown formatting
   - Test Antigravity Router trigger

3. **`scan_commit_history`**
   - Test git log parsing
   - Test decision keyword extraction
   - Test missing git (graceful error)

### Integration Tests

1. **Agent Workflow**
   - Agent reads Domain Memory before making changes
   - Agent updates Domain Memory after making changes
   - Domain Memory is ingested into Zep

2. **Search Enhancement**
   - Domain Memory results appear in search
   - Domain Memory results get boost
   - RRF fusion works correctly

### Manual Testing

1. **Multi-IDE Test**
   - Test in Cursor
   - Test in VS Code
   - Test in Antigravity

2. **Developer Workflow**
   - New developer clones repo
   - Developer uses agent
   - Agent uses Domain Memory
   - Developer updates Domain Memory

---

## Risk Mitigation

### Risk 1: Git Merge Conflicts

**Problem:** Multiple developers updating Domain Memory simultaneously

**Mitigation:**
- Use append-only structure (new entries at top)
- Encourage section-based updates (different sections)
- Git merge conflicts are manageable (markdown is text)

### Risk 2: File Not Found

**Problem:** `.ctxeco/domain-memory.md` doesn't exist

**Mitigation:**
- Seed file in repo (always present)
- Graceful error handling in tools
- Clear error messages with instructions

### Risk 3: Git Not Available

**Problem:** `scan_commit_history` fails if git is not available

**Mitigation:**
- Graceful error handling
- Return empty results (don't crash)
- Log warning (not error)

### Risk 4: Performance (Large Domain Memory File)

**Problem:** Domain Memory file grows large over time

**Mitigation:**
- Use section-based reading (read only needed sections)
- Cache file content (refresh on change)
- Consider splitting into multiple files (future enhancement)

---

## Success Metrics

### Phase 1 (Foundation)
- ✅ `.ctxeco/domain-memory.md` exists in repo
- ✅ Developers can read/understand Domain Memory
- ✅ Quick start guide is clear

### Phase 2 (Tools)
- ✅ All three MCP tools implemented
- ✅ Tools work in Cursor, VS Code, Antigravity
- ✅ Tools handle errors gracefully

### Phase 3 (Agent Integration)
- ✅ Agents use Domain Memory in Research phase
- ✅ Agents update Domain Memory after decisions
- ✅ Domain Memory entries are ingested into Zep

### Phase 4 (Search Enhancement)
- ✅ Domain Memory results appear in search
- ✅ Domain Memory results get boost
- ✅ Search performance is acceptable

---

## Next Steps

1. **Create `.ctxeco/` directory structure** (Phase 1.1)
2. **Implement `read_domain_memory` tool** (Phase 2.1)
3. **Implement `update_domain_memory` tool** (Phase 2.2)
4. **Implement `scan_commit_history` tool** (Phase 2.3)
5. **Update agent prompts** (Phase 3.1)
6. **Integrate with Antigravity Router** (Phase 4)
7. **Enhance Tri-Search** (Phase 5)

---

## References

- [Domain Memory Integration Design](./domain-memory-integration.md)
- [Domain Memory Implementation Examples](./domain-memory-implementation-example.md)
- [Nate B. Jones: AI Agents That Actually Work](https://www.youtube.com/watch?v=xNcEgqzlPqs)
- [ctxEco Self-Enriching Workflow](../architecture/01-self-enriching-workflow.md)
