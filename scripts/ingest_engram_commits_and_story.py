#!/usr/bin/env python3
"""
Ingest Engram commit history and generate a story with Sage.

This script:
1. Reads commit history from engram repo
2. Formats it as a markdown document
3. Ingests it through Antigravity Router (Class A - immutable truth)
4. Triggers Sage to generate a story about the project evolution
5. Generates a visual diagram
"""

import asyncio
import logging
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from etl import get_antigravity_router, DataClass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_engram_commit_history() -> str:
    """Get commit history from engram repo."""
    engram_repo = Path("/Users/derek/Library/CloudStorage/OneDrive-zimaxnet/code/engram")
    
    if not engram_repo.exists():
        raise FileNotFoundError(f"Engram repo not found at {engram_repo}")
    
    logger.info(f"Reading commit history from {engram_repo}")
    
    # Get commit history since 2024-01-01
    result = subprocess.run(
        ["git", "log", "--since=2024-01-01", "--pretty=format:%H|%an|%ad|%s|%b", "--date=iso"],
        cwd=str(engram_repo),
        capture_output=True,
        text=True,
        check=True,
    )
    
    commits = result.stdout.strip().split("\n")
    logger.info(f"Found {len(commits)} commits")
    
    return result.stdout


def format_commit_history_as_markdown(commit_history: str) -> str:
    """Format commit history as markdown document."""
    lines = commit_history.strip().split("\n")
    
    md = """# Engram Project Evolution: Commit History

> **Source:** Engram repository (zimaxnet/engram)  
> **Period:** 2024-01-01 to present  
> **Purpose:** Project evolution and architectural decisions captured from git commit logs

## Overview

This document captures the evolution of the Engram project through its commit history. Each commit represents a decision, fix, feature, or architectural change that shaped the system.

## Commit Timeline

"""
    
    current_date = None
    for line in lines:
        if not line.strip():
            continue
        
        parts = line.split("|", 4)
        if len(parts) < 4:
            continue
        
        commit_hash = parts[0]
        author = parts[1]
        date_str = parts[2]
        subject = parts[3]
        body = parts[4] if len(parts) > 4 else ""
        
        # Parse date for grouping
        try:
            commit_date = datetime.fromisoformat(date_str.replace(" -0700", "").replace(" -0600", ""))
            date_group = commit_date.strftime("%Y-%m-%d")
            
            # Add date header if new day
            if date_group != current_date:
                md += f"\n### {date_group}\n\n"
                current_date = date_group
        except:
            pass
        
        # Format commit entry
        md += f"#### {subject}\n\n"
        md += f"**Commit:** `{commit_hash[:8]}`  \n"
        md += f"**Author:** {author}  \n"
        md += f"**Date:** {date_str}  \n\n"
        
        if body.strip():
            md += f"{body.strip()}\n\n"
        
        md += "---\n\n"
    
    md += f"\n\n*Document generated: {datetime.now().isoformat()}*\n"
    
    return md


async def ingest_commit_history(markdown_content: str) -> dict:
    """Ingest commit history through Antigravity Router."""
    logger.info("Ingesting commit history through Antigravity Router...")
    
    antigravity = get_antigravity_router()
    
    # Ingest as Class A (immutable truth - historical record)
    content_bytes = markdown_content.encode("utf-8")
    
    chunks = await antigravity.ingest_bytes(
        content=content_bytes,
        filename="engram-commit-history.md",
        force_class=DataClass.CLASS_A_TRUTH,
        user_id="system",
        tenant_id="default",
    )
    
    logger.info(f"Ingested {len(chunks)} chunks from commit history")
    
    return {
        "chunks": len(chunks),
        "status": "success",
    }


def generate_story_instructions() -> str:
    """Return instructions for generating the story via API."""
    return """
To generate the story, use one of these methods:

1. Via MCP Tool (if API is running):
   curl -X POST http://localhost:8000/mcp \\
     -H "Content-Type: application/json" \\
     -d '{
       "jsonrpc": "2.0",
       "method": "tools/call",
       "params": {
         "name": "generate_story",
         "arguments": {
           "topic": "The Evolution of Engram: A Journey Through Commit History",
           "style": "informative",
           "length": "long"
         }
       },
       "id": 1
     }'

2. Via API Endpoint (if API is running):
   curl -X POST http://localhost:8000/api/v1/stories/create \\
     -H "Content-Type: application/json" \\
     -H "Authorization: Bearer <token>" \\
     -d '{
       "topic": "The Evolution of Engram: A Journey Through Commit History",
       "style": "informative",
       "length": "long",
       "include_diagram": true,
       "include_image": true
     }'

3. The commit history has been ingested into memory. You can now ask Sage directly:
   "Write a story about the evolution of Engram based on the commit history we just ingested."
"""


async def main():
    """Main execution flow."""
    logger.info("Starting Engram commit history ingestion and story generation...")
    
    try:
        # Step 1: Get commit history
        commit_history = get_engram_commit_history()
        
        # Step 2: Format as markdown
        markdown_content = format_commit_history_as_markdown(commit_history)
        
        # Save formatted content for reference
        output_path = Path(__file__).parent.parent / "docs" / "stories" / "engram-commit-history.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown_content, encoding="utf-8")
        logger.info(f"Saved formatted commit history to {output_path}")
        
        # Step 3: Ingest through Antigravity Router
        ingestion_result = await ingest_commit_history(markdown_content)
        logger.info(f"Ingestion result: {ingestion_result}")
        
        # Step 4: Instructions for story generation
        story_instructions = generate_story_instructions()
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✅ Commit history formatted: {len(markdown_content)} bytes")
        print(f"✅ Saved to: {output_path}")
        print(f"✅ Ingested chunks: {ingestion_result['chunks']}")
        print(f"\n📝 Next step: Generate story with Sage")
        print(story_instructions)
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
