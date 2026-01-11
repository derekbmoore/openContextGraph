"""
OpenContextGraph - Core Context Schema

4-Layer Enterprise Context:
- Layer 1: SecurityContext (Identity)
- Layer 2: EpisodicContext (Conversation)
- Layer 3: SemanticContext (Knowledge)
- Layer 4: OperationalContext (Runtime)
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class Role(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    ANALYST = "analyst"
    PM = "pm"
    VIEWER = "viewer"
    DEVELOPER = "developer"


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
    conversation_id: str = ""
    turn_count: int = 0
    recent_messages: list[Message] = Field(default_factory=list)
    channel: str = "chat"  # "chat", "voice", "episode"
    metadata: dict = Field(default_factory=dict)


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
