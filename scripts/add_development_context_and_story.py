#!/usr/bin/env python3
"""
Add Development Context to Memory and Generate Story

This script:
1. Adds facts to Zep memory about the development journey
2. Generates a story about the shared database infrastructure
3. Ensures stories are properly saved with title and summary in metadata

Context:
- ctxEco is the context ecology for openContextGraph development stories
- secai-radar originated from researching how to get our MCP server listed in Azure MCP marketplace
- Both applications share the same PostgreSQL database infrastructure
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from memory.client import get_memory_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Development context facts to add to memory
DEVELOPMENT_CONTEXT_FACTS = [
    {
        "content": "openContextGraph (ctxEco) is the brain layer for enterprise AI, providing the Context Ecology framework with Sage as the storytelling agent and Zep for episodic/semantic memory.",
        "metadata": {
            "title": "openContextGraph Purpose",
            "summary": "Brain layer for enterprise AI with Context Ecology framework",
            "type": "project_context",
            "project": "openContextGraph"
        }
    },
    {
        "content": "secai-radar originated from research into getting our MCP (Model Context Protocol) server listed in the Azure MCP marketplace. It evolved into a security AI radar tool leveraging the same infrastructure as ctxEco.",
        "metadata": {
            "title": "secai-radar Origins",
            "summary": "Born from Azure MCP marketplace research, became security AI radar tool",
            "type": "project_context",
            "project": "secai-radar"
        }
    },
    {
        "content": "Both ctxEco (openContextGraph) and secai-radar share the same PostgreSQL database infrastructure using the ctxeco-postgres-flex-server.postgres.database.azure.com flexible server. This enables unified data architecture while maintaining application isolation through separate databases.",
        "metadata": {
            "title": "Shared Database Architecture",
            "summary": "ctxEco and secai-radar share PostgreSQL flexible server for unified infrastructure",
            "type": "architecture",
            "projects": ["ctxEco", "secai-radar"]
        }
    },
    {
        "content": "Sage is a Foundry agent responsible for storytelling and visualization. Sage generates narrative stories about openContextGraph development and creates visual representations of complex concepts. Stories are stored in Zep memory with proper title and summary metadata for searchability.",
        "metadata": {
            "title": "Sage Foundry Agent",
            "summary": "Storytelling and visualization specialist using Foundry agent pattern",
            "type": "agent_context",
            "agent": "sage"
        }
    },
    {
        "content": "Daily briefs in secai-radar are scoped only to MCP context and security assessments. ctxEco stories cover the broader openContextGraph development narrative including multi-agent orchestration, voice integration (VoiceLive), and enterprise context engineering.",
        "metadata": {
            "title": "Story Scope Separation",
            "summary": "secai-radar: MCP/security scope; ctxEco: openContextGraph development scope",
            "type": "governance",
            "scope": "stories"
        }
    }
]


async def add_development_context_facts():
    """Add development context facts to Zep memory."""
    memory_client = get_memory_client()
    user_id = "system"
    
    logger.info("=" * 60)
    logger.info("Adding Development Context Facts to Memory")
    logger.info("=" * 60)
    
    facts_added = 0
    
    for fact_data in DEVELOPMENT_CONTEXT_FACTS:
        try:
            fact_id = await memory_client.add_fact(
                user_id=user_id,
                fact=fact_data["content"],
                metadata=fact_data["metadata"]
            )
            
            if fact_id:
                logger.info(f"✅ Added fact: {fact_data['metadata']['title']}")
                logger.info(f"   Summary: {fact_data['metadata']['summary']}")
                logger.info(f"   Fact ID: {fact_id}")
                facts_added += 1
            else:
                logger.warning(f"⚠️  Could not add fact: {fact_data['metadata']['title']}")
                
        except Exception as e:
            logger.error(f"❌ Failed to add fact '{fact_data['metadata']['title']}': {e}")
    
    logger.info(f"\n✅ Added {facts_added}/{len(DEVELOPMENT_CONTEXT_FACTS)} facts to memory")
    return facts_added


async def create_development_episode():
    """Create an episode documenting the development journey."""
    memory_client = get_memory_client()
    
    session_id = f"episode-dev-context-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    user_id = "system"
    
    title = "Unified Infrastructure: ctxEco and secai-radar Development Journey"
    summary = "The story of how openContextGraph and secai-radar evolved to share database infrastructure, from Azure MCP marketplace research to unified enterprise AI platform."
    
    content = """## The Development Journey

