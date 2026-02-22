"""
ETL API Routes - Antigravity Ingestion

Provides endpoints for:
- Document ingestion with truth-value classification
- Ingestion status tracking
- Data class inspection

OpenContextGraph - API Layer
NIST AI RMF: MAP 1.5 (Boundaries), MANAGE 2.3 (Governance)
"""

import logging
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from api.middleware.auth import get_current_user, require_scopes
from core.context import SecurityContext
from etl import get_antigravity_router, DataClass
from memory import get_memory_client

logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory job tracking (replace with Redis/DB in production)
_ingestion_jobs: dict[str, dict] = {}


class IngestResponse(BaseModel):
    """Document ingestion result."""
    document_id: str = Field(..., description="Unique document identifier")
    data_class: str = Field(..., description="Classification (immutable_truth, ephemeral_stream, operational_pulse)")
    chunks: int = Field(..., description="Number of chunks extracted")
    status: str = Field(..., description="Processing status")


class JobStatus(BaseModel):
    """Ingestion job status."""
    document_id: str
    status: str
    data_class: Optional[str] = None
    chunks: Optional[int] = None
    error: Optional[str] = None


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    force_class: Optional[DataClass] = None,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Ingest a document through the Antigravity Router.
    
    Classification System:
    - **Class A (immutable_truth)**: Technical docs, manuals, standards
      → High-fidelity extraction (Docling)
    - **Class B (ephemeral_stream)**: Emails, slides, chats
      → Semantic chunking (Unstructured)  
    - **Class C (operational_pulse)**: CSV, JSON, logs
      → Structured handling (Pandas)
    
    NIST AI RMF Controls:
    - MAP 1.5: Provenance ID assigned to all chunks
    - MANAGE 2.3: Classification determines retention rules
    
    Args:
        file: Document to ingest
        force_class: Override automatic classification
        user: Authenticated user from token
    
    Returns:
        Ingestion result with document ID and chunk count
    """
    document_id = f"doc-{uuid.uuid4().hex[:12]}"
    
    try:
        # Read file content
        content = await file.read()
        filename = file.filename or "unnamed"
        
        logger.info(
            f"Ingesting document: {filename} ({len(content)} bytes) "
            f"for user {user.user_id}"
        )
        
        # Process through Antigravity Router
        antigravity = get_antigravity_router()
        chunks = await antigravity.ingest_bytes(
            content=content,
            filename=filename,
            force_class=force_class,
            user_id=user.user_id,
            tenant_id=user.tenant_id,
        )
        
        # Determine data class from chunks
        data_class = DataClass.CLASS_B_CHATTER  # Default
        if chunks:
            chunk_class = chunks[0].get("metadata", {}).get("data_class")
            if chunk_class:
                data_class = DataClass(chunk_class)
        
        # Store job status
        _ingestion_jobs[document_id] = {
            "status": "complete",
            "data_class": data_class.value,
            "chunks": len(chunks),
            "filename": filename,
            "user_id": user.user_id,
        }
        
        # TODO: Store chunks in vector database
        # await vector_store.store_chunks(document_id, chunks)

        # Standardized interaction memory write (ingestion milestone)
        try:
            memory_client = get_memory_client()
            ingest_session_id = f"ingest-{document_id}"
            await memory_client.get_or_create_session(
                session_id=ingest_session_id,
                user_id=user.user_id,
                metadata={
                    "tenant_id": user.tenant_id,
                    "type": "milestone",
                    "channel": "ingestion",
                    "title": f"Ingested {filename}",
                    "summary": f"{filename} classified as {data_class.value} with {len(chunks)} chunks",
                    "document_id": document_id,
                },
            )
            await memory_client.add_memory(
                session_id=ingest_session_id,
                messages=[
                    {
                        "role": "assistant",
                        "content": (
                            f"Ingestion milestone: {filename} ({len(content)} bytes) "
                            f"was classified as {data_class.value} and produced {len(chunks)} chunks."
                        ),
                        "metadata": {
                            "agent_id": "ingestion-router",
                            "interaction_type": "ingestion_milestone",
                            "document_id": document_id,
                        },
                    }
                ],
                metadata={"source": "etl.ingest"},
            )
        except Exception as e:
            logger.warning(f"Failed to persist ingestion milestone memory: {e}")
        
        return IngestResponse(
            document_id=document_id,
            data_class=data_class.value,
            chunks=len(chunks),
            status="complete",
        )
        
    except Exception as e:
        logger.error(f"Ingestion failed for {file.filename}: {e}")
        
        _ingestion_jobs[document_id] = {
            "status": "error",
            "error": str(e),
        }
        
        raise HTTPException(
            status_code=500,
            detail=f"Ingestion failed: {str(e)}"
        )


@router.get("/status/{document_id}", response_model=JobStatus)
async def get_ingestion_status(
    document_id: str,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Get the status of a document ingestion job.
    
    Returns:
        Job status including chunk count if complete
    """
    job = _ingestion_jobs.get(document_id)
    
    if not job:
        return JobStatus(
            document_id=document_id,
            status="not_found",
        )
    
    # Verify user owns this document
    if job.get("user_id") != user.user_id and not user.has_role("admin"):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return JobStatus(
        document_id=document_id,
        status=job.get("status", "unknown"),
        data_class=job.get("data_class"),
        chunks=job.get("chunks"),
        error=job.get("error"),
    )


@router.get("/classify")
async def classify_file(
    filename: str,
):
    """
    Preview how a file would be classified.
    
    Useful for UI to show expected classification before upload.
    
    Args:
        filename: Filename to classify (extension used)
    
    Returns:
        Expected data class and reason
    """
    antigravity = get_antigravity_router()
    data_class, reason = antigravity.classify(filename)
    
    return {
        "filename": filename,
        "data_class": data_class.value,
        "reason": reason,
    }
