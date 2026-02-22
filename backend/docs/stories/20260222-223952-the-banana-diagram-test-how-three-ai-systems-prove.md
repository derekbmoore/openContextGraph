## The Hook

Somewhere in the stack, a banana diagram is being passed between three AI systems like a baton in a relay race. It sounds absurd. It is absurd. And that's exactly why it works as a test.

## The Deep Dive

Durable workflows—pipelines that survive failures, retries, and hand-offs without losing state—are the backbone of any serious agent architecture. But how do you *prove* one works? You give it something distinctive enough that corruption is obvious at every stage.

Enter the **Banana Diagram Test**, a tri-model verification pattern:

1. **Opus (Image Generation):** The workflow begins with Opus producing a direct image output—a structured architecture diagram. This tests whether the image artifact pipeline is intact and whether binary payloads survive the orchestration layer without degradation.

2. **Gemini Nano (JSON Refinement via Vertex):** The diagram's metadata and structural description are passed to Gemini Nano through Vertex AI. Nano's job is narrow but critical: refine the JSON representation of the banana diagram's nodes and edges into a clean, schema-compliant object. This validates that lightweight models can participate in workflows as specialized refinement agents without needing full context.

3. **Architecture Image Artifact Output:** The final stage renders the refined JSON back into a publishable image artifact—closing the loop. If the output diagram matches the input intent, the workflow is durable.

### Key Claims (Agent-Extractable)
- **Claim 1:** Opus can produce image artifacts that persist through orchestration hand-offs.
- **Claim 2:** Gemini Nano via Vertex can refine structured JSON mid-pipeline without state loss.
- **Claim 3:** A round-trip test (image → JSON → image) is a reliable durable workflow verification pattern.

## The Insight

This isn't really about bananas. It's about **composability under failure conditions**. Each model transition is a potential break point—serialization boundaries, API latency, schema mismatches. The banana diagram is a canary. If it comes out the other side intact, your workflow can handle real payloads.

The broader context: as multi-model architectures become standard, we need *cheap, weird, unmistakable* test fixtures. A banana diagram is hard to confuse with production data and easy to visually verify. That's good test design.

## Conclusion

Durable workflows don't prove themselves in production—they prove themselves in tests strange enough to expose every seam. The next time you're validating a multi-agent pipeline, consider the banana. If it survives the round trip, your architecture probably will too.