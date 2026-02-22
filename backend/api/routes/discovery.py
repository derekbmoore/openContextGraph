"""
Agent-first discovery endpoints for ctxEco.

Serves:
- /llms.txt
- /.well-known/ctxeco-discovery.json

These endpoints make ctxEco easier for autonomous agents to discover and
consume programmatically.
"""

from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, PlainTextResponse


router = APIRouter(tags=["discovery"])


def _base_url(request: Request) -> str:
    return str(request.base_url).rstrip("/")


@router.get("/llms.txt", response_class=PlainTextResponse)
@router.get("/api/v1/public/llms.txt", response_class=PlainTextResponse)
async def llms_txt(request: Request):
    """LLMs.txt cheat-sheet for AI agents."""
    base_url = _base_url(request)
    now = datetime.now(timezone.utc).isoformat()

    content = f"""# ctxEco (openContextGraph)

> Agent-first context ecology platform for memory, tri-search, story workflows, and document ingestion.

## Core capabilities

- Tri-Search memory retrieval (keyword + similarity + hybrid)
- Session and episode memory operations
- Durable story generation workflows (Claude + Gemini + Nano Banana schema)
- ETL ingestion and provenance-aware processing

## High-value endpoints

- Memory Search: {base_url}/api/v1/memory/search
- Sessions: {base_url}/api/v1/memory/sessions
- Episodes: {base_url}/api/v1/memory/episodes
- Story Create: {base_url}/api/v1/story/create
- Story Latest: {base_url}/api/v1/story/latest
- ETL Ingest: {base_url}/api/v1/etl/ingest
- MCP Endpoint: {base_url}/mcp
- Discovery Manifest: {base_url}/.well-known/ctxeco-discovery.json

## Agent notes

- Authentication: Bearer token (OIDC / Entra) unless AUTH_REQUIRED=false in dev
- Tenant isolation is enforced via security context and metadata
- Story artifacts include markdown, Nano Banana JSON spec, and optional image

Generated at: {now}
"""
    return PlainTextResponse(content=content, media_type="text/markdown")


@router.get("/.well-known/ctxeco-discovery.json", response_class=JSONResponse)
@router.get("/api/v1/public/discovery", response_class=JSONResponse)
async def discovery_manifest(request: Request):
    """Machine-readable discovery manifest for agents."""
    base_url = _base_url(request)
    now = datetime.now(timezone.utc).isoformat()

    return JSONResponse(
        content={
            "@context": "https://schema.org",
            "@type": "WebAPI",
            "name": "ctxEco Discovery Manifest",
            "description": "Agent-first discovery metadata for ctxEco APIs and workflows.",
            "url": base_url,
            "version": "v1.0",
            "capabilities": {
                "memory": {
                    "search": f"{base_url}/api/v1/memory/search",
                    "sessions": f"{base_url}/api/v1/memory/sessions",
                    "episodes": f"{base_url}/api/v1/memory/episodes",
                },
                "story": {
                    "create": f"{base_url}/api/v1/story/create",
                    "latest": f"{base_url}/api/v1/story/latest",
                    "workflow": "temporal-durable-execution",
                    "diagram_schema": "nano-banana-pro-v1",
                },
                "ingestion": {
                    "ingest": f"{base_url}/api/v1/etl/ingest",
                    "status": f"{base_url}/api/v1/etl/status/{{document_id}}",
                },
                "mcp": {
                    "endpoint": f"{base_url}/mcp",
                    "protocol": "json-rpc-2.0",
                },
            },
            "generatedAt": now,
        }
    )
