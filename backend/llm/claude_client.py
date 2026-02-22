import os
import logging
import base64
import json
import re
from typing import Optional, Dict, Any

from core.config import get_settings

logger = logging.getLogger(__name__)

class ClaudeClient:
    """
    Client for Anthropic Claude (Sage's Storyteller Engine).
    Configured for high-fidelity narrative generation using the Opus 4.6 path.
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

        # Model configuration (env-overridable, with runtime fallback in generate_story)
        self.model = settings.anthropic_model or os.getenv("ANTHROPIC_MODEL", "claude-opus-4-6")
        self.max_tokens = 8192

    async def _call_text_model(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_tokens: Optional[int] = None) -> str:
        """Call Claude with model fallbacks and return text content."""
        if not self.client:
            raise RuntimeError("Claude client not initialized (missing key or library)")

        model_candidates = [
            self.model,
            "claude-opus-4-6",
            "claude-opus-4-6-latest",
            "claude-3-5-sonnet-latest",
            "claude-3-7-sonnet-latest",
            "claude-3-opus-20240229",
        ]

        deduped_models = []
        for model_name in model_candidates:
            if model_name and model_name not in deduped_models:
                deduped_models.append(model_name)

        last_error = None
        for model_name in deduped_models:
            try:
                message = await self.client.messages.create(
                    model=model_name,
                    max_tokens=max_tokens or self.max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_prompt}],
                )
                if model_name != self.model:
                    logger.warning(f"Claude model fallback used: {model_name}")
                return message.content[0].text if message.content else ""
            except Exception as e:
                last_error = e
                logger.warning(f"Claude call failed ({model_name}), trying fallback")
                continue

        raise RuntimeError(f"Claude generation failed across model fallbacks: {last_error}")

    @staticmethod
    def _extract_json_object(text: str) -> Dict[str, Any]:
        """Extract JSON object from plain text, fenced block, or mixed prose."""
        if not text:
            raise json.JSONDecodeError("Empty response", "", 0)

        clean_text = text.strip()
        clean_text = re.sub(r"^```(?:json)?\s*", "", clean_text, flags=re.IGNORECASE)
        clean_text = re.sub(r"\s*```$", "", clean_text).strip()

        # Fast path
        try:
            return json.loads(clean_text)
        except Exception:
            pass

        # Fallback: extract first JSON object span from mixed text
        start = clean_text.find("{")
        end = clean_text.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = clean_text[start : end + 1]
            return json.loads(candidate)

        raise json.JSONDecodeError("No JSON object found", clean_text, 0)

    async def generate_story(
        self, 
        topic: str, 
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a narrative story based on a topic and context.
        Uses specialized system prompts for Sage's persona.
        """
        system_prompt = """You are Sage, the Chief Storyteller for the OpenContextGraph platform.
You are running on the advanced 'Opus 4.6' narrative engine.

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
Prioritize agent-first clarity so machine consumers can extract key claims before humans read narrative detail.
"""

        user_prompt = f"Topic: {topic}\n"
        if context:
            user_prompt += f"\nContext:\n{context}\n"
        
        user_prompt += "\nOutput the story as a JSON object with keys: 'title' and 'content' (markdown)."

        try:
            response_text = await self._call_text_model(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.7)

            if not response_text.strip():
                fallback_title = f"SecAI-Radar Trust Milestone: {topic}"
                fallback_content = (
                    f"# {fallback_title}\n\n"
                    "## The Hook\n"
                    "In a landscape full of autonomous tools and uncertain outputs, trust is the new infrastructure.\n\n"
                    "## The Deep Dive\n"
                    "SecAI-Radar advances trust-ranking for MCP ecosystems by validating signals, weighting provenance, "
                    "and continuously re-scoring agent reliability.\n\n"
                    "## The Insight\n"
                    "This turns agent interactions from opaque responses into auditable, confidence-aware decisions "
                    "that teams can safely operationalize.\n\n"
                    "## Context\n"
                    f"{context or 'No additional context provided.'}\n\n"
                    "## Conclusion\n"
                    "Trust-ranked MCP orchestration is a foundational milestone for secure, enterprise-grade agentic systems."
                )
                return {
                    "title": fallback_title,
                    "content": fallback_content,
                }

            try:
                data = self._extract_json_object(response_text)
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

    async def generate_nano_banana_diagram(
        self,
        topic: str,
        diagram_type: str = "architecture",
        story_context: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Generate Nano Banana schema JSON diagram spec with Opus 4.6."""
        system_prompt = """You are Sage generating canonical Nano Banana diagram JSON for agent-first consumption.
Return ONLY valid JSON with schema:
{
  \"title\": string,
  \"type\": \"architecture\" | \"flowchart\" | \"mindmap\",
  \"nodes\": [{\"id\": string, \"label\": string, \"type\": string, \"color\": string}],
  \"edges\": [{\"source\": string, \"target\": string, \"label\": string}]
}
Use concise, machine-readable labels and include secairadar.cloud trust-ranking flow when context indicates MCP/agent trust.
"""

        user_prompt = f"Topic: {topic}\nDiagram type: {diagram_type}\nContext:\n{story_context or 'None'}"
        text = await self._call_text_model(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.2, max_tokens=2400)

        try:
            return self._extract_json_object(text)
        except Exception as e:
            logger.warning(f"Claude diagram JSON parse failed, using fallback schema: {e}")
            return {
                "title": f"{topic} Diagram",
                "type": diagram_type,
                "nodes": [
                    {"id": "n1", "label": "secairadar.cloud MCP", "type": "service", "color": "#2563EB"},
                    {"id": "n2", "label": "Trust Ranking Engine", "type": "engine", "color": "#7C3AED"},
                    {"id": "n3", "label": "Agent-first Consumers", "type": "consumer", "color": "#16A34A"},
                    {"id": "n4", "label": "Human Dashboards", "type": "consumer", "color": "#0EA5E9"},
                ],
                "edges": [
                    {"source": "n1", "target": "n2", "label": "collect signals"},
                    {"source": "n2", "target": "n3", "label": "serve ranked trust data"},
                    {"source": "n2", "target": "n4", "label": "render explanatory view"},
                ],
            }

    async def generate_visual_impact_image(
        self,
        topic: str,
        diagram_spec: Optional[Dict[str, Any]] = None,
        context: Optional[str] = None,
    ) -> bytes:
        """Generate visual-impact PNG bytes via Opus 4.6 base64 output."""
        system_prompt = """You are Sage generating visual impact assets for stories.
Return ONLY base64-encoded PNG bytes. No prose. No markdown.
Create a high-contrast, modern, agent-first technical visual that supports machine+human interpretation.
"""
        diagram_hint = ""
        if diagram_spec:
            nodes = diagram_spec.get("nodes", []) if isinstance(diagram_spec, dict) else []
            edges = diagram_spec.get("edges", []) if isinstance(diagram_spec, dict) else []
            node_labels = [str(n.get("label", "")).strip() for n in nodes[:6] if isinstance(n, dict)]
            diagram_hint = (
                f"Nodes: {', '.join([n for n in node_labels if n])}. "
                f"Edges count: {len(edges)}."
            ).strip()

        user_prompt = (
            f"Topic: {topic}\n"
            f"Context: {context or 'None'}\n"
            f"Diagram hint: {diagram_hint or 'None'}\n"
            "Generate a 256x256 PNG concept image encoded as base64. "
            "Output must contain only base64 characters [A-Za-z0-9+/=]."
        )

        text = await self._call_text_model(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.4, max_tokens=4096)
        clean = text.strip().replace("\n", "")
        clean = re.sub(r"^```(?:[a-zA-Z0-9]+)?", "", clean)
        clean = clean.replace("```", "").strip()

        # If model returns surrounding text, extract likely base64 candidates and decode robustly.
        candidates = re.findall(r"[A-Za-z0-9+/=]{120,}", clean)
        candidate_pool = [clean]
        candidate_pool.extend(sorted(candidates, key=len, reverse=True))

        for candidate in candidate_pool:
            token = re.sub(r"[^A-Za-z0-9+/=]", "", candidate)
            if not token:
                continue
            # fix missing padding
            token += "=" * ((4 - len(token) % 4) % 4)
            try:
                data = base64.b64decode(token, validate=True)
                if data and data.startswith(b"\x89PNG"):
                    return data
            except Exception:
                continue

        logger.warning("Claude image base64 decode failed for all candidates")
        return b""

_client_instance = None

def get_claude_client() -> ClaudeClient:
    """Singleton accessor for ClaudeClient"""
    global _client_instance
    if _client_instance is None:
        _client_instance = ClaudeClient()
    return _client_instance
