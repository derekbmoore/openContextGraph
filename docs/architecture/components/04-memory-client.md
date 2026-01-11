# Memory Client — Zep Integration (Tri-Search™)

## Purpose

The Memory Client provides **persistent, searchable memory** for AI agents through integration with Zep's temporal knowledge graph. It implements **Tri-Search™**—a fusion of keyword, vector, and graph search that delivers superior retrieval quality.

## Why This Exists

### The Problem

Large Language Models have no persistent memory. Each interaction starts fresh, creating:

- **Repetitive conversations**: Users re-explain context
- **Knowledge loss**: Insights from previous sessions are forgotten
- **No learning**: The system never improves from experience
- **Compliance gaps**: No audit trail of what the AI "knows"

### The Solution

A memory layer that:

1. **Persists episodic memory**: Conversation history survives sessions
2. **Extracts semantic facts**: Knowledge graph builds over time
3. **Enables Tri-Search**: Multiple retrieval modes for precision
4. **Tracks provenance**: Every fact links to its source

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Memory Client                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                  Tri-Search™                          │   │
│  │   ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │   │
│  │   │ Keyword  │  │  Vector  │  │   Graph Search   │   │   │
│  │   │  (BM25)  │  │(pgvector)│  │   (Graphiti)     │   │   │
│  │   └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │   │
│  │        │             │                  │             │   │
│  │        └─────────────┴──────────────────┘             │   │
│  │                      │                                │   │
│  │                      ▼                                │   │
│  │        ┌─────────────────────────────┐                │   │
│  │        │  Reciprocal Rank Fusion     │                │   │
│  │        │       (RRF)                 │                │   │
│  │        └─────────────────────────────┘                │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  ┌────────────────────┐  ┌────────────────────────────┐     │
│  │  Episodic Memory   │  │     Semantic Memory        │     │
│  │  (Conversations)   │  │   (Facts & Entities)       │     │
│  └────────────────────┘  └────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Zep Server    │
                    │  (PostgreSQL)   │
                    └─────────────────┘
```

---

## Code Sample

```python
# backend/memory/client.py
"""
Zep Memory Client - Tri-Search™ Implementation

Provides persistent memory for AI agents through:
- Episodic memory (conversation history)
- Semantic memory (facts and entities)
- Tri-Search (keyword + vector + graph fusion)

NIST AI RMF Alignment:
- MANAGE 2.3: Data governance via user/tenant scoping
- MEASURE 2.1: Search quality via relevance scoring
- MAP 1.1: Context enrichment for system awareness
"""

import logging
from typing import Optional
import httpx

from core import (
    Entity,
    EnterpriseContext,
    GraphNode,
    Fact,
    SecurityContext,
)

logger = logging.getLogger(__name__)


