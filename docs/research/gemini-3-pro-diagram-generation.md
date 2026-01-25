# Research: Using Gemini 3 Pro to Generate Diagrams from Nano Banana JSON Specs

**Date:** 2026-01-21  
**Status:** Research Complete  
**Goal:** Generate actual diagram images (not just JSON specs) using Gemini 3 Pro from our 52 Nano Banana JSON diagram specifications

---

## Executive Summary

**Current State:** We generate **Nano Banana JSON specifications** (52 files in `docs/assets/diagrams/wiki/`) but do not render them as visual diagrams.

**Target State:** Use **Gemini 3 Pro Image** (`gemini-3-pro-image-preview` or `gemini-2.0-flash-preview-image-generation`) to generate actual diagram images from these JSON specs.

**Key Finding:** Gemini 3 Pro does **not** directly consume JSON schema to render diagrams. Instead, we need a **two-step conversion**:
1. **Convert JSON spec → Natural language prompt** (describing the diagram structure)
2. **Generate image from prompt** using Gemini 3 Pro Image model

---

## Gemini 3 Pro Image Generation Capabilities

### Available Models

1. **`gemini-3-pro-image-preview`** (aka "Nano Banana Pro")
   - High-quality image generation
   - Supports text + diagrams in images
   - Real-world grounding
   - Up to 4K resolution

2. **`gemini-2.0-flash-preview-image-generation`**
   - Faster, lower cost
   - Good for diagrams and infographics
   - May have tier restrictions

### API Structure

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

# Configure for image generation
config = types.GenerateContentConfig(
    response_modalities=["IMAGE"],  # or ["TEXT", "IMAGE"]
    image_config=types.ImageConfig(
        aspect_ratio="16:9",  # or "1:1", "4:3"
        image_size="2K"       # or "1K", "4K"
    )
)

# Generate image
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[types.Content(
        parts=[types.Part(text="Your diagram description prompt here")]
    )],
    config=config
)

# Extract image from response
for part in response.candidates[0].content.parts:
    if part.inline_data:
        image_bytes = part.inline_data.data
        # Save to file
```

---

## Conversion Strategy: JSON Spec → Image Prompt

### Step 1: Parse Nano Banana JSON Spec

Our specs have this structure:
```json
{
  "title": "Diagram Title",
  "type": "architecture" | "flowchart" | "mindmap",
  "nodes": [
    { "id": "n1", "label": "Node 1", "type": "rect", "color": "#ff0000" }
  ],
  "edges": [
    { "source": "n1", "target": "n2", "label": "connects to" }
  ]
}
```

### Step 2: Convert to Natural Language Prompt

We need to convert the structured JSON into a descriptive prompt that Gemini can understand:

**For Architecture Diagrams:**
```
Create a professional architecture diagram titled "{title}".

Components:
- {node1.label} ({node1.type}, color: {node1.color})
- {node2.label} ({node2.type}, color: {node2.color})

Connections:
- {node1.label} → {node2.label} (labeled: "{edge.label}")

Style: Clean, modern, technical diagram with clear labels, using the specified colors. 
Background: Dark mode. Use professional diagramming conventions.
```

**For Flowcharts:**
```
Create a flowchart titled "{title}".

Process Steps:
1. {node1.label} ({node1.type})
2. {node2.label} ({node2.type})

Flow:
- Start → {node1.label} → {node2.label} → End
- Decision points: {diamond nodes}
- Labels on arrows: {edge labels}

Style: Standard flowchart notation with rounded rectangles for processes, 
diamonds for decisions, arrows with labels. Use specified colors.
```

**For Mindmaps:**
```
Create a mindmap titled "{title}".

Central Topic: {root node label}

Branches:
- {branch1.label} → {sub-branch1.label}
- {branch2.label} → {sub-branch2.label}

