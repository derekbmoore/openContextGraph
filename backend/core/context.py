"""
OpenContextGraph - Core Context Schema

4-Layer Enterprise Context:
- Layer 1: SecurityContext (Identity)
- Layer 2: EpisodicContext (Conversation)
- Layer 3: SemanticContext (Knowledge)
- Layer 4: OperationalContext (Runtime)
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, Field


class Role(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    ANALYST = "analyst"
    PM = "pm"
    VIEWER = "viewer"
    DEVELOPER = "developer"


class MessageRole(str, Enum):
    """Conversation message roles"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"


class Turn(BaseModel):
    """A single conversation turn"""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: Optional[str] = Field(None, description="Which agent responded (elena/marcus/sage)")
    tool_calls: Optional[list[dict]] = Field(None, description="Tool calls made in this turn")
    token_count: Optional[int] = Field(None, description="Token count for this turn")


class SecurityContext(BaseModel):
    """Layer 1: Identity and Access Control"""
    user_id: str
    tenant_id: str = "default"
    session_id: str = ""
    project_id: Optional[str] = None
    roles: list[Role] = Field(default_factory=list)
    scopes: list[str] = Field(default_factory=list)
    email: Optional[str] = None
    display_name: Optional[str] = None
    token_expiry: Optional[datetime] = None
    
    def has_role(self, role: Role) -> bool:
        return role in self.roles or Role.ADMIN in self.roles
    
    def has_scope(self, scope: str) -> bool:
        if Role.ADMIN in self.roles:
            return True
        return scope in self.scopes
    
    def get_memory_filter(self) -> dict:
        return {
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
        }


class Message(BaseModel):
    """A single message in conversation"""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: dict = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EpisodicContext(BaseModel):
    """Layer 2: Conversation History"""
    conversation_id: str = Field(default_factory=lambda: str(uuid4()))
    recent_turns: list[Turn] = Field(default_factory=list, description="Rolling window of recent turns")
    # Compatibility with legacy code expecting a raw messages list
    recent_messages: list[Message] = Field(default_factory=list, description="Legacy message list (for compatibility)")
    turn_count: int = Field(0, description="Total turns in conversation (alias for total_turns)")
    total_turns: int = Field(0, description="Total turns in conversation")
    summary: str = Field("", description="Compressed narrative of conversation so far")
    channel: str = "chat"  # "chat", "voice", "episode"
    metadata: dict = Field(default_factory=dict)
    # Configuration
    max_turns: int = Field(10, description="Maximum turns to keep in window")
    # Metrics
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_activity: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    def add_turn(self, turn: Turn) -> None:
        """Add a turn, maintaining the rolling window"""
        self.recent_turns.append(turn)
        self.total_turns += 1
        self.turn_count = self.total_turns  # Keep in sync for compatibility
        self.last_activity = datetime.now(timezone.utc)
        
        # Compact if exceeding max turns
        if len(self.recent_turns) > self.max_turns:
            self.recent_turns = self.recent_turns[-self.max_turns:]
    
    def get_formatted_history(self) -> str:
        """Get conversation history formatted for LLM context"""
        history_parts = []
        if self.summary:
            history_parts.append(f"[Previous conversation summary: {self.summary}]")
        
        for turn in self.recent_turns:
            prefix = turn.agent_id.upper() if turn.agent_id else turn.role.value.upper()
            history_parts.append(f"{prefix}: {turn.content}")
        
        return "\n".join(history_parts)


class Fact(BaseModel):
    """A semantic fact from knowledge graph"""
    content: str
    source: Optional[str] = None
    confidence: float = 1.0
    timestamp: Optional[datetime] = None


class Entity(BaseModel):
    """An entity from knowledge graph"""
    name: str
    entity_type: str
    properties: dict = Field(default_factory=dict)


class GraphNode(BaseModel):
    """A node from the knowledge graph"""
    id: str
    label: str
    properties: dict = Field(default_factory=dict)
    relationships: list[str] = Field(default_factory=list)


