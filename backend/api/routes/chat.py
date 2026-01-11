"""
Chat API Routes - Agent Integration

Provides endpoints for:
- Multi-agent chat (Elena, Marcus, Sage)
- Session management
- Context-aware responses

OpenContextGraph - API Layer
NIST AI RMF: GOVERN 1.2 (Attribution), MAP 1.1 (Context)
"""

import logging
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any

from api.middleware.auth import get_current_user
from core.context import (
    SecurityContext,
    EnterpriseContext,
    EpisodicContext,
    SemanticContext,
    OperationalContext,
)
from agents import get_agent_router
from memory import get_memory_client

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatRequest(BaseModel):
    """Request to send a message to an agent."""
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Existing session ID")
    agent: str = Field("elena", description="Target agent (elena, marcus, sage)")


class ChatResponse(BaseModel):
    """Response from an agent."""
    response: str
    session_id: str
    agent: str
    sources: list[str] = []
    tool_calls: list[dict] = []


class SessionInfo(BaseModel):
    """Session metadata."""
    session_id: str
    created_at: Optional[str] = None
    agent: Optional[str] = None
    message_count: int = 0


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Send a message to an AI agent.
    
    NIST AI RMF Controls:
    - GOVERN 1.2: Request attributed to authenticated user
    - MAP 1.1: Full enterprise context provided to agent
    - MANAGE 4.3: Conversation persisted to memory
    
    Args:
        request: Chat request with message and session info
        user: Authenticated user from token
    
    Returns:
        Agent response with sources and attribution
    """
    # Generate session ID if not provided
    session_id = request.session_id or f"sess-{uuid.uuid4().hex[:12]}"
    
    # Build 4-layer enterprise context
    context = EnterpriseContext(
        security=user,
        episodic=EpisodicContext(
            conversation_id=session_id,
            recent_messages=[],
            metadata={"agent_id": request.agent}
        ),
        semantic=SemanticContext(),
        operational=OperationalContext(
            current_agent=request.agent,
        ),
    )
    
    # Enrich context with memory
    memory_client = get_memory_client()
    try:
        context = await memory_client.enrich_context(context, request.message)
    except Exception as e:
        logger.warning(f"Memory enrichment failed: {e}")
    
    # Route to agent
    agent_router = get_agent_router()
    result = await agent_router.route(request.agent, request.message, context)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Persist conversation to memory
    try:
        await memory_client.add_memory(
            session_id=session_id,
            messages=[
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": result["response"]},
            ],
            metadata={"agent_id": request.agent}
        )
    except Exception as e:
        logger.warning(f"Memory persistence failed: {e}")
    
    return ChatResponse(
        response=result["response"],
        session_id=session_id,
        agent=result["agent_id"],
        sources=result.get("sources", []),
        tool_calls=result.get("tool_calls", []),
    )


@router.get("/sessions", response_model=list[SessionInfo])
async def list_sessions(
    limit: int = 20,
    offset: int = 0,
    user: SecurityContext = Depends(get_current_user),
):
    """
    List user's chat sessions.
    
    NIST AI RMF: MANAGE 2.3 - Results scoped to authenticated user
    """
    memory_client = get_memory_client()
    
    try:
        sessions = await memory_client.list_sessions(
            user_id=user.user_id,
            limit=limit,
            offset=offset,
        )
        
        return [
            SessionInfo(
                session_id=s.get("session_id", ""),
                created_at=s.get("created_at"),
                agent=s.get("metadata", {}).get("agent_id"),
                message_count=0,  # TODO: Get from session
            )
            for s in sessions
        ]
        
    except Exception as e:
        logger.error(f"Failed to list sessions: {e}")
        return []


@router.get("/agents")
async def list_agents():
    """List available agents and their capabilities."""
    agent_router = get_agent_router()
    
    agents = []
    for name in agent_router.list_agents():
        agent = agent_router.get_agent(name)
        if agent:
            agents.append({
                "id": agent.agent_id,
                "name": agent.display_name,
                "tools": [t.get("name") for t in agent.get_tools()],
            })
    
    return {"agents": agents}
