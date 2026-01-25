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
    
    # ---------------------------------------------------------------------
    # Domain Memory Tools (Elena, Marcus, Sage)
    # ---------------------------------------------------------------------
    "read_domain_memory": ToolDefinition(
        name="read_domain_memory",
        description="""Read the current Domain Memory file to understand project patterns and decisions.
        
        Use this in the Research phase before making changes.
        Returns the full Domain Memory content for context.""",
        parameters=[
            ToolParameter(name="section", type="string", description="Optional: specific section to read (e.g., 'architectural_patterns', 'known_issues')", required=False),
        ],
        handler="api.mcp_handlers.read_domain_memory",
    ),
    "update_domain_memory": ToolDefinition(
        name="update_domain_memory",
        description="""Update the Domain Memory file (.ctxeco/domain-memory.md) with new knowledge.
        
        Use this after making architectural decisions, fixing bugs, or establishing patterns.
        The tool will:
        1. Update the domain-memory.md file
        2. Automatically ingest it into Zep (via Antigravity Router)
        3. Return the memory reference for future retrieval
        
        Categories:
        - architectural_decision: New architecture pattern
        - bug_fix: Solution to a recurring problem
        - pattern_established: Code/style convention
        - anti_pattern_identified: What NOT to do
        - configuration_note: Critical config requirement""",
        parameters=[
            ToolParameter(name="decision", type="string", description="The decision or pattern (e.g., 'Use openai.azure.com for Foundry agents')"),
            ToolParameter(name="why", type="string", description="Why this decision was made (rationale)"),
            ToolParameter(name="pattern", type="string", description="Optional: Code pattern or example", required=False),
            ToolParameter(name="anti_pattern", type="string", description="Optional: What NOT to do", required=False),
            ToolParameter(name="commit_hash", type="string", description="Optional: Related commit hash", required=False),
            ToolParameter(name="category", type="string", description="Category: architectural_decision, bug_fix, pattern_established, anti_pattern_identified, configuration_note (default: architectural_decision)", required=False, default="architectural_decision"),
            ToolParameter(name="related_docs", type="array", description="Optional: Array of related doc paths", required=False),
        ],
        handler="api.mcp_handlers.update_domain_memory",
    ),
    "scan_commit_history": ToolDefinition(
        name="scan_commit_history",
        description="""Scan git commit logs to extract architectural decisions, patterns, and project evolution.
        
        Returns structured data about:
        - Recent commits with decision keywords
        - Pattern changes (code style, architecture)
        - Bug fixes and solutions
        - Project evolution timeline
        
        Use this in the Research phase before making changes.""",
        parameters=[
            ToolParameter(name="since_days", type="integer", description="Number of days to look back (default: 30)", required=False, default=30),
            ToolParameter(name="pattern", type="string", description="Optional: filter commits by pattern (e.g., 'auth', 'foundry')", required=False),
            ToolParameter(name="extract_decisions", type="boolean", description="Whether to extract decision keywords from commit messages (default: true)", required=False, default=True),
        ],
        handler="api.mcp_handlers.scan_commit_history",
    ),
    
    # ---------------------------------------------------------------------
    # Foundry IQ Tools (Elena, Marcus, Sage)
    # ---------------------------------------------------------------------
    "list_foundry_iq_kbs": ToolDefinition(
        name="list_foundry_iq_kbs",
        description="""List available Foundry IQ knowledge bases in the project.
        
        Returns metadata about configured knowledge bases including:
        - Knowledge base ID and name
        - Status (configured, available, etc.)
        - Source count (if available)
        
        Use this to discover available knowledge bases before querying.""",
        parameters=[
            ToolParameter(name="project_id", type="string", description="Optional: Foundry project ID", required=False),
        ],
        handler="api.mcp_handlers.list_foundry_iq_kbs",
    ),
    "query_foundry_iq_kb": ToolDefinition(
        name="query_foundry_iq_kb",
        description="""Query a Foundry IQ knowledge base for enterprise documents.
        
        Foundry IQ knowledge bases provide access to enterprise documents
        (SharePoint, OneLake, etc.) with built-in permission trimming.
        
        Returns ranked results with:
        - Content snippets
        - Relevance scores
        - Source attribution
        - Citations
        
        Use this for enterprise document retrieval when Foundry IQ is configured.""",
        parameters=[
            ToolParameter(name="kb_id", type="string", description="Knowledge base ID to query"),
            ToolParameter(name="query", type="string", description="Search query"),
            ToolParameter(name="limit", type="integer", description="Maximum results (default: 5)", required=False, default=5),
            ToolParameter(name="search_type", type="string", description="keyword | vector | hybrid (default: hybrid)", required=False, default="hybrid"),
        ],
        handler="api.mcp_handlers.query_foundry_iq_kb",
    ),
    "get_foundry_iq_kb_status": ToolDefinition(
        name="get_foundry_iq_kb_status",
        description="""Get status and health of a Foundry IQ knowledge base.
        
        Returns:
        - Enabled status
        - Configuration status
        - Search client availability
        - Health indicators
        
        Use this to check if a KB is available before querying.""",
        parameters=[
            ToolParameter(name="kb_id", type="string", description="Knowledge base ID"),
        ],
        handler="api.mcp_handlers.get_foundry_iq_kb_status",
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
