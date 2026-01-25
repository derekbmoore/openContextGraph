# Domain Memory Implementation Example

**Quick Reference:** How to implement Domain Memory tools in ctxEco

---

## Tool 1: `scan_commit_history`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

```python
# In mcp_tools.py
"scan_commit_history": ToolDefinition(
    name="scan_commit_history",
    description="""Scan git commit logs to extract architectural decisions, patterns, and project evolution.
    
    Returns structured data about:
    - Recent commits with decision keywords
    - Pattern changes (code style, architecture)
    - Bug fixes and solutions
    - Project evolution timeline
    
    Use this in the Research phase before making changes.""",
    parameters=[
        ToolParameter(name="since_days", type="number", description="Number of days to look back (default: 30)"),
        ToolParameter(name="pattern", type="string", description="Optional: filter commits by pattern (e.g., 'auth', 'foundry')"),
        ToolParameter(name="extract_decisions", type="boolean", description="Whether to extract decision keywords from commit messages (default: true)"),
    ],
    handler="api.mcp_handlers.scan_commit_history",
)

# In mcp_handlers.py
import subprocess
import re
from datetime import datetime, timedelta

async def scan_commit_history(
    since_days: int = 30,
    pattern: str = None,
    extract_decisions: bool = True
) -> dict:
    """Scan git commit history for Domain Memory extraction."""
    
    # Build git log command
    since_date = (datetime.now() - timedelta(days=since_days)).strftime("%Y-%m-%d")
    cmd = [
        "git", "log",
        f"--since={since_date}",
        "--pretty=format:%H|%an|%ad|%s|%b",
        "--date=iso"
    ]
    
    if pattern:
        cmd.extend(["--grep", pattern])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits = []
        
        # Decision keywords to extract
        decision_keywords = [
            "decided", "chose", "switched", "refactored", "migrated",
            "pattern", "convention", "standard", "architecture", "design"
        ]
        
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
                
            parts = line.split("|", 4)
            if len(parts) < 4:
                continue
                
            commit_hash, author, date, subject, body = parts[0], parts[1], parts[2], parts[3], parts[4] if len(parts) > 4 else ""
            
            commit_data = {
                "hash": commit_hash[:8],
                "author": author,
                "date": date,
                "subject": subject,
                "body": body,
            }
            
            # Extract decisions if requested
            if extract_decisions:
                full_text = f"{subject} {body}".lower()
                decisions = [kw for kw in decision_keywords if kw in full_text]
                if decisions:
                    commit_data["decisions"] = decisions
                    commit_data["is_decision"] = True
            
            commits.append(commit_data)
        
        return {
            "success": True,
            "commits": commits,
            "count": len(commits),
            "since_days": since_days,
            "pattern": pattern,
        }
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Git log scan failed: {e}")
        return {
            "success": False,
            "error": str(e),
            "commits": [],
        }
```

---

## Tool 2: `update_domain_memory`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

