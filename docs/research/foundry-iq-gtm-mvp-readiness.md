# Foundry IQ MCP Server: GTM MVP Readiness Assessment

**Date:** 2026-01-21  
**Focus:** GTM-ready MCP server for Foundry IQ integration  
**Goal:** Ship a sellable MCP server that pairs with Foundry IQ knowledge bases

> **📘 Master Document:** See [Foundry IQ Marketplace GTM Master Plan](./foundry-iq-marketplace-gtm-master.md) for complete marketplace strategy, competitive positioning, and enterprise value proposition.

---

## Executive Summary

**Current Status:** ✅ **Strong Foundation, Needs Foundry IQ Integration**

We have:
- ✅ **9 operational MCP tools** (memory, stories, domain memory, code search)
- ✅ **Domain Memory** with architectural patterns and project knowledge
- ✅ **Episodic Memory** (5+ episodes accessible)
- ✅ **Stories** (Antigravity router, Engram evolution)
- ✅ **Tri-Search™** (keyword + vector + graph retrieval)
- ✅ **MCP endpoint** operational at `https://api.ctxeco.com/mcp`

**Missing for GTM MVP:**
- ❌ **Foundry IQ client** (query knowledge bases)
- ❌ **Hybrid search** (Foundry IQ + Tri-Search™ fusion)
- ❌ **Evidence bundles** (citations + provenance)
- ❌ **Source management** (list/status/trigger ingestion)

---

## What We Can Build On

### 1. Domain Memory ✅

**Location:** `.ctxeco/domain-memory.md`

**What's in it:**
- Architectural patterns (code style, integration patterns)
- Anti-patterns (what NOT to do)
- Critical configurations (Foundry endpoints, API versions)
- Project-specific knowledge (tech stack, deployment)

**GTM Value:**
- Agents remember project context
- Avoids "Green Intern" problem
- Can be extended with customer-specific patterns

### 2. Episodic Memory ✅

**Access:** Via `list_episodes` MCP tool

**What we have:**
- 5+ conversation episodes
- Session tracking
- Metadata storage

**GTM Value:**
- Cross-session continuity
- Conversation history
- Can be extended with summaries and topics

### 3. Stories ✅

**Location:** `docs/stories/`

**Available stories:**
- `antigravity-ingestion-router.md` - Ingestion architecture
- `engram-commit-history.md` - Project evolution (3,122 commits)
- `engram-commit-history-summary.md` - Evolution summary

**GTM Value:**
- Narrative examples for demos
- Architecture explanations
- Can generate customer-specific stories

### 4. MCP Tools (9 Available) ✅

**Current tools:**
1. `search_memory` - Tri-Search™ retrieval
2. `list_episodes` - Conversation history
3. `generate_story` - Narrative generation
4. `generate_diagram` - Visual diagrams
5. `search_codebase` - Code search
6. `read_domain_memory` - Project memory
7. `update_domain_memory` - Update memory
8. `scan_commit_history` - Git analysis
9. `query_database` - SQL queries

**GTM Value:**
- Already operational
- Can be extended with Foundry IQ tools
- Demonstrates capability

---

## GTM MVP Requirements (From Master Doc)

### Minimum Viable ctxEco MCP Toolset

From `docs/architecture/08-foundry-iq-ctxeco-integration-master.md`:

1. ✅ **`search_memory`** (already live): Tri-Search™ retrieval with evidence metadata
2. ❌ **`trigger_ingestion`**: create/refresh a source; route via Antigravity (A/B/C)
3. ❌ **`get_evidence_bundle`** (new): return citations + provenance + why-this-result (auditable)
4. ❌ **`list_sources` / `get_source_status`** (new): "are we connected, indexed, fresh?"
5. ❌ **`policy_check`** (new): explain if a tool action is allowed for this agent/user context

### Foundry IQ Integration Requirements

**Missing:**
- ❌ Foundry IQ client (`backend/integrations/foundry_iq.py`)
- ❌ Knowledge base query functions
- ❌ Hybrid search (Foundry IQ + Tri-Search™)
- ❌ KB status checking

---

## GTM MVP Implementation Plan

### Phase 1: Foundry IQ Integration (Week 1-2)

#### 1.1 Create Foundry IQ Client
**File:** `backend/integrations/foundry_iq.py`

**Functions:**
```python
async def list_knowledge_bases(project_id: str) -> List[Dict]
async def query_knowledge_base(
    kb_id: str, 
    query: str, 
    limit: int = 5,
    filters: Optional[Dict] = None
) -> List[Dict]
async def get_kb_status(kb_id: str) -> Dict
```

**Dependencies:**
- Azure AI Foundry SDK or REST API
- Same auth as Foundry agents

#### 1.2 Implement Hybrid Search
**File:** `backend/memory/hybrid_search.py`

**Function:**
```python
async def hybrid_search(
    query: str,
    foundry_iq_kb_id: Optional[str] = None,
    limit: int = 10,
    tenant_id: str = "default",
    user_id: Optional[str] = None
) -> Dict[str, Any]
```

**Algorithm:**
1. Query Foundry IQ KB (if configured)
2. Query ctxEco Tri-Search™
3. Normalize result schemas
4. Apply RRF (Reciprocal Rank Fusion)
5. Return ranked results with provenance

#### 1.3 Add Foundry IQ MCP Tools
**File:** `backend/api/mcp_tools.py`

**New tools:**
- `query_foundry_iq_kb` - Query a specific KB
- `list_foundry_iq_kbs` - List available KBs
- `get_foundry_iq_kb_status` - Get KB health/status

