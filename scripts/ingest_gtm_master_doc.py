#!/usr/bin/env python3
"""
Ingest GTM Master Document into ctxEco Memory

This script ingests the master GTM document (foundry-iq-marketplace-gtm-master.md)
into ctxEco's memory system via the Antigravity Router as Class A (Immutable Truth).

The document contains comprehensive GTM strategy, competitive positioning, and
product differentiation for ctxEco Verified MCP in the Microsoft Marketplace.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from etl import get_antigravity_router, DataClass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def ingest_gtm_master_doc():
    """Ingest the master GTM document into ctxEco memory."""
    
    # Path to master GTM document
    gtm_doc_path = Path(__file__).parent.parent / "docs" / "research" / "foundry-iq-marketplace-gtm-master.md"
    
    if not gtm_doc_path.exists():
        logger.error(f"GTM master document not found at {gtm_doc_path}")
        return False
    
    logger.info(f"Reading GTM master document: {gtm_doc_path}")
    
    # Read the document
    with open(gtm_doc_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    logger.info(f"Document size: {len(content)} bytes ({len(content.split())} words)")
    
    # Get Antigravity Router
    antigravity = get_antigravity_router()
    
    # Ingest as Class A (Immutable Truth) - this is strategic GTM documentation
    logger.info("Ingesting through Antigravity Router as Class A (Immutable Truth)...")
    
    content_bytes = content.encode("utf-8")
    chunks = await antigravity.ingest_bytes(
        content=content_bytes,
        filename="foundry-iq-marketplace-gtm-master.md",
        force_class=DataClass.CLASS_A_TRUTH,
        user_id="system",
        tenant_id="default",
    )
    
    logger.info(f"✅ Successfully ingested {len(chunks)} chunks from GTM master document")
    
    # Log chunk details
    for i, chunk in enumerate(chunks[:5], 1):
        logger.info(f"  Chunk {i}: {chunk.get('chunk_id', 'N/A')[:20]}... ({len(chunk.get('content', ''))} chars)")
    
    if len(chunks) > 5:
        logger.info(f"  ... and {len(chunks) - 5} more chunks")
    
    return True


async def main():
    """Main execution."""
    logger.info("=" * 80)
    logger.info("Ingesting GTM Master Document into ctxEco Memory")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        success = await ingest_gtm_master_doc()
        
        if success:
            logger.info("")
            logger.info("=" * 80)
            logger.info("✅ INGESTION COMPLETE")
            logger.info("=" * 80)
            logger.info("")
            logger.info("The GTM master document is now in ctxEco memory and searchable via:")
            logger.info("  - Tri-Search™ (keyword + vector + graph)")
            logger.info("  - MCP tools (search_memory)")
            logger.info("  - Graph Knowledge (Gk) queries")
            logger.info("")
            logger.info("Next: Incorporate remaining research files")
        else:
            logger.error("Ingestion failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error ingesting GTM master document: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
