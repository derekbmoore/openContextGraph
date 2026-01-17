"""
Story API Router

Endpoints for Sage Meridian's story generation and diagram creation.
Supports both local filesystem and Azure Blob Storage for persistence.
"""

import json
import logging
import io
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel

from api.middleware.auth import get_current_user
from core import SecurityContext, get_settings

logger = logging.getLogger(__name__)

router = APIRouter(tags=["story"])


# =============================================================================
# Azure Blob Storage Helpers
# =============================================================================


async def _get_blob_service():
    """Get Azure Blob Service client if configured."""
    settings = get_settings()
    if not settings.azure_storage_connection_string:
        return None
    try:
        from azure.storage.blob.aio import BlobServiceClient
        return BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
    except ImportError:
        logger.warning("azure-storage-blob not installed")
        return None
    except Exception as e:
        logger.warning(f"Failed to create blob service client: {e}")
        return None


async def _list_stories_from_blob() -> list[dict]:
    """List stories from Azure Blob Storage."""
    settings = get_settings()
    blob_service = await _get_blob_service()
    if not blob_service:
        return []
    
    stories = []
    try:
        async with blob_service:
            container_name = settings.azure_storage_stories_container or "stories"
            container_client = blob_service.get_container_client(container_name)
            
            async for blob in container_client.list_blobs():
                if blob.name.endswith(".md"):
                    story_id = blob.name.replace(".md", "")
                    stories.append({
                        "story_id": story_id,
                        "name": blob.name,
                        "last_modified": blob.last_modified,
                        "source": "blob"
                    })
    except Exception as e:
        logger.warning(f"Failed to list stories from blob: {e}")
    
    return stories


async def _get_story_from_blob(story_id: str) -> Optional[str]:
    """Get story content from Azure Blob Storage."""
    settings = get_settings()
    blob_service = await _get_blob_service()
    if not blob_service:
        return None
    
    try:
        async with blob_service:
            container_name = settings.azure_storage_stories_container or "stories"
            container_client = blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(f"{story_id}.md")
            
            if await blob_client.exists():
                download = await blob_client.download_blob()
                content = await download.readall()
                return content.decode("utf-8")
    except Exception as e:
        logger.warning(f"Failed to get story from blob: {e}")
    
    return None


async def _save_story_to_blob(story_id: str, content: str) -> bool:
    """Save story content to Azure Blob Storage."""
    settings = get_settings()
    blob_service = await _get_blob_service()
    if not blob_service:
        return False
    
    try:
        async with blob_service:
            container_name = settings.azure_storage_stories_container or "stories"
            container_client = blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(f"{story_id}.md")
            
            await blob_client.upload_blob(content.encode("utf-8"), overwrite=True)
            return True
    except Exception as e:
        logger.error(f"Failed to save story to blob: {e}")
    
    return False


async def _save_image_to_blob(filename: str, content: bytes) -> bool:
    """Save image to Azure Blob Storage."""
    settings = get_settings()
    blob_service = await _get_blob_service()
    if not blob_service:
        return False
    
    try:
        async with blob_service:
            container_name = settings.azure_storage_images_container or "images"
            container_client = blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(filename)
            
            await blob_client.upload_blob(content, overwrite=True)
            return True
    except Exception as e:
        logger.error(f"Failed to save image to blob: {e}")
    
    return False


async def _check_image_in_blob(filename: str) -> bool:
    """Check if image exists in Azure Blob Storage."""
    settings = get_settings()
    blob_service = await _get_blob_service()
    if not blob_service:
        return False
    
    try:
        async with blob_service:
            container_name = settings.azure_storage_images_container or "images"
            container_client = blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(filename)
            return await blob_client.exists()
    except Exception as e:
        logger.warning(f"Failed to check image in blob: {e}")
    
    return False


# =============================================================================
# Request/Response Models
# =============================================================================


class StoryCreateRequest(BaseModel):
    """Request to create a new story."""
    topic: str
    context: Optional[str] = None
    include_diagram: bool = True
    diagram_type: str = "architecture"


class StoryResponse(BaseModel):
    """Response containing story and optional diagram."""
    story_id: str
    topic: str
    story_content: str
    story_path: Optional[str] = None
    diagram_spec: Optional[dict] = None
    diagram_path: Optional[str] = None
    image_path: Optional[str] = None
    architecture_image_path: Optional[str] = None
    created_at: str


class StoryListItem(BaseModel):
    """Summary of a story for listing."""
    story_id: str
    topic: str
    created_at: str
    story_path: str
    image_path: Optional[str] = None


class VisualGenerateRequest(BaseModel):
    """Request to generate a visual for an existing story."""
    prompt: Optional[str] = None
    context: Optional[str] = None


# =============================================================================
# Helper Functions
# =============================================================================


def _get_stories_dir() -> Path:
    """Get the stories directory path."""
    settings = get_settings()
    docs_path = Path(settings.onedrive_docs_path or "docs")
    stories_dir = docs_path / "stories"
    try:
        stories_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create stories directory: {e}")
    return stories_dir


