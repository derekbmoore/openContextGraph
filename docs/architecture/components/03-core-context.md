# Core Context — 4-Layer Enterprise Schema

## Purpose

The Core Context module defines the **4-Layer Enterprise Context Schema**—the fundamental data structure that flows through every interaction in openContextGraph. This isn't just a data model; it's the **embodiment of enterprise AI governance**.

## Why This Exists

### The Problem

Traditional AI systems lack:

- **Identity**: Who is making the request?
- **History**: What happened before?
- **Knowledge**: What does the system know?
- **Constraints**: What are the operational boundaries?

Without these, AI systems cannot meet enterprise security, compliance, or auditability requirements.

### The Solution

A 4-layer context schema where each layer builds on the previous:

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: OperationalContext (Runtime Constraints)          │
│  ─────────────────────────────────────────────────────────  │
│  Layer 3: SemanticContext (Knowledge Graph)                 │
│  ─────────────────────────────────────────────────────────  │
│  Layer 2: EpisodicContext (Conversation History)            │
│  ─────────────────────────────────────────────────────────  │
│  Layer 1: SecurityContext (Identity & Access)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    EnterpriseContext                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ SecurityContext (Layer 1)                            │    │
│  │  • user_id      - Unique identifier                  │    │
│  │  • tenant_id    - Multi-tenant isolation             │    │
│  │  • roles        - RBAC permissions                   │    │
│  │  • scopes       - Fine-grained access                │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ EpisodicContext (Layer 2)                            │    │
│  │  • conversation_id - Session identifier              │    │
│  │  • turn_count      - Interaction count               │    │
│  │  • recent_messages - Conversation history            │    │
│  │  • channel         - chat/voice/episode              │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ SemanticContext (Layer 3)                            │    │
│  │  • facts           - Knowledge statements            │    │
│  │  • entities        - Named entities                  │    │
│  │  • graph_nodes     - Knowledge graph nodes           │    │
│  │  • relevance_scores - Retrieval rankings             │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ OperationalContext (Layer 4)                         │    │
│  │  • current_agent   - Active agent                    │    │
│  │  • tool_calls      - Function invocations            │    │
│  │  • latency_budget  - Time constraint                 │    │
│  │  • cost_budget     - Token limit                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Code Sample

