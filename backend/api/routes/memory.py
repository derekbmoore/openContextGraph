"""
Memory API Routes - Tri-Search™

Provides endpoints for:
- Hybrid memory search (keyword + vector + graph)
- Fact retrieval from knowledge graph
- Session listing
- Episode listing and transcripts

OpenContextGraph - API Layer
NIST AI RMF: MANAGE 2.3 (Data Governance), MAP 1.1 (Context)
"""

import logging
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional

from api.middleware.auth import get_current_user
from core import SecurityContext, get_settings
from core.context import Fact
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


# =============================================================================
# Episodes Routes
# =============================================================================


class Episode(BaseModel):
    id: str
    summary: str
    turn_count: int
    agent_id: str
    started_at: datetime
    ended_at: Optional[datetime]
    topics: list[str] = []


class EpisodeListResponse(BaseModel):
    episodes: list[Episode]
    total_count: int


@router.get("/episodes", response_model=EpisodeListResponse)
async def list_episodes(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    user: SecurityContext = Depends(get_current_user),
):
    """
    List conversation episodes from memory.

    Episodes are discrete conversation sessions that have been
    processed and stored in the knowledge graph.
    """
    try:
        memory_client = get_memory_client()
        
        # Use list_sessions to get episodes
        # Episodes are sessions with metadata indicating they're episodes
        sessions = await memory_client.list_sessions(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            limit=limit,
            offset=offset,
        )

        episodes = []
        for s in sessions:
            metadata = s.get("metadata", {})
            # Filter for episodes (exclude stories)
            if metadata.get("type") != "story":
                episodes.append(
                    Episode(
                        id=s["session_id"],
                        summary=metadata.get("summary", "No summary available"),
                        turn_count=metadata.get("turn_count", 0),
                        agent_id=metadata.get("agent_id", "unknown"),
                        started_at=(
                            datetime.fromisoformat(s["created_at"]) if isinstance(s["created_at"], str) else s["created_at"]
                        ),
                        ended_at=(
                            datetime.fromisoformat(s["updated_at"]) if isinstance(s["updated_at"], str) else s["updated_at"]
                        ) if s.get("updated_at") else None,
                        topics=metadata.get("topics", []),
                    )
                )

        return EpisodeListResponse(
            episodes=episodes,
            total_count=len(episodes),
        )
    except Exception as e:
        logger.error(f"Failed to list episodes: {e}")
        # In test, raise to avoid masking issues
        settings = get_settings()
        if settings.environment == "test":
            raise
        # Fallback return empty
        return EpisodeListResponse(episodes=[], total_count=0)


class EpisodeTranscriptResponse(BaseModel):
    id: str
    transcript: list[dict]


@router.get("/episodes/{session_id}", response_model=EpisodeTranscriptResponse)
async def get_episode_transcript(session_id: str, user: SecurityContext = Depends(get_current_user)):
    """
    Get the detailed transcript for a specific episode.
    """
    try:
        memory_client = get_memory_client()
        
        # Get session messages as transcript
        messages = await memory_client.get_session_messages(session_id, limit=1000)
        
        transcript = [
            {
                "role": msg.get("role", "user"),
                "content": msg.get("content", ""),
                "metadata": msg.get("metadata", {}),
            }
            for msg in messages
        ]

        return EpisodeTranscriptResponse(id=session_id, transcript=transcript)
    except Exception as e:
        logger.error(f"Failed to get episode transcript: {e}")
        # Fallback
        return EpisodeTranscriptResponse(id=session_id, transcript=[])


# =============================================================================
# Memory Enrichment (VoiceLive / Automation Context)
# =============================================================================

class EnrichRequest(BaseModel):
    """Request body for voice transcript enrichment"""
    text: str
    session_id: Optional[str] = None
    speaker: str = "user"  # 'user' or 'assistant'
    agent_id: Optional[str] = None
    channel: str = "voice"
    title: Optional[str] = None
    summary: Optional[str] = None
    metadata: dict = {}


class EnrichResponse(BaseModel):
    """Response for enrichment request"""
    success: bool
    session_id: str
    message: str


@router.post("/enrich", response_model=EnrichResponse)
async def enrich_memory(request: EnrichRequest, user: SecurityContext = Depends(get_current_user)):
    """
    Enrich memory with voice transcripts or automation context.
    
    This endpoint is called by the browser after receiving transcription
    from the Azure Realtime API, or by automation tools to store context.
    It's fire-and-forget — the experience continues regardless of 
    whether memory persistence succeeds.
    """
    import uuid
    from datetime import datetime, timezone
    
    try:
        memory_client = get_memory_client()
        
        # Generate session ID if not provided
        session_id = request.session_id or f"voice-{uuid.uuid4()}"
        
        # Create/update session with metadata including summary/title
        summary = request.summary or (request.text[:200] + ("..." if len(request.text) > 200 else ""))
        title = request.title
        
        # Merge request metadata with session metadata
        session_metadata = {
            "tenant_id": user.tenant_id,
            "channel": request.channel,
            "agent_id": request.agent_id or "unknown",
            "summary": summary,
            "title": title,
            "turn_count": 1,
            **request.metadata  # Include extra context in session metadata too
        }

        await memory_client.get_or_create_session(
            session_id=session_id,
            user_id=user.user_id,
            metadata=session_metadata,
        )
        
        # Directly add the message to memory
        role = "user" if request.speaker == "user" else "assistant"
        
        # Merge message metadata
        message_metadata = {
            "agent_id": request.agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "channel": request.channel,
            **request.metadata
        }

        await memory_client.add_memory(
            session_id=session_id,
            messages=[{
                "role": role,
                "content": request.text,
                "metadata": message_metadata,
            }],
        )
        
        logger.info(f"Memory enriched: session={session_id}, speaker={request.speaker}, len={len(request.text)}")
        
        return EnrichResponse(
            success=True,
            session_id=session_id,
            message="Transcript enriched successfully",
        )
        
    except Exception as e:
        logger.warning(f"Memory enrichment failed (non-blocking): {e}")
        return EnrichResponse(
            success=False,
            session_id=request.session_id or "",
            message=f"Enrichment failed: {str(e)}",
        )

