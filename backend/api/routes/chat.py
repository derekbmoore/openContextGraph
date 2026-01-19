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
    
    # Check for Foundry Agent configuration
    from core.config import get_settings
    settings = get_settings()
    foundry_agent_id = None
    if request.agent == "elena":
        foundry_agent_id = settings.elena_foundry_agent_id
    elif request.agent == "marcus":
        foundry_agent_id = settings.marcus_foundry_agent_id
    elif request.agent == "sage":
        foundry_agent_id = settings.sage_foundry_agent_id
    
    def build_memory_context(ctx: EnterpriseContext) -> str:
        if not ctx.semantic.facts:
            return ""
        lines = ["Relevant memory context (facts + episodes):"]
        for fact in ctx.semantic.facts[:12]:
            if fact.content:
                lines.append(f"- {fact.content}")
        return "\n".join(lines)

    memory_context = build_memory_context(context)

    # Try Foundry First
    result = None
    if foundry_agent_id and settings.azure_foundry_agent_endpoint and settings.azure_foundry_agent_key:
        try:
            logger.info(f"Routing chat to Foundry Agent: {request.agent} ({foundry_agent_id})")
            
            # Initialize Foundry Client
            from backend.integrations.foundry import FoundryClient
            foundry_client = FoundryClient(settings)
            
            # Send message
            foundry_response = await foundry_client.chat(
                agent_id=foundry_agent_id,
                message=request.message,
                thread_id=None, # TODO: We need to store thread_id in Session metadata to resume conversations
                memory_context=memory_context,
            )
            
            if foundry_response.status == "completed":
                result = {
                    "response": foundry_response.response, # No stripped quotes here
                    "agent_id": request.agent,
                    "sources": ["Azure AI Foundry"],
                    "tool_calls": foundry_response.tool_calls
                }
            else:
                logger.error(f"Foundry failed: {foundry_response.error}")
                # Fallback to local
                
        except Exception as e:
            logger.error(f"Foundry chat failed: {e}", exc_info=True)
            # Fallback to local

    # Fallback to local if Foundry didn't produce a result
    if result is None:
        logger.info(f"Falling back to local agent for {request.agent}")
        from agents import get_agent_router
        agent_router = get_agent_router()
        
        agent = agent_router.get_agent(request.agent)
        if agent:
            try:
                agent_response = await agent.run(request.message, context)
                result = {
                    "response": agent_response.content if hasattr(agent_response, 'content') else str(agent_response),
                    "agent_id": request.agent,
                    "sources": [],
                    "tool_calls": []
                }
            except Exception as e:
                logger.error(f"Local agent failed: {e}", exc_info=True)
                result = {
                    "response": f"I encountered an issue processing your request. Please try again.",
                    "agent_id": request.agent,
                    "sources": [],
                    "tool_calls": []
                }
        else:
            result = {
                "response": f"Agent '{request.agent}' is not available.",
                "agent_id": request.agent,
                "sources": [],
                "tool_calls": []
            }
    
    # Always return a valid ChatResponse
    return ChatResponse(
        response=result["response"],
        session_id=session_id,
        agent=result.get("agent_id", request.agent),
        sources=result.get("sources", []),
        tool_calls=result.get("tool_calls", [])
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
    # Mix local capabilities + Foundry status
    from core.config import get_settings
    settings = get_settings()
    
    for name in agent_router.list_agents():
        agent = agent_router.get_agent(name)
        if agent:
            # Check if this agent is Foundry-backed
            is_foundry = False
            if name == "elena" and settings.elena_foundry_agent_id: is_foundry = True
            if name == "marcus" and settings.marcus_foundry_agent_id: is_foundry = True
            if name == "sage" and settings.sage_foundry_agent_id: is_foundry = True
            
            agents.append({
                "id": agent.agent_id,
                "name": agent.display_name,
                "tools": [t.get("name") for t in agent.get_tools()],
                "foundry_backed": is_foundry
            })
    
    return {"agents": agents}

