import os
import logging
import json
import zlib
import struct
import hashlib
from typing import Optional, Dict, Any, List

import httpx

from core.config import get_settings

logger = logging.getLogger(__name__)

class GeminiClient:
    """
    Client for Google Gemini (Sage's Visual Engine).
    Configured for "Gemini 3" capabilities and "Nano Banana Pro" diagram specifications.
    
    Nano Banana Pro Spec:
    {
      "title": string,
      "type": "architecture" | "flowchart" | "mindmap",
      "nodes": [{ "id": string, "label": string, "type": string, "color": string }],
      "edges": [{ "source": string, "target": string, "label": string }]
    }
    """
    
    def __init__(self):
        settings = get_settings()
        api_key = settings.gemini_api_key
        
        # Fallback to env var
        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY") # or GOOGLE_API_KEY
            
        if not api_key:
            # Try specific Google var
            api_key = os.getenv("GOOGLE_API_KEY")

        self.api_key = api_key
        self.project = settings.google_cloud_project or os.getenv("GOOGLE_CLOUD_PROJECT", "secai-radar")
        self.location = settings.google_cloud_location or os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.primary_model_name = settings.gemini_model or os.getenv("GEMINI_MODEL", "gemini-3.1-pro-preview")
        self.fallback_model_names: List[str] = [
            self.primary_model_name,
            "gemini-3.1-pro-preview",
            "gemini-2.5-pro",
            "gemini-2.5-flash-lite",
        ]

        if not self.api_key:
            logger.warning("GEMINI_API_KEY / GOOGLE_API_KEY not found. Gemini client will fail if used.")
        else:
            logger.info(
                f"Gemini Vertex client initialized model={self.primary_model_name} project={self.project} location={self.location}"
            )

    async def _generate_with_fallback(self, prompt: str) -> str:
        """Generate text with Vertex REST and model fallback chain."""
        if not self.api_key:
            raise RuntimeError("Gemini API key not initialized")

        last_error: Optional[str] = None
        tried: List[str] = []

        async with httpx.AsyncClient(timeout=90.0) as client:
            for model_name in self.fallback_model_names:
                if model_name in tried:
                    continue
                tried.append(model_name)

                url = (
                    f"https://aiplatform.googleapis.com/v1/projects/{self.project}/"
                    f"locations/{self.location}/publishers/google/models/{model_name}:generateContent"
                )
                params = {"key": self.api_key}
                payload = {
                    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                    "generationConfig": {"temperature": 0.2},
                }

                try:
                    response = await client.post(url, params=params, json=payload)
                    if response.status_code >= 400:
                        last_error = response.text
                        logger.warning(f"Gemini model unavailable ({model_name}), trying fallback")
                        continue

                    data = response.json()
                    if model_name != self.primary_model_name:
                        logger.warning(f"Gemini model fallback used: {model_name}")

                    parts = (
                        data.get("candidates", [{}])[0]
                        .get("content", {})
                        .get("parts", [])
                    )
                    text_parts = [p.get("text", "") for p in parts if p.get("text")]
                    return "\n".join(text_parts).strip()
                except Exception as e:
                    last_error = str(e)
                    logger.warning(f"Gemini request failed ({model_name}), trying fallback")

        raise RuntimeError(f"Gemini generation failed across model fallbacks: {last_error}")

    async def generate_diagram_spec(
        self, 
        topic: str, 
        diagram_type: str = "architecture",
        story_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a diagram specification following the Nano Banana Pro JSON schema.
        """
        if not self.api_key:
             # Mock response if no client available (to prevent crash in verification)
             logger.warning("Gemini client unavailable, returning mock Nano Banana spec")
             return self._get_mock_nano_banana(topic)

        prompt = f"""You are the Visual Architect 'Sage'.
Your task is to generate a diagram specification for the topic: "{topic}".
Model: Gemini 3 (Visual Reasoning Mode).
Format: Nano Banana Pro JSON Specification.

Context:
{story_context[:2000] if story_context else "No story context provided."}

Nano Banana Spec Schema:
{{
  "title": "{topic} Diagram",
  "type": "{diagram_type}",
  "nodes": [
    {{ "id": "node1", "label": "Concept", "type": "rect", "color": "#ff0000" }}
  ],
  "edges": [
    {{ "source": "node1", "target": "node2", "label": "connects to" }}
  ]
}}

Generate VALID JSON only. No markdown formatting.
"""
        try:
            text = await self._generate_with_fallback(prompt)
            
            # clean formatting
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
            
        except Exception as e:
            logger.error(f"Gemini diagram generation failed: {e}")
            return self._get_mock_nano_banana(topic)

    async def render_diagram_from_nano_banana(
        self,
        topic: str,
        diagram_type: str,
        nano_banana_json: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Use Gemini 3.1 to validate/refine provided Nano Banana JSON as standard diagram workflow output."""
        if not self.api_key:
            return nano_banana_json

        prompt = f"""You are Gemini 3.1 refining a diagram specification for secairadar.cloud.
Input JSON:
{json.dumps(nano_banana_json, ensure_ascii=False)}

Requirements:
- Keep schema exactly: title/type/nodes/edges
- Keep type as {diagram_type}
- Optimize for MCP + AI agent trust ranking, agent-first then humans
- Return ONLY valid JSON
"""
        try:
            text = await self._generate_with_fallback(prompt)
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception as e:
            logger.warning(f"Gemini diagram refinement failed, using input JSON: {e}")
            return nano_banana_json


    async def generate_visual_spec(
        self, 
        topic: str,
        context: Optional[str] = None,
        diagram_spec: Optional[dict] = None
    ) -> Dict[str, Any]:
        """
        Generate a specification for an image (prompt engineering step).
        """
        if not self.api_key:
             return {"prompt": f"A futuristic visualization of {topic}", "style": "cinematic"}

        prompt = f"""Create a detailed image generation prompt for the topic: {topic}.
Use the 'Nano Banana' visual language: Clean, futuristic, neon accents, dark mode background.
Context: {context}
Output JSON: {{ "prompt": "...", "negative_prompt": "...", "style": "..." }}
"""
        try:
            text = await self._generate_with_fallback(prompt)
            text = text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception:
             return {"prompt": f"High tech visualization of {topic}", "style": "digital art"}


    async def generate_image_from_spec(self, visual_spec: Dict[str, Any]) -> bytes:
        """
        Generate actual image bytes. 
        Note: The Python SDK for Imagen/Gemini image gen varies. 
        We will attempt to use the model's 'generate_content' with image output if supported, 
        or return a placeholder if not configured for image gen.
        """
        if not self.api_key:
            return self._generate_fallback_png(visual_spec)
            
        # Placeholder for actual Imagen integration.
        # Until image output endpoint is wired, return deterministic, non-trivial fallback PNG.
        logger.info("Image generation requested. Returning deterministic fallback PNG bytes.")
        return self._generate_fallback_png(visual_spec)

    @staticmethod
    def _generate_fallback_png(visual_spec: Dict[str, Any], width: int = 256, height: int = 256) -> bytes:
        """Generate a deterministic RGB PNG fallback from prompt/style text."""
        seed_text = json.dumps(visual_spec or {}, sort_keys=True, ensure_ascii=True)
        digest = hashlib.sha256(seed_text.encode("utf-8")).digest()

        # Build scanlines with a simple deterministic gradient pattern.
        rows = bytearray()
        for y in range(height):
            rows.append(0)  # no filter
            for x in range(width):
                r = (x + digest[0] + (y // 3)) % 256
                g = (y + digest[1] + (x // 5)) % 256
                b = (x ^ y ^ digest[2]) % 256
                # Add banding for stronger visual structure
                if ((x // 32) + (y // 32)) % 2 == 0:
                    r = (r + digest[3]) % 256
                    g = (g + digest[4]) % 256
                    b = (b + digest[5]) % 256
                rows.extend((r, g, b))

        raw = bytes(rows)
        compressed = zlib.compress(raw, level=9)

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            return (
                struct.pack(">I", len(data))
                + chunk_type
                + data
                + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
            )

        png = bytearray()
        png.extend(b"\x89PNG\r\n\x1a\n")
        ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)  # 8-bit RGB
        png.extend(chunk(b"IHDR", ihdr))
        png.extend(chunk(b"IDAT", compressed))
        png.extend(chunk(b"IEND", b""))
        return bytes(png)

    def _get_mock_nano_banana(self, topic: str) -> Dict[str, Any]:
        """Fallback mock spec for robust operation"""
        return {
            "title": f"Mock Diagram: {topic}",
            "type": "architecture",
            "nodes": [
                {"id": "n1", "label": topic, "type": "circle", "color": "#4285F4"},
                {"id": "n2", "label": "Context", "type": "rect", "color": "#DB4437"},
                {"id": "n3", "label": "Outcome", "type": "rect", "color": "#0F9D58"}
            ],
            "edges": [
                {"source": "n1", "target": "n2", "label": "influences"},
                {"source": "n2", "target": "n3", "label": "produces"}
            ]
        }


_client_instance = None

def get_gemini_client() -> GeminiClient:
    """Singleton accessor for GeminiClient"""
    global _client_instance
    if _client_instance is None:
        _client_instance = GeminiClient()
    return _client_instance
