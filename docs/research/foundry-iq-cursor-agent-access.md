# Foundry IQ Ecosystem: Cursor Agent Access Guide

**Date:** 2026-01-21  
**Purpose:** What components are accessible from this Cursor agent session?

---

## ✅ Directly Accessible (Via Code/File System)

### 1. Foundry Agent Integration
- **File:** `backend/integrations/foundry.py`
- **Status:** ✅ Implemented
- **Access:** Can read, modify, test
- **Capabilities:**
  - Thread management
  - Run execution
  - Memory context injection

### 2. MCP Tools Registry
- **File:** `backend/api/mcp_tools.py`
- **Status:** ✅ Implemented
- **Access:** Can read, modify, add tools
- **Tools Available:** 9 tools defined

### 3. MCP Handlers
- **File:** `backend/api/mcp_handlers.py`
- **Status:** ✅ Implemented
- **Access:** Can read, modify, add handlers
- **Handlers:** Domain memory, commit scanning, code search

### 4. Configuration
- **File:** `backend/core/config.py`
- **Status:** ✅ Implemented
- **Access:** Can read, see config structure
- **Foundry IQ Config:**
  - `USE_FOUNDRY_IQ` (bool)
  - `FOUNDRY_IQ_KB_ID` (optional string)

### 5. Documentation
- **Location:** `docs/`
- **Status:** ✅ Comprehensive
- **Access:** Can read, update, create
- **Key Docs:**
  - `docs/architecture/08-foundry-iq-ctxeco-integration-master.md`
  - `docs/knowledge/02-foundry-iq-hybrid-search.md`
  - `docs/knowledge/03-m365-integration.md`

---

## ⚠️ Partially Accessible (Via API/Remote)

### 1. MCP Endpoint
- **URL:** `https://api.ctxeco.com/mcp`
- **Status:** ✅ Operational
- **Access:** Can test via HTTP/curl
- **Tools Available:** 9 tools via JSON-RPC 2.0

**Test Command:**
```bash
curl -X POST https://api.ctxeco.com/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### 2. Foundry Agents (Elena, Marcus, Sage)
- **Status:** ✅ Configured in Foundry portal
- **Access:** Via Foundry API (requires credentials)
- **Note:** Can't directly access from Cursor without credentials

### 3. Foundry IQ Knowledge Bases
- **Status:** ⚠️ Not implemented
- **Access:** Would need `foundry_iq.py` client
- **Note:** Can create the client implementation

---

## ❌ Not Accessible (Need Implementation)

### 1. Foundry IQ Client
- **File:** `backend/integrations/foundry_iq.py`
- **Status:** ❌ Missing
- **Access:** Can create this file
- **What's Needed:**
  - List KBs
  - Query KB
  - Get KB status

### 2. Hybrid Search
- **File:** `backend/memory/hybrid_search.py`
- **Status:** ❌ Missing
- **Access:** Can create this file
- **What's Needed:**
  - Fuse Foundry IQ + Tri-Search™
  - RRF ranking

### 3. Fabric IQ Integration
- **Status:** ❌ Not explored
- **Access:** Can research and implement
- **What's Needed:**
  - Research Fabric APIs
  - Create integration client

### 4. Work IQ Integration
- **Status:** ❌ Not explored
- **Access:** Can research and implement
- **What's Needed:**
  - Research Work IQ APIs
  - Create integration client

### 5. M365 Connectors
- **Status:** ❌ Not implemented
- **Access:** Can implement
- **What's Needed:**
  - SharePoint connector
  - Teams bot
  - OneDrive tool

---

## What This Cursor Agent Can Do

### ✅ Can Do Now

1. **Read & Understand**
   - Read all Foundry integration code
   - Understand current architecture
   - Review documentation

2. **Create Missing Components**
   - Create `foundry_iq.py` client
   - Create `hybrid_search.py` implementation
   - Create M365 connectors

3. **Test & Validate**
   - Test MCP endpoint via HTTP
   - Run test scripts
   - Validate configurations

4. **Document & Plan**
   - Update documentation
   - Create implementation plans
   - Generate test scripts

### ⚠️ Limited By

1. **No Direct API Access**
   - Can't directly call Foundry APIs (needs credentials)
   - Can't query knowledge bases (client missing)
   - Can test via HTTP if API is public

2. **No Runtime Access**
   - Can't execute running code
   - Can't access live data
   - Can create code that others can run

3. **No Credentials**
   - Can't access Foundry portal
   - Can't query knowledge bases
   - Can create code that uses credentials from env

---

## Recommended Actions from Cursor Agent

### Immediate (Can Do Now)

1. **Create Foundry IQ Client**
   ```python
   # File: backend/integrations/foundry_iq.py
   # Implement: list_knowledge_bases(), query_knowledge_base(), etc.
   ```

2. **Create Hybrid Search**
   ```python
   # File: backend/memory/hybrid_search.py
   # Implement: hybrid_search() with RRF fusion
   ```

3. **Create Test Scripts**
   ```python
   # File: scripts/test_foundry_iq_kb.py
   # Test: KB access, queries, hybrid search
   ```

### Short-term (Requires Credentials/Runtime)

4. **Test Knowledge Base Access**
   - Requires: Foundry credentials
   - Requires: KB ID configured
   - Can create test script for others to run

5. **Test Hybrid Search**
   - Requires: Foundry IQ client working
   - Requires: KB configured
   - Can create test script

### Research (Can Do Now)

6. **Research Fabric IQ APIs**
   - Search documentation
   - Find API references
   - Create integration plan

7. **Research Work IQ APIs**
   - Search documentation
   - Find API references
   - Create integration plan

---

## Quick Reference: Available Tools

### Via MCP Endpoint (`https://api.ctxeco.com/mcp`)

1. `search_memory` - Tri-Search™ (keyword + vector + graph)
2. `list_episodes` - Conversation history
3. `generate_story` - Narrative generation
4. `generate_diagram` - Visual diagrams
5. `search_codebase` - Code search
6. `read_domain_memory` - Project memory
7. `update_domain_memory` - Update project memory
8. `scan_commit_history` - Git log analysis
9. `query_database` - SQL queries

### Via Code (Can Create)

- Foundry IQ client functions
- Hybrid search implementation
- M365 connectors
- Fabric IQ integration
- Work IQ integration

---

## Summary

**From this Cursor agent, you can:**

✅ **Read & Understand** - All code and docs  
✅ **Create Missing Code** - Foundry IQ client, hybrid search, connectors  
✅ **Test via HTTP** - MCP endpoint (if public)  
✅ **Document & Plan** - Implementation roadmaps  

⚠️ **Limited by:**
- No direct API credentials
- No runtime execution
- Can create code for others to run

**Best Next Step:** Create the missing `foundry_iq.py` client and `hybrid_search.py` implementation so the system can actually use Foundry IQ knowledge bases.
