"""
Elena - Senior System Architect Agent

Expertise:
- System architecture analysis
- Technical guidance
- Security assessment
- Integration patterns

OpenContextGraph - Brain Layer
"""

import logging
import os
from typing import Optional

from agents.base import BaseAgent
from core.context import EnterpriseContext

logger = logging.getLogger(__name__)


class ElenaAgent(BaseAgent):
    """
    Elena - Senior System Architect
    
    Provides technical architecture analysis, security guidance,
    and system design recommendations.
    """
    
    SYSTEM_PROMPT = """You are Elena, a Senior System Architect with deep expertise in:
- Distributed systems and microservices architecture
- Security architecture and compliance (NIST, FedRAMP)
- Enterprise integration patterns
- AI/ML system design and deployment

You are precise, authoritative, and detail-oriented. You base your answers on 
the provided context and always cite your sources when available.

Guidelines:
1. Provide specific, actionable technical guidance
2. Consider security implications in all recommendations
3. Reference relevant standards and best practices
4. Acknowledge uncertainty when appropriate

Current user: {user_id}
Tenant: {tenant_id}
"""
    
    def __init__(self, model: str = None):
        super().__init__(
            agent_id="elena",
            display_name="Elena",
            system_prompt=self.SYSTEM_PROMPT,
            model=model or os.getenv("LLM_MODEL", "gpt-4o")
        )
    
    def get_tools(self) -> list:
        """Elena's available tools."""
        return [
            {
                "name": "search_architecture_docs",
                "description": "Search architecture documentation and technical specs",
            },
            {
                "name": "generate_diagram",
                "description": "Generate architecture diagram in Mermaid format",
            },
            {
                "name": "security_assessment",
                "description": "Perform security assessment on a design or implementation",
            },
        ]
    
    async def _execute(
        self, 
        message: str, 
        context: EnterpriseContext
    ) -> tuple[str, list[dict]]:
        """
        Execute Elena's reasoning.
        
        Uses LLM provider (OpenAI, Azure OpenAI, or vLLM)
        with memory context for grounded responses.
        """
        tool_calls = []
        
        try:
            # Build messages for LLM
            system_prompt = self.format_system_prompt(context)
            
            # Add memory context
            memory_context = ""
            if context.semantic.facts:
                memory_context = "\n\nRelevant context from memory:\n"
                for fact in context.semantic.facts[:5]:
                    memory_context += f"- {fact.content}\n"
            
            # Try to use LLM
            response = await self._call_llm(
                system_prompt + memory_context,
                message,
                context
            )
            
            return response, tool_calls
            
        except Exception as e:
            logger.error(f"Elena execution error: {e}")
            
            # Fallback response
            return (
                f"I understand you're asking about: {message[:100]}... "
                f"I'm currently unable to provide a detailed response, "
                f"but I can help once my LLM connection is restored.",
                tool_calls
            )
    
    async def _call_llm(
        self, 
        system_prompt: str, 
        message: str,
        context: EnterpriseContext
    ) -> str:
        """
        Call the configured LLM provider.
        
        Supports:
        - OpenAI API
        - Azure OpenAI
        - vLLM (OpenAI-compatible)
        - Ollama (OpenAI-compatible)
        """
        import httpx
        
        llm_provider = os.getenv("LLM_PROVIDER", "openai")
        llm_api_base = os.getenv("LLM_API_BASE", "https://api.openai.com/v1")
        llm_api_key = os.getenv("LLM_API_KEY", "")
        llm_model = os.getenv("LLM_MODEL", "gpt-4o")
        
        # Build request
        messages = [
            {"role": "system", "content": system_prompt},
        ]
        
        # Add recent conversation history
        for msg in context.episodic.recent_messages[-5:]:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": llm_model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
        }
        
        headers = {
            "Content-Type": "application/json",
        }
        
        if llm_api_key:
            headers["Authorization"] = f"Bearer {llm_api_key}"
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{llm_api_base.rstrip('/')}/chat/completions",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