class SemanticContext(BaseModel):
    """Layer 3: Knowledge Graph Context"""
    facts: list[Fact] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    graph_nodes: list[GraphNode] = Field(default_factory=list)
    relevance_scores: dict = Field(default_factory=dict)
    
    def add_fact(self, fact_or_node) -> None:
        """
        Add a fact to the semantic context.
        
        Accepts Fact, GraphNode, or dict/object with content/id attributes.
        """
        # Handle Fact objects
        if isinstance(fact_or_node, Fact):
            self.facts.append(fact_or_node)
            if fact_or_node.source:
                self.relevance_scores[fact_or_node.source] = fact_or_node.confidence
        # Handle GraphNode objects
        elif isinstance(fact_or_node, GraphNode):
            self.graph_nodes.append(fact_or_node)
            if fact_or_node.id:
                self.relevance_scores[fact_or_node.id] = 1.0
        # Handle dict/object with attributes (from Zep API)
        else:
            # Try to extract content and id
            content = None
            fact_id = None
            confidence = 1.0
            
            if hasattr(fact_or_node, 'content'):
                content = fact_or_node.content
            elif hasattr(fact_or_node, 'fact'):
                content = fact_or_node.fact
            elif isinstance(fact_or_node, dict):
                content = fact_or_node.get('content') or fact_or_node.get('fact')
            
            if hasattr(fact_or_node, 'id'):
                fact_id = fact_or_node.id
            elif hasattr(fact_or_node, 'uuid'):
                fact_id = fact_or_node.uuid
            elif isinstance(fact_or_node, dict):
                fact_id = fact_or_node.get('id') or fact_or_node.get('uuid')
            
            if hasattr(fact_or_node, 'confidence'):
                confidence = fact_or_node.confidence
            elif isinstance(fact_or_node, dict):
                confidence = fact_or_node.get('confidence', 1.0)
            
            if content:
                # Create a Fact object
                fact = Fact(
                    content=content,
                    source=fact_id,
                    confidence=confidence
                )
                self.facts.append(fact)
                if fact_id:
                    self.relevance_scores[fact_id] = confidence
    
    def get_context_summary(self) -> str:
        """Generate a summary of semantic context for the LLM"""
        parts = []
        
        # Add entities
        if self.entities:
            entities = [f"- {e.name} ({e.entity_type})" for e in self.entities[:10]]
            parts.append("Known Entities:\n" + "\n".join(entities))
        
        # Add facts (prioritize Fact objects, then graph_nodes)
        fact_list = []
        if self.facts:
            fact_list = [f"- {f.content}" for f in self.facts[:10]]
        elif self.graph_nodes:
            # Extract content from graph_nodes (check properties or use label)
            for node in self.graph_nodes[:10]:
                content = node.properties.get('content') or node.properties.get('fact') or node.label
                if content:
                    fact_list.append(f"- {content}")
        
        if fact_list:
            parts.append("Relevant Facts:\n" + "\n".join(fact_list))
        
        return "\n\n".join(parts) if parts else "No relevant context found."


class ToolCall(BaseModel):
    """A tool invocation record"""
    tool_name: str
    arguments: dict = Field(default_factory=dict)
    result: Optional[str] = None
    duration_ms: Optional[int] = None


class OperationalContext(BaseModel):
    """Layer 4: Runtime Operational Context"""
    current_agent: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    latency_budget_ms: int = 30000
    cost_budget_tokens: int = 100000
    request_id: str = ""


class EnterpriseContext(BaseModel):
    """Complete 4-Layer Enterprise Context"""
    security: SecurityContext
    episodic: EpisodicContext = Field(default_factory=EpisodicContext)
    semantic: SemanticContext = Field(default_factory=SemanticContext)
    operational: OperationalContext = Field(default_factory=OperationalContext)
    
    @classmethod
    def create(cls, user_id: str, tenant_id: str = "default") -> "EnterpriseContext":
        """Factory method for creating context"""
        return cls(
            security=SecurityContext(user_id=user_id, tenant_id=tenant_id)
        )
