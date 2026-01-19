from fastapi import APIRouter, Query
from typing import List, Optional, Literal
from pydantic import BaseModel

router = APIRouter()

class MetricCard(BaseModel):
    label: string
    value: string
    status: Literal['ok', 'warn', 'bad']
    note: Optional[string] = None

class AlertItem(BaseModel):
    id: string
    severity: Literal['P0', 'P1', 'P2', 'P3']
    title: string
    detail: string
    time_label: string
    status: Literal['open', 'closed']

class Narrative(BaseModel):
    elena: string
    marcus: string

class ChangeItem(BaseModel):
    label: string
    value: string

class EvidenceTelemetrySnapshot(BaseModel):
    range_label: string
    reliability: List[MetricCard]
    ingestion: List[MetricCard]
    memory_quality: List[MetricCard]
    alerts: List[AlertItem]
    narrative: Narrative
    changes: List[ChangeItem]

@router.get("/evidence", response_model=EvidenceTelemetrySnapshot)
async def get_evidence_telemetry(range: str = Query("15m")):
    """
    Get operational telemetry snapshot for the Evidence dashboard.
    Currently returns mock data.
    """
    return {
        "range_label": range,
        "reliability": [
            {"label": "System Uptime", "value": "99.99%", "status": "ok"},
            {"label": "API Latency (p95)", "value": "142ms", "status": "ok", "note": "-12ms vs last week"},
            {"label": "Error Rate", "value": "0.02%", "status": "ok"}
        ],
        "ingestion": [
            {"label": "Docs Processed", "value": "1,240", "status": "ok"},
            {"label": "Vector Lag", "value": "3s", "status": "warn", "note": "Spike detected in queue"},
            {"label": "Failed Jobs", "value": "0", "status": "ok"}
        ],
        "memory_quality": [
            {"label": "Graph Nodes", "value": "84,392", "status": "ok"},
            {"label": "Ambiguity Score", "value": "Low", "status": "ok"},
            {"label": "Context Density", "value": "High", "status": "ok"}
        ],
        "alerts": [
            {
                "id": "alt-102",
                "severity": "P2",
                "title": "Ingestion Queue Backlog",
                "detail": "Vector processing lag increased > 5s",
                "time_label": "10m ago",
                "status": "open"
            }
        ],
        "narrative": {
            "elena": "System performance is nominal. I've noted a slight increase in vectorization latency, but it remains within acceptable parameters. No critical anomalies detected.",
            "marcus": "Operations are smooth. All safety guardrails are active. I'm monitoring the ingestion queue for that minor lag spike, but otherwise we're green across the board."
        },
        "changes": [
            {"label": "Deployed", "value": "v2.4.0-rc1"},
            {"label": "Config", "value": "Updated RAG thresholds"}
        ]
    }
