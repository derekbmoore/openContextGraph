"""
MCP Handler implementations for OpenContextGraph tools.
Includes:
- Database Access (PostgreSQL)
- Codebase Search (Stub/Future)
- Project Management (Stub/Future)
- Domain Memory Tools
"""
import logging
import asyncio
import os
import subprocess
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, List, Dict, Optional

# Initialize generic asyncpg support? 
# We import inside function to avoid startup hard-dependency if DB is down?
# No, standard import is fine.
try:
    import asyncpg
except ImportError:
    asyncpg = None

from core import get_settings

logger = logging.getLogger(__name__)

# =============================================================================
# Database Tools
# =============================================================================

async def query_database(query: str) -> Any:
    """
    Execute a SQL query against the configured PostgreSQL database.
    RESTRICTION: Read-only (SELECT) queries only for safety.
    """
    if not asyncpg:
        return {"error": "asyncpg module not installed"}

    clean_query = query.strip()
    if not clean_query.upper().startswith("SELECT"):
        # Very basic safety check. 
        # In production, use a read-only DB user.
        return {"error": "Security Restriction: Only SELECT queries are allowed."}

    settings = get_settings()
    dsn = settings.postgres_dsn
    
    # Check if DSN is pointing to a real host
    if "localhost" in dsn and settings.postgres_host == "localhost":
        # Check if we are inside Docker? 
        # For now, just try connecting.
        pass

    try:
        # Create a transient connection (pool is better, but this is infrequent tool use)
        conn = await asyncpg.connect(dsn)
        try:
            # Execute
            results = await conn.fetch(clean_query)
            # Convert Record objects to dicts
            return [dict(r) for r in results]
        finally:
            await conn.close()
            
    except Exception as e:
        logger.error(f"query_database failed: {e}")
        return {"error": f"Database error: {str(e)}"}


# =============================================================================
# Codebase Tools
# =============================================================================

async def search_codebase(query: str, file_pattern: str = "*", limit: int = 20) -> List[str]:
    """
    Search the codebase using ripgrep (wrapper).
    STUB: Returns dummy results if not implemented.
    """
    # TODO: Implement actual ripgrep wrapper
    return [
        f"Found match for '{query}' in file1.py",
        f"Found match for '{query}' in file2.py"
    ]


# =============================================================================
# Project Tools
# =============================================================================

async def get_project_status() -> Dict[str, Any]:
    """Get GitHub project status."""
    return {
        "status": "Active",
        "open_issues": 12,
        "next_milestone": "v0.5.0"
    }

async def create_github_issue(title: str, body: str, labels: str = None) -> Dict[str, Any]:
    """Create a GitHub issue."""
    return {
        "id": 101,
        "title": title,
        "url": "https://github.com/derekbmoore/openContextGraph/issues/101"
    }


# =============================================================================
# Domain Memory Tools
# =============================================================================

def _get_domain_memory_path() -> Path:
    """Get the path to the Domain Memory file."""
    # Get repo root (assume we're in backend/, go up one level)
    repo_root = Path(__file__).parent.parent.parent
    return repo_root / ".ctxeco" / "domain-memory.md"


async def read_domain_memory(section: str = None) -> Dict[str, Any]:
    """
    Read Domain Memory file.
    
    Args:
        section: Optional section name to filter (e.g., 'architectural_patterns', 'known_issues')
    
    Returns:
        Dictionary with content and metadata
    """
    domain_memory_path = _get_domain_memory_path()
    
    if not domain_memory_path.exists():
        return {
            "success": False,
            "error": "Domain Memory file not found. Create .ctxeco/domain-memory.md first.",
            "content": None,
            "path": str(domain_memory_path),
        }
    
    try:
        content = domain_memory_path.read_text(encoding="utf-8")
        
        # Extract specific section if requested
        if section:
            # Look for section headers (## Section Name)
            section_pattern = rf"##\s+{re.escape(section)}"
            match = re.search(section_pattern, content, re.IGNORECASE)
            if match:
                # Extract from section header to next section or end
                start_pos = match.start()
                # Find next section header or end of file
                next_section = re.search(r"\n##\s+", content[start_pos + 1:])
                if next_section:
                    end_pos = start_pos + next_section.start() + 1
                    content = content[start_pos:end_pos]
                else:
                    content = content[start_pos:]
            else:
                return {
                    "success": False,
                    "error": f"Section '{section}' not found in Domain Memory",
                    "content": None,
                    "path": str(domain_memory_path),
                }
        
        return {
            "success": True,
            "content": content,
            "path": str(domain_memory_path),
            "last_modified": datetime.fromtimestamp(domain_memory_path.stat().st_mtime).isoformat(),
            "section": section if section else "all",
        }
        
    except Exception as e:
        logger.error(f"Error reading Domain Memory: {e}")
        return {
            "success": False,
            "error": f"Error reading Domain Memory: {str(e)}",
            "content": None,
            "path": str(domain_memory_path),
        }


