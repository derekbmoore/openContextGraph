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
    
    # Try Foundry First
    result = None
    if foundry_agent_id and settings.azure_foundry_agent_endpoint and settings.azure_foundry_agent_key:
        try:
            logger.info(f"Routing chat to Foundry Agent: {request.agent} ({foundry_agent_id})")
            response_text = await chat_via_foundry(
                agent_id=foundry_agent_id,
                message=request.message,
                settings=settings
            )
            result = {
                "response": response_text,
                "agent_id": request.agent,
                "sources": ["Azure AI Foundry"],
                "tool_calls": [] 
            }
        except Exception as e:
            logger.error(f"Foundry chat failed: {e}")
            # Fallback to local will happen below if result is None
    
    # Fallback to local routing
    if not result:
        agent_router = get_agent_router()
        result = await agent_router.route(request.agent, request.message, context)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    # Persist conversation to memory
    try:
        # Ensure session exists with security context metadata
        await memory_client.get_or_create_session(
            session_id=session_id,
            user_id=user.user_id,
            metadata={
                "tenant_id": user.tenant_id,
                "project_id": user.project_id or "",
                "groups": user.groups,
                "agent_id": request.agent,
                "created_at": str(uuid.uuid1())
            }
        )
        
        await memory_client.add_memory(
            session_id=session_id,
            messages=[
                {"role": "user", "content": request.message},
                {"role": "assistant", "content": result["response"]},
            ],
            metadata={
                "agent_id": request.agent,
                "project_id": user.project_id
            }
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


async def chat_via_foundry(agent_id: str, message: str, settings: Any) -> str:
    """
    Route chat to Azure AI Foundry Assistants API.
    
    Agents are configured with Action Groups (MCP) to access tools.
    The run execution handles tool calls server-side.
    """
    from openai import AzureOpenAI
    import asyncio
    
    client = AzureOpenAI(
        azure_endpoint=settings.azure_foundry_agent_endpoint,
        api_key=settings.azure_foundry_agent_key,
        api_version=settings.azure_foundry_agent_api_version,
    )
    
    # Create Thread
    thread = client.beta.threads.create()
    
    # Add Message
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=message
    )
    
    # Run Agent
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=agent_id
    )
    
    # Poll for completion
    # Timeout after 60 seconds
    for _ in range(120):
        await asyncio.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        
        if run.status == "completed":
            break
        elif run.status == "failed":
            raise Exception(f"Foundry Run Failed: {run.last_error}")
        elif run.status == "requires_action":
            # NOTE: If we get here, it means the agent trying to call a function locally
            # instead of using the server-side Action Group (HTTP). 
            # For now, we treat this as a failure or incomplete configuration.
            # Ideally, we would handle local function dispatch here if needed.
            logger.warning("Foundry agent requires local action - cancelling run")
            client.beta.threads.runs.cancel(thread_id=thread.id, run_id=run.id)
            raise Exception("Agent requires local tool action (not implemented)")
            
    if run.status != "completed":
        raise Exception("Foundry Run Timed Out")
        
    # Get Messages
    messages = client.beta.threads.messages.list(
        thread_id=thread.id,
        order="desc",
        limit=1
    )
    
    if not messages.data:
        return "No response from agent."
        
    return messages.data[0].content[0].text.value


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

