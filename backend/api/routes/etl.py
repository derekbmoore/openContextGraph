"""ETL API routes - Antigravity Router"""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional
from enum import Enum

router = APIRouter()


class DataClass(str, Enum):
    CLASS_A_TRUTH = "immutable_truth"
    CLASS_B_CHATTER = "ephemeral_stream"
    CLASS_C_OPS = "operational_pulse"


class IngestResponse(BaseModel):
    document_id: str
    data_class: DataClass
    chunks: int
    status: str


@router.post("/ingest", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    force_class: Optional[DataClass] = None,
):
    # TODO: Integrate with Antigravity Router
    return IngestResponse(
        document_id="doc-placeholder",
        data_class=force_class or DataClass.CLASS_B_CHATTER,
        chunks=0,
        status="pending",
    )


@router.get("/status/{document_id}")
async def get_ingestion_status(document_id: str):
    return {"document_id": document_id, "status": "unknown"}
