from fastapi import APIRouter, Body
from typing import List, Optional, Literal
from pydantic import BaseModel
import uuid
from datetime import datetime

router = APIRouter()

class GoldenRunSummary(BaseModel):
    run_id: str
    dataset_id: str
    status: Literal['PASS', 'FAIL', 'WARN', 'RUNNING']
    checks_total: int
    checks_passed: int
    started_at: str
    ended_at: Optional[str] = None
    duration_ms: Optional[int] = None
    trace_id: Optional[str] = None
    workflow_id: Optional[str] = None
    session_id: Optional[str] = None

class GoldenCheck(BaseModel):
    id: str
    name: str
    status: Literal['pending', 'running', 'pass', 'fail', 'warn']
    duration_ms: Optional[int] = None
    evidence_summary: Optional[str] = None

class Narrative(BaseModel):
    elena: string
    marcus: string

class GoldenRun(BaseModel):
    summary: GoldenRunSummary
    checks: List[GoldenCheck]
    narrative: Narrative

class GoldenDataset(BaseModel):
    id: str
    name: str
    filename: str
    hash: str
    size_label: str
    anchors: List[str]

class RunRequest(BaseModel):
    dataset_id: str
    mode: Literal['deterministic', 'acceptance'] = 'deterministic'

@router.get("/datasets", response_model=List[GoldenDataset])
async def list_golden_datasets():
    """List available Golden Thread datasets."""
    return [
        {
            "id": "cogai-thread",
            "name": "Cognitive Architecture Baseline",
            "filename": "cog_arch_v1.jsonl",
            "hash": "sha256:e3b0c442...",
            "size_label": "42KB",
            "anchors": ["Memory", "Inference", "Safety"]
        },
        {
            "id": "sample-policy",
            "name": "Enterprise Policy Set",
            "filename": "policies_2024.pdf",
            "hash": "sha256:a8f9d2...",
            "size_label": "1.2MB",
            "anchors": ["Compliance", "RAG"]
        }
    ]

@router.get("/runs/latest", response_model=Optional[GoldenRun])
async def get_latest_golden_run():
    """Get the most recent Golden Thread execution result."""
    # Return mock passed run
    return {
        "summary": {
            "run_id": "run-8f7d2a",
            "dataset_id": "cogai-thread",
            "status": "PASS",
            "checks_total": 5,
            "checks_passed": 5,
            "started_at": datetime.now().isoformat(),
            "ended_at": datetime.now().isoformat(),
            "duration_ms": 1240,
            "trace_id": "trc-" + str(uuid.uuid4())[:8],
            "workflow_id": "wf-" + str(uuid.uuid4())[:8],
            "session_id": "sess-" + str(uuid.uuid4())[:8]
        },
        "checks": [
            {"id": "CHK-01", "name": "Context Injection", "status": "pass", "duration_ms": 120, "evidence_summary": "Context injected successfully"},
            {"id": "CHK-02", "name": "Prompt Assembly", "status": "pass", "duration_ms": 45, "evidence_summary": "Template rendered with 0 errors"},
            {"id": "CHK-03", "name": "LLM Inference", "status": "pass", "duration_ms": 890, "evidence_summary": "Response generated"},
            {"id": "CHK-04", "name": "Safety Rails", "status": "pass", "duration_ms": 80, "evidence_summary": "No PII leak detected"},
            {"id": "CHK-05", "name": "Response Formatting", "status": "pass", "duration_ms": 105, "evidence_summary": "Valid JSON output"}
        ],
        "narrative": {
            "elena": "Golden thread execution successful. All cognitive subsystems responded within nominal latency bounds. Context fidelity confirmed at 99.8%.",
            "marcus": "Validation pass complete. No regression detected in safety protocols or memory recall. Proceed with deployment."
        }
    }

@router.post("/run", response_model=GoldenRun)
async def run_golden_thread(request: RunRequest = Body(...)):
    """Execute the Golden Thread suite."""
    # Mock immediate success for demo purposes
    return {
        "summary": {
            "run_id": "run-" + str(uuid.uuid4())[:6],
            "dataset_id": request.dataset_id,
            "status": "PASS",
            "checks_total": 5,
            "checks_passed": 5,
            "started_at": datetime.now().isoformat(),
            "ended_at": datetime.now().isoformat(),
            "duration_ms": 1500,
            "trace_id": "trc-" + str(uuid.uuid4())[:8],
            "workflow_id": "wf-" + str(uuid.uuid4())[:8],
            "session_id": "sess-" + str(uuid.uuid4())[:8]
        },
        "checks": [
            {"id": "CHK-01", "name": "Context Injection", "status": "pass", "duration_ms": 150, "evidence_summary": "Context injected successfully"},
            {"id": "CHK-02", "name": "Prompt Assembly", "status": "pass", "duration_ms": 50, "evidence_summary": "Template rendered with 0 errors"},
            {"id": "CHK-03", "name": "LLM Inference", "status": "pass", "duration_ms": 950, "evidence_summary": "Response generated"},
            {"id": "CHK-04", "name": "Safety Rails", "status": "pass", "duration_ms": 90, "evidence_summary": "No PII leak detected"},
            {"id": "CHK-05", "name": "Response Formatting", "status": "pass", "duration_ms": 110, "evidence_summary": "Valid JSON output"}
        ],
        "narrative": {
            "elena": "New validation run completed. Metrics indicate stable performance across all subsystems.",
            "marcus": "Confirmed. Safety checks passed. The system is ready for user traffic."
        }
    }

@router.get("/runs/{run_id}", response_model=GoldenRun)
async def get_golden_run(run_id: str):
    """Retrieve details for a specific run."""
    # Mock response
    return {
        "summary": {
            "run_id": run_id,
            "dataset_id": "cogai-thread",
            "status": "PASS",
            "checks_total": 5,
            "checks_passed": 5,
            "started_at": datetime.now().isoformat(),
            "ended_at": datetime.now().isoformat(),
            "duration_ms": 1240,
            "trace_id": "trc-mock",
            "workflow_id": "wf-mock",
            "session_id": "sess-mock"
        },
        "checks": [
            {"id": "CHK-01", "name": "Context Injection", "status": "pass", "duration_ms": 120, "evidence_summary": "Context injected successfully"},
            {"id": "CHK-02", "name": "Prompt Assembly", "status": "pass", "duration_ms": 45, "evidence_summary": "Template rendered with 0 errors"},
            {"id": "CHK-03", "name": "LLM Inference", "status": "pass", "duration_ms": 890, "evidence_summary": "Response generated"},
            {"id": "CHK-04", "name": "Safety Rails", "status": "pass", "duration_ms": 80, "evidence_summary": "No PII leak detected"},
            {"id": "CHK-05", "name": "Response Formatting", "status": "pass", "duration_ms": 105, "evidence_summary": "Valid JSON output"}
        ],
        "narrative": {
            "elena": "Run details retrieved. Integrity verified.",
            "marcus": "Archive log access successful."
        }
    }
