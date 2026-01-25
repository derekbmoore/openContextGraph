#!/usr/bin/env python3
"""
Ingest MCP Trust Index Scored Content (Batch 1) into ctxEco Memory

This script ingests the scored Batch 1 data including:
- Scored report with rankings and insights
- Scored CSV and markdown backlog
- Updated scorecards with Trust Scores
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


# Base directory for scored content
SCORED_DIR = Path(__file__).parent.parent / "docs" / "mcp_trust_index_seed 2"


async def ingest_file(file_path: Path, antigravity) -> Tuple[str, int, bool]:
    """
    Ingest a single file into memory.
    
    Returns: (filename, chunk_count, success)
    """
    try:
        if not file_path.exists():
            logger.warning(f"  ⚠️  File not found: {file_path}")
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


async def ingest_scored_content():
    """Ingest all scored content files into ctxEco memory."""
    
    if not SCORED_DIR.exists():
        logger.error(f"Scored directory not found: {SCORED_DIR}")
        return False
    
    logger.info(f"Scored directory: {SCORED_DIR}")
    logger.info("")
    
    # Get Antigravity Router
    antigravity = get_antigravity_router()
    
    # Track results
    results: List[Tuple[str, int, bool]] = []
    
    # Ingest scored report
    report_file = SCORED_DIR / "batch1-scored-report.md"
    if report_file.exists():
        result = await ingest_file(report_file, antigravity)
        results.append(result)
        logger.info("")
    
    # Ingest scored backlog files
    scored_backlog_md = SCORED_DIR / "mcp-trust-index-seed-backlog.scored.md"
    if scored_backlog_md.exists():
        result = await ingest_file(scored_backlog_md, antigravity)
        results.append(result)
        logger.info("")
    
    scored_backlog_csv = SCORED_DIR / "mcp-trust-index-seed-backlog.scored.csv"
    if scored_backlog_csv.exists():
        result = await ingest_file(scored_backlog_csv, antigravity)
        results.append(result)
        logger.info("")
    
    # Ingest all scored scorecards
    scorecards_dir = SCORED_DIR / "scorecards"
    if scorecards_dir.exists():
        scorecard_files = sorted(scorecards_dir.glob("*.md"))
        logger.info(f"Ingesting {len(scorecard_files)} scored scorecards...")
        logger.info("")
        
        for scorecard_file in scorecard_files:
            result = await ingest_file(scorecard_file, antigravity)
            results.append(result)
            logger.info("")
    
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
    logger.info("Ingesting MCP Trust Index Scored Content (Batch 1) into ctxEco Memory")
    logger.info("=" * 80)
    logger.info("")
    
    try:
        success = await ingest_scored_content()
        
        if success:
            logger.info("=" * 80)
            logger.info("✅ INGESTION COMPLETE")
            logger.info("=" * 80)
            logger.info("")
            logger.info("Batch 1 scored content is now in ctxEco memory:")
            logger.info("  - Scored report with rankings and insights")
            logger.info("  - Scored backlog (CSV + Markdown)")
            logger.info("  - Updated scorecards with Trust Scores")
            logger.info("  - Searchable via Tri-Search™, MCP tools, Graph Knowledge (Gk)")
            logger.info("")
            logger.info("This represents the first scoring pass using Trust Score v1 rubric.")
        else:
            logger.error("No files were successfully ingested")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error ingesting scored content: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