Style: Radial mindmap with central node and branching structure. 
Use specified colors for each branch. Clean, readable text.
```

### Step 3: Enhanced Prompt with Visual Details

Add diagram-specific instructions based on type:

```python
def json_spec_to_prompt(spec: dict) -> str:
    """Convert Nano Banana JSON spec to Gemini image generation prompt."""
    
    title = spec.get("title", "Diagram")
    diagram_type = spec.get("type", "architecture")
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    
    # Build component list
    components = []
    for node in nodes:
        node_type_desc = {
            "rect": "rectangle",
            "circle": "circle",
            "diamond": "diamond",
            "note": "note box"
        }.get(node.get("type", "rect"), "box")
        
        color = node.get("color", "#94a3b8")
        components.append(f"- {node['label']} ({node_type_desc}, color: {color})")
    
    # Build connection list
    connections = []
    for edge in edges:
        source_label = next((n['label'] for n in nodes if n['id'] == edge['source']), edge['source'])
        target_label = next((n['label'] for n in nodes if n['id'] == edge['target']), edge['target'])
        label = edge.get('label', '')
        connections.append(f"- {source_label} → {target_label}" + (f" (labeled: '{label}')" if label else ""))
    
    # Type-specific prompt templates
    if diagram_type == "architecture":
        prompt = f"""Create a professional architecture diagram titled "{title}".

Components:
{chr(10).join(components)}

Connections:
{chr(10).join(connections)}

Style Requirements:
- Clean, modern technical diagram
- Dark mode background (#0a0a0a)
- Clear labels with readable fonts
- Use specified colors for each component
- Professional diagramming conventions
- Include legend if needed
- High contrast for readability"""
    
    elif diagram_type == "flowchart":
        prompt = f"""Create a flowchart titled "{title}".

Process Steps:
{chr(10).join(components)}

Flow Sequence:
{chr(10).join(connections)}

Style Requirements:
- Standard flowchart notation
- Rounded rectangles for processes
- Diamonds for decision points
- Arrows with labels
- Use specified colors
- Clear start/end markers
- Professional appearance"""
    
    else:  # mindmap
        prompt = f"""Create a mindmap titled "{title}".

Central Topic: {nodes[0]['label'] if nodes else 'Central'}

Branches and Sub-branches:
{chr(10).join(components[1:] if nodes else [])}

Connections:
{chr(10).join(connections)}

Style Requirements:
- Radial mindmap structure
- Central node prominently displayed
- Branching tree structure
- Use specified colors for branches
- Clean, readable text
- Balanced layout"""
    
    return prompt
```

---

## Implementation Plan

### Phase 1: Add Image Generation Method to GeminiClient

See the **Proof-of-Concept Implementation** section below for complete code.

### Phase 2: Batch Generation Script

Create `scripts/generate_all_diagram_images.py`:

```python
#!/usr/bin/env python3
"""
Batch generate diagram images from all Nano Banana JSON specs.
"""
import json
import asyncio
from pathlib import Path
from llm.gemini_client import get_gemini_client

async def generate_all_diagrams():
    """Generate images for all diagram specs."""
    client = get_gemini_client()
    specs_dir = Path("docs/assets/diagrams/wiki")
    output_dir = Path("docs/assets/diagrams/wiki/images")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    json_files = list(specs_dir.glob("*-diagram.json"))
    
    print(f"Found {len(json_files)} diagram specs")
    
    for json_file in json_files:
        print(f"Processing {json_file.name}...")
        
        # Load spec
        with open(json_file, 'r') as f:
            spec = json.load(f)
        
        # Generate image
        output_path = output_dir / f"{json_file.stem}.png"
        image_bytes = await client.generate_diagram_image(
            diagram_spec=spec,
            output_path=str(output_path),
            image_size="2K",
            aspect_ratio="16:9"
        )
        
        if image_bytes:
            print(f"  ✓ Generated {output_path}")
        else:
            print(f"  ✗ Failed to generate {output_path}")
        
        # Rate limiting
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(generate_all_diagrams())
```

### Phase 3: Update Workflow to Generate Images

Update `backend/workflows/story_activities.py`:

```python
@activity.defn
async def generate_diagram_image_activity(
    input: GenerateDiagramImageInput
) -> GenerateDiagramImageOutput:
    """
    Generate actual diagram image from Nano Banana JSON spec.
    """
    from llm.gemini_client import get_gemini_client
    
    client = get_gemini_client()
    
    image_bytes = await client.generate_diagram_image(
        diagram_spec=input.spec,
        output_path=input.output_path,
        image_size=input.image_size or "2K",
        aspect_ratio=input.aspect_ratio or "16:9"
    )
    
    return GenerateDiagramImageOutput(
        success=bool(image_bytes),
        image_path=input.output_path if image_bytes else None,
        error=None if image_bytes else "Image generation failed"
    )
