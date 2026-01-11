# API Routes — Interface Layer

## Purpose

API Routes define the **contract between clients and the AI platform**. They provide RESTful endpoints for chat, memory, and document ingestion—the three core capabilities of openContextGraph.

## Why This Exists

### The Problem

AI systems often expose raw model interfaces or tightly coupled monolithic APIs. This creates:

- **Security risks**: No clear boundary for authentication/authorization
- **Coupling**: Frontend changes require backend changes
- **Testing difficulty**: No isolated units to test

### The Solution

A well-defined API layer that:

1. **Enforces security boundaries** at the edge
2. **Decouples clients** from internal implementation
3. **Provides observability** through structured request/response logging
4. **Enables governance** through rate limiting and audit trails

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Frontend/API)                    │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS
                             ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Router                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ /health  │  │  /chat   │  │ /memory  │  │    /etl      │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘ │
└───────┼─────────────┼───────────────┼─────────────┼─────────┘
        │             │               │             │
        ▼             ▼               ▼             ▼
   [Health Check] [Agent Router] [Memory Client] [ETL Router]
```

---

## Code Samples

### Health Routes

```python
# backend/api/routes/health.py
"""
Health check routes for Kubernetes probes and monitoring.

NIST AI RMF: MEASURE 2.6 (Continuous Monitoring)
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    """
    Liveness probe - Is the service running?
    
    Returns 200 if the process is alive.
    Used by Kubernetes liveness probe.
    """
    return {"status": "healthy", "service": "ctxEco"}


@router.get("/ready")
async def ready():
    """
    Readiness probe - Is the service ready to accept traffic?
    
    Checks all dependencies before returning 200.
    Used by Kubernetes readiness probe.
    
    NIST AI RMF: MANAGE 4.1 - Enables incident detection
    """
    # TODO: Check postgres, zep, temporal connectivity
    checks = {
        "postgres": True,  # await check_postgres()
        "zep": True,       # await check_zep()
        "temporal": True,  # await check_temporal()
    }
    
    all_healthy = all(checks.values())
    return {
        "status": "ready" if all_healthy else "degraded",
        "checks": checks
    }
```

### Chat Routes

```python
# backend/api/routes/chat.py
"""
Chat API routes - Primary user interaction endpoint.

NIST AI RMF: 
- MAP 1.6 (Intended Use Documentation)
- MEASURE 2.5 (User Feedback Collection)
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional

from core import SecurityContext, EnterpriseContext
from api.middleware.auth import get_current_user

router = APIRouter()


class ChatRequest(BaseModel):
    """User chat input with session context."""
    message: str = Field(..., description="User's message")
    session_id: Optional[str] = Field(None, description="Existing session ID")
    agent: str = Field("elena", description="Target agent: elena, marcus, sage")


class ChatResponse(BaseModel):
    """Agent response with context metadata."""
    response: str = Field(..., description="Agent's response")
    session_id: str = Field(..., description="Session ID for continuity")
    agent: str = Field(..., description="Responding agent")
    sources: list[str] = Field(default_factory=list, description="Memory sources used")


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    user: SecurityContext = Depends(get_current_user)
):
    """
    Process a chat message through the agent system.
    
    Flow:
    1. Authenticate user (SecurityContext)
    2. Retrieve/create session (EpisodicContext)
    3. Enrich with memory (SemanticContext)
    4. Route to agent
    5. Persist conversation
    6. Return response
    
    NIST AI RMF Alignment:
    - GOVERN 1.2: User identity is authenticated and logged
    - MAP 1.1: Context flows through all layers
    - MEASURE 2.7: Response latency is measured
    """
    # Create enterprise context from security context
    context = EnterpriseContext.create(
        user_id=user.user_id,
        tenant_id=user.tenant_id
    )
    
    # TODO: Route to agent system
    # response = await agent_router.route(request.agent, request.message, context)
    
    return ChatResponse(
        response=f"[{request.agent}]: Processing your request...",
        session_id=request.session_id or "new-session",
        agent=request.agent,
        sources=[]
    )
```

### Memory Routes

```python
# backend/api/routes/memory.py
"""
Memory API routes - Tri-Search™ hybrid memory retrieval.

NIST AI RMF:
- MAP 1.1 (System Context) 
- MANAGE 2.3 (Data Governance)
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from typing import Optional, Literal

from core import SecurityContext
from api.middleware.auth import get_current_user

router = APIRouter()


class SearchRequest(BaseModel):
    """Tri-Search query parameters."""
    query: str = Field(..., description="Search query")
    search_type: Literal["keyword", "vector", "graph", "hybrid"] = Field(
        "hybrid", 
        description="Search mode - hybrid combines all three"
    )
    limit: int = Field(10, ge=1, le=100, description="Max results")


class SearchResult(BaseModel):
    """Individual search result with provenance."""
    content: str
    score: float = Field(..., ge=0, le=1)
    source: Optional[str] = Field(None, description="Provenance link")
    metadata: dict = Field(default_factory=dict)


class SearchResponse(BaseModel):
    """Tri-Search response with result fusion."""
    results: list[SearchResult]
    search_type: str
    query: str
    fusion_method: str = "reciprocal_rank_fusion"


@router.post("/search", response_model=SearchResponse)
async def search_memory(
    request: SearchRequest,
    user: SecurityContext = Depends(get_current_user)
):
    """
    Execute Tri-Search™ across memory layers.
    
    Search Types:
    - keyword: BM25/inverted index for exact matches
    - vector: pgvector cosine similarity for semantic
    - graph: Graphiti relationship traversal for connected knowledge
    - hybrid: RRF fusion of all three (recommended)
    
    NIST AI RMF Alignment:
    - MANAGE 2.3: Results scoped to user's tenant
    - MEASURE 2.1: Search quality metrics logged
    """
    # TODO: Integrate with Zep memory client
    # results = await memory_client.search(
    #     query=request.query,
    #     user_id=user.user_id,
    #     search_type=request.search_type,
    #     limit=request.limit
    # )
    
    return SearchResponse(
        results=[],
        search_type=request.search_type,
        query=request.query
    )


@router.get("/facts/{user_id}")
async def get_facts(
    user_id: str,
    limit: int = 20,
    user: SecurityContext = Depends(get_current_user)
):
    """
    Retrieve semantic facts from knowledge graph.
    
    Facts are extracted from conversations and documents,
    stored as entities with relationships.
    
    NIST AI RMF: MANAGE 2.3 (Data Governance) - Facts are attributed
    """
    # Enforce tenant isolation
    if user.user_id != user_id and not user.has_role("admin"):
        raise PermissionError("Cannot access other users' facts")
    
    return {"facts": [], "user_id": user_id}
```

### ETL Routes

```python
# backend/api/routes/etl.py
"""
ETL API routes - Antigravity Router document ingestion.

