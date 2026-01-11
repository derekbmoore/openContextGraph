"""
Agent Router

Routes requests to the appropriate specialized agent.

OpenContextGraph - Brain Layer
NIST AI RMF: GOVERN 1.2 - Routing decisions are logged
"""

import logging
from typing import Optional

from agents.base import BaseAgent
from agents.elena import ElenaAgent
from core.context import EnterpriseContext

logger = logging.getLogger(__name__)


class AgentRouter:
    """
    Routes requests to the appropriate agent.
    
    Available agents:
    - elena: Senior System Architect
    - marcus: Project Manager (coming soon)
    - sage: Storyteller (coming soon)
    
    NIST AI RMF: GOVERN 1.2 - Routing decisions are logged
    """
    
    def __init__(self):
        self.agents: dict[str, BaseAgent] = {
            "elena": ElenaAgent(),
            # TODO: Add Marcus and Sage
            # "marcus": MarcusAgent(),
            # "sage": SageAgent(),
        }
        logger.info(f"AgentRouter initialized with agents: {list(self.agents.keys())}")
    
    def get_agent(self, agent_name: str) -> Optional[BaseAgent]:
        """Get an agent by name."""
        return self.agents.get(agent_name.lower())
    
    def list_agents(self) -> list[str]:
        """List available agent names."""
        return list(self.agents.keys())
    
    async def route(
        self,
        agent_name: str,
        message: str,
        context: EnterpriseContext
    ) -> dict:
        """
        Route to the specified agent.
        
        Args:
            agent_name: Target agent ("elena", "marcus", "sage")
            message: User's input
            context: Full enterprise context
        
        Returns:
            Agent response dict
        """
        agent = self.get_agent(agent_name)
        
        if not agent:
            available = ", ".join(self.list_agents())
            logger.warning(f"Unknown agent: {agent_name}")
            return {
                "error": f"Unknown agent: {agent_name}. Available: {available}",
                "agent_id": None
            }
        
        logger.info(
            f"Routing to agent {agent_name} for user {context.security.user_id}"
        )
        
        return await agent.process(message, context)


# Singleton router
_router: Optional[AgentRouter] = None


def get_agent_router() -> AgentRouter:
    """Get the singleton agent router."""
    global _router
    if _router is None:
        _router = AgentRouter()
    return _router
