"""
MCP Handler implementations for OpenContextGraph tools.
Includes:
- Database Access (PostgreSQL)
- Codebase Search (Stub/Future)
- Project Management (Stub/Future)
"""
import logging
import asyncio
import os
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