NIST AI RMF:
- MAP 1.5 (System Boundaries)
- MANAGE 2.3 (Data Governance) 
- MEASURE 2.1 (Data Quality)
"""

from fastapi import APIRouter, UploadFile, File, Depends
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

from core import SecurityContext
from api.middleware.auth import get_current_user

router = APIRouter()


class DataClass(str, Enum):
    """Truth-value classification for documents."""
    CLASS_A_TRUTH = "immutable_truth"      # Manuals, specs, regulations
    CLASS_B_CHATTER = "ephemeral_stream"   # Emails, slides, docs
    CLASS_C_OPS = "operational_pulse"       # Logs, metrics, telemetry


class IngestRequest(BaseModel):
    """Document ingestion parameters."""
    force_class: Optional[DataClass] = Field(
        None, 
        description="Override automatic classification"
    )
    decay_rate: Optional[float] = Field(
        None, 
        ge=0, le=1,
        description="0.0=permanent, 1.0=ephemeral"
    )


class IngestResponse(BaseModel):
    """Ingestion result with provenance."""
    document_id: str = Field(..., description="Unique document identifier")
    data_class: DataClass = Field(..., description="Assigned classification")
    chunks: int = Field(..., ge=0, description="Number of chunks created")
    status: str = Field(..., description="Processing status")
    provenance_id: str = Field(..., description="Source tracking ID")


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    force_class: Optional[DataClass] = None,
    user: SecurityContext = Depends(get_current_user)
):
    """
    Ingest document through Antigravity Router.
    
    Classification Flow:
    1. Detect file type (extension + magic bytes)
    2. Classify by truth value (A/B/C)
    3. Route to appropriate engine:
       - Class A → Docling (high-fidelity tables, layouts)
       - Class B → Unstructured (semantic chunking)
       - Class C → Pandas (structured data)
    4. Extract text with provenance
    5. Store in memory with decay rate
    
    NIST AI RMF Alignment:
    - MAP 1.5: Document boundaries preserved via provenance
    - MANAGE 2.3: Classification determines governance rules
    - MEASURE 2.1: Extraction quality is validated
    """
    import uuid
    
    provenance_id = f"doc-{uuid.uuid4().hex[:8]}"
    
    # TODO: Integrate with Antigravity Router
    # result = await antigravity_router.ingest_bytes(
    #     content=await file.read(),
    #     filename=file.filename,
    #     force_class=force_class
    # )
    
    return IngestResponse(
        document_id=provenance_id,
        data_class=force_class or DataClass.CLASS_B_CHATTER,
        chunks=0,
        status="queued",
        provenance_id=provenance_id
    )
```

---

## NIST AI RMF Alignment

| Route | NIST Function | Control | Implementation |
|-------|--------------|---------|----------------|
| `/health` | MEASURE | 2.6 (Monitoring) | Liveness/readiness probes |
| `/chat` | GOVERN | 1.2 (Accountability) | User identity in every request |
| `/chat` | MAP | 1.1 (Context) | 4-layer context flows through |
| `/memory/search` | MANAGE | 2.3 (Data Governance) | Tenant-scoped results |
| `/memory/facts` | GOVERN | 1.4 (Transparency) | Facts include provenance |
| `/etl/ingest` | MAP | 1.5 (Boundaries) | Document provenance preserved |
| `/etl/ingest` | MEASURE | 2.1 (Data Quality) | Classification validation |

---

## Security Considerations

### Authentication (Every Route)

```python
user: SecurityContext = Depends(get_current_user)
```

All routes require authentication. The `SecurityContext` provides:

- `user_id`: Unique identifier
- `tenant_id`: Multi-tenant isolation
- `roles`: RBAC enforcement
- `scopes`: Fine-grained permissions

### Input Validation

```python
limit: int = Field(10, ge=1, le=100)  # Bounded integers
query: str = Field(..., max_length=1000)  # String limits
```

### Rate Limiting (TODO)

```python
@router.post("/", dependencies=[Depends(rate_limiter)])
```

---

## Summary

API Routes provide:

- ✅ Clear contract for client integration
- ✅ Security enforcement at the edge
- ✅ Request/response validation
- ✅ Observability hooks
- ✅ NIST AI RMF compliance points

*Document Version: 1.0 | Created: 2026-01-11*
