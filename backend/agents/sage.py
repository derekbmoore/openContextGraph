"""
Sage - Creative Storyteller & Analyst Agent

Expertise:
- Narrative Generation (Episodes/Stories)
- Visual storytelling (Diagrams/Images)
- Data synthesis and insights
- User engagement

OpenContextGraph - Brain Layer
"""

import logging
import os
from typing import Optional

from agents.base import BaseAgent
from core.context import EnterpriseContext

logger = logging.getLogger(__name__)


class SageAgent(BaseAgent):
    """
    Sage - Storyteller & Analyst
    
    Responsible for synthesizing complex data into compelling
    narratives ("Stories") and visual artifacts.
    """
    
    SYSTEM_PROMPT = """You are Sage, the Creative Storyteller for OpenContextGraph.
Your goals are:
- Translate technical/complex data into clear, engaging narratives.
- Create visual representations (diagrams, images) to aid understanding.
- Connect disparate facts into coherent episodes.

You are empathetic, articulate, and insightful. You care about the "Why" and the user experience.

Current user: {user_id}
Tenant: {tenant_id}
"""
    
    def __init__(self, model: str = None):
        super().__init__(
            agent_id="sage",
            display_name="Sage",
            system_prompt=self.SYSTEM_PROMPT,
            model=model or os.getenv("LLM_MODEL", "gpt-4o")
        )
    
    def get_tools(self) -> list:
        """Sage's available tools."""
        return [
            {
                "name": "generate_story",
                "description": "Create a narrative story from a topic",
            },
            {
                "name": "generate_diagram",
                "description": "Create a visual diagram for a concept",
            },
            {
                "name": "search_memory",
                "description": "Deep search for semantic connections",
            },
        ]
    
    async def _execute(
        self, 
        message: str, 
        context: EnterpriseContext
    ) -> tuple[str, list[dict]]:
        """
        Execute Sage's reasoning.
        """
        return await super()._execute(message, context)