### Phase 2: Evidence & Governance (Week 2-3)

#### 2.1 Evidence Bundle Tool
**File:** `backend/api/mcp_handlers.py`

**Function:**
```python
async def get_evidence_bundle(
    query: str,
    results: List[Dict],
    tenant_id: str,
    user_id: str
) -> Dict
```

**Returns:**
- Citations with provenance
- Why-this-result explanations
- Source metadata
- Permission context

#### 2.2 Source Management Tools
**New MCP tools:**
- `list_sources` - List connected sources
- `get_source_status` - Source health/indexing status
- `trigger_ingestion` - Refresh a source

#### 2.3 Policy Check Tool
**New MCP tool:**
- `policy_check` - Explain if action is allowed
- Returns: ALLOW/DENY + reasoning
- Considers: tenant, project, user, tool, sensitivity

### Phase 3: Testing & Hardening (Week 3-4)

#### 3.1 Integration Tests
- Test Foundry IQ KB queries
- Test hybrid search fusion
- Test evidence bundles
- Test source management

#### 3.2 Security Hardening
- Tenant isolation verification
- Permission trimming tests
- Audit logging
- Rate limiting

#### 3.3 Documentation
- API documentation
- Integration guides
- Demo scripts
- GTM playbook

---

## GTM MVP Toolset (Final)

### Core Tools (Must Have)

1. ✅ **`search_memory`** - Tri-Search™ (already live)
2. ❌ **`hybrid_search`** - Foundry IQ + Tri-Search™ fusion
3. ❌ **`query_foundry_iq_kb`** - Direct KB query
4. ❌ **`get_evidence_bundle`** - Citations + provenance
5. ❌ **`list_sources`** - Source inventory
6. ❌ **`get_source_status`** - Source health
7. ❌ **`trigger_ingestion`** - Refresh sources
8. ❌ **`policy_check`** - Governance check

### Enhanced Tools (Nice to Have)

9. ✅ **`list_episodes`** - Conversation history
10. ✅ **`read_domain_memory`** - Project context
11. ✅ **`update_domain_memory`** - Learn patterns
12. ✅ **`generate_story`** - Narrative generation
13. ✅ **`generate_diagram`** - Visual diagrams

### Source Unlockers (High GTM Leverage)

14. ❌ **`ingest_onedrive`** - OneDrive connector
15. ❌ **`ingest_teams_chat`** - Teams export
16. ❌ **`query_github_issues`** - GitHub integration
17. ❌ **`query_jira`** - Jira tickets
18. ❌ **`query_splunk`** - Splunk telemetry

---

## GTM Positioning

### Market Differentiation

**"Knowledge Substrate + Governance + Evidence"**

Not just "yet another RAG connector" but:
- **Hybrid retrieval** (Foundry IQ + Tri-Search™)
- **Governed memory** (decay + truth classes + sensitivity)
- **Evidence-first** (provenance + citations + explainability)
- **Cross-source synthesis** (unify Foundry IQ with operational memory)

### Packaging Options

1. **Option 1 (Fastest GTM):** "Bring your own MCP URL" + deployment templates
2. **Option 2 (Enterprise):** Register in Azure API Center for discovery
3. **Option 3 (Marketplace):** Microsoft Marketplace SaaS offer

---

## North-Star Metrics (GTM MVP)

From master doc:
- ✅ **Time-to-first-answer:** < 60 minutes (new tenant → agent answers)
- ✅ **Coverage:** 6+ meaningful sources connected
- ✅ **Evidence rate:** > 80% answers include citations
- ✅ **Safety:** Zero cross-tenant leakage

---

## Implementation Priority

### Week 1: Foundry IQ Client
- [ ] Create `foundry_iq.py` client
- [ ] Implement KB query functions
- [ ] Test KB access

### Week 2: Hybrid Search
- [ ] Create `hybrid_search.py`
- [ ] Implement RRF fusion
- [ ] Test hybrid results

### Week 3: Evidence & Governance
- [ ] Evidence bundle tool
- [ ] Source management tools
- [ ] Policy check tool

### Week 4: Testing & Docs
- [ ] Integration tests
- [ ] Security hardening
- [ ] GTM documentation

---

## What We're Building On

### ✅ Available Now

1. **Domain Memory** - Project patterns and knowledge
2. **Episodic Memory** - 5+ conversation episodes
3. **Stories** - Narrative examples
4. **9 MCP Tools** - Operational and tested
5. **Tri-Search™** - Hybrid retrieval engine
6. **MCP Endpoint** - Live at `https://api.ctxeco.com/mcp`

### ❌ Need to Build

1. **Foundry IQ Client** - Query knowledge bases
2. **Hybrid Search** - Fuse Foundry IQ + Tri-Search™
3. **Evidence Bundles** - Citations + provenance
4. **Source Management** - List/status/trigger
5. **Policy Checks** - Governance validation

---

## Next Steps

1. **Create Foundry IQ Client** (`backend/integrations/foundry_iq.py`)
2. **Implement Hybrid Search** (`backend/memory/hybrid_search.py`)
3. **Add Evidence Bundle Tool** (MCP handler)
4. **Add Source Management Tools** (MCP handlers)
5. **Test End-to-End** (Foundry IQ + ctxEco integration)

---

## References

- [Foundry IQ + ctxEco Integration Master](../architecture/08-foundry-iq-ctxeco-integration-master.md)
- [Foundry IQ Ecosystem Exploration](./foundry-iq-ecosystem-exploration.md)
- [Domain Memory](../.ctxeco/domain-memory.md)
- [Stories](../stories/)
