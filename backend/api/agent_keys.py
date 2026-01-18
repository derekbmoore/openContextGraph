"""
Shared agent API key handling for MCP and tool endpoints.
"""

from typing import Optional
import logging
import os

from fastapi import HTTPException

logger = logging.getLogger(__name__)

# Agent API Keys (from environment or hardcoded for dev)
# In production, these should be in Azure Key Vault
MCP_AGENT_KEYS = {
    # Format: "key" -> {"agent_id": "...", "agent_name": "..."}
    os.getenv("MCP_KEY_MARCUS", "mcp_marcus_Xwo6uNm3k0FU42et9SPjTZ0u5xeO5kOZmZ5Z8db7tNI"): {
        "agent_id": "marcus",
        "agent_name": "Marcus Chen",
        "tenant_id": "zimax",
    },
    os.getenv("MCP_KEY_SAGE", "mcp_sage_oE5J2v28ZXTz_xyfkMQ5r-L8e-UaVgmuv9brQR1z_sI"): {
        "agent_id": "sage",
        "agent_name": "Sage",
        "tenant_id": "zimax",
    },
    os.getenv("MCP_KEY_ELENA", "mcp_elena_iRsyOL6J6PfeY_vH6n3LG7XEYi70DrLxG_rcjoCwI-k"): {
        "agent_id": "elena",
        "agent_name": "Dr. Elena Vasquez",
        "tenant_id": "zimax",
    },
}


def validate_api_key(api_key: Optional[str]) -> Optional[dict]:
    """
    Validate x-api-key header and return agent info if valid.
    Returns None if no key provided.
    Raises HTTPException if key is invalid.
    """
    if not api_key:
        return None

    agent_info = MCP_AGENT_KEYS.get(api_key)
    if not agent_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    logger.info("Tool Auth: Agent %s authenticated", agent_info.get("agent_name"))
    return agent_info
