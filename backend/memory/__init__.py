"""
Memory Package - openContextGraph

Provides memory services for the AI platform:
- ZepMemoryClient: Zep integration for episodic/semantic memory
- Tri-Search™: Hybrid search (keyword + vector + graph)
"""

from memory.client import (
    ZepMemoryClient,
    get_memory_client,
)

__all__ = [
    "ZepMemoryClient",
    "get_memory_client",
]