```python
# backend/core/context.py
"""
OpenContextGraph - Core Context Schema

The 4-Layer Enterprise Context Schema:
- Layer 1: SecurityContext (Identity)
- Layer 2: EpisodicContext (Conversation)
- Layer 3: SemanticContext (Knowledge)  
- Layer 4: OperationalContext (Runtime)

NIST AI RMF Alignment:
- GOVERN 1.1: Schema defines accountability structure
- MAP 1.1: Layers map to system components
- MEASURE 2.3: Context enables quality measurement
- MANAGE 2.3: Layers enforce data governance
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


# =============================================================================
# LAYER 1: SECURITY CONTEXT
# NIST AI RMF: GOVERN 1.2 (Accountability), MAP 1.5 (Boundaries)
# =============================================================================

class Role(str, Enum):
    """User roles for Role-Based Access Control (RBAC)."""
    ADMIN = "admin"          # Full system access
    ANALYST = "analyst"      # Read + analyze, limited write
    PM = "pm"                # Project management scope
    VIEWER = "viewer"        # Read-only access
    DEVELOPER = "developer"  # API access, no admin


class SecurityContext(BaseModel):
    """
    Layer 1: Identity and Access Control
    
    This is the FOUNDATION of enterprise AI governance.
    Every request MUST have a SecurityContext.
    
    NIST AI RMF Controls:
    - GOVERN 1.2: Accountability through user_id
    - MAP 1.5: Boundaries through tenant_id
    - MANAGE 1.3: Access control through roles/scopes
    """
    user_id: str = Field(..., description="Unique user identifier from IdP")
    tenant_id: str = Field("default", description="Organization isolation")
    session_id: str = Field("", description="Current session identifier")
    
    # Permissions
    roles: list[Role] = Field(default_factory=list, description="RBAC roles")
    scopes: list[str] = Field(default_factory=list, description="Fine-grained permissions")
    
    # User metadata (from IdP claims)
    email: Optional[str] = Field(None, description="User email")
    display_name: Optional[str] = Field(None, description="Display name")
    token_expiry: Optional[datetime] = Field(None, description="Token expiration")
    
    def has_role(self, role: Role) -> bool:
        """Check if user has a specific role. Admins have all roles."""
        return role in self.roles or Role.ADMIN in self.roles
    
    def has_scope(self, scope: str) -> bool:
        """Check if user has a specific scope. Admins have all scopes."""
        if Role.ADMIN in self.roles:
            return True
        return scope in self.scopes
    
    def get_memory_filter(self) -> dict:
        """
        Generate filter for memory queries.
        
        Ensures all memory operations are scoped to the user's
        tenant and identity—critical for multi-tenant isolation.
        """
        return {
            "tenant_id": self.tenant_id,
            "user_id": self.user_id,
        }


# =============================================================================
# LAYER 2: EPISODIC CONTEXT
# NIST AI RMF: MAP 1.1 (System Context), MEASURE 2.5 (Feedback)
# =============================================================================

class Message(BaseModel):
    """A single message in conversation history."""
    role: str = Field(..., description="user, assistant, or system")
    content: str = Field(..., description="Message content")
    metadata: dict = Field(default_factory=dict, description="Additional context")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class EpisodicContext(BaseModel):
    """
    Layer 2: Conversation History
    
    Maintains the temporal flow of interactions within a session.
    Enables context-aware responses and conversation continuity.
    
    NIST AI RMF Controls:
    - MAP 1.1: Captures system interaction context
    - MEASURE 2.5: Enables user feedback collection
    - MANAGE 4.3: Supports incident reconstruction
    """
    conversation_id: str = Field("", description="Session identifier")
    turn_count: int = Field(0, description="Number of exchanges")
    recent_messages: list[Message] = Field(
        default_factory=list, 
        description="Recent conversation history"
    )
    channel: str = Field("chat", description="Interaction channel: chat, voice, episode")


# =============================================================================
# LAYER 3: SEMANTIC CONTEXT
# NIST AI RMF: MANAGE 2.3 (Data Governance), MEASURE 2.1 (Quality)
# =============================================================================

class Fact(BaseModel):
    """A semantic fact from the knowledge graph."""
    content: str = Field(..., description="The factual statement")
    source: Optional[str] = Field(None, description="Provenance link")
    confidence: float = Field(1.0, ge=0, le=1, description="Confidence score")
    timestamp: Optional[datetime] = Field(None, description="When fact was learned")


class Entity(BaseModel):
    """An entity extracted from content."""
    name: str = Field(..., description="Entity name")
    entity_type: str = Field(..., description="Type: person, org, concept, etc.")
    properties: dict = Field(default_factory=dict, description="Entity properties")


class GraphNode(BaseModel):
    """A node in the knowledge graph."""
    id: str = Field(..., description="Node identifier")
    label: str = Field(..., description="Node label/name")
    properties: dict = Field(default_factory=dict, description="Node properties")
    relationships: list[str] = Field(
        default_factory=list, 
        description="Connected node IDs"
    )


class SemanticContext(BaseModel):
    """
    Layer 3: Knowledge Graph Context
    
    Retrieved knowledge relevant to the current interaction.
    Populated by Tri-Search™ from episodic and semantic memory.
    
    NIST AI RMF Controls:
    - MANAGE 2.3: Facts include provenance for governance
    - MEASURE 2.1: Relevance scores measure retrieval quality
    - MAP 1.3: Entities map to domain concepts
    """
    facts: list[Fact] = Field(default_factory=list, description="Relevant facts")
    entities: list[Entity] = Field(default_factory=list, description="Extracted entities")
    graph_nodes: list[GraphNode] = Field(
        default_factory=list, 
        description="Knowledge graph context"
    )
    relevance_scores: dict = Field(
        default_factory=dict, 
        description="Search result rankings"
    )


# =============================================================================
# LAYER 4: OPERATIONAL CONTEXT
# NIST AI RMF: GOVERN 1.5 (Resource Management), MEASURE 2.7 (Performance)
# =============================================================================

class ToolCall(BaseModel):
    """A record of a tool/function invocation."""
    tool_name: str = Field(..., description="Name of the tool")
    arguments: dict = Field(default_factory=dict, description="Tool arguments")
    result: Optional[str] = Field(None, description="Tool output")
    duration_ms: Optional[int] = Field(None, description="Execution time")


class OperationalContext(BaseModel):
    """
    Layer 4: Runtime Operational Context
    
    Tracks execution state and enforces operational constraints.
    Enables cost control, performance budgets, and audit trails.
    
    NIST AI RMF Controls:
    - GOVERN 1.5: Resource budgets enforce limits
    - MEASURE 2.7: Latency tracking enables SLA monitoring
    - MANAGE 4.2: Tool calls provide audit trail
    """
    current_agent: str = Field("", description="Active agent identifier")
    tool_calls: list[ToolCall] = Field(
        default_factory=list, 
        description="Function invocation history"
    )
    latency_budget_ms: int = Field(30000, description="Max response time (ms)")
    cost_budget_tokens: int = Field(100000, description="Max token usage")
    request_id: str = Field("", description="Unique request identifier for tracing")


# =============================================================================
# ENTERPRISE CONTEXT (COMPLETE)
# =============================================================================

class EnterpriseContext(BaseModel):
    """
    Complete 4-Layer Enterprise Context
    
    This is the primary data structure that flows through every
    component of openContextGraph. It carries:
    - WHO is making the request (Layer 1)
    - WHAT happened before (Layer 2)
    - WHAT the system knows (Layer 3)
    - WHAT the constraints are (Layer 4)
    
    NIST AI RMF: Complete lifecycle governance
    """
    security: SecurityContext
    episodic: EpisodicContext = Field(default_factory=EpisodicContext)
    semantic: SemanticContext = Field(default_factory=SemanticContext)
    operational: OperationalContext = Field(default_factory=OperationalContext)
    
    @classmethod
    def create(cls, user_id: str, tenant_id: str = "default") -> "EnterpriseContext":
        """
        Factory method for creating a new context.
        
        Usage:
            context = EnterpriseContext.create(
                user_id="sarah.chen@contoso.com",
                tenant_id="contoso-corp"
            )
        """
        return cls(
            security=SecurityContext(user_id=user_id, tenant_id=tenant_id)
        )
    
    def with_episodic(self, conversation_id: str, channel: str = "chat") -> "EnterpriseContext":
        """Add episodic context to the current context."""
        self.episodic.conversation_id = conversation_id
        self.episodic.channel = channel
        return self
    
    def with_semantic(self, facts: list[Fact]) -> "EnterpriseContext":
        """Add semantic facts to the current context."""
        self.semantic.facts = facts
        return self
```