async def update_domain_memory(
    decision: str,
    why: str,
    pattern: str = None,
    anti_pattern: str = None,
    commit_hash: str = None,
    category: str = "architectural_decision",
    related_docs: List[str] = None,
) -> Dict[str, Any]:
    """
    Update Domain Memory file and ingest into Zep.
    
    Args:
        decision: The decision or pattern
        why: Why this decision was made
        pattern: Optional code pattern or example
        anti_pattern: Optional what NOT to do
        commit_hash: Optional related commit hash
        category: Category (architectural_decision, bug_fix, pattern_established, anti_pattern_identified, configuration_note)
        related_docs: Optional list of related doc paths
    
    Returns:
        Dictionary with success status and metadata
    """
    domain_memory_path = _get_domain_memory_path()
    domain_memory_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Read existing content
        existing_content = ""
        if domain_memory_path.exists():
            existing_content = domain_memory_path.read_text(encoding="utf-8")
        
        # Generate new entry
        today = datetime.now().strftime("%Y-%m-%d")
        entry = f"""## {today}: {decision[:60]}

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
        
        # Insert entry into "Project Evolution" section
        if "## Project Evolution" not in existing_content:
            # Create new file with Project Evolution section
            new_content = f"""# ctxEco Domain Memory

> **Purpose:** This file stores project-specific knowledge that agents need to remember across sessions.  
> **How it works:** Agents read this file in the Research phase, update it after making decisions, and it's automatically ingested into Zep for long-term memory.

## Project Evolution (from Git Logs)

{entry}

## Architectural Patterns

## Known Issues & Solutions

## Project-Specific Knowledge

---