```python
# In mcp_tools.py
"update_domain_memory": ToolDefinition(
    name="update_domain_memory",
    description="""Update the Domain Memory file (.ctxeco/domain-memory.md) with new knowledge.
    
    Use this after making architectural decisions, fixing bugs, or establishing patterns.
    The tool will:
    1. Update the domain-memory.md file
    2. Automatically ingest it into Zep (via Antigravity Router)
    3. Return the memory reference for future retrieval
    
    Categories:
    - architectural_decision: New architecture pattern
    - bug_fix: Solution to a recurring problem
    - pattern_established: Code/style convention
    - anti_pattern_identified: What NOT to do
    - configuration_note: Critical config requirement""",
    parameters=[
        ToolParameter(name="decision", type="string", description="The decision or pattern (e.g., 'Use openai.azure.com for Foundry agents')"),
        ToolParameter(name="why", type="string", description="Why this decision was made (rationale)"),
        ToolParameter(name="pattern", type="string", description="Optional: Code pattern or example"),
        ToolParameter(name="anti_pattern", type="string", description="Optional: What NOT to do"),
        ToolParameter(name="commit_hash", type="string", description="Optional: Related commit hash"),
        ToolParameter(name="category", type="string", description="Category: architectural_decision, bug_fix, pattern_established, anti_pattern_identified, configuration_note"),
        ToolParameter(name="related_docs", type="array", description="Optional: Array of related doc paths"),
    ],
    handler="api.mcp_handlers.update_domain_memory",
)

# In mcp_handlers.py
from pathlib import Path
from datetime import datetime

async def update_domain_memory(
    decision: str,
    why: str,
    pattern: str = None,
    anti_pattern: str = None,
    commit_hash: str = None,
    category: str = "architectural_decision",
    related_docs: list = None,
    user: SecurityContext = None
) -> dict:
    """Update Domain Memory file and ingest into Zep."""
    
    domain_memory_path = Path(".ctxeco/domain-memory.md")
    domain_memory_path.parent.mkdir(exist_ok=True)
    
    # Read existing content
    existing_content = ""
    if domain_memory_path.exists():
        existing_content = domain_memory_path.read_text()
    
    # Generate new entry
    today = datetime.now().strftime("%Y-%m-%d")
    entry = f"""
## {today}: {decision[:60]}

**Decision:** {decision}

**Why:** 
{why}

"""
    
    if pattern:
        entry += f"**Pattern:**\n```\n{pattern}\n```\n\n"
    
    if anti_pattern:
        entry += f"**Anti-Pattern:**\n❌ {anti_pattern}\n\n"
    
    if commit_hash:
        entry += f"**Commit:** `{commit_hash}`\n\n"
    
    if related_docs:
        entry += "**Related:**\n"
        for doc in related_docs:
            entry += f"- {doc}\n"
        entry += "\n"
    
    # Append to file (or create new section)
    if "## Project Evolution" not in existing_content:
        new_content = f"""# ctxEco Domain Memory

## Project Evolution (from Git Logs)

{entry}

## Architectural Patterns

## Known Issues & Solutions

"""
    else:
        # Insert after "## Project Evolution"
        sections = existing_content.split("## Architectural Patterns")
        new_content = sections[0] + entry + "\n## Architectural Patterns" + (sections[1] if len(sections) > 1 else "")
    
    # Write file
    domain_memory_path.write_text(new_content)
    
    # Ingest into Zep via Antigravity Router
    from api.routes.etl import trigger_ingestion
    
    ingestion_result = await trigger_ingestion(
        source_type="file",
        source_path=str(domain_memory_path),
        data_class="CLASS_A_TRUTH",  # Domain Memory is immutable truth
        user=user
    )
    
    return {
        "success": True,
        "domain_memory_path": str(domain_memory_path),
        "entry_date": today,
        "category": category,
        "zep_session_id": ingestion_result.get("session_id"),
        "message": f"Domain Memory updated and ingested. Future agents will remember: '{decision[:50]}...'"
    }
```

---

## Tool 3: `read_domain_memory`

**Location:** `backend/api/mcp_tools.py` + `backend/api/mcp_handlers.py`

```python
# In mcp_tools.py
"read_domain_memory": ToolDefinition(
    name="read_domain_memory",
    description="""Read the current Domain Memory file to understand project patterns and decisions.
    
    Use this in the Research phase before making changes.
    Returns the full Domain Memory content for context.""",
    parameters=[
        ToolParameter(name="section", type="string", description="Optional: specific section to read (e.g., 'architectural_patterns', 'known_issues')"),
    ],
    handler="api.mcp_handlers.read_domain_memory",
)

# In mcp_handlers.py
async def read_domain_memory(section: str = None) -> dict:
    """Read Domain Memory file."""
    
    domain_memory_path = Path(".ctxeco/domain-memory.md")
    
    if not domain_memory_path.exists():
        return {
            "success": False,
            "error": "Domain Memory file not found. Create .ctxeco/domain-memory.md first.",
            "content": None,
        }
    
    content = domain_memory_path.read_text()
    
    # Extract specific section if requested
    if section:
        # Simple section extraction (can be enhanced)
        if f"## {section}" in content:
            # Extract section content
            sections = content.split(f"## {section}")
            if len(sections) > 1:
                next_section = sections[1].split("## ", 1)[0] if "## " in sections[1] else sections[1]
                content = f"## {section}{next_section}"
    
    return {
        "success": True,
        "content": content,
        "path": str(domain_memory_path),
        "last_modified": datetime.fromtimestamp(domain_memory_path.stat().st_mtime).isoformat(),
    }
```