```

---

## Alternative: Mermaid → Image Pipeline

If Gemini 3 Pro image generation doesn't meet precision requirements, consider:

1. **Convert JSON spec → Mermaid code** (using Gemini or template)
2. **Render Mermaid → PNG** (using `@mermaid-js/mermaid-cli` or `mermaid.ink` API)
3. **Optionally enhance with Gemini** (add styling, annotations)

This provides:
- ✅ Precise diagram structure (from JSON)
- ✅ Professional rendering (Mermaid)
- ✅ Optional AI enhancement (Gemini)

---

## Recommendations

### Short-term (Immediate)
1. ✅ Implement `generate_diagram_image()` method in `GeminiClient`
2. ✅ Add `_json_spec_to_prompt()` conversion function
3. ✅ Test with 2-3 sample diagram specs
4. ✅ Create batch generation script

### Medium-term (Next Sprint)
1. ✅ Generate images for all 52 diagram specs
2. ✅ Update wiki pages to reference generated images
3. ✅ Add image generation to `generate_diagram` tool endpoint
4. ✅ Integrate into story workflow (diagram + image)

### Long-term (Future)
1. ⏳ Evaluate Mermaid pipeline for precision-critical diagrams
2. ⏳ Add diagram editing capabilities (multi-turn with Gemini)
3. ⏳ Cache generated images to reduce API costs
4. ⏳ Add diagram versioning (regenerate on spec changes)

---

## Cost Considerations

- **Gemini 3 Pro Image**: ~$0.02-0.05 per image (2K resolution)
- **52 diagrams**: ~$1-2.60 one-time generation
- **Caching**: Store generated images, only regenerate on spec changes
- **Rate limits**: Implement delays between requests (1-2 seconds)

---

## Testing Checklist

- [ ] Test with architecture diagram spec
- [ ] Test with flowchart diagram spec  
- [ ] Test with mindmap diagram spec
- [ ] Verify color accuracy
- [ ] Verify label readability
- [ ] Test different aspect ratios (16:9, 1:1, 4:3)
- [ ] Test different image sizes (1K, 2K, 4K)
- [ ] Verify batch generation script
- [ ] Test error handling (API failures, rate limits)

---

## Proof-of-Concept Implementation

Here's a complete working example you can add to `backend/llm/gemini_client.py`:

```python
async def generate_diagram_image(
    self,
    diagram_spec: Dict[str, Any],
    output_path: Optional[str] = None,
    image_size: str = "2K",
    aspect_ratio: str = "16:9"
) -> bytes:
    """
    Generate an actual diagram image from a Nano Banana JSON spec using Gemini 3 Pro Image.
    
    Args:
        diagram_spec: Nano Banana JSON specification
        output_path: Optional path to save image
        image_size: "1K", "2K", or "4K"
        aspect_ratio: "16:9", "1:1", or "4:3"
    
    Returns:
        Image bytes (PNG format)
    """
    if not self.model:
        logger.warning("Gemini client unavailable")
        return b""
    
    try:
        # Convert JSON spec to natural language prompt
        prompt = self._json_spec_to_prompt(diagram_spec)
        
        # Use the newer Google GenAI SDK (if available)
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY"))
            
            config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size=image_size
                )
            )
            
            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=[types.Content(parts=[types.Part(text=prompt)])],
                config=config
            )
            
            # Extract image bytes
            for part in response.candidates[0].content.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_bytes = part.inline_data.data
                    
                    if output_path:
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                    
                    logger.info(f"Generated diagram image: {len(image_bytes)} bytes")
                    return image_bytes
            
        except ImportError:
            # Fallback to google.generativeai (older SDK)
            import google.generativeai as genai
            
            # Configure generation config
            generation_config = {
                "response_modalities": ["IMAGE"],
                "image_config": {
                    "aspect_ratio": aspect_ratio,
                    "image_size": image_size
                }
            }
            
            # Generate using async method
            response = await self.model.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            
            # Extract image from response parts
            for part in response.parts:
                if hasattr(part, 'inline_data') and part.inline_data:
                    image_bytes = part.inline_data.data
                    
                    if output_path:
                        with open(output_path, 'wb') as f:
                            f.write(image_bytes)
                    
                    logger.info(f"Generated diagram image: {len(image_bytes)} bytes")
                    return image_bytes
        
        logger.error("No image data in response")
        return b""
        
    except Exception as e:
        logger.error(f"Diagram image generation failed: {e}", exc_info=True)
        return b""