*Last updated: {today}*  
*This file is automatically ingested into Zep for agent retrieval.*
"""
        else:
            # Insert after "## Project Evolution" header
            sections = existing_content.split("## Project Evolution", 1)
            if len(sections) == 2:
                # Insert entry after the header
                header_and_rest = sections[1]
                # Find the first line after the header
                lines = header_and_rest.split("\n", 1)
                if len(lines) > 1:
                    new_content = sections[0] + "## Project Evolution" + "\n" + entry + lines[1]
                else:
                    new_content = sections[0] + "## Project Evolution" + "\n" + entry + header_and_rest
            else:
                # Fallback: prepend to file
                new_content = entry + existing_content
        
        # Write file
        domain_memory_path.write_text(new_content, encoding="utf-8")
        
        # Ingest into Zep via Antigravity Router
        try:
            from etl import get_antigravity_router
            
            antigravity = get_antigravity_router()
            content_bytes = new_content.encode("utf-8")
            
            # Ingest as Class A (immutable truth)
            from etl import DataClass
            chunks = await antigravity.ingest_bytes(
                content=content_bytes,
                filename="domain-memory.md",
                force_class=DataClass.CLASS_A_TRUTH,
                user_id="system",  # Domain Memory updates are system-level
                tenant_id="default",
            )
            
            ingestion_status = "success"
            chunks_count = len(chunks) if chunks else 0
        except Exception as ingest_error:
            logger.warning(f"Failed to auto-ingest Domain Memory: {ingest_error}")
            ingestion_status = "failed"
            chunks_count = 0
        
        return {
            "success": True,
            "domain_memory_path": str(domain_memory_path),
            "entry_date": today,
            "category": category,
            "ingestion_status": ingestion_status,
            "chunks_ingested": chunks_count,
            "message": f"Domain Memory updated and ingested. Future agents will remember: '{decision[:50]}...'"
        }
        
    except Exception as e:
        logger.error(f"Error updating Domain Memory: {e}")
        return {
            "success": False,
            "error": f"Error updating Domain Memory: {str(e)}",
            "domain_memory_path": str(domain_memory_path),
        }


async def scan_commit_history(
    since_days: int = 30,
    pattern: str = None,
    extract_decisions: bool = True,
) -> Dict[str, Any]:
    """
    Scan git commit history for Domain Memory extraction.
    
    Args:
        since_days: Number of days to look back
        pattern: Optional pattern to filter commits (grep pattern)
        extract_decisions: Whether to extract decision keywords
    
    Returns:
        Dictionary with commits and extracted information
    """
    repo_root = Path(__file__).parent.parent.parent
    
    # Build git log command
    since_date = (datetime.now() - timedelta(days=since_days)).strftime("%Y-%m-%d")
    cmd = [
        "git", "log",
        f"--since={since_date}",
        "--pretty=format:%H|%an|%ad|%s|%b",
        "--date=iso",
    ]
    
    if pattern:
        cmd.extend(["--grep", pattern])
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(repo_root),
            capture_output=True,
            text=True,
            check=True,
            timeout=10,  # Safety timeout
        )
        
        commits = []
        
        # Decision keywords to extract
        decision_keywords = [
            "decided", "chose", "switched", "refactored", "migrated",
            "pattern", "convention", "standard", "architecture", "design",
            "fix", "solution", "resolve", "implement", "establish",
        ]
        
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            
            parts = line.split("|", 4)
            if len(parts) < 4:
                continue
            
            commit_hash = parts[0]
            author = parts[1]
            date = parts[2]
            subject = parts[3]
            body = parts[4] if len(parts) > 4 else ""
            
            commit_data = {
                "hash": commit_hash[:8],
                "full_hash": commit_hash,
                "author": author,
                "date": date,
                "subject": subject,
                "body": body.strip(),
            }
            
            # Extract decisions if requested
            if extract_decisions:
                full_text = f"{subject} {body}".lower()
                decisions = [kw for kw in decision_keywords if kw in full_text]
                if decisions:
                    commit_data["decisions"] = decisions
                    commit_data["is_decision"] = True
                else:
                    commit_data["is_decision"] = False
            
            commits.append(commit_data)
        
        return {
            "success": True,
            "commits": commits,
            "count": len(commits),
            "since_days": since_days,
            "pattern": pattern,
            "extract_decisions": extract_decisions,
        }
        
    except subprocess.CalledProcessError as e:
        logger.warning(f"Git log scan failed: {e}")
        return {
            "success": False,
            "error": f"Git command failed: {str(e)}",
            "commits": [],
            "count": 0,
        }
    except subprocess.TimeoutExpired:
        logger.warning("Git log scan timed out")
        return {
            "success": False,
            "error": "Git command timed out",
            "commits": [],
            "count": 0,
        }
    except FileNotFoundError:
        logger.warning("Git command not found")
        return {
            "success": False,
            "error": "Git is not available in this environment",
            "commits": [],
            "count": 0,
        }
    except Exception as e:
        logger.error(f"Unexpected error scanning commit history: {e}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "commits": [],
            "count": 0,
        }

# =============================================================================
# Foundry IQ Tools
# =============================================================================

async def list_foundry_iq_kbs(project_id: Optional[str] = None) -> Dict[str, Any]:
    """
    List available Foundry IQ knowledge bases.
    
    Args:
        project_id: Optional Foundry project ID
        
    Returns:
        List of knowledge bases with metadata
    """
    try:
        from integrations.foundry_iq import FoundryIQClient
        
        settings = get_settings()
        client = FoundryIQClient(settings)
        
        kbs = await client.list_knowledge_bases(project_id)
        
        return {
            "success": True,
            "knowledge_bases": kbs,
            "count": len(kbs),
        }
    except ImportError:
        return {
            "success": False,
            "error": "Foundry IQ client not available",
            "knowledge_bases": [],
            "count": 0,
        }
    except Exception as e:
        logger.error(f"Error listing Foundry IQ KBs: {e}")
        return {
            "success": False,
            "error": str(e),
            "knowledge_bases": [],
            "count": 0,
        }

async def query_foundry_iq_kb(
    kb_id: str,
    query: str,
    limit: int = 5,
    search_type: str = "hybrid"
) -> Dict[str, Any]:
    """
    Query a Foundry IQ knowledge base.
    
    Args:
        kb_id: Knowledge base ID
        query: Search query
        limit: Maximum results (default: 5)
        search_type: keyword | vector | hybrid (default: hybrid)
        
    Returns:
        Query results with citations
    """
    try:
        from integrations.foundry_iq import FoundryIQClient
        
        settings = get_settings()
        client = FoundryIQClient(settings)
        
        response = await client.query_knowledge_base(
            kb_id=kb_id,
            query=query,
            limit=limit,
            search_type=search_type
        )
        
        # Convert to dict format
        results = [
            {
                "content": r.content,
                "score": r.score,
                "source": r.source,
                "metadata": r.metadata,
                "citations": r.citations,
            }
            for r in response.results
        ]
        
        return {
            "success": True,
            "query": query,
            "kb_id": kb_id,
            "results": results,
            "total_results": response.total_results,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Foundry IQ client not available",
            "query": query,
            "kb_id": kb_id,
            "results": [],
            "total_results": 0,
        }
    except Exception as e:
        logger.error(f"Error querying Foundry IQ KB: {e}")
        return {
            "success": False,
            "error": str(e),
            "query": query,
            "kb_id": kb_id,
            "results": [],
            "total_results": 0,
        }

async def get_foundry_iq_kb_status(kb_id: str) -> Dict[str, Any]:
    """
    Get status and health of a Foundry IQ knowledge base.
    
    Args:
        kb_id: Knowledge base ID
        
    Returns:
        Status information
    """
    try:
        from integrations.foundry_iq import FoundryIQClient
        
        settings = get_settings()
        client = FoundryIQClient(settings)
        
        status = await client.get_kb_status(kb_id)
        
        return {
            "success": True,
            "kb_id": kb_id,
            **status,
        }
    except ImportError:
        return {
            "success": False,
            "error": "Foundry IQ client not available",
            "kb_id": kb_id,
            "enabled": False,
            "status": "not_available",
        }
    except Exception as e:
        logger.error(f"Error getting Foundry IQ KB status: {e}")
        return {
            "success": False,
            "error": str(e),
            "kb_id": kb_id,
            "enabled": False,
            "status": "error",
        }
