#!/usr/bin/env python3
"""
Generate Engram evolution story directly (without HTTP API).

This script calls the story generation activities directly to create
a story about Engram's evolution based on the ingested commit history.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from workflows.story_activities import (
    GenerateStoryInput,
    GenerateStoryOutput,
    GenerateDiagramInput,
    GenerateDiagramOutput,
    SaveArtifactsInput,
    SaveArtifactsOutput,
    generate_story_activity,
    generate_diagram_activity,
    save_artifacts_activity,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Main execution."""
    logger.info("Generating Engram evolution story directly...")
    
    topic = "The Evolution of Engram: A Journey Through Commit History"
    context = """This story should synthesize the commit history of the Engram project to tell the narrative of how the system evolved. Focus on:
- Major architectural decisions and their rationale
- Key features and capabilities that were added
- Challenges overcome and solutions implemented
- The progression from initial concept to production-ready system
- How the project demonstrates recursive self-awareness and context engineering

The story should be engaging, technical but accessible, and highlight the innovative aspects of Engram's architecture. Use the ingested commit history from memory to ground the narrative in actual project evolution."""
    
    try:
        # Step 1: Generate story
        logger.info(f"Step 1: Generating story about '{topic}'...")
        story_input = GenerateStoryInput(
            topic=topic,
            context=context,
            user_id="system",
            tenant_id="default",
        )
        
        story_result: GenerateStoryOutput = await generate_story_activity(story_input)
        
        if not story_result.success:
            logger.error(f"Story generation failed: {story_result.error}")
            sys.exit(1)
        
        logger.info(f"✅ Story generated: {story_result.title} ({len(story_result.content)} chars)")
        
        # Step 2: Generate diagram
        logger.info("Step 2: Generating architecture diagram...")
        diagram_input = GenerateDiagramInput(
            topic=topic,
            story_content=story_result.content,
            diagram_type="architecture",
        )
        
        diagram_result: GenerateDiagramOutput = await generate_diagram_activity(diagram_input)
        
        if not diagram_result.success:
            logger.warning(f"Diagram generation failed: {diagram_result.error}")
            diagram_spec = None
        else:
            logger.info("✅ Diagram spec generated")
            diagram_spec = diagram_result.spec
        
        # Step 3: Save artifacts
        logger.info("Step 3: Saving artifacts...")
        save_input = SaveArtifactsInput(
            story_id=story_result.story_id,
            topic=story_result.title,
            story_content=story_result.content,
            diagram_spec=diagram_spec,
            image_data=None,  # Skip image generation for now
        )
        
        save_result: SaveArtifactsOutput = await save_artifacts_activity(save_input)
        
        if not save_result.success:
            logger.error(f"Failed to save artifacts: {save_result.error}")
            sys.exit(1)
        
        logger.info("✅ Artifacts saved")
        
        # Summary
        print("\n" + "="*80)
        print("STORY GENERATION COMPLETE")
        print("="*80)
        print(f"Story ID: {story_result.story_id}")
        print(f"Title: {story_result.title}")
        print(f"Story Path: {save_result.story_path}")
        if save_result.diagram_path:
            print(f"Diagram Path: {save_result.diagram_path}")
        if save_result.image_path:
            print(f"Image Path: {save_result.image_path}")
        print("="*80)
        
    except Exception as e:
        logger.error(f"Error generating story: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