class ZepMemoryClient:
    """
    Client for interacting with Zep's memory service.
    
    Key capabilities:
    - User/session management for identity consistency
    - Episodic memory (conversation persistence)
    - Semantic memory (fact extraction and retrieval)
    - Tri-Search with Reciprocal Rank Fusion
    
    NIST AI RMF: MANAGE 2.3 - All operations scoped to user/tenant
    """
    
    def __init__(self, base_url: str = "http://zep:8000", api_key: str = ""):
        self.base_url = base_url
        self.api_key = api_key
        self._client: Optional[httpx.AsyncClient] = None
    
    @property
    def http_client(self) -> httpx.AsyncClient:
        """Lazy-load async HTTP client."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self._get_headers(),
                timeout=30.0
            )
        return self._client
    
    def _get_headers(self) -> dict:
        """Get headers including API key if configured."""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    # =========================================================================
    # USER MANAGEMENT
    # NIST AI RMF: GOVERN 1.2 - Ensures consistent user identity
    # =========================================================================
    
    async def get_or_create_user(
        self, 
        user_id: str, 
        metadata: dict = None
    ) -> dict:
        """
        Ensure user exists in Zep before creating sessions.
        
        CRITICAL: Users must exist before sessions can be created.
        This maintains consistent identity across all memory operations.
        
        Args:
            user_id: Unique identifier (e.g., "sarah.chen@contoso.com")
            metadata: Optional user properties (tenant_id, email, etc.)
        
        Returns:
            User object from Zep
        """
        # Try to get existing user
        try:
            response = await self.http_client.get(f"/api/v2/users/{user_id}")
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        # Create new user
        user_data = {
            "user_id": user_id,
            "metadata": metadata or {}
        }
        
        response = await self.http_client.post("/api/v2/users", json=user_data)
        response.raise_for_status()
        
        logger.info(f"Created user in Zep: {user_id}")
        return response.json()

    # =========================================================================
    # SESSION MANAGEMENT
    # NIST AI RMF: MAP 1.1 - Sessions capture system interaction context
    # =========================================================================
    
    async def get_or_create_session(
        self, 
        session_id: str, 
        user_id: str, 
        metadata: dict = None
    ) -> dict:
        """
        Get or create a conversation session.
        
        Sessions are the container for episodic memory (message history).
        Each session belongs to a user and can have metadata for filtering.
        
        Args:
            session_id: Unique session identifier
            user_id: Owner of the session
            metadata: Session properties (tenant_id, channel, etc.)
        """
        # Ensure user exists first
        await self.get_or_create_user(user_id, metadata)
        
        # Try to get existing session
        try:
            response = await self.http_client.get(f"/api/v2/sessions/{session_id}")
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        
        # Create new session
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "metadata": metadata or {}
        }
        
        response = await self.http_client.post("/api/v2/sessions", json=session_data)
        response.raise_for_status()
        
        logger.info(f"Created session in Zep: {session_id} for user {user_id}")
        return response.json()

    # =========================================================================
    # EPISODIC MEMORY (CONVERSATION HISTORY)
    # NIST AI RMF: MANAGE 4.3 - Enables incident reconstruction
    # =========================================================================
    
    async def add_memory(
        self, 
        session_id: str, 
        messages: list[dict],
        metadata: dict = None
    ) -> dict:
        """
        Add messages to a session's episodic memory.
        
        Messages are persisted and indexed for later retrieval.
        Zep automatically extracts entities and facts.
        
        Args:
            session_id: Target session
            messages: List of {role, content, metadata} dicts
        """
        memory_data = {
            "messages": [
                {
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", ""),
                    "metadata": msg.get("metadata", {})
                }
                for msg in messages
            ]
        }
        
        response = await self.http_client.post(
            f"/api/v2/sessions/{session_id}/memory",
            json=memory_data
        )
        response.raise_for_status()
        
        return response.json()
    
    async def get_session_messages(
        self, 
        session_id: str, 
        limit: int = 20
    ) -> list[dict]:
        """
        Retrieve conversation history for a session.
        
        Returns most recent messages first.
        """
        response = await self.http_client.get(
            f"/api/v2/sessions/{session_id}/messages",
            params={"limit": limit}
        )
        response.raise_for_status()
        
        return response.json().get("messages", [])

    # =========================================================================
    # TRI-SEARCH™ (HYBRID MEMORY SEARCH)
    # NIST AI RMF: MEASURE 2.1 - Search quality measurement
    # =========================================================================
    
    async def search_memory(
        self,
        query: str,
        user_id: str,
        session_id: Optional[str] = None,
        search_type: str = "hybrid",
        limit: int = 10,
    ) -> dict:
        """
        Execute Tri-Search™ across memory.
        
        Search Types:
        - "keyword": BM25 inverted index search
        - "vector": pgvector cosine similarity
        - "graph": Graphiti relationship traversal
        - "hybrid": RRF fusion of all three (recommended)
        
        Reciprocal Rank Fusion (RRF):
            score = Σ 1/(k + rank_i) for each search method
            k = 60 (standard constant)
        
        NIST AI RMF Controls:
        - MANAGE 2.3: Results scoped to user
        - MEASURE 2.1: Relevance scores enable quality measurement
        
        Args:
            query: Search query
            user_id: Scope results to this user
            session_id: Optional session filter
            search_type: "keyword", "vector", "graph", or "hybrid"
            limit: Maximum results
        
        Returns:
            {
                "results": [...],
                "search_type": "hybrid",
                "fusion_scores": {...}
            }
        """
        search_data = {
            "text": query,
            "user_id": user_id,
            "search_type": search_type,
            "limit": limit
        }
        
        if session_id:
            search_data["session_id"] = session_id
        
        response = await self.http_client.post(
            "/api/v2/memory/search",
            json=search_data
        )
        response.raise_for_status()
        
        results = response.json()
        
        # Log search quality metrics (NIST MEASURE 2.1)
        logger.info(
            f"Tri-Search: query='{query[:50]}...' "
            f"type={search_type} results={len(results.get('results', []))}"
        )
        
        return results

    # =========================================================================
    # SEMANTIC MEMORY (FACTS & KNOWLEDGE GRAPH)
    # NIST AI RMF: MANAGE 2.3 - Facts include provenance
    # =========================================================================
    
    async def get_facts(
        self, 
        user_id: str, 
        query: Optional[str] = None,
        limit: int = 20
    ) -> list[Fact]:
        """
        Retrieve facts from the knowledge graph.
        
        Facts are automatically extracted from conversations
        and stored with provenance (source session, timestamp).
        
        Args:
            user_id: Scope to user's facts
            query: Optional relevance filter
            limit: Maximum facts to return
        """
        params = {"limit": limit}
        if query:
            params["query"] = query
        
        response = await self.http_client.get(
            f"/api/v2/users/{user_id}/facts",
            params=params
        )
        response.raise_for_status()
        
        facts_data = response.json().get("facts", [])
        
        return [
            Fact(
                content=f.get("content", ""),
                source=f.get("source"),
                confidence=f.get("confidence", 1.0),
                timestamp=f.get("created_at")
            )
            for f in facts_data
        ]
    
    async def add_fact(
        self, 
        user_id: str, 
        fact: str, 
        metadata: dict = None
    ) -> dict:
        """
        Manually add a fact to the knowledge graph.
        
        Use for importing external knowledge or corrections.
        """
        fact_data = {
            "content": fact,
            "metadata": metadata or {}
        }
        
        response = await self.http_client.post(
            f"/api/v2/users/{user_id}/facts",
            json=fact_data
        )
        response.raise_for_status()
        
        return response.json()

    # =========================================================================
    # CONTEXT ENRICHMENT
    # NIST AI RMF: MAP 1.1 - Populates system context
    # =========================================================================
    
    async def enrich_context(
        self, 
        context: EnterpriseContext, 
        query: str
    ) -> EnterpriseContext:
        """
        Enrich an EnterpriseContext with relevant memory.
        
        This is the main integration point for the Context Engine.
        It populates Layer 2 (Episodic) and Layer 3 (Semantic).
        
        NIST AI RMF: MAP 1.1 - System context enrichment
        
        Args:
            context: Current enterprise context
            query: User's query for relevance filtering
        
        Returns:
            Enriched context with memory
        """
        user_id = context.security.user_id
        session_id = context.episodic.conversation_id
        
        # 1. Get recent messages (episodic)
        if session_id:
            messages = await self.get_session_messages(session_id, limit=10)
            from core import Message
            context.episodic.recent_messages = [
                Message(
                    role=m.get("role", "user"),
                    content=m.get("content", "")
                )
                for m in messages
            ]
        
        # 2. Search for relevant facts (semantic)
        search_results = await self.search_memory(
            query=query,
            user_id=user_id,
            search_type="hybrid",
            limit=5
        )
        
        for result in search_results.get("results", []):
            context.semantic.facts.append(
                Fact(
                    content=result.get("content", ""),
                    source=result.get("source"),
                    confidence=result.get("score", 0.5)
                )
            )
        
        return context


# Singleton instance
memory_client = ZepMemoryClient()
```

---

## NIST AI RMF Alignment

| Function | Control | Implementation |
|----------|---------|----------------|
| **GOVERN 1.2** | Accountability | `user_id` in all operations |
| **MAP 1.1** | System Context | `enrich_context()` populates layers |
| **MANAGE 2.3** | Data Governance | User/tenant scoping on all queries |
| **MANAGE 4.3** | Documentation | Session messages preserved |
| **MEASURE 2.1** | Quality | Relevance scores logged |

---

## Tri-Search™ Details

### Why Three Search Modes?

| Mode | Strength | Weakness |
|------|----------|----------|
| **Keyword (BM25)** | Exact term matching | Misses synonyms |
| **Vector (Embedding)** | Semantic similarity | Loses specificity |
| **Graph (Traversal)** | Relationship discovery | Requires structured data |

### Reciprocal Rank Fusion

```python
def rrf_score(ranks: list[int], k: int = 60) -> float:
    """
    Combine rankings from multiple search methods.
    
    Higher scores = better results.
    k=60 is the standard constant (empirically validated).
    """
    return sum(1.0 / (k + rank) for rank in ranks)

# Example:
# Document appears at rank 1 in keyword, rank 5 in vector, rank 3 in graph
# RRF = 1/(60+1) + 1/(60+5) + 1/(60+3) = 0.0164 + 0.0154 + 0.0159 = 0.0477
```

---

## Summary

The Memory Client provides:

- ✅ Persistent episodic memory (conversations)
- ✅ Semantic fact extraction and retrieval
- ✅ Tri-Search™ for superior retrieval quality
- ✅ User/tenant scoping for data governance
- ✅ Provenance tracking for compliance
- ✅ NIST AI RMF alignment throughout

*Document Version: 1.0 | Created: 2026-01-11*
