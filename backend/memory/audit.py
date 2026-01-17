"""
Memory access audit logging for compliance.

Provides structured logging of all memory access operations
for security audit trails and compliance reporting.
"""

import logging
from datetime import datetime, timezone
from typing import Optional

# Dedicated audit logger - can be forwarded to SIEM/Azure Monitor
logger = logging.getLogger("ctxeco.memory.audit")


async def log_memory_access(
    action: str,  # "search", "read", "write", "delete", "list"
    user_id: str,
    tenant_id: str,
    session_id: Optional[str] = None,
    resource_type: str = "memory",
    success: bool = True,
    result_count: Optional[int] = None,
    metadata: Optional[dict] = None,
) -> None:
    """
    Log memory access for audit trail.
    
    Args:
        action: The operation performed (search, read, write, delete, list)
        user_id: ID of the user performing the action
        tenant_id: Tenant ID for multi-tenant isolation
        session_id: Optional session ID if action is session-scoped
        resource_type: Type of resource accessed (memory, episode, fact)
        success: Whether the operation succeeded
        result_count: Number of results returned (for search/list operations)
        metadata: Additional context about the operation
    """
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id": user_id,
        "tenant_id": tenant_id,
        "session_id": session_id,
        "resource_type": resource_type,
        "success": success,
        "result_count": result_count,
        "metadata": metadata or {},
    }
    
    # Log to structured logger (can be forwarded to SIEM/Azure Monitor)
    if success:
        logger.info(f"MEMORY_ACCESS: {log_entry}")
    else:
        logger.warning(f"MEMORY_ACCESS_DENIED: {log_entry}")


def log_memory_access_sync(
    action: str,
    user_id: str,
    tenant_id: str,
    session_id: Optional[str] = None,
    resource_type: str = "memory",
    success: bool = True,
    result_count: Optional[int] = None,
    metadata: Optional[dict] = None,
) -> None:
    """Synchronous version of log_memory_access for non-async contexts."""
    log_entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "user_id": user_id,
        "tenant_id": tenant_id,
        "session_id": session_id,
        "resource_type": resource_type,
        "success": success,
        "result_count": result_count,
        "metadata": metadata or {},
    }
    
    if success:
        logger.info(f"MEMORY_ACCESS: {log_entry}")
    else:
        logger.warning(f"MEMORY_ACCESS_DENIED: {log_entry}")
