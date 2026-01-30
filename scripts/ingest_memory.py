#!/usr/bin/env python3
"""
Memory Ingestion Script for Context Ecology

This script ingests working memory documents and domain memory updates
into the Zep memory system for Tri-Search retrieval.

Usage:
    python ingest_memory.py <file_or_directory>
    python ingest_memory.py --working-memory   # Ingest all working-memory docs
    python ingest_memory.py --domain-memory    # Ingest domain memory
    python ingest_memory.py --all              # Ingest everything

OpenContextGraph - Context Ecology
"""

import argparse
import asyncio
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import httpx
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
# Production Azure endpoint (default)
ZEP_API_URL = os.getenv("ZEP_API_URL", "https://ctxeco-api.whitecliff-aa751815.eastus2.azurecontainerapps.io")
ZEP_API_KEY = os.getenv("ZEP_API_KEY", "")
DEFAULT_USER_ID = "system"
DEFAULT_TENANT_ID = "zimax-workspace"
SESSION_ID_WORKING_MEMORY = "working-memory"
SESSION_ID_DOMAIN_MEMORY = "domain-memory"


class MemoryIngester:
    """Ingest markdown documents into Zep memory."""
    
    def __init__(self, base_url: str = ZEP_API_URL, api_key: str = ZEP_API_KEY):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    def _get_headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[dict]:
        """Make request to Zep API."""
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
        kwargs["headers"] = headers
        
        try:
            response = await self.client.request(method, url, **kwargs)
            if response.status_code == 404:
                return None
            response.raise_for_status()
            if response.content:
                return response.json()
            return {}
        except httpx.HTTPStatusError as e:
            logger.error(f"API error: {e.response.status_code} - {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Request failed: {e}")
            return None
    
    async def ensure_session(self, session_id: str) -> bool:
        """Ensure session exists via ctxEco API."""
        # ctxEco uses /api/v1/memory/sessions endpoint
        result = await self._request("GET", f"/api/v1/memory/sessions")
        # Sessions are auto-created, so we just verify the endpoint works
        return result is not None
    
    async def add_episode(
        self,
        title: str,
        summary: str,
        content: str,
        tags: str = ""
    ) -> bool:
        """Add content as an episode to the memory system."""
        payload = {
            "title": title,
            "summary": summary,
            "content": content,
            "tags": tags
        }
        
        result = await self._request(
            "POST",
            "/api/v1/tools/create_episode",
            json=payload
        )
        return result is not None
    
    async def add_fact(
        self,
        content: str,
        metadata: dict = None
    ) -> bool:
        """Add a fact to semantic memory."""
        payload = {
            "content": content,
            "metadata": metadata or {}
        }
        
        result = await self._request(
            "POST",
            "/api/v1/tools/add_fact",
            json=payload
        )
        return result is not None
    
    def parse_frontmatter(self, content: str) -> tuple[dict, str]:
        """Extract YAML frontmatter from markdown."""
        frontmatter = {}
        body = content
        
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1]) or {}
                    body = parts[2].strip()
                except yaml.YAMLError:
                    pass
        
        return frontmatter, body
    
    def chunk_content(self, content: str, max_chars: int = 4000) -> list[str]:
        """Split content into chunks by headers or paragraphs."""
        chunks = []
        current_chunk = ""
        
        # Split by headers first
        sections = re.split(r'(^#{1,3}\s+.+$)', content, flags=re.MULTILINE)
        
        for section in sections:
            if not section.strip():
                continue
            
            if len(current_chunk) + len(section) > max_chars:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = section
            else:
                current_chunk += "\n" + section
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks if chunks else [content[:max_chars]]
    
    async def ingest_document(
        self,
        file_path: Path,
        session_id: str,
        user_id: str = DEFAULT_USER_ID
    ) -> bool:
        """Ingest a markdown document into memory."""
        logger.info(f"Ingesting: {file_path}")
        
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return False
        
        frontmatter, body = self.parse_frontmatter(content)
        
        # Build metadata
        metadata = {
            "source_file": str(file_path),
            "ingested_at": datetime.now(timezone.utc).isoformat(),
            "tenant_id": DEFAULT_TENANT_ID,
            "type": "document",
        }
        
        # Extract frontmatter fields
        if "title" in frontmatter:
            metadata["title"] = frontmatter["title"]
        if "summary" in frontmatter:
            metadata["summary"] = frontmatter["summary"]
        if "classification" in frontmatter:
            metadata["classification"] = frontmatter["classification"]
        if "tags" in frontmatter:
            metadata["tags"] = frontmatter["tags"]
        if "date" in frontmatter:
            metadata["document_date"] = str(frontmatter["date"])
        
        # Get title and summary from frontmatter
        title = frontmatter.get("title", file_path.stem.replace("-", " ").title())
        summary = frontmatter.get("summary", f"Memory document: {file_path.name}")
        tags_list = frontmatter.get("tags", [])
        tags = ",".join(tags_list) if isinstance(tags_list, list) else str(tags_list)
        
        # Chunk and ingest using ctxEco API
        chunks = self.chunk_content(body)
        logger.info(f"  → {len(chunks)} chunks")
        
        success_count = 0
        for i, chunk in enumerate(chunks):
            chunk_title = f"{title} (Part {i+1}/{len(chunks)})" if len(chunks) > 1 else title
            chunk_summary = f"{summary} [Chunk {i+1} of {len(chunks)}]" if len(chunks) > 1 else summary
            
            # Use create_episode endpoint for ctxEco API
            success = await self.add_episode(
                title=chunk_title,
                summary=chunk_summary,
                content=chunk,
                tags=tags
            )
            if success:
                success_count += 1
        
        if success_count > 0:
            logger.info(f"  ✓ Ingested {success_count}/{len(chunks)} chunks successfully")
            return True
        else:
            logger.error(f"  ✗ Failed to ingest")
            return False
    
    async def ingest_as_fact(
        self,
        content: str,
        user_id: str = DEFAULT_USER_ID,
        metadata: dict = None
    ) -> bool:
        """Ingest content as a semantic fact."""
        await self.ensure_user(user_id)
        
        fact_data = {
            "fact": content[:2000],  # Zep fact limit
            "metadata": metadata or {}
        }
        
        result = await self._request(
            "POST",
            f"/api/v1/users/{user_id}/facts",
            json=fact_data
        )
        
        return result is not None
    
    async def close(self):
        await self.client.aclose()


