"""
Tools API Routes

Lightweight HTTP tool endpoints for Foundry action groups and demo flows.
These map to existing memory ingestion and Tri-Search functionality.
"""

import os
import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field

from api.agent_keys import validate_api_key
from api.middleware.auth import get_auth
from core import SecurityContext
from core.context import Role
from memory.client import get_memory_client

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer(auto_error=False)


async def get_tool_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> SecurityContext:
    """Resolve a user for tool calls (API key, bearer token, or POC fallback)."""
    api_key = request.headers.get("x-api-key")
    agent_info = validate_api_key(api_key)
    if agent_info:
        return SecurityContext(
            user_id=agent_info.get("agent_id", "tool-agent"),
            tenant_id=agent_info.get("tenant_id", "zimax"),
            email=None,
            display_name=agent_info.get("agent_name"),
            roles=[Role.ADMIN],
            scopes=["*"],
        )

    if credentials:
        auth = get_auth()
        payload = await auth.validate_token(credentials.credentials)
        return SecurityContext(
            user_id=payload.oid or payload.sub,
            tenant_id=payload.tid or "default",
            roles=auth.map_roles(payload.roles),
            scopes=auth.extract_scopes(payload),
            email=payload.email or payload.preferred_username,
            display_name=payload.name,
            groups=payload.groups,
        )

    if os.getenv("AUTH_REQUIRED", "true").lower() == "true":
        raise HTTPException(status_code=401, detail="Authentication required")

    return SecurityContext(
        user_id=os.getenv("POC_USER_ID", "poc-user"),
        tenant_id=os.getenv("POC_TENANT_ID", "zimax"),
        roles=[Role.ADMIN],
        scopes=["*"],
        email=os.getenv("POC_USER_EMAIL", "poc@example.com"),
        display_name=os.getenv("POC_USER_NAME", "POC User"),
    )


class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    limit: int = Field(5, ge=1, le=100)
    search_type: str = Field("hybrid", description="keyword | similarity | hybrid")


class SearchResponse(BaseModel):
    results: list[dict]
    search_type: str
    query: str