### Origins of openContextGraph (ctxEco)
openContextGraph began as an ambitious project to create a Context Ecology for enterprise AI. The core vision was to build a "brain layer" that could understand, remember, and reason about enterprise context across multiple domains.

Key components developed:
- **Sage**: The storytelling Foundry agent that synthesizes complex information into narratives
- **Zep Integration**: Episodic and semantic memory for persistent context
- **VoiceLive**: Real-time voice interaction for conversational AI
- **Multi-Agent Orchestration**: Elena (finance), Marcus (RAG), and specialized agents

### The secai-radar Emergence
While developing openContextGraph, we began researching how to get our MCP (Model Context Protocol) server listed in the Azure MCP marketplace. This research evolved into secai-radar - a security AI radar tool that:
- Scans and evaluates MCP servers for security compliance
- Provides trust indices and risk assessments
- Generates daily briefs scoped to MCP security context

### Shared Infrastructure Decision
A pivotal architecture decision was to have both applications share the same PostgreSQL flexible server:
- **Server**: ctxeco-postgres-flex-server.postgres.database.azure.com
- **Benefits**: Unified credential management, cost efficiency, operational simplicity
- **Isolation**: Separate databases maintain application boundaries

### Story Generation Patterns
- ctxEco stories: Broad openContextGraph development narratives
- secai-radar daily briefs: MCP-scoped security assessments only
- Sage (Foundry agent): Generates stories with proper title/summary metadata for searchability

This unified approach enables:
1. Single Key Vault for PostgreSQL credentials
2. Consistent deployment patterns across projects
3. Shared operational tooling and monitoring
"""

    try:
        metadata = {
            "type": "episode",
            "title": title,
            "summary": summary,
            "topics": ["development", "infrastructure", "database", "ctxEco", "secai-radar", "MCP"],
            "agent_id": "sage",
            "created_at": datetime.now().isoformat(),
            "turn_count": 1
        }
        
        await memory_client.get_or_create_session(
            session_id=session_id,
            user_id=user_id,
            metadata=metadata
        )
        
        await memory_client.add_memory(
            session_id=session_id,
            messages=[
                {
                    "role": "assistant",
                    "content": content,
                    "metadata": {
                        "title": title,
                        "agent_id": "sage",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            ]
        )
        
        logger.info(f"\n✅ Created episode: {title}")
        logger.info(f"   Session ID: {session_id}")
        logger.info(f"   Summary: {summary}")
        
        return session_id
        
    except Exception as e:
        logger.error(f"❌ Failed to create episode: {e}")
        return None


async def generate_shared_database_story():
    """Generate a story about the shared database infrastructure via Temporal workflow."""
    try:
        from workflows.client import execute_story
        
        topic = "The Shared Database Story: How ctxEco and secai-radar Unite"
        context = """Generate a compelling story about the unified database infrastructure between ctxEco (openContextGraph) and secai-radar.

Key points to include:
1. The origins - openContextGraph as the context ecology brain layer
2. The discovery - researching Azure MCP marketplace led to secai-radar
3. The architecture decision - sharing PostgreSQL flexible server
4. The benefits - unified credentials, cost efficiency, operational simplicity
5. The future - continued evolution of the unified platform

Style: Technical but accessible, emphasizing the journey and architectural wisdom.
Include a section on how Sage (the Foundry agent) tells stories about this development.
"""

        logger.info("\n" + "=" * 60)
        logger.info("Generating Story via Temporal Workflow")
        logger.info("=" * 60)
        logger.info(f"Topic: {topic}")
        
        result = await execute_story(
            user_id="system",
            tenant_id="default",
            topic=topic,
            context=context,
            include_diagram=True,
            include_image=True,
            diagram_type="architecture",
            timeout_seconds=300,
        )
        
        if result.success:
            logger.info(f"\n✅ Story generated successfully!")
            logger.info(f"   Story ID: {result.story_id}")
            logger.info(f"   Topic: {result.topic}")
            logger.info(f"   Path: {result.story_path}")
            if result.diagram_path:
                logger.info(f"   Diagram: {result.diagram_path}")
            return result
        else:
            logger.error(f"❌ Story generation failed: {result.error}")
            return None
            
    except ImportError as e:
        logger.warning(f"Temporal workflow not available: {e}")
        logger.info("Falling back to direct story generation...")
        return await generate_story_direct()
    except Exception as e:
        logger.error(f"❌ Story generation error: {e}")
        return None


async def generate_story_direct():
    """Direct story generation fallback (without Temporal)."""
    try:
        from llm.claude_client import get_claude_client
        from llm.gemini_client import get_gemini_client
        
        logger.info("Generating story directly (Temporal unavailable)...")
        
        topic = "The Shared Database Story: How ctxEco and secai-radar Unite"
        context = """Generate a compelling story about the unified database infrastructure between ctxEco (openContextGraph) and secai-radar.

