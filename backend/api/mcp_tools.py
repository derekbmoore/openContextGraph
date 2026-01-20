"""
MCP Tool Registry

Defines all tools exposed via Model Context Protocol for Azure AI Foundry agents.
Each tool maps to an existing backend handler.

Reference: https://spec.modelcontextprotocol.io/
"""
from typing import Any, Callable, Optional
from pydantic import BaseModel, Field
import logging

logger = logging.getLogger(__name__)


class ToolParameter(BaseModel):
    """JSON Schema for a tool parameter."""
    name: str
    type: str  # string, integer, boolean, object, array
    description: str
    required: bool = True
    default: Any = None


class ToolDefinition(BaseModel):
    """MCP Tool Definition."""
    name: str
    description: str
    parameters: list[ToolParameter] = Field(default_factory=list)
    handler: Optional[str] = None  # Module path to handler function


# =============================================================================
# Tool Definitions
# =============================================================================

TOOL_REGISTRY: dict[str, ToolDefinition] = {
    # ---------------------------------------------------------------------
    # Memory Tools (Sage, Elena, Marcus)
    # ---------------------------------------------------------------------
    "search_memory": ToolDefinition(
        name="search_memory",
        description="""Search long-term memory (Zep) for facts, documents, or past episodes.
Uses Tri-Search™ combining keyword, semantic, and graph methods.
Returns ranked results with relevance scores.""",
        parameters=[
            ToolParameter(name="query", type="string", description="The search query"),
            ToolParameter(name="limit", type="integer", description="Maximum results (default: 5)", required=False, default=5),
            ToolParameter(name="search_type", type="string", description="keyword | similarity | hybrid (default: hybrid)", required=False, default="hybrid"),
        ],
        handler="api.routes.memory.search_memory",
    ),
    "list_episodes": ToolDefinition(
        name="list_episodes",
        description="List conversation episodes from memory with summaries and topics.",
        parameters=[
            ToolParameter(name="limit", type="integer", description="Maximum episodes (default: 10)", required=False, default=10),
        ],
        handler="api.routes.memory.list_episodes",
    ),
    
    # ---------------------------------------------------------------------
    # Story Tools (Sage)
    # ---------------------------------------------------------------------
    "generate_story": ToolDefinition(
        name="generate_story",
        description="""Generate a narrative story about a topic by synthesizing information from memory.
Creates engaging content that explains complex topics in accessible ways.""",
        parameters=[
            ToolParameter(name="topic", type="string", description="The subject of the story"),
            ToolParameter(name="style", type="string", description="informative | dramatic | whimsical (default: informative)", required=False, default="informative"),
            ToolParameter(name="length", type="string", description="short | medium | long (default: medium)", required=False, default="medium"),
        ],
        handler="api.routes.stories.create_story",
    ),
    "generate_diagram": ToolDefinition(
        name="generate_diagram",
        description="""Generate a visual diagram (architecture, flowchart, sequence, timeline).
Returns Mermaid code that can be rendered as an image.""",
        parameters=[
            ToolParameter(name="description", type="string", description="What the diagram should show"),
            ToolParameter(name="diagram_type", type="string", description="architecture | flowchart | sequence | timeline (default: architecture)", required=False, default="architecture"),
        ],
        handler="api.routes.stories.generate_visual",
    ),
    
    # ---------------------------------------------------------------------
    # Code Tools (Marcus)
    # ---------------------------------------------------------------------
    "search_codebase": ToolDefinition(
        name="search_codebase",
        description="""Search the codebase for patterns, function names, or code structures.
Uses ripgrep for fast, regex-capable code search.""",
        parameters=[
            ToolParameter(name="query", type="string", description="The search pattern (supports regex)"),
            ToolParameter(name="file_pattern", type="string", description="Glob pattern to filter files (e.g., '*.py')", required=False, default="*"),
            ToolParameter(name="limit", type="integer", description="Maximum results (default: 20)", required=False, default=20),
        ],
        handler="api.mcp_handlers.search_codebase",
    ),
    
    # ---------------------------------------------------------------------
    # ETL Tools (Elena)
    # ---------------------------------------------------------------------
    "trigger_ingestion": ToolDefinition(
        name="trigger_ingestion",
        description="Trigger document ingestion into the context ecology.",
        parameters=[
            ToolParameter(name="source_name", type="string", description="Name of the ingestion source"),
            ToolParameter(name="kind", type="string", description="Upload | OneDrive | URL (default: Upload)", required=False, default="Upload"),
        ],
        handler="api.routes.etl.ingest",
    ),
    
    # ---------------------------------------------------------------------
    # GitHub Tools (Elena, Marcus)
    # ---------------------------------------------------------------------
    "get_project_status": ToolDefinition(
        name="get_project_status",
        description="Get current status metrics of the GitHub project (total, completed, open tasks).",
        parameters=[],
        handler="api.mcp_handlers.get_project_status",
    ),
    "create_github_issue": ToolDefinition(
        name="create_github_issue",
        description="Create a GitHub issue for tracking a task or bug.",
        parameters=[
            ToolParameter(name="title", type="string", description="Issue title"),
            ToolParameter(name="body", type="string", description="Issue description (markdown supported)"),
            ToolParameter(name="labels", type="string", description="Comma-separated labels", required=False),
        ],
        handler="api.mcp_handlers.create_github_issue",
    ),
    
    # ---------------------------------------------------------------------
    # Database Tools (Admin/Analyst)
    # ---------------------------------------------------------------------
    "query_database": ToolDefinition(
        name="query_database",
        description="Execute a read-only SQL SELECT query against the internal PostgreSQL database.",
        parameters=[
            ToolParameter(name="query", type="string", description="SQL SELECT query to execute"),
        ],
        handler="api.mcp_handlers.query_database",
    ),
}


def get_tool_manifest() -> list[dict]:
    """
    Generate MCP-compliant tool manifest.
    
    Returns tools in the format expected by MCP tools/list response.
    """
    tools = []
    for name, definition in TOOL_REGISTRY.items():
        # Build JSON Schema for parameters
        properties = {}
        required = []
        
        for param in definition.parameters:
            properties[param.name] = {
                "type": param.type,
                "description": param.description,
            }
            if param.default is not None:
                properties[param.name]["default"] = param.default
            if param.required:
                required.append(param.name)
        
        tools.append({
            "name": name,
            "description": definition.description,
            "inputSchema": {
                "type": "object",
                "properties": properties,
                "required": required,
            }
        })
    
    return tools


def get_tool_handler(tool_name: str) -> Optional[ToolDefinition]:
    """Get tool definition by name."""
    return TOOL_REGISTRY.get(tool_name)