@router.post("/search_memory", response_model=SearchResponse)
async def tool_search_memory(
    request: SearchRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    memory_client = get_memory_client()
    result = await memory_client.search_memory(
        query=request.query,
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        search_type=request.search_type,
        limit=request.limit,
    )
    return SearchResponse(
        results=result.get("results", []),
        search_type=result.get("search_type", request.search_type),
        query=request.query,
    )


class AddFactRequest(BaseModel):
    content: str = Field(..., description="Fact content")
    metadata: dict = Field(default_factory=dict)


class AddFactResponse(BaseModel):
    success: bool
    fact_id: Optional[str] = None


@router.post("/add_fact", response_model=AddFactResponse)
async def tool_add_fact(
    request: AddFactRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    memory_client = get_memory_client()
    fact_id = await memory_client.add_fact(
        user_id=user.user_id,
        fact=request.content,
        metadata=request.metadata,
    )
    return AddFactResponse(success=True, fact_id=fact_id)


class EnrichRequest(BaseModel):
    text: str
    session_id: Optional[str] = None
    speaker: str = "user"
    agent_id: Optional[str] = None
    channel: str = "voice"
    title: Optional[str] = None
    summary: Optional[str] = None
    metadata: dict = Field(default_factory=dict)


class EnrichResponse(BaseModel):
    success: bool
    session_id: str
    message: str


@router.post("/enrich_memory", response_model=EnrichResponse)
async def tool_enrich_memory(
    request: EnrichRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    try:
        memory_client = get_memory_client()
        session_id = request.session_id or f"poc-{os.urandom(6).hex()}"
        summary = request.summary or (request.text[:200] + ("..." if len(request.text) > 200 else ""))
        title = request.title

        session_metadata = {
            "tenant_id": user.tenant_id,
            "channel": request.channel,
            "agent_id": request.agent_id or "unknown",
            "summary": summary,
            "title": title,
            "turn_count": 1,
            **request.metadata,
        }

        await memory_client.get_or_create_session(
            session_id=session_id,
            user_id=user.user_id,
            metadata=session_metadata,
        )

        message_metadata = {
            "agent_id": request.agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "channel": request.channel,
            **request.metadata,
        }

        await memory_client.add_memory(
            session_id=session_id,
            messages=[
                {
                    "role": "user" if request.speaker == "user" else "assistant",
                    "content": request.text,
                    "metadata": message_metadata,
                }
            ],
        )

        return EnrichResponse(
            success=True,
            session_id=session_id,
            message="Transcript enriched successfully",
        )
    except Exception as e:
        logger.warning("Memory enrichment failed (non-blocking): %s", e)
        return EnrichResponse(
            success=False,
            session_id=request.session_id or "",
            message=f"Enrichment failed: {str(e)}",
        )


class ListEpisodesRequest(BaseModel):
    limit: int = Field(10, ge=1, le=100)


class ListEpisodesResponse(BaseModel):
    episodes: list[dict]


@router.post("/list_episodes", response_model=ListEpisodesResponse)
async def tool_list_episodes(
    request: ListEpisodesRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    memory_client = get_memory_client()
    sessions = await memory_client.list_sessions(
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        limit=request.limit,
        offset=0,
    )
    return ListEpisodesResponse(episodes=sessions)


class CreateEpisodeRequest(BaseModel):
    title: str
    summary: str
    content: str
    tags: str = ""


class CreateEpisodeResponse(BaseModel):
    success: bool
    episode_id: str


@router.post("/create_episode", response_model=CreateEpisodeResponse)
async def tool_create_episode(
    request: CreateEpisodeRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    memory_client = get_memory_client()
    session_id = f"episode-{os.urandom(6).hex()}"
    metadata = {
        "type": "episode",
        "title": request.title,
        "summary": request.summary,
        "topics": [t.strip() for t in request.tags.split(",") if t.strip()],
        "agent_id": "sage",
        "turn_count": 1,
    }
    await memory_client.get_or_create_session(
        session_id=session_id,
        user_id=user.user_id,
        metadata=metadata,
    )
    await memory_client.add_memory(
        session_id=session_id,
        messages=[
            {
                "role": "assistant",
                "content": request.content,
                "metadata": {"title": request.title},
            }
        ],
    )
    return CreateEpisodeResponse(success=True, episode_id=session_id)


class GenerateStoryRequest(BaseModel):
    topic: str
    style: str = "informative"
    length: str = "medium"


@router.post("/generate_story")
async def tool_generate_story(
    request: GenerateStoryRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    from workflows.client import execute_story

    include_image = True
    result = await execute_story(
        user_id=user.user_id,
        tenant_id=user.tenant_id,
        topic=request.topic,
        context=f"Style: {request.style}. Length: {request.length}.",
        include_diagram=True,
        include_image=include_image,
        diagram_type="architecture",
        timeout_seconds=300,
    )

    if result.success:
        return {
            "status": "completed",
            "story_id": result.story_id,
            "topic": result.topic,
            "story_content": result.story_content,
            "story_path": result.story_path,
            "diagram_path": result.diagram_path,
            "image_path": f"/api/v1/images/{result.story_id}.png" if result.story_id else None,
        }

    return {
        "status": "failed",
        "error": result.error,
    }


class GenerateDiagramRequest(BaseModel):
    description: str
    diagram_type: str = "architecture"


@router.post("/generate_diagram")
async def tool_generate_diagram(
    request: GenerateDiagramRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    from workflows.story_activities import generate_diagram_activity, GenerateDiagramInput

    result = await generate_diagram_activity(
        GenerateDiagramInput(
            topic=request.description,
            diagram_type=request.diagram_type,
        )
    )

    if result.success:
        return {
            "status": "completed",
            "diagram_type": request.diagram_type,
            "spec": result.spec,
        }

    return {
        "status": "failed",
        "error": result.error,
    }


class SearchCodebaseRequest(BaseModel):
    query: str
    file_pattern: str = "*"
    limit: int = 20


@router.post("/search_codebase")
async def tool_search_codebase(
    request: SearchCodebaseRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    return {
        "query": request.query,
        "results": [],
        "message": "Codebase search is not enabled on the API host.",
    }


@router.post("/get_project_status")
async def tool_get_project_status(user: SecurityContext = Depends(get_tool_user)):
    return {
        "total_tasks": 42,
        "completed": 35,
        "open": 7,
        "progress_percent": 83,
    }


class CreateGithubIssueRequest(BaseModel):
    title: str
    body: str
    labels: Optional[str] = None


@router.post("/create_github_issue")
async def tool_create_github_issue(
    request: CreateGithubIssueRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    return {
        "issue_number": 123,
        "url": "https://github.com/zimaxnet/openContextGraph/issues/123",
        "title": request.title,
    }


@router.post("/list_my_tasks")
async def tool_list_my_tasks(user: SecurityContext = Depends(get_tool_user)):
    return {
        "tasks": [],
        "message": "Task listing is not enabled on the API host.",
    }


class RunDeploymentCheckRequest(BaseModel):
    environment: str = "dev"


@router.post("/run_deployment_check")
async def tool_run_deployment_check(
    request: RunDeploymentCheckRequest,
    user: SecurityContext = Depends(get_tool_user),
):
    return {
        "environment": request.environment,
        "status": "not_configured",
        "message": "Deployment checks are not enabled on the API host.",
    }
