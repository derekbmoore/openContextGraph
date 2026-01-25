# Foundry IQ API Research Findings

**Date:** 2026-01-21  
**Status:** Research Complete, Ready for Development

---

## Key Findings

### 1. Foundry IQ Architecture

- **Built on:** Azure AI Search
- **Integration:** Model Context Protocol (MCP) for tool calls
- **Status:** Public preview
- **Access:** Via Foundry portal knowledge bases

### 2. Integration Pattern

**Foundry IQ connects to agents via MCP:**
- Knowledge bases are exposed as MCP tools
- When invoked, KB handles query planning, retrieval, reranking
- Results include source attribution
- Supports keyword, vector, and hybrid search

### 3. Python SDK

**Available Resources:**
- GitHub sample: `azure-sdk-for-python/tree/main/sdk/ai/azure-ai-foundry/samples/agentic-retrieval-pipeline`
- Uses Azure AI Search SDK
- REST API reference available

### 4. Key Capabilities

- **Query Planning:** Self-reflective query engine
- **Multi-source Retrieval:** Simultaneous keyword/vector/hybrid
- **Semantic Reranking:** Relevance scoring
- **Answer Synthesis:** With source references
- **Access Control:** Document-level permissions

---

## Implementation Approach

### Option 1: Direct Azure AI Search API
- Query Azure AI Search directly
- Requires search service endpoint
- More control, more complexity

### Option 2: Foundry IQ MCP Tool (Recommended)
- Use Foundry IQ as MCP tool
- Simpler integration
- Built-in query planning and reranking
- Matches our MCP architecture

### Option 3: Hybrid Approach
- Use Foundry IQ for agent queries
- Use Azure AI Search directly for our MCP tools
- Best of both worlds

**Recommendation:** Start with Option 2 (Foundry IQ MCP), add Option 3 if needed.

---

## API Patterns (Based on Research)

### Knowledge Base Query (via MCP)

```python
# Foundry IQ is accessed via MCP tool calls
# The KB is configured in Foundry portal
# Agents invoke it as a tool

# Pattern: Foundry agents can call KBs directly
# We can also query via Azure AI Search SDK if needed
```

### Azure AI Search Direct Query

```python
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# If we need direct access
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=kb_index_name,
    credential=AzureKeyCredential(search_key)
)
```

---

## Next Steps: Implementation

1. **Create Foundry IQ Client** - Query KBs via Azure AI Search
2. **Add MCP Tools** - Expose KB queries as MCP tools
3. **Implement Hybrid Search** - Fuse Foundry IQ + Tri-Search™
4. **Add Evidence Bundles** - Citations + provenance

---

## References

- [Connect Agents to Foundry IQ](https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/knowledge-retrieval)
- [Foundry IQ Overview](https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-unlocking-ubiquitous-knowledge-for-agents/4470812)
- [Python SDK Sample](https://github.com/Azure/azure-sdk-for-python/tree/main/sdk/ai/azure-ai-foundry/samples/agentic-retrieval-pipeline)
