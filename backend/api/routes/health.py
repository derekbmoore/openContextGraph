"""Health check routes"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "healthy", "service": "ctxgraph"}


@router.get("/ready")
async def ready():
    # TODO: Check dependencies (postgres, zep, temporal)
    return {"status": "ready"}