async def ingest_working_memory(ingester: MemoryIngester, docs_path: Path) -> int:
    """Ingest all working memory documents."""
    working_memory_dir = docs_path / "working-memory"
    if not working_memory_dir.exists():
        logger.warning(f"Working memory directory not found: {working_memory_dir}")
        return 0
    
    count = 0
    for md_file in working_memory_dir.glob("*.md"):
        success = await ingester.ingest_document(
            md_file,
            session_id=SESSION_ID_WORKING_MEMORY
        )
        if success:
            count += 1
    
    return count


async def ingest_domain_memory(ingester: MemoryIngester, ctxeco_path: Path) -> int:
    """Ingest domain memory file."""
    domain_memory_file = ctxeco_path / ".ctxeco" / "domain-memory.md"
    if not domain_memory_file.exists():
        logger.warning(f"Domain memory not found: {domain_memory_file}")
        return 0
    
    success = await ingester.ingest_document(
        domain_memory_file,
        session_id=SESSION_ID_DOMAIN_MEMORY
    )
    
    return 1 if success else 0


async def ingest_stories(ingester: MemoryIngester, docs_path: Path) -> int:
    """Ingest story documents."""
    stories_dir = docs_path / "stories"
    if not stories_dir.exists():
        logger.warning(f"Stories directory not found: {stories_dir}")
        return 0
    
    count = 0
    for md_file in stories_dir.glob("*.md"):
        if md_file.name.startswith("story-request-"):
            continue  # Skip request files
        success = await ingester.ingest_document(
            md_file,
            session_id="stories"
        )
        if success:
            count += 1
    
    return count


async def main():
    parser = argparse.ArgumentParser(description="Ingest memories into Context Ecology")
    parser.add_argument("path", nargs="?", help="File or directory to ingest")
    parser.add_argument("--working-memory", action="store_true", help="Ingest all working memory")
    parser.add_argument("--domain-memory", action="store_true", help="Ingest domain memory")
    parser.add_argument("--stories", action="store_true", help="Ingest story documents")
    parser.add_argument("--all", action="store_true", help="Ingest everything")
    parser.add_argument("--api-url", default=ZEP_API_URL, help="Zep API URL")
    
    args = parser.parse_args()
    
    # Find workspace root
    script_dir = Path(__file__).parent
    if script_dir.name == "scripts":
        ctxeco_path = script_dir.parent
    else:
        ctxeco_path = script_dir
    
    docs_path = ctxeco_path / "docs"
    
    ingester = MemoryIngester(base_url=args.api_url)
    
    try:
        total = 0
        
        if args.all or args.working_memory:
            logger.info("=== Ingesting Working Memory ===")
            count = await ingest_working_memory(ingester, docs_path)
            logger.info(f"Ingested {count} working memory documents")
            total += count
        
        if args.all or args.domain_memory:
            logger.info("=== Ingesting Domain Memory ===")
            count = await ingest_domain_memory(ingester, ctxeco_path)
            logger.info(f"Ingested {count} domain memory documents")
            total += count
        
        if args.all or args.stories:
            logger.info("=== Ingesting Stories ===")
            count = await ingest_stories(ingester, docs_path)
            logger.info(f"Ingested {count} story documents")
            total += count
        
        if args.path:
            path = Path(args.path)
            if path.is_file():
                success = await ingester.ingest_document(
                    path,
                    session_id="manual-ingestion"
                )
                total += 1 if success else 0
            elif path.is_dir():
                for md_file in path.glob("**/*.md"):
                    success = await ingester.ingest_document(
                        md_file,
                        session_id="manual-ingestion"
                    )
                    if success:
                        total += 1
        
        if total == 0 and not any([args.all, args.working_memory, args.domain_memory, args.stories, args.path]):
            parser.print_help()
            return
        
        logger.info(f"\n=== Complete: {total} documents ingested ===")
        
    finally:
        await ingester.close()


if __name__ == "__main__":
    asyncio.run(main())
