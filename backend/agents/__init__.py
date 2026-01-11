"""
Agents Package - openContextGraph

Provides AI agent capabilities:
- BaseAgent: Foundation for all agents
- ElenaAgent: Senior System Architect
- AgentRouter: Routes to appropriate agent
"""

from agents.base import BaseAgent
from agents.elena import ElenaAgent
from agents.router import AgentRouter, get_agent_router

__all__ = [
    "BaseAgent",
    "ElenaAgent",
    "AgentRouter",
    "get_agent_router",
]
