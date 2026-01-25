#!/usr/bin/env python3
"""
Generate Engram evolution story directly using LLM clients.

This script calls Claude and Gemini directly to create a story
about Engram's evolution based on the ingested commit history.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from llm.claude_client import get_claude_client
from llm.gemini_client import get_gemini_client
from memory.client import memory_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def search_memory_for_context(topic: str) -> str:
    """Search memory for relevant context about the topic."""
    try:
        logger.info(f"Searching memory for context about '{topic}'...")
        results = await memory_client.search_memory(
            session_id="global-search",
            query=topic,
            limit=5,
            user_id="system",
            tenant_id="default"
        )
        
        if results:
            context = "\n\n## Memory Context (from Ingested Commit History)\n"
            for i, res in enumerate(results[:3], 1):
                content = res.get("content", "")[:500]
                context += f"{i}. {content}\n\n"
            logger.info(f"Found {len(results)} relevant memory results")
            return context
        else:
            logger.warning("No memory results found")
            return ""
    except Exception as e:
        logger.warning(f"Memory search failed: {e}")
        return ""


async def main():
    """Main execution."""
    logger.info("Generating Engram evolution story...")
    
    topic = "The Evolution of Engram: A Journey Through Commit History"
    base_context = """This story should synthesize the commit history of the Engram project to tell the narrative of how the system evolved. Focus on:
- Major architectural decisions and their rationale
- Key features and capabilities that were added
- Challenges overcome and solutions implemented
- The progression from initial concept to production-ready system
- How the project demonstrates recursive self-awareness and context engineering

The story should be engaging, technical but accessible, and highlight the innovative aspects of Engram's architecture."""
    
    try:
        # Step 1: Search memory for commit history context
        memory_context = await search_memory_for_context("Engram commit history evolution")
        full_context = base_context + memory_context
        
        # Step 2: Generate story with Claude
        logger.info(f"Generating story about '{topic}'...")
        claude = get_claude_client()
        story_result = await claude.generate_story(
            topic=topic,
            context=full_context,
        )
        
        if isinstance(story_result, dict):
            title = story_result.get("title", topic)
            content = story_result.get("content", "")
        else:
            title = topic
            content = str(story_result)
        
        logger.info(f"✅ Story generated: {title} ({len(content)} chars)")
        
        # Step 3: Generate diagram with Gemini
        logger.info("Generating architecture diagram...")
        gemini = get_gemini_client()
        diagram_spec = await gemini.generate_diagram_spec(
            topic=topic,
            diagram_type="architecture",
            story_context=content[:2000],  # First 2000 chars for context
        )
        
        logger.info("✅ Diagram spec generated")
        
        # Step 4: Save artifacts
        stories_dir = Path(__file__).parent.parent / "docs" / "stories"
        stories_dir.mkdir(parents=True, exist_ok=True)
        
        diagrams_dir = Path(__file__).parent.parent / "docs" / "assets" / "diagrams"
        diagrams_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate story ID
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip()
        slug = safe_title.lower().replace(" ", "-").replace("_", "-")[:50]
        slug = slug.replace(":", "").replace("/", "")
        story_id = f"{timestamp}-{slug}"
        
        # Save story
        story_path = stories_dir / f"{story_id}.md"
        story_path.write_text(content, encoding="utf-8")
        logger.info(f"✅ Story saved: {story_path}")
        
        # Save diagram
        diagram_path = diagrams_dir / f"{story_id}.json"
        diagram_path.write_text(json.dumps(diagram_spec, indent=2), encoding="utf-8")
        logger.info(f"✅ Diagram saved: {diagram_path}")
        
        # Summary
        print("\n" + "="*80)
        print("STORY GENERATION COMPLETE")
        print("="*80)
        print(f"Story ID: {story_id}")
        print(f"Title: {title}")
        print(f"Story Path: {story_path}")
        print(f"Diagram Path: {diagram_path}")
        print(f"\nStory Preview (first 500 chars):")
        print("-" * 80)
        print(content[:500] + "...")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error generating story: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
