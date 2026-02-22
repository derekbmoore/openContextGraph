"""
MCP Router - Model Context Protocol Endpoint

Implements JSON-RPC 2.0 protocol for Azure AI Foundry agent tool calls.

Protocol Reference: https://spec.modelcontextprotocol.io/

Endpoints:
  POST /mcp - Main JSON-RPC endpoint
  
Methods:
  initialize - Handshake and capability exchange
  tools/list - Return available tools
  tools/call - Execute a tool
"""
import json
import logging
from typing import Any, Optional
from fastapi import APIRouter, Request, Depends, HTTPException
from pydantic import BaseModel, Field

from api.mcp_tools import get_tool_manifest, get_tool_handler, TOOL_REGISTRY
from api.middleware.auth import get_current_user, get_optional_user
from api.agent_keys import validate_api_key
from core import SecurityContext

logger = logging.getLogger(__name__)

router = APIRouter()


# =============================================================================
# JSON-RPC Models
# =============================================================================

class JsonRpcRequest(BaseModel):
    """JSON-RPC 2.0 Request."""
    jsonrpc: str = "2.0"
    method: str
    params: Optional[dict] = None
    id: Optional[str | int] = None


class JsonRpcResponse(BaseModel):
    """JSON-RPC 2.0 Response."""
    jsonrpc: str = "2.0"
    result: Optional[Any] = None
    error: Optional[dict] = None
    id: Optional[str | int] = None


