"""
Images API Router

Serves images from docs/images directory or Azure Blob Storage.
"""

from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import logging
import io

from core import get_settings

router = APIRouter()
logger = logging.getLogger(__name__)


async def _get_image_from_blob(filename: str) -> bytes | None:
    """
    Try to fetch image from Azure Blob Storage.
    Returns None if blob storage is not configured or image not found.
    """
    settings = get_settings()
    
    if not settings.azure_storage_connection_string:
        return None
    
    try:
        from azure.storage.blob.aio import BlobServiceClient
        
        blob_service = BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
        container_name = settings.azure_storage_images_container or "images"
        
        async with blob_service:
            container_client = blob_service.get_container_client(container_name)
            blob_client = container_client.get_blob_client(filename)
            
            if await blob_client.exists():
                download = await blob_client.download_blob()
                return await download.readall()
                
    except ImportError:
        logger.warning("azure-storage-blob not installed, skipping blob storage")
    except Exception as e:
        logger.warning(f"Failed to fetch image from blob storage: {e}")
    
    return None


@router.get("/{filename}")
async def get_image(filename: str):
    """
    Serve an image from the docs/images directory or Azure Blob Storage.
    
    Priority:
    1. Local filesystem (docs/images/)
    2. Azure Blob Storage (if configured)
    """
    # Sanitize filename (basic check)
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
    
    settings = get_settings()
    docs_path = Path(settings.onedrive_docs_path or "docs")
    images_dir = docs_path / "images"
    file_path = images_dir / filename
    
    # Try local filesystem first
    if file_path.exists():
        logger.debug(f"Serving image from filesystem: {file_path}")
        return FileResponse(file_path)
    
    # Try Azure Blob Storage
    blob_data = await _get_image_from_blob(filename)
    if blob_data:
        logger.debug(f"Serving image from blob storage: {filename}")
        # Determine content type from extension
        content_type = "image/png"
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            content_type = "image/jpeg"
        elif filename.endswith(".webp"):
            content_type = "image/webp"
        elif filename.endswith(".gif"):
            content_type = "image/gif"
        
        return StreamingResponse(
            io.BytesIO(blob_data),
            media_type=content_type,
            headers={"Cache-Control": "public, max-age=86400"}  # Cache for 24 hours
        )
    
    # Not found anywhere
    logger.warning(f"Image not found: {filename}")
    raise HTTPException(status_code=404, detail="Image not found")
