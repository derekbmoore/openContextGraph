"""
OpenContextGraph - FastAPI Application

Main entry point for the backend API.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import health, chat, memory, etl

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    logger.info("🚀 OpenContextGraph starting...")
    yield
    logger.info("👋 OpenContextGraph shutting down...")


app = FastAPI(
    title="OpenContextGraph",
    description="Enterprise AI Context Orchestration Platform",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router, tags=["Health"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
app.include_router(etl.router, prefix="/api/v1/etl", tags=["ETL"])


@app.get("/")
async def root():
    return {
        "name": "OpenContextGraph",
        "version": "0.1.0",
        "status": "running"
    }
