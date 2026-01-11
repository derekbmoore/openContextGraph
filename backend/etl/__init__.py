"""
ETL Package - openContextGraph

Provides document ingestion services:
- AntigravityRouter: Truth-value based document classification
- Class A/B/C extraction engines
"""

from etl.antigravity_router import (
    AntigravityRouter,
    DataClass,
    get_antigravity_router,
)

__all__ = [
    "AntigravityRouter",
    "DataClass",
    "get_antigravity_router",
]
