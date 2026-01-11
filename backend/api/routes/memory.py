"""Memory API routes - Tri-Search"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    user_id: Optional[str] = None
    search_type: str = "hybrid"  # "keyword", "vector", "graph", "hybrid"
    limit: int = 10


class SearchResult(BaseModel):
    content: str
    score: float
    source: Optional[str] = None
    metadata: dict = {}


class SearchResponse(BaseModel):
    results: list[SearchResult]
    search_type: str
    query: str


@router.post("/search", response_model=SearchResponse)
async def search_memory(request: SearchRequest):
    # TODO: Integrate with Zep memory client
    return SearchResponse(
        results=[],
        search_type=request.search_type,
        query=request.query,
    )


@router.get("/facts/{user_id}")
async def get_facts(user_id: str, limit: int = 20):
    # TODO: Get facts from knowledge graph
    return {"facts": [], "user_id": user_id}


@router.get("/sessions/{user_id}")
async def list_sessions(user_id: str, limit: int = 20, offset: int = 0):
    # TODO: List user sessions
    return {"sessions": [], "user_id": user_id}
