# Domain Memory Integration: Solving the "Green Intern" Problem in ctxEco

**Date:** 2026-01-21  
**Status:** Design Proposal  
**Inspired by:** Nate B. Jones's Domain Memory concept  
**Builds on:** ctxEco's existing recursive self-awareness patterns

---

## Executive Summary

**Domain Memory** solves the "Green Intern" problem: AI agents that forget project context between sessions. By integrating Nate B. Jones's Domain Memory pattern with ctxEco's existing recursive self-awareness, we create agents that remember architectural decisions, project evolution, and "why" behind code changes—not just "what" was changed.

---

## The Problem: "Green Intern" vs. "Senior Dev"

### Current State (Without Domain Memory)

Every new chat session with an AI agent is like hiring a brand-new intern:
- ✅ Knows *how* to code (general programming knowledge)
- ❌ Doesn't know *your* project's patterns
- ❌ Doesn't remember past architectural decisions
- ❌ Makes generic suggestions that violate project conventions
- ❌ Repeats past mistakes

### Target State (With Domain Memory)

Agents become "Senior Devs" who:
- ✅ Remember project history (from git commit logs)
- ✅ Know architectural patterns (from ingested docs)
- ✅ Understand "why" decisions were made (from episodic memory)
- ✅ Avoid repeating past mistakes
- ✅ Suggest solutions that match project conventions

---

## Integration Architecture: Domain Memory + ctxEco

### Three-Layer Memory Model

```
┌─────────────────────────────────────────────────────────┐
│ Layer 1: Domain Memory (Project-Specific)                │
│ - .ctxeco/domain-memory.md (in repo)                    │
│ - Git commit log analysis                                │
│ - Architectural decision log                            │
│ - Project patterns & conventions                         │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 2: Episodic Memory (Conversation History)         │
│ - Zep sessions (conversation persistence)               │
│ - Episode summaries with topics                         │
│ - Cross-session context retrieval                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Layer 3: Semantic Memory (Knowledge Graph)              │
│ - Tri-Search™ (keyword + vector + graph)                │
│ - Facts, entities, relationships                         │
│ - Provenance-linked knowledge                            │
└─────────────────────────────────────────────────────────┘
```

---

## Implementation Design

### 1. Domain Memory File Structure

**Location:** `.ctxeco/domain-memory.md` (checked into git)

**Structure:**
```markdown
# ctxEco Domain Memory

## Project Evolution (from Git Logs)

### 2026-01-21: Foundry IQ Integration
- **Decision:** Use hybrid approach (Foundry IQ + ctxEco MCP)
- **Why:** Leverage Foundry's enterprise docs while keeping ctxEco differentiation
- **Pattern:** Always pair Foundry IQ KBs with ctxEco evidence bundles
- **Commit:** `abc123` - "docs: Foundry IQ integration master doc"

### 2026-01-19: Voice/Avatar Architecture
- **Decision:** Direct WebRTC for Avatar, WebSocket proxy for Voice
- **Why:** Latency critical for video, simpler for audio-only
- **Pattern:** Use `rt-client` for Avatar, VoiceLive SDK for Voice
- **Commit:** `def456` - "feat: VoiceLive WebSocket proxy"

## Architectural Patterns

### Code Style
- **Database columns:** Always use `snake_case`
- **Python classes:** Use `PascalCase`
- **API routes:** RESTful, `/api/v1/{resource}/{id}`
- **Error handling:** Always include CORS headers in exception handlers

### Integration Patterns
- **Foundry agents:** Always attach ctxEco MCP server for cross-source retrieval
- **Memory search:** Always include tenant_id + acl_groups in filters
- **Tool calls:** Always attribute to authenticated user (Entra OID)

### Anti-Patterns (What NOT to Do)
- ❌ Don't use `api.openai.com` as default endpoint (use Azure env vars)
- ❌ Don't commit secrets to Key Vault (use Managed Identity)
- ❌ Don't make multiple commits within 14 minutes (deployment conflicts)

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

## Known Issues & Solutions

### Issue: Chat returns 500 with CORS errors
**Solution:** Ensure `main.py` has generic exception handler with CORS headers
**Reference:** `docs/operations/troubleshooting_chat_deployment.md`

### Issue: VoiceLive 401 errors
**Solution:** Use Cognitive Services key (not APIM key) for `voicelive-api-key`
**Reference:** `docs/operations/avatar_voice_deployment_guide.md`
```

### 2. Git Commit Log Scanner

**New MCP Tool:** `scan_commit_history`

```python
async def scan_commit_history(
    since_days: int = 30,
    pattern: str = None,
    extract_decisions: bool = True
) -> dict:
    """
    Scan git commit logs to extract:
    - Architectural decisions
    - Pattern changes
    - Bug fixes and solutions
    - Project evolution
    
    Returns structured data for Domain Memory update.
    """
```