def _get_diagrams_dir() -> Path:
    """Get the diagrams directory path."""
    settings = get_settings()
    docs_path = Path(settings.onedrive_docs_path or "docs")
    diagrams_dir = docs_path / "diagrams"
    try:
        diagrams_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create diagrams directory: {e}")
    return diagrams_dir


def _get_images_dir() -> Path:
    """Get the images directory path."""
    settings = get_settings()
    docs_path = Path(settings.onedrive_docs_path or "docs")
    images_dir = docs_path / "images"
    try:
        images_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create images directory: {e}")
    return images_dir


# =============================================================================
# Endpoints
# =============================================================================


@router.post("/create", response_model=StoryResponse)
async def create_story(
    request: StoryCreateRequest,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Create a new story and optional diagram via Temporal workflow.
    
    Uses durable execution for the multi-step process:
    1. Generate story with Claude
    2. Generate diagram spec with Gemini
    3. Save artifacts to docs folder (OneDrive sync)
    4. Enrich Zep memory
    
    The workflow survives crashes and can be monitored.
    """
    try:
        from workflows.client import execute_story
        
        logger.info(f"Creating story via Temporal: {request.topic}")
        
        # Execute via Temporal workflow for durability
        result = await execute_story(
            user_id=user.user_id,
            tenant_id=user.tenant_id,
            topic=request.topic,
            context=request.context,
            include_diagram=request.include_diagram,
            include_image=True, # Always include image for now, or add to request model
            diagram_type=request.diagram_type,
        )
        
        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)
        
        return StoryResponse(
            story_id=result.story_id,
            topic=result.topic,
            story_content=result.story_content,
            story_path=result.story_path,
            diagram_spec=result.diagram_spec,
            diagram_path=result.diagram_path,
            image_path=f"/api/v1/images/{result.story_id}.png" if (await _check_image_exists(result.story_id)) else None,
            created_at=datetime.now().isoformat(),
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating story: {e}")
        # Fallback to direct execution if Temporal unavailable
        logger.warning("Falling back to direct execution (Temporal may be unavailable)")
        return await _create_story_direct(request, user)


async def _check_image_exists(story_id: str) -> bool:
    """Check if an image exists for the story."""
    settings = get_settings()
    docs_path = Path(settings.onedrive_docs_path or "docs")
    image_path = docs_path / "images" / f"{story_id}.png"
    return image_path.exists()


async def _create_story_direct(request: StoryCreateRequest, user: SecurityContext) -> StoryResponse:
    """
    Direct story creation (fallback when Temporal is unavailable).
    """
    # Note: This requires LLM clients - adjust imports based on actual implementation
    # For now, this is a placeholder that will fail gracefully
    raise HTTPException(status_code=503, detail="Direct story creation not yet implemented. Temporal workflow required.")


@router.get("/latest", response_model=StoryResponse)
async def get_latest_story(user: SecurityContext = Depends(get_current_user)):
    """Get the most recently created story."""
    stories_dir = _get_stories_dir()
    
    story_files = sorted(stories_dir.glob("*.md"), reverse=True)
    if not story_files:
        raise HTTPException(status_code=404, detail="No stories found")
    
    latest = story_files[0]
    story_id = latest.stem
    
    # Try to load corresponding diagram
    diagrams_dir = _get_diagrams_dir()
    diagram_path = diagrams_dir / f"{story_id}.json"
    diagram_spec = None
    if diagram_path.exists():
        diagram_spec = json.loads(diagram_path.read_text())
    
    # Check for image
    image_path_str = None
    if (stories_dir.parent / "images" / f"{story_id}.png").exists():
        image_path_str = f"/api/v1/images/{story_id}.png"
    
    return StoryResponse(
        story_id=story_id,
        topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
        story_content=latest.read_text(),
        story_path=str(latest),
        diagram_spec=diagram_spec,
        diagram_path=str(diagram_path) if diagram_path.exists() else None,
        image_path=image_path_str,
        created_at=datetime.fromtimestamp(latest.stat().st_mtime).isoformat(),
    )


@router.post("/{story_id}/visual", response_model=StoryResponse)
async def generate_story_visual(
    story_id: str,
    request: VisualGenerateRequest,
    user: SecurityContext = Depends(get_current_user),
):
    """
    Generate (or regenerate) a visual for an existing story.
    Useful for repairs or adding visuals to text-only stories.
    """
    stories_dir = _get_stories_dir()
    story_path = stories_dir / f"{story_id}.md"
    
    if not story_path.exists():
        raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
        
    # Note: This requires LLM clients - adjust imports based on actual implementation
    raise HTTPException(status_code=503, detail="Visual generation not yet implemented")


@router.post("/{story_id}/architecture-image", response_model=StoryResponse)
async def upload_architecture_image(
    story_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: SecurityContext = Depends(get_current_user),
):
    """
    Upload a high-quality architecture diagram image for a story.
    
    The image is:
    1. Validated (PNG, JPG, WebP only)
    2. Saved to docs/images/{story_id}-architecture.{ext}
    3. Processed with Unstructured for OCR/text extraction
    4. Extracted text enriched to Zep memory for searchability
    """
    stories_dir = _get_stories_dir()
    story_path = stories_dir / f"{story_id}.md"
    
    if not story_path.exists():
        raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
    
    # Validate file type
    allowed_types = {"image/png", "image/jpeg", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type: {file.content_type}. Allowed: PNG, JPG, WebP"
        )
    
    # Determine extension from content type
    ext_map = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp"}
    ext = ext_map.get(file.content_type, "png")
    
    try:
        # Read file content
        content = await file.read()
        
        # Save architecture image
        images_dir = _get_images_dir()
        arch_image_filename = f"{story_id}-architecture.{ext}"
        arch_image_path = images_dir / arch_image_filename
        arch_image_path.write_bytes(content)
        
        logger.info(f"Saved architecture image: {arch_image_path}")
        
        # Note: OCR processing would go here if ETL processor is available
        # For now, just save the image
        
        # Return updated story
        return await get_story(story_id, user)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Architecture image upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(story_id: str, user: SecurityContext = Depends(get_current_user)):
    """Get a specific story by ID from filesystem or blob storage."""
    stories_dir = _get_stories_dir()
    story_path = stories_dir / f"{story_id}.md"
    
    story_content = None
    created_at = None
    story_path_str = None
    
    # Try local filesystem first
    if story_path.exists():
        story_content = story_path.read_text()
        created_at = datetime.fromtimestamp(story_path.stat().st_mtime).isoformat()
        story_path_str = str(story_path)
    else:
        # Try blob storage
        story_content = await _get_story_from_blob(story_id)
        if story_content:
            created_at = datetime.now().isoformat()  # Blob doesn't give us easy access to modified time here
            story_path_str = f"blob://{story_id}.md"
    
    if not story_content:
        raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
    
    # Try to load corresponding diagram (local only for now)
    diagrams_dir = _get_diagrams_dir()
    diagram_path = diagrams_dir / f"{story_id}.json"
    diagram_spec = None
    if diagram_path.exists():
        diagram_spec = json.loads(diagram_path.read_text())
    
    # Check for Imagen-generated image (local first, then blob)
    images_dir = _get_images_dir()
    image_path_str = None
    if (images_dir / f"{story_id}.png").exists():
        image_path_str = f"/api/v1/images/{story_id}.png"
    elif await _check_image_in_blob(f"{story_id}.png"):
        image_path_str = f"/api/v1/images/{story_id}.png"
    
    # Check for uploaded architecture image (try all extensions, local first then blob)
    architecture_image_path_str = None
    for ext in ["png", "jpg", "webp"]:
        arch_image = images_dir / f"{story_id}-architecture.{ext}"
        if arch_image.exists():
            architecture_image_path_str = f"/api/v1/images/{story_id}-architecture.{ext}"
            break
        elif await _check_image_in_blob(f"{story_id}-architecture.{ext}"):
            architecture_image_path_str = f"/api/v1/images/{story_id}-architecture.{ext}"
            break
    
    return StoryResponse(
        story_id=story_id,
        topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
        story_content=story_content,
        story_path=story_path_str,
        diagram_spec=diagram_spec,
        diagram_path=str(diagram_path) if diagram_path.exists() else None,
        image_path=image_path_str,
        architecture_image_path=architecture_image_path_str,
        created_at=created_at,
    )


@router.get("/", response_model=list[StoryListItem])
async def list_stories(user: SecurityContext = Depends(get_current_user)):
    """List all available stories from filesystem and blob storage."""
    stories_dir = _get_stories_dir()
    
    stories = []
    seen_ids = set()
    
    # First, get stories from local filesystem
    for story_file in sorted(stories_dir.glob("*.md"), reverse=True):
        story_id = story_file.stem
        seen_ids.add(story_id)
        
        # Check for image (local first, then blob)
        image_path_str = None
        if (stories_dir.parent / "images" / f"{story_id}.png").exists():
            image_path_str = f"/api/v1/images/{story_id}.png"
        elif await _check_image_in_blob(f"{story_id}.png"):
            image_path_str = f"/api/v1/images/{story_id}.png"
            
        stories.append(StoryListItem(
            story_id=story_id,
            topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
            created_at=datetime.fromtimestamp(story_file.stat().st_mtime).isoformat(),
            story_path=str(story_file),
            image_path=image_path_str
        ))
    
    # Then, get stories from blob storage (if not already in local)
    blob_stories = await _list_stories_from_blob()
    for blob_story in blob_stories:
        story_id = blob_story["story_id"]
        if story_id in seen_ids:
            continue
        
        # Check for image in blob
        image_path_str = None
        if await _check_image_in_blob(f"{story_id}.png"):
            image_path_str = f"/api/v1/images/{story_id}.png"
        
        stories.append(StoryListItem(
            story_id=story_id,
            topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
            created_at=blob_story["last_modified"].isoformat() if blob_story.get("last_modified") else datetime.now().isoformat(),
            story_path=f"blob://{story_id}.md",
            image_path=image_path_str
        ))
    
    # Sort by created_at descending
    stories.sort(key=lambda x: x.created_at, reverse=True)
    return stories
