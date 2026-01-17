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

# Singleton client instance (for compatibility with voice router)
memory_client = get_memory_client()


async def persist_conversation(context) -> None:
    """
    Persist conversation to memory.
    
    Convenience function that calls ZepMemoryClient.persist_conversation().
    """
    client = get_memory_client()
    await client.persist_conversation(context)


__all__ = [
    "ZepMemoryClient",
    "get_memory_client",
    "memory_client",
    "persist_conversation",
]
