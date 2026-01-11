"""
Base Agent Implementation

LangGraph-based agent with:
- Full EnterpriseContext integration
- Memory enrichment
- Tool execution
- Attribution tracking

OpenContextGraph - Brain Layer
NIST AI RMF: GOVERN 1.2 (Accountability), MAP 1.1 (Context)
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Any
from datetime import datetime, timezone

from core.context import EnterpriseContext, ToolCall

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all agents.
    
    NIST AI RMF: GOVERN 1.2 - All agent actions are attributed to user
    """
    
    def __init__(
        self, 
        agent_id: str,
        display_name: str,
        system_prompt: str,
        model: str = "gpt-4o"
    ):
        self.agent_id = agent_id
        self.display_name = display_name
        self.system_prompt = system_prompt
        self.model = model
        self._graph = None
        logger.info(f"Agent initialized: {agent_id} ({display_name})")
    
    @abstractmethod
    def get_tools(self) -> list:
        """Return tools available to this agent. Override in subclasses."""
        pass
    
    def format_system_prompt(self, context: EnterpriseContext) -> str:
        """Format system prompt with context placeholders."""
        return self.system_prompt.format(
            user_id=context.security.user_id,
            tenant_id=context.security.tenant_id,
            agent_id=self.agent_id,
        )
    
    async def process(
        self,
        message: str,
        context: EnterpriseContext
    ) -> dict:
        """
        Process a user message through the agent.
        
        NIST AI RMF Controls:
        - GOVERN 1.2: Records invoking user
        - MAP 1.1: Context enrichment
        - MEASURE 2.5: Response tracking
        
        Args:
            message: User's input
            context: Full 4-layer enterprise context
        
        Returns:
            {response, agent_id, sources, tool_calls}
        """
        # Track who invoked this agent
        context.operational.current_agent = self.agent_id
        context.operational.request_id = f"req-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        
        logger.info(
            f"Agent {self.agent_id} processing request from "
            f"{context.security.user_id}"
        )
        
        try:
            # Execute agent logic (implemented by subclasses)
            response_text, tool_calls = await self._execute(message, context)
            
            # Record tool calls for attribution
            recorded_calls = [
                ToolCall(
                    tool_name=tc.get("name", "unknown"),
                    arguments=tc.get("args", {}),
                    result=tc.get("result"),
                    duration_ms=tc.get("duration_ms")
                )
                for tc in tool_calls
            ]
            context.operational.tool_calls.extend(recorded_calls)
            
            return {
                "response": response_text,
                "agent_id": self.agent_id,
                "user_id": context.security.user_id,
                "sources": self._extract_sources(context),
                "tool_calls": [tc.model_dump() for tc in recorded_calls],
            }
            
        except Exception as e:
            logger.error(f"Agent {self.agent_id} error: {e}")
            return {
                "response": f"I encountered an error: {str(e)}",
                "agent_id": self.agent_id,
                "user_id": context.security.user_id,
                "sources": [],
                "tool_calls": [],
                "error": str(e),
            }
    
    @abstractmethod
    async def _execute(
        self, 
        message: str, 
        context: EnterpriseContext
    ) -> tuple[str, list[dict]]:
        """
        Execute agent-specific logic.
        
        Returns:
            Tuple of (response_text, tool_calls)
        """
        pass
    
    def _extract_sources(self, context: EnterpriseContext) -> list[str]:
        """Extract source references from semantic context."""
        return [
            fact.source 
            for fact in context.semantic.facts 
            if fact.source
        ]
