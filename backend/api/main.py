"""
OpenContextGraph - FastAPI Application

Main entry point for the backend API.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse

from core import get_settings
from .routes import health, chat, memory, etl, stories, voice, images
from .middleware.cors_preflight import CORSPreflightMiddleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler"""
    settings = get_settings()
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    yield
    logger.info("👋 openContextGraph shutting down...")


def create_app() -> FastAPI:
    """Application factory"""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Context Ecology Platform - Enterprise AI Context Orchestration",
        version=settings.app_version,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )

    # CORS middleware (handles preflight OPTIONS requests automatically)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers to ensure CORS headers are added to error responses
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Ensure CORS headers are added to HTTPException responses"""
        origin = request.headers.get("origin")
        allowed_origins = settings.cors_origins
        is_allowed = origin and (origin in allowed_origins or "*" in allowed_origins)
        
        headers = dict(exc.headers) if exc.headers else {}
        
        # Add CORS headers
        if is_allowed and origin:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"
        elif "*" in allowed_origins:
            headers["Access-Control-Allow-Origin"] = "*"
        
        headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        headers["Access-Control-Allow-Headers"] = "authorization, content-type"
        
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=headers,
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Ensure CORS headers are added to validation error responses"""
        origin = request.headers.get("origin")
        allowed_origins = settings.cors_origins
        is_allowed = origin and (origin in allowed_origins or "*" in allowed_origins)
        
        headers = {}
        
        # Add CORS headers
        if is_allowed and origin:
            headers["Access-Control-Allow-Origin"] = origin
            headers["Access-Control-Allow-Credentials"] = "true"
        elif "*" in allowed_origins:
            headers["Access-Control-Allow-Origin"] = "*"
        
        headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
        headers["Access-Control-Allow-Headers"] = "authorization, content-type"
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors()},
            headers=headers,
        )

    # Custom middleware
    # NOTE: Middleware runs in REVERSE order from how they're added.
    app.add_middleware(CORSPreflightMiddleware)

    # Routes
    app.include_router(health.router, tags=["Health"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
    app.include_router(memory.router, prefix="/api/v1/memory", tags=["Memory"])
    app.include_router(etl.router, prefix="/api/v1/etl", tags=["ETL"])
    app.include_router(stories.router, prefix="/api/v1/story", tags=["Story"])
    app.include_router(voice.router, prefix="/api/v1/voice", tags=["Voice"])
    app.include_router(images.router, prefix="/api/v1/images", tags=["Images"])

    @app.get("/")
    async def root():
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "status": "running"
        }

    return app


app = create_app()