**Implementation:**
- Use `git log --since="{since_days} days ago" --pretty=format:"%H|%an|%ad|%s|%b"`
- Parse commit messages for decision keywords ("decided", "chose", "switched", "refactored")
- Extract code patterns from diffs (when `extract_decisions=True`)
- Return structured JSON for Domain Memory ingestion

### 3. Domain Memory Updater

**New MCP Tool:** `update_domain_memory`

```python
async def update_domain_memory(
    decision: str,
    why: str,
    pattern: str = None,
    commit_hash: str = None,
    category: str = "architectural_decision"
) -> dict:
    """
    Update .ctxeco/domain-memory.md with new knowledge.
    
    Categories:
    - architectural_decision
    - bug_fix
    - pattern_established
    - anti_pattern_identified
    - configuration_note
    """
```

**Workflow:**
1. Agent makes architectural decision or fixes bug
2. Agent calls `update_domain_memory` with context
3. Tool updates `.ctxeco/domain-memory.md` file
4. Tool automatically ingests updated file into Zep (via Antigravity Router)
5. Future agents can retrieve this via Tri-Search™

### 4. Domain Memory Retriever

**Enhanced `search_memory` Tool:**

When agents search memory, prioritize Domain Memory results:

```python
async def search_memory_with_domain_context(
    query: str,
    include_domain_memory: bool = True,
    limit: int = 10
) -> dict:
    """
    Search memory with Domain Memory boost.
    
    Strategy:
    1. Search Domain Memory first (project-specific)
    2. Search Episodic Memory (conversation history)
    3. Search Semantic Memory (knowledge graph)
    4. Fuse with RRF, but boost Domain Memory results
    """
```

---

## RPI Pattern Integration (Research → Plan → Implement)

### Research Phase: Domain Memory + Git Logs

**Before writing code, agents should:**

1. **Read Domain Memory** (`.ctxeco/domain-memory.md`)
   - Understand project patterns
   - Learn from past decisions
   - Avoid known anti-patterns

2. **Scan Recent Commits** (via `scan_commit_history`)
   - Understand recent changes
   - Identify evolution patterns
   - Learn from recent fixes

3. **Search Episodic Memory** (via `search_memory`)
   - Find related past conversations
   - Retrieve architectural discussions
   - Understand "why" behind decisions

### Plan Phase: Context-Aware Planning

Agents create plans that:
- Reference Domain Memory patterns
- Avoid known anti-patterns
- Follow project conventions
- Build on past decisions

### Implement Phase: Self-Enriching Loop

After implementation:
1. **Update Domain Memory** (if new pattern/decision)
2. **Ingest solution** into Zep (existing self-enriching workflow)
3. **Create episode** with topics for future retrieval

---

## Integration with Existing ctxEco Features

### Antigravity Router Integration

Domain Memory files should be:
- **Class A (Immutable Truth)**: Architectural decisions, patterns
- **Decay Rate:** 0.01 (very low, these are foundational)
- **Ingested via:** Docling (for layout fidelity) or direct markdown parsing

### Tri-Search™ Enhancement

Domain Memory gets **boosted ranking** in search results:
- Domain Memory matches: +0.3 score boost
- Episodic Memory matches: +0.1 score boost
- Semantic Memory matches: baseline

### MCP Tool Integration

New tools for agents:
1. `scan_commit_history` - Analyze git logs
2. `update_domain_memory` - Write to domain-memory.md
3. `read_domain_memory` - Retrieve current domain memory
4. Enhanced `search_memory` - Domain Memory-aware search

---

## Example Workflow: Fixing a Bug with Domain Memory

**User:** "The chat endpoint is returning 500 errors."

**Agent (Elena) Research Phase:**
1. Calls `read_domain_memory()` → Finds: "Issue: Chat returns 500 with CORS errors. Solution: Ensure main.py has generic exception handler"
2. Calls `scan_commit_history(since_days=7, pattern="chat|error|500")` → Finds recent CORS fix
3. Calls `search_memory("chat 500 error CORS")` → Retrieves past troubleshooting episode

**Agent Plan Phase:**
> "Based on Domain Memory, this is a known issue. The solution is to add a generic exception handler in `main.py` with CORS headers. I see from commit `xyz789` that we fixed this before by ensuring all exceptions include CORS headers."

**Agent Implement Phase:**
1. Fixes the code
2. Calls `update_domain_memory()`:
   ```python
   await update_domain_memory(
       decision="Chat 500 errors require generic exception handler",
       why="FastAPI bypasses middleware on unhandled exceptions, causing CORS failures",
       pattern="Always include CORS headers in exception handlers",
       commit_hash="abc123",
       category="bug_fix"
   )
   ```
3. Calls `trigger_ingestion()` to ingest the fix into Zep

