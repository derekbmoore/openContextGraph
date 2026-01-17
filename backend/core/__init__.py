"""
OpenContextGraph - Core Package

Exports the 4-layer context schema and core utilities.
"""

from .context import (
    Role,
    SecurityContext,
    Message,
    MessageRole,
    Turn,
    EpisodicContext,
    Fact,
    Entity,
    GraphNode,
    SemanticContext,
    ToolCall,
    OperationalContext,
    EnterpriseContext,
)
from .config import Settings, get_settings

__all__ = [
    # Config
    "Settings",
    "get_settings",
    # Context
    "Role",
    "SecurityContext",
    "Message",
    "MessageRole",
    "Turn",
    "EpisodicContext",
    "Fact",
    "Entity",
    "GraphNode",
    "SemanticContext",
    "ToolCall",
    "OperationalContext",
    "EnterpriseContext",
]