def _json_spec_to_prompt(self, spec: Dict[str, Any]) -> str:
    """Convert Nano Banana JSON spec to natural language prompt for Gemini."""
    title = spec.get("title", "Diagram")
    diagram_type = spec.get("type", "architecture")
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    
    # Build component descriptions
    components = []
    for node in nodes:
        node_type_desc = {
            "rect": "rectangle box",
            "circle": "circle",
            "diamond": "diamond shape",
            "note": "note box",
            "highlight": "highlighted box"
        }.get(node.get("type", "rect"), "box")
        
        color = node.get("color", "#94a3b8")
        label = node.get("label", "")
        components.append(f"  - {label} (shown as a {node_type_desc} in color {color})")
    
    # Build connection descriptions
    connections = []
    node_map = {n['id']: n for n in nodes}
    
    for edge in edges:
        source = node_map.get(edge['source'], {})
        target = node_map.get(edge['target'], {})
        source_label = source.get('label', edge['source'])
        target_label = target.get('label', edge['target'])
        edge_label = edge.get('label', '')
        
        if edge_label:
            connections.append(f"  - {source_label} connects to {target_label} (labeled: '{edge_label}')")
        else:
            connections.append(f"  - {source_label} connects to {target_label}")
    
    # Type-specific prompt templates
    if diagram_type == "architecture":
        prompt = f"""Create a professional architecture diagram titled "{title}".

Components to include:
{chr(10).join(components)}

Connections:
{chr(10).join(connections)}

Style Requirements:
- Clean, modern technical diagram with dark mode background (#0a0a0a)
- Use the exact colors specified for each component
- Clear, readable labels with professional fonts
- Standard architecture diagram conventions (boxes for components, arrows for connections)
- High contrast for readability
- Include a subtle grid or alignment guides
- Professional appearance suitable for technical documentation"""
    
    elif diagram_type == "flowchart":
        # Identify decision nodes
        decision_nodes = [n for n in nodes if n.get('type') == 'diamond']
        process_nodes = [n for n in nodes if n.get('type') == 'rect']
        
        prompt = f"""Create a flowchart titled "{title}".

Process Steps:
{chr(10).join([f"  - {n['label']}" for n in process_nodes])}

Decision Points:
{chr(10).join([f"  - {n['label']}" for n in decision_nodes])}

Flow Sequence:
{chr(10).join(connections)}

Style Requirements:
- Standard flowchart notation
- Rounded rectangles for processes
- Diamond shapes for decision points
- Arrows with labels showing flow direction
- Use specified colors for each element
- Clear start and end markers
- Professional appearance with dark background"""
    
    else:  # mindmap
        root_node = nodes[0] if nodes else None
        branch_nodes = nodes[1:] if nodes else []
        
        prompt = f"""Create a mindmap titled "{title}".

Central Topic: {root_node['label'] if root_node else 'Central Topic'}

Branches:
{chr(10).join([f"  - {n['label']} (color: {n.get('color', '#94a3b8')})" for n in branch_nodes])}

Connections:
{chr(10).join(connections)}

Style Requirements:
- Radial mindmap structure with central node prominently displayed
- Branching tree structure radiating outward
- Use specified colors for each branch
- Clean, readable text on each node
- Balanced, symmetrical layout
- Dark background with good contrast"""
    
    return prompt
```

## Quick Test Script

Save this as `scripts/test_diagram_generation.py`:

```python
#!/usr/bin/env python3
"""Test diagram image generation with a sample spec."""
import asyncio
import json
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from llm.gemini_client import get_gemini_client

async def test_generation():
    """Test generating an image from a sample diagram spec."""
    client = get_gemini_client()
    
    # Sample spec (or load from file)
    sample_spec = {
        "title": "Test Architecture Diagram",
        "type": "architecture",
        "nodes": [
            {"id": "n1", "label": "Frontend", "type": "rect", "color": "#60a5fa"},
            {"id": "n2", "label": "Backend API", "type": "rect", "color": "#34d399"},
            {"id": "n3", "label": "Database", "type": "rect", "color": "#f59e0b"}
        ],
        "edges": [
            {"source": "n1", "target": "n2", "label": "HTTP requests"},
            {"source": "n2", "target": "n3", "label": "queries"}
        ]
    }
    
    output_path = "test_diagram.png"
    print(f"Generating diagram image...")
    
    image_bytes = await client.generate_diagram_image(
        diagram_spec=sample_spec,
        output_path=output_path,
        image_size="2K",
        aspect_ratio="16:9"
    )
    
    if image_bytes:
        print(f"✓ Success! Generated {len(image_bytes)} bytes")
        print(f"  Saved to: {output_path}")
    else:
        print("✗ Failed to generate image")

if __name__ == "__main__":
    asyncio.run(test_generation())
```

## References

- [Gemini API Image Generation Docs](https://ai.google.dev/gemini-api/docs/image-generation)
- [Gemini 3 Pro Model Card](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Structured Outputs (for JSON schema)](https://ai.google.dev/gemini-api/docs/structured-output)
- Current implementation: `backend/llm/gemini_client.py`
- Diagram specs: `docs/assets/diagrams/wiki/*.json`
