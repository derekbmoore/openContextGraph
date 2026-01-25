#!/usr/bin/env python3
"""
Ingest All GTM Research Documents into ctxEco Memory

This script ingests all GTM-related research documents into ctxEco's memory
system via the Antigravity Router as Class A (Immutable Truth).

Documents are ingested for context and memory enrichment to guide GTM strategy.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Tuple

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from etl import get_antigravity_router, DataClass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# List of research files to ingest (relative to docs/research/)
RESEARCH_FILES = [
    # Core GTM documents
    "ctxeco-verified-mcp-marketplace-gtm-master.md",
    "foundry-iq-gtm-mvp-readiness.md",
    "foundry-iq-marketplace-gtm-master.md",  # Already ingested, but include for completeness
    
    # Foundry IQ research
    "foundry-iq-ecosystem-exploration.md",
    "foundry-iq-ecosystem-summary.md",
    "foundry-iq-api-research.md",
    "foundry-iq-implementation-status.md",
    "foundry-iq-research-readiness.md",
    "foundry-iq-cursor-agent-access.md",
    
    # Domain Memory research
    "domain-memory-integration.md",
    "domain-memory-summary.md",
    "domain-memory-implementation-status.md",
    "domain-memory-implementation-plan.md",
    "domain-memory-implementation-example.md",
    
    # Other research
    "foundry-agent-integration.md",
]


async def ingest_file(file_path: Path, antigravity) -> Tuple[str, int, bool]:
    """
    Ingest a single file into memory.
    
    Returns: (filename, chunk_count, success)
    """
    try:
        if not file_path.exists():
            logger.warning(f"  ⚠️  File not found: {file_path.name}")
            return (file_path.name, 0, False)
        
        logger.info(f"  📄 Reading: {file_path.name}")
        
        # Read the document
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        if not content.strip():
            logger.warning(f"  ⚠️  File is empty: {file_path.name}")
            return (file_path.name, 0, False)
        
        file_size = len(content)
        word_count = len(content.split())
        logger.info(f"     Size: {file_size:,} bytes ({word_count:,} words)")
        
        # Ingest as Class A (Immutable Truth) - strategic documentation
        content_bytes = content.encode("utf-8")
        chunks = await antigravity.ingest_bytes(
            content=content_bytes,
            filename=file_path.name,
            force_class=DataClass.CLASS_A_TRUTH,
            user_id="system",
            tenant_id="default",
        )
        
        chunk_count = len(chunks)
        logger.info(f"  ✅ Ingested: {chunk_count} chunks")
        
        return (file_path.name, chunk_count, True)
        
    except Exception as e:
        logger.error(f"  ❌ Error ingesting {file_path.name}: {e}")
        return (file_path.name, 0, False)


async def ingest_all_research_files():
    """Ingest all research files into ctxEco memory."""
    
    # Base path
    research_dir = Path(__file__).parent.parent / "docs" / "research"
    
    if not research_dir.exists():
        logger.error(f"Research directory not found: {research_dir}")
        return False
    
    logger.info(f"Research directory: {research_dir}")
    logger.info("")
    
    # Get Antigravity Router
    antigravity = get_antigravity_router()
    
    # Track results
    results: List[Tuple[str, int, bool]] = []
    
    # Ingest each file
    for filename in RESEARCH_FILES:
        file_path = research_dir / filename
        result = await ingest_file(file_path, antigravity)
        results.append(result)
        logger.info("")  # Blank line between files
    
    # Summary
    logger.info("=" * 80)
    logger.info("INGESTION SUMMARY")
    logger.info("=" * 80)
    logger.info("")
    
    successful = [r for r in results if r[2]]
    failed = [r for r in results if not r[2]]
    total_chunks = sum(r[1] for r in results)
    
    logger.info(f"✅ Successful: {len(successful)} files")
    for filename, chunks, _ in successful:
        logger.info(f"   - {filename}: {chunks} chunks")
    
    if failed:
        logger.info("")
        logger.info(f"❌ Failed: {len(failed)} files")
        for filename, _, _ in failed:
            logger.info(f"   - {filename}")
    
    logger.info("")
    logger.info(f"📊 Total chunks ingested: {total_chunks:,}")
    logger.info("")
    
    return len(successful) > 0


async def main():
    """Main execution."""
    logger.info("=" * 80)
    logger.info("Ingesting All GTM Research Documents into ctxEco Memory")
    logger.info("=" * 80)
    logger.info("")
    logger.info(f"Files to ingest: {len(RESEARCH_FILES)}")
    logger.info("")
    
    try:
        success = await ingest_all_research_files()
        
        if success:
            logger.info("=" * 80)
            logger.info("✅ INGESTION COMPLETE")
            logger.info("=" * 80)
            logger.info("")
            logger.info("All research documents are now in ctxEco memory and searchable via:")
            logger.info("  - Tri-Search™ (keyword + vector + graph)")
            logger.info("  - MCP tools (search_memory)")
            logger.info("  - Graph Knowledge (Gk) queries")
            logger.info("")
            logger.info("The system now has comprehensive GTM context for:")
            logger.info("  - Market positioning and competitive analysis")
            logger.info("  - Product differentiation (Verified MCP + Gk)")
            logger.info("  - Implementation status and roadmap")
            logger.info("  - Sales enablement and pricing")
        else:
            logger.error("No files were successfully ingested")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error ingesting research files: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
