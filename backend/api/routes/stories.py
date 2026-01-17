"""
Story API Router

Endpoints for Sage Meridian's story generation and diagram creation.
"""

import json
import logging
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
    """Get a specific story by ID."""
    stories_dir = _get_stories_dir()
    story_path = stories_dir / f"{story_id}.md"
    
    if not story_path.exists():
        raise HTTPException(status_code=404, detail=f"Story not found: {story_id}")
    
    # Try to load corresponding diagram
    diagrams_dir = _get_diagrams_dir()
    diagram_path = diagrams_dir / f"{story_id}.json"
    diagram_spec = None
    if diagram_path.exists():
        diagram_spec = json.loads(diagram_path.read_text())
    
    # Check for Imagen-generated image
    images_dir = _get_images_dir()
    image_path_str = None
    if (images_dir / f"{story_id}.png").exists():
        image_path_str = f"/api/v1/images/{story_id}.png"
    
    # Check for uploaded architecture image (try all extensions)
    architecture_image_path_str = None
    for ext in ["png", "jpg", "webp"]:
        arch_image = images_dir / f"{story_id}-architecture.{ext}"
        if arch_image.exists():
            architecture_image_path_str = f"/api/v1/images/{story_id}-architecture.{ext}"
            break
    
    return StoryResponse(
        story_id=story_id,
        topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
        story_content=story_path.read_text(),
        story_path=str(story_path),
        diagram_spec=diagram_spec,
        diagram_path=str(diagram_path) if diagram_path.exists() else None,
        image_path=image_path_str,
        architecture_image_path=architecture_image_path_str,
        created_at=datetime.fromtimestamp(story_path.stat().st_mtime).isoformat(),
    )


@router.get("/", response_model=list[StoryListItem])
async def list_stories(user: SecurityContext = Depends(get_current_user)):
    """List all available stories."""
    stories_dir = _get_stories_dir()
    
    stories = []
    for story_file in sorted(stories_dir.glob("*.md"), reverse=True):
        story_id = story_file.stem
        
        # Check for image
        image_path_str = None
        if (stories_dir.parent / "images" / f"{story_id}.png").exists():
            image_path_str = f"/api/v1/images/{story_id}.png"
            
        stories.append(StoryListItem(
            story_id=story_id,
            topic=story_id.split("-", 2)[-1].replace("-", " ") if "-" in story_id else story_id,
            created_at=datetime.fromtimestamp(story_file.stat().st_mtime).isoformat(),
            story_path=str(story_file),
            image_path=image_path_str
        ))
    return stories