**Result:**
- ✅ Bug fixed
- ✅ Domain Memory updated
- ✅ Future agents will remember this solution
- ✅ No regression loops

---

## File Structure

```
openContextGraph/
├── .ctxeco/
│   ├── domain-memory.md          # Main Domain Memory file
│   ├── domain-memory-history/    # Versioned history
│   │   ├── 2026-01-21.md
│   │   └── 2026-01-20.md
│   └── patterns/                 # Extracted patterns
│       ├── api-patterns.md
│       └── deployment-patterns.md
├── backend/
│   └── memory/
│       └── domain_memory.py      # Domain Memory client
└── backend/api/
    └── mcp_tools.py              # New tools: scan_commit_history, update_domain_memory
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Create `.ctxeco/domain-memory.md` template
- [ ] Implement `read_domain_memory` MCP tool
- [ ] Implement `scan_commit_history` MCP tool
- [ ] Add Domain Memory to Antigravity Router (Class A)

### Phase 2: Auto-Update (Week 2)
- [ ] Implement `update_domain_memory` MCP tool
- [ ] Create git hook to auto-scan commits
- [ ] Integrate with self-enriching workflow
- [ ] Add Domain Memory boost to Tri-Search™

### Phase 3: Agent Integration (Week 3)
- [ ] Update agent prompts to use Domain Memory in Research phase
- [ ] Add RPI pattern to agent workflows
- [ ] Create Domain Memory retrieval helper
- [ ] Test with real bug fixes

### Phase 4: Enhancement (Week 4)
- [ ] Pattern extraction from code diffs
- [ ] Anti-pattern detection
- [ ] Domain Memory versioning
- [ ] Cross-project Domain Memory sharing

---

## Benefits

### For Agents
- ✅ No more "Green Intern" problem
- ✅ Remember project-specific patterns
- ✅ Avoid repeating past mistakes
- ✅ Understand "why" not just "what"

### For Developers
- ✅ Knowledge persists in codebase (not just in agent memory)
- ✅ Onboarding new team members faster
- ✅ Architectural decisions documented automatically
- ✅ Project evolution tracked in git

### For Enterprises
- ✅ Compliance: decisions are auditable (in git)
- ✅ Knowledge transfer: Domain Memory is version-controlled
- ✅ Consistency: agents follow established patterns
- ✅ Reduced regression: agents remember past fixes

---

## Technical Considerations

### Git Integration
- **Read-only:** Agents can read git logs (no write access)
- **File updates:** Agents write to `.ctxeco/domain-memory.md` (requires file system access)
- **Version control:** Domain Memory changes are committed to git (manual or automated)

### Security
- **Tenant isolation:** Domain Memory scoped to project/tenant
- **Access control:** Only authorized agents can update Domain Memory
- **Audit trail:** All Domain Memory updates logged with user/agent attribution

### Performance
- **Caching:** Domain Memory file cached in memory
- **Incremental updates:** Only scan new commits since last scan
- **Search optimization:** Domain Memory indexed separately for fast retrieval

---

## Example: Domain Memory Entry

```markdown
## 2026-01-21: Foundry Agent Endpoint Configuration

**Decision:** Use `openai.azure.com` endpoint (not `cognitiveservices`)

**Why:** 
- Foundry Agent Service requires inference endpoint for Assistants API
- Management endpoint (`cognitiveservices`) doesn't support Threads API
- API version `2024-05-01-preview` is stable (not `2025-xx` previews)

**Pattern:**
```python
AZURE_FOUNDRY_AGENT_ENDPOINT = "https://{account}.openai.azure.com/"
AZURE_FOUNDRY_AGENT_API_VERSION = "2024-05-01-preview"
```

**Anti-Pattern:**
❌ Don't use `https://{account}.services.ai.azure.com` for Assistants API
❌ Don't use `2025-xx` API versions (not stable for Threads)

**Related:**
- Commit: `b0ad1fb` - "docs: remove GE Vernova references"
- Episode: `ep-2026-01-19-foundry-integration`
- Doc: `docs/operations/troubleshooting_chat_deployment.md`
```

---

## Next Steps

1. **Create Domain Memory template** (`.ctxeco/domain-memory.md`)
2. **Implement `scan_commit_history` tool** (git log parsing)
3. **Implement `update_domain_memory` tool** (file writing + Zep ingestion)
4. **Update agent prompts** to use Domain Memory in Research phase
5. **Test with real workflow** (fix a bug, verify Domain Memory update)

---

## References

- Nate B. Jones: "AI Agents That Actually Work" (Domain Memory concept)
- ctxEco Self-Enriching Workflow: `docs/01-architecture/self-enriching-workflow.md`
- Recursive Self-Awareness: Existing pattern in ctxEco agents
- RPI Pattern: Research → Plan → Implement
