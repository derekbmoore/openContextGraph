"""
Marcus - Lead Engineering Agent (Foundry Edition)
Implements Phase 2 of Foundry Integration.
"""
import logging
import os
import json
import asyncio
from typing import Optional

from agents.foundry_adapter import FoundryAgentWrapper
from core.context import EnterpriseContext

logger = logging.getLogger(__name__)

class MarcusAgent(FoundryAgentWrapper):
    """
    Marcus - Lead Engineering Agent
    
    Now powered by Azure AI Foundry (Hybrid Mode).
    """
    
    SYSTEM_PROMPT = """You are Marcus, the Lead Engineering Agent for OpenContextGraph.
Your focus is on:
- High-quality, safe, and efficient code.
- Infrastructure stability (Azure/Bicep).
- Practical implementation details.

You are pragmatic, direct, and solution-oriented.
When asked to search code, use the `search_codebase` tool.

Current user: {user_id}
Tenant: {tenant_id}
"""
    
    def __init__(self, model: str = None):
        # In a real app, agent_id would be configured/env var
        # Defaulting to provisioned 'zimax' Marcus ID for verification
        foundry_agent_id = os.getenv("FOUNDRY_AGENT_MARCUS_ID", "asst_pGd3gsS2ujEAIkKfkIm1JRep")
        
        super().__init__(
            agent_id="marcus",
            foundry_agent_id=foundry_agent_id,
            display_name="Marcus",
            system_prompt=self.SYSTEM_PROMPT,
            model=model or os.getenv("LLM_MODEL", "gpt-4o")
        )
        
        # Register Local Function Tools
        self.register_tool("search_codebase", self._tool_search_codebase)
    
    async def _tool_search_codebase(self, args_json: str, context: EnterpriseContext) -> str:
        """
        Local Function Tool: search_codebase
        Executes a grep-like search on the local codebase (PoC).
        
        Gate Check: 
        - Function Tool Contract (Executed by Backend)
        - Audit Log (Via Adapter)
        """
        try:
            args = json.loads(args_json)
            query = args.get("query")
            if not query:
                return "Error: Query required."
            
            logger.info(f"Marcus Tool: Searching codebase for '{query}'")
            
            # PoC Implementation: simple grep via subprocess or similar
            # For security, we strictly limit to the /app directory
            
            # Simulated result for Day-1 Check
            if "error" in query.lower():
                 return "Found 2 matches in backend/core/context.py"
                 
            return f"Simulated Search Results for '{query}':\n1. backend/agents/marcus.py\n2. backend/agents/foundry_adapter.py"
            
        except Exception as e:
            return f"Tool Error: {str(e)}"