---

## Enhanced `search_memory` with Domain Memory Boost

**Location:** `backend/memory/client.py`

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
    
    # Step 1: Search Domain Memory first (if enabled)
    domain_results = []
    if include_domain_memory:
        domain_memory_path = Path(".ctxeco/domain-memory.md")
        if domain_memory_path.exists():
            content = domain_memory_path.read_text()
            # Simple keyword matching (can be enhanced with vector search)
            if query.lower() in content.lower():
                domain_results.append({
                    "content": content,
                    "source": "domain_memory",
                    "score": 1.0,  # High score for Domain Memory
                    "boost": 0.3,  # Additional boost in RRF
                })
    
    # Step 2: Search Episodic Memory (Zep sessions)
    episodic_results = await self.search_episodes(query, limit=limit)
    
    # Step 3: Search Semantic Memory (Tri-Search™)
    semantic_results = await self.search_memory(query, user_id, tenant_id, limit=limit)
    
    # Step 4: Fuse with RRF (Reciprocal Rank Fusion)
    # Domain Memory gets +0.3 boost
    all_results = []
    
    # Add Domain Memory with boost
    for result in domain_results:
        all_results.append({
            **result,
            "final_score": result["score"] + result["boost"],
        })
    
    # Add Episodic with small boost
    for i, result in enumerate(episodic_results):
        all_results.append({
            **result,
            "source": "episodic",
            "final_score": 1.0 / (i + 1) + 0.1,  # RRF + small boost
        })
    
    # Add Semantic
    for i, result in enumerate(semantic_results):
        all_results.append({
            **result,
            "source": "semantic",
            "final_score": 1.0 / (i + 1),  # Standard RRF
        })
    
    # Sort by final_score
    all_results.sort(key=lambda x: x["final_score"], reverse=True)
    
    return {
        "results": all_results[:limit],
        "domain_memory_count": len(domain_results),
        "episodic_count": len(episodic_results),
        "semantic_count": len(semantic_results),
    }
```

---

## Agent Prompt Enhancement

**Update agent system prompts to include Domain Memory in Research phase:**

```yaml
# In docs/agents/elena.yaml or similar
system_prompt: |
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

---

## Example: Complete Workflow

**User:** "Fix the chat 500 error"

**Agent (Elena) Research:**
```python
# Step 1: Read Domain Memory
domain_memory = await read_domain_memory()
# Finds: "Issue: Chat returns 500 with CORS errors. Solution: Ensure main.py has generic exception handler"

# Step 2: Scan recent commits
commits = await scan_commit_history(since_days=7, pattern="chat|error|500")
# Finds: Commit abc123 - "fix: Add CORS headers to exception handler"

# Step 3: Search episodic memory
memory_results = await search_memory("chat 500 error CORS", limit=5)
# Finds: Episode ep-2026-01-19-chat-troubleshooting
```

**Agent Plan:**
> "Based on Domain Memory and commit history, this is a known issue. The solution is to ensure `main.py` has a generic exception handler with CORS headers. I'll check the current implementation and apply the fix."

**Agent Implement:**
1. Fixes the code
2. Updates Domain Memory:
```python
await update_domain_memory(
    decision="Chat 500 errors require generic exception handler with CORS",
    why="FastAPI bypasses middleware on unhandled exceptions, causing CORS failures in browser",
    pattern="Always include CORS headers in @app.exception_handler(Exception)",
    commit_hash="def456",
    category="bug_fix",
    related_docs=["docs/operations/troubleshooting_chat_deployment.md"]
)
```

**Result:**
- ✅ Bug fixed
- ✅ Domain Memory updated
- ✅ Ingested into Zep automatically
- ✅ Future agents will remember this solution

---

## Next Steps

1. **Create `.ctxeco/domain-memory.md` template** (initial file)
2. **Implement the three tools** (`scan_commit_history`, `update_domain_memory`, `read_domain_memory`)
3. **Update agent prompts** to use Domain Memory in Research phase
4. **Test with real workflow** (fix a bug, verify Domain Memory update)
5. **Enhance search** to boost Domain Memory results
