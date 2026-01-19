import os
import logging
from typing import Optional, Union, Dict, Any

from core.config import get_settings

logger = logging.getLogger(__name__)

class ClaudeClient:
    """
    Client for Anthropic Claude (Sage's Storyteller Engine).
    Configured for high-fidelity narrative generation using the "Opus 4.5" intent.
    """
    
    def __init__(self):
        settings = get_settings()
        api_key = settings.anthropic_api_key
        
        # Fallback to env var if not in settings
        if not api_key:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not found. Claude client will fail if used.")
            self.client = None
        else:
            try:
                from anthropic import AsyncAnthropic
                self.client = AsyncAnthropic(api_key=api_key)
            except ImportError:
                logger.error("anthropic library not installed. Please install 'anthropic'.")
                self.client = None

        # Model configuration - "Opus 4.5" (2026 Standard)
        self.model = "claude-4.5-opus" 
        self.max_tokens = 8192

    async def generate_story(
        self, 
        topic: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a narrative story based on a topic and context.
        Uses specialized system prompts for Sage's persona.
        """
        if not self.client:
            raise RuntimeError("Claude client not initialized (missing key or library)")

        system_prompt = """You are Sage, the Chief Storyteller for the OpenContextGraph platform.
You are running on the advanced 'Opus 4.5' narrative engine.

Your Goal:
Transform technical topics into compelling, human-centric narratives ("Stories").
Stories should be engaging, insightful, and connect dot between disparate data points.

Structure:
1. Title: Catchy and relevant.
2. The Hook: Draw the reader in.
3. The Deep Dive: Explore the technical details with clarity.
4. The Insight: Why does this matter? What is the larger context?
5. Conclusion: A forward-looking wrap-up.

Tone:
Empathetic, intelligent, slightly futuristic but grounded.
"""

        user_prompt = f"Topic: {topic}\n"
        if context:
            user_prompt += f"\nContext:\n{context}\n"
        
        user_prompt += "\nOutput the story as a JSON object with keys: 'title' and 'content' (markdown)."

        try:
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.7,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Simple parsing of the response
            # In a real scenario, we'd use function calling or strict JSON mode
            response_text = message.content[0].text
            
            # Attempt to find JSON if wrapped in markdown code blocks
            import json
            import re
            
            # Remove markdown code blocks if present
            clean_text = re.sub(r'```json\s*', '', response_text)
            clean_text = re.sub(r'```\s*$', '', clean_text)
            
            try:
                data = json.loads(clean_text)
                return data
            except json.JSONDecodeError:
                # Fallback if raw text
                logger.warning("Failed to parse JSON from Claude response, returning raw text")
                return {
                    "title": topic,
                    "content": response_text
                }

        except Exception as e:
            logger.error(f"Claude generation error: {e}")
            raise

_client_instance = None

def get_claude_client() -> ClaudeClient:
    """Singleton accessor for ClaudeClient"""
    global _client_instance
    if _client_instance is None:
        _client_instance = ClaudeClient()
    return _client_instance