---

## Usage Example

```python
# Creating and using EnterpriseContext

# 1. Create from authenticated user
context = EnterpriseContext.create(
    user_id="sarah.chen@contoso.com",
    tenant_id="contoso-corp"
)

# 2. Add conversation context
context.episodic.conversation_id = "sess-12345"
context.episodic.recent_messages.append(
    Message(role="user", content="What's the status of Project Delta?")
)

# 3. Enrich with memory (populated by Tri-Search)
context.semantic.facts = [
    Fact(
        content="Project Delta is on track for Q2 delivery",
        source="doc-pm-report-2026-01",
        confidence=0.95
    )
]

# 4. Track operational state
context.operational.current_agent = "marcus"
context.operational.request_id = "req-abc123"

# 5. Pass to agent
response = await agent.process(context)
```

---

## NIST AI RMF Alignment

| Layer | NIST Function | Control | Implementation |
|-------|--------------|---------|----------------|
| **Security** | GOVERN | 1.2 (Accountability) | `user_id` attribution |
| **Security** | MAP | 1.5 (Boundaries) | `tenant_id` isolation |
| **Security** | MANAGE | 1.3 (Access Control) | `roles`, `scopes` |
| **Episodic** | MAP | 1.1 (System Context) | `conversation_id`, `messages` |
| **Episodic** | MANAGE | 4.3 (Documentation) | Conversation history |
| **Semantic** | MANAGE | 2.3 (Data Governance) | `source` provenance |
| **Semantic** | MEASURE | 2.1 (Quality) | `confidence`, `relevance_scores` |
| **Operational** | GOVERN | 1.5 (Resources) | `latency_budget`, `cost_budget` |
| **Operational** | MEASURE | 2.7 (Performance) | `duration_ms`, `request_id` |
| **Operational** | MANAGE | 4.2 (Audit) | `tool_calls` history |

---

## Summary

The 4-Layer Enterprise Context Schema provides:

- ✅ **Identity**: Every request attributed to a user and tenant
- ✅ **History**: Conversation context preserved and accessible
- ✅ **Knowledge**: Semantic facts with provenance
- ✅ **Constraints**: Operational budgets and audit trails
- ✅ **NIST AI RMF**: Complete lifecycle governance

*Document Version: 1.0 | Created: 2026-01-11*