class JsonRpcError:
    """Standard JSON-RPC error codes."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


# =============================================================================
# MCP Protocol Constants
# =============================================================================

MCP_PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {
    "name": "ctxeco-mcp-server",
    "version": "1.0.0",
}
SERVER_CAPABILITIES = {
    "tools": {},  # We support tools
}

# =============================================================================
# API Key Authentication for MCP Agents
# =============================================================================


def validate_api_key_from_request(request: Request) -> Optional[dict]:
    """
    Validate x-api-key header and return agent info if valid.
    
    Returns None if no key provided (for unauthenticated access).
    Raises HTTPException if key is invalid.
    """
    api_key = request.headers.get("x-api-key")
    return validate_api_key(api_key)


# =============================================================================
# Main MCP Endpoint
# =============================================================================

@router.post("")
@router.post("/")
async def mcp_endpoint(
    request: Request,
    user: Optional[SecurityContext] = Depends(get_optional_user),
):
    """
    Main MCP JSON-RPC endpoint.
    
    Handles all MCP protocol methods:
    - initialize: Handshake
    - tools/list: Return tool manifest
    - tools/call: Execute tool
    """
    try:
        body = await request.json()
    except json.JSONDecodeError:
        return JsonRpcResponse(
            error={"code": JsonRpcError.PARSE_ERROR, "message": "Parse error"},
            id=None,
        )
    
    # Parse request
    try:
        rpc_request = JsonRpcRequest(**body)
    except Exception as e:
        return JsonRpcResponse(
            error={"code": JsonRpcError.INVALID_REQUEST, "message": str(e)},
            id=body.get("id"),
        )
    
    # Route to handler
    method = rpc_request.method
    params = rpc_request.params or {}
    request_id = rpc_request.id
    
    logger.info(f"MCP Request: {method} (id={request_id})")
    
    try:
        if method == "initialize":
            result = await handle_initialize(params)
        elif method == "tools/list":
            result = await handle_tools_list(params)
        elif method == "tools/call":
            result = await handle_tools_call(params, user)
        elif method == "ping":
            result = {"pong": True}
        else:
            return JsonRpcResponse(
                error={"code": JsonRpcError.METHOD_NOT_FOUND, "message": f"Unknown method: {method}"},
                id=request_id,
            )
        
        return JsonRpcResponse(result=result, id=request_id)
        
    except Exception as e:
        logger.error(f"MCP Error handling {method}: {e}")
        return JsonRpcResponse(
            error={"code": JsonRpcError.INTERNAL_ERROR, "message": str(e)},
            id=request_id,
        )


# =============================================================================
# MCP Method Handlers
# =============================================================================

async def handle_initialize(params: dict) -> dict:
    """
    Handle MCP initialize handshake.
    
    Returns server info and capabilities.
    """
    client_info = params.get("clientInfo", {})
    logger.info(f"MCP Initialize from: {client_info.get('name', 'unknown')}")
    
    return {
        "protocolVersion": MCP_PROTOCOL_VERSION,
        "serverInfo": SERVER_INFO,
        "capabilities": SERVER_CAPABILITIES,
    }


async def handle_tools_list(params: dict) -> dict:
    """
    Handle tools/list request.
    
    Returns manifest of all available tools.
    """
    tools = get_tool_manifest()
    logger.info(f"MCP tools/list: Returning {len(tools)} tools")
    
    return {"tools": tools}


async def handle_tools_call(params: dict, user: Optional[SecurityContext]) -> dict:
    """
    Handle tools/call request.
    
    Dispatches to the registered tool handler.
    """
    tool_name = params.get("name")
    tool_args = params.get("arguments", {})
    
    if not tool_name:
        raise ValueError("Missing 'name' in tools/call params")
    
    tool_def = get_tool_handler(tool_name)
    if not tool_def:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    logger.info(f"MCP tools/call: {tool_name} args={list(tool_args.keys())}")
    
    # Dispatch to handler
    # For now, we implement handlers inline. In production, these would
    # dynamically import and call the registered handler path.
    
    result = await dispatch_tool(tool_name, tool_args, user)
    
    return {
        "content": [
            {
                "type": "text",
                "text": json.dumps(result) if isinstance(result, (dict, list)) else str(result),
            }
        ],
        "isError": False,
    }


# =============================================================================
# Tool Dispatch
# =============================================================================

async def dispatch_tool(tool_name: str, args: dict, user: Optional[SecurityContext]) -> Any:
    """
    Dispatch tool call to appropriate handler.
    
    This bridges MCP requests to existing backend functions.
    """
    from memory import get_memory_client
    
    # Create a default security context if none provided
    if user is None:
        user = SecurityContext(user_id="mcp-agent", tenant_id="default")
    
    if tool_name == "search_memory":
        memory_client = get_memory_client()
        result = await memory_client.search_memory(
            query=args.get("query", ""),
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            search_type=args.get("search_type", "hybrid"),
            limit=args.get("limit", 5),
        )
        return result
    
    elif tool_name == "list_episodes":
        memory_client = get_memory_client()
        sessions = await memory_client.list_sessions(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            limit=args.get("limit", 10),
        )
        return {"episodes": sessions}
    
    elif tool_name == "generate_story":
        # Call Temporal workflow for durable story generation
        # Uses Claude for story, Gemini for diagram
        from workflows.client import execute_story
        
        topic = args.get("topic", "Untitled")
        style = args.get("style", "informative")
        length = args.get("length", "medium")
        user_context = args.get("context")
        
        # Default Sage workflow always includes visual generation
        include_image = True
        
        contextual_guidance = [f"Style: {style}.", f"Length: {length}."]
        if user_context:
            contextual_guidance.append(str(user_context))
        if "secai" in topic.lower() or "secairadar" in topic.lower() or "mcp" in topic.lower():
            contextual_guidance.append(
                "Focus on secairadar.cloud MCP + AI trust ranking system with outputs optimized for agents first, then humans."
            )

        logger.info(f"MCP: Triggering Temporal story workflow for '{topic}'")
        
        try:
            result = await execute_story(
                user_id=user.user_id,
                tenant_id=user.tenant_id,
                topic=topic,
                context=" ".join(contextual_guidance),
                include_diagram=True,
                include_image=include_image,
                diagram_type="architecture",
                timeout_seconds=300,  # 5 minute timeout
            )
            
            if result.success:
                return {
                    "status": "completed",
                    "story_id": result.story_id,
                    "topic": result.topic,
                    "story_content": result.story_content[:2000] + "..." if len(result.story_content) > 2000 else result.story_content,
                    "story_path": result.story_path,
                    "diagram_path": result.diagram_path,
                    "image_path": f"/api/v1/images/{result.story_id}.png" if result.image_path else None,
                }
            else:
                return {
                    "status": "failed",
                    "error": result.error,
                }
        except Exception as e:
            logger.error(f"MCP generate_story failed: {e}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Story generation failed. Temporal may be unavailable.",
            }
    
    elif tool_name == "generate_diagram":
        # Call Temporal diagram activity directly for standalone diagrams
        from workflows.story_activities import generate_diagram_activity, GenerateDiagramInput
        
        description = args.get("description", "System Architecture")
        diagram_type = args.get("diagram_type", "architecture")
        
        logger.info(f"MCP: Generating diagram for '{description}'")
        
        try:
            # Note: This calls the activity function directly (not via workflow)
            # For full durability, wrap in a workflow
            result = await generate_diagram_activity(
                GenerateDiagramInput(
                    topic=description,
                    diagram_type=diagram_type,
                )
            )
            
            if result.success:
                return {
                    "status": "completed",
                    "diagram_type": diagram_type,
                    "spec": result.spec,
                }
            else:
                return {
                    "status": "failed",
                    "error": result.error,
                }
        except Exception as e:
            logger.error(f"MCP generate_diagram failed: {e}")
            return {
                "status": "error",
                "error": str(e),
            }
    
    elif tool_name == "search_codebase":
        # Placeholder - would call ripgrep
        query = args.get("query", "")
        return {
            "query": query,
            "results": [
                {"file": "backend/api/mcp.py", "line": 1, "match": f"Found: {query}"},
            ],
            "message": "Codebase search is a placeholder in this implementation.",
        }
    
    elif tool_name == "get_project_status":
        # Placeholder - would call GitHub API
        return {
            "total_tasks": 42,
            "completed": 35,
            "open": 7,
            "progress_percent": 83,
        }
    
    elif tool_name == "create_github_issue":
        # Placeholder - would call GitHub API
        return {
            "issue_number": 123,
            "url": f"https://github.com/zimaxnet/openContextGraph/issues/123",
            "title": args.get("title"),
        }
    
    elif tool_name == "trigger_ingestion":
        # Placeholder - would call ETL
        return {
            "status": "queued",
            "source": args.get("source_name"),
        }
    
    elif tool_name == "query_database":
        from api.mcp_handlers import query_database
        query = args.get("query", "")
        return await query_database(query)
    
    elif tool_name == "read_domain_memory":
        from api.mcp_handlers import read_domain_memory
        section = args.get("section")
        return await read_domain_memory(section=section)
    
    elif tool_name == "update_domain_memory":
        from api.mcp_handlers import update_domain_memory
        return await update_domain_memory(
            decision=args.get("decision", ""),
            why=args.get("why", ""),
            pattern=args.get("pattern"),
            anti_pattern=args.get("anti_pattern"),
            commit_hash=args.get("commit_hash"),
            category=args.get("category", "architectural_decision"),
            related_docs=args.get("related_docs"),
        )
    
    elif tool_name == "scan_commit_history":
        from api.mcp_handlers import scan_commit_history
        return await scan_commit_history(
            since_days=args.get("since_days", 30),
            pattern=args.get("pattern"),
            extract_decisions=args.get("extract_decisions", True),
        )
    
    elif tool_name == "list_foundry_iq_kbs":
        from api.mcp_handlers import list_foundry_iq_kbs
        return await list_foundry_iq_kbs(
            project_id=args.get("project_id"),
        )
    
    elif tool_name == "query_foundry_iq_kb":
        from api.mcp_handlers import query_foundry_iq_kb
        return await query_foundry_iq_kb(
            kb_id=args.get("kb_id", ""),
            query=args.get("query", ""),
            limit=args.get("limit", 5),
            search_type=args.get("search_type", "hybrid"),
        )
    
    elif tool_name == "get_foundry_iq_kb_status":
        from api.mcp_handlers import get_foundry_iq_kb_status
        return await get_foundry_iq_kb_status(
            kb_id=args.get("kb_id", ""),
        )
    
    else:
        raise ValueError(f"No handler implemented for tool: {tool_name}")
