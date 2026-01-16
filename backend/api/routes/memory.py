"""
Memory API Routes - Tri-Search™

Provides endpoints for:
- Hybrid memory search (keyword + vector + graph)
- Fact retrieval from knowledge graph
- Session listing

OpenContextGraph - API Layer
NIST AI RMF: MANAGE 2.3 (Data Governance), MAP 1.1 (Context)
"""

import logging
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional

from api.middleware.auth import get_current_user
from core.context import SecurityContext, Fact
from memory import get_memory_client

logger = logging.getLogger(__name__)

router = APIRouter()


class SearchRequest(BaseModel):
    """Memory search request."""
    query: str = Field(..., description="Search query")
    user_id: Optional[str] = Field(None, description="Override user (admin only)")
    search_type: str = Field("hybrid", description="keyword | similarity | hybrid")
    limit: int = Field(10, ge=1, le=100)


class SearchResult(BaseModel):
    """Single search result."""
    content: str
    score: float
    source: Optional[str] = None
    metadata: dict = {}


class SearchResponse(BaseModel):
    """Memory search response."""
    results: list[SearchResult]
    search_type: str
    query: str


class FactResponse(BaseModel):
    """Fact from knowledge graph."""
    content: str
    source: Optional[str] = None
    confidence: float = 1.0


class SessionResponse(BaseModel):
    """Session metadata."""
    session_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: dict = {}


@router.post("/search", response_model=SearchResponse)
async def search_memory(
    request: SearchRequest,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Execute Tri-Search™ across memory.
    
    Search Types:
    - "keyword": BM25 inverted index search
    - "similarity": Vector cosine similarity  
    - "hybrid": RRF fusion of all sources (recommended)
    
    NIST AI RMF Controls:
    - MANAGE 2.3: Results scoped to authenticated user
    - MEASURE 2.1: Relevance scores enable quality measurement
    
    Args:
        request: Search parameters
        user: Authenticated user from token
    
    Returns:
        Ranked search results with scores
    """
    memory_client = get_memory_client()
    
    # Use authenticated user unless admin override
    search_user_id = user.user_id
    if request.user_id and user.has_role("admin"):
        search_user_id = request.user_id
    
    try:
        result = await memory_client.search_memory(
            query=request.query,
            user_id=search_user_id,
            tenant_id=user.tenant_id,  # SECURITY: Enforce tenant isolation
            search_type=request.search_type,
            limit=request.limit,
        )
        
        return SearchResponse(
            results=[
                SearchResult(
                    content=r.get("content", ""),
                    score=r.get("score", 0.0),
                    source=r.get("session_id"),
                    metadata=r.get("metadata", {}),
                )
                for r in result.get("results", [])
            ],
            search_type=result.get("search_type", request.search_type),
            query=request.query,
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return SearchResponse(
            results=[],
            search_type=request.search_type,
            query=request.query,
        )


@router.get("/facts/{user_id}", response_model=list[FactResponse])
async def get_facts(
    user_id: str,
    query: Optional[str] = None,
    limit: int = 20,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Get facts from the knowledge graph.
    
    Facts are automatically extracted from conversations
    and stored with provenance tracking.
    
    NIST AI RMF: MANAGE 2.3 - User isolation enforced
    
    Args:
        user_id: Target user (must match auth or be admin)
        query: Optional relevance filter
        limit: Maximum facts to return
    
    Returns:
        List of facts with confidence scores
    """
    # Enforce user isolation (unless admin)
    if user_id != user.user_id and not user.has_role("admin"):
        return []
    
    memory_client = get_memory_client()
    
    try:
        facts = await memory_client.get_facts(
            user_id=user_id,
            query=query,
            limit=limit,
        )
        
        return [
            FactResponse(
                content=f.content,
                source=f.source,
                confidence=f.confidence,
            )
            for f in facts
        ]
        
    except Exception as e:
        logger.error(f"Failed to get facts: {e}")
        return []


@router.get("/sessions", response_model=list[SessionResponse])
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    user: SecurityContext = Depends(get_current_user),
):
    """
    List conversation sessions for the authenticated user.
    
    NIST AI RMF: MANAGE 2.3 - Scoped to authenticated user
    """
    memory_client = get_memory_client()
    
    try:
        sessions = await memory_client.list_sessions(
            user_id=user.user_id,
            tenant_id=user.tenant_id,  # SECURITY: Enforce tenant isolation
            limit=limit,
            offset=offset,
        )
        
        return [
            SessionResponse(
                session_id=s.get("session_id", ""),
                created_at=s.get("created_at"),
                updated_at=s.get("updated_at"),
                metadata=s.get("metadata", {}),
            )
            for s in sessions
        ]
        
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        return []
