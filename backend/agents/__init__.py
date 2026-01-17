"""
Agents Package - openContextGraph

Provides AI agent capabilities:
- BaseAgent: Foundation for all agents
- ElenaAgent: Senior System Architect
- MarcusAgent: [Description for MarcusAgent]
- SageAgent: [Description for SageAgent]
- AgentRouter: Routes to appropriate agent
"""

from .base import BaseAgent
from .elena import ElenaAgent
from .marcus import MarcusAgent
from .sage import SageAgent
from .router import AgentRouter, get_agent_router

__all__ = [
    "BaseAgent",
    "ElenaAgent",
    "MarcusAgent",
    "SageAgent",
    "AgentRouter",
    "get_agent_router",
]