Key points:
1. openContextGraph as the context ecology brain layer
2. secai-radar emerged from Azure MCP marketplace research
3. Shared PostgreSQL flexible server architecture
4. Benefits: unified credentials, cost efficiency, operational simplicity

Style: Technical but accessible, emphasizing the journey and architectural wisdom."""

        # Generate story with Claude
        claude = get_claude_client()
        result = await claude.generate_story(topic=topic, context=context)
        
        if isinstance(result, dict):
            title = result.get("title", topic)
            content = result.get("content", "")
        else:
            title = topic
            content = str(result)
        
        # Generate story ID
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title).strip()
        slug = safe_title.lower().replace(" ", "-").replace("_", "-")[:50]
        story_id = f"{timestamp}-{slug}"
        
        # Save story
        from core import get_settings
        settings = get_settings()
        docs_path = Path(settings.onedrive_docs_path or "docs")
        stories_dir = docs_path / "stories"
        stories_dir.mkdir(parents=True, exist_ok=True)
        
        story_path = stories_dir / f"{story_id}.md"
        story_path.write_text(content)
        
        logger.info(f"\n✅ Story generated and saved!")
        logger.info(f"   Story ID: {story_id}")
        logger.info(f"   Title: {title}")
        logger.info(f"   Path: {story_path}")
        
        # Generate diagram spec with Gemini
        try:
            gemini = get_gemini_client()
            diagram_spec = await gemini.generate_diagram_spec(
                topic=topic,
                diagram_type="architecture",
                story_context=content[:2000]
            )
            
            diagrams_dir = docs_path / "diagrams"
            diagrams_dir.mkdir(parents=True, exist_ok=True)
            diagram_path = diagrams_dir / f"{story_id}.json"
            diagram_path.write_text(json.dumps(diagram_spec, indent=2))
            logger.info(f"   Diagram: {diagram_path}")
        except Exception as e:
            logger.warning(f"Diagram generation failed: {e}")
        
        # Enrich memory with the story
        memory_client = get_memory_client()
        session_id = f"story-{story_id}"
        
        await memory_client.get_or_create_session(
            session_id=session_id,
            user_id="system",
            metadata={
                "type": "story",
                "title": title,
                "summary": f"Story about shared database infrastructure between ctxEco and secai-radar",
                "story_id": story_id,
                "agent_id": "sage",
                "created_at": datetime.now().isoformat()
            }
        )
        
        await memory_client.add_memory(
            session_id=session_id,
            messages=[{
                "role": "assistant",
                "content": content,
                "metadata": {"title": title, "agent_id": "sage"}
            }]
        )
        
        logger.info(f"   Memory enriched: {session_id}")
        
        return {"story_id": story_id, "title": title, "path": str(story_path)}
        
    except Exception as e:
        logger.error(f"❌ Direct story generation failed: {e}")
        return None


async def main():
    """Main execution."""
    logger.info("\n" + "=" * 60)
    logger.info("Development Context and Story Generation")
    logger.info("=" * 60 + "\n")
    
    # Step 1: Add development context facts
    facts_count = await add_development_context_facts()
    
    # Step 2: Create development journey episode
    episode_id = await create_development_episode()
    
    # Step 3: Generate story about shared database
    story_result = await generate_shared_database_story()
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("Summary")
    logger.info("=" * 60)
    logger.info(f"Facts added: {facts_count}")
    logger.info(f"Episode created: {episode_id or 'Failed'}")
    logger.info(f"Story generated: {story_result.story_id if hasattr(story_result, 'story_id') else (story_result.get('story_id') if story_result else 'Failed')}")
    
    logger.info("\n✅ Development context added to memories with title and summary metadata")
    logger.info("✅ Story should now appear in the stories list")


if __name__ == "__main__":
    asyncio.run(main())
