"""
Azure AI Foundry IQ Integration Client

Handles communication with Foundry IQ knowledge bases via Azure AI Search.
Provides query capabilities for knowledge bases configured in Foundry portal.

OpenContextGraph - Foundry Integration Layer
NIST AI RMF: MANAGE 2.3 (Data Governance), MAP 1.1 (System Context)
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class FoundryIQResult(BaseModel):
    """Single result from Foundry IQ knowledge base query."""
    content: str
    score: float
    source: str
    metadata: Dict[str, Any] = {}
    citations: List[str] = []


class FoundryIQResponse(BaseModel):
    """Response from Foundry IQ knowledge base query."""
    results: List[FoundryIQResult]
    query: str
    kb_id: str
    total_results: int


class FoundryIQClient:
    """
    Client for querying Foundry IQ knowledge bases.
    
    Foundry IQ knowledge bases are built on Azure AI Search and can be accessed:
    1. Via MCP tools (when agents invoke KBs as tools)
    2. Via Azure AI Search SDK (direct query)
    
    This client provides direct query capabilities for hybrid search integration.
    """
    
    def __init__(self, settings: Any):
        """
        Initialize Foundry IQ Client.
        
        Args:
            settings: App settings containing Foundry IQ configuration
        """
        self.settings = settings
        self.use_foundry_iq = settings.use_foundry_iq
        self.kb_id = settings.foundry_iq_knowledge_base_id
        
        # Azure AI Search configuration
        # Note: Foundry IQ KBs are backed by Azure AI Search indexes
        # We'll need search endpoint and key to query directly
        self.search_endpoint = getattr(settings, 'azure_search_endpoint', None)
        self.search_key = getattr(settings, 'azure_search_key', None)
        self.search_index_name = getattr(settings, 'azure_search_index_name', None)
        
        logger.info(
            f"FoundryIQClient init: enabled={self.use_foundry_iq}, "
            f"kb_id={bool(self.kb_id)}, search_endpoint={bool(self.search_endpoint)}"
        )
        
        # Lazy-load Azure AI Search client if needed
        self._search_client = None
    
    @property
    def search_client(self):
        """Lazy-load Azure AI Search client."""
        if self._search_client is None and self.search_endpoint and self.search_key:
            try:
                from azure.search.documents import SearchClient
                from azure.core.credentials import AzureKeyCredential
                
                self._search_client = SearchClient(
                    endpoint=self.search_endpoint,
                    index_name=self.search_index_name or self.kb_id,
                    credential=AzureKeyCredential(self.search_key)
                )
                logger.info("Azure AI Search client initialized")
            except ImportError:
                logger.warning("azure-search-documents not installed. Install with: pip install azure-search-documents")
            except Exception as e:
                logger.error(f"Failed to initialize Azure AI Search client: {e}")
        
        return self._search_client
    
    async def list_knowledge_bases(self, project_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List available knowledge bases in the Foundry project.
        
        Note: This requires Foundry API access. For now, we return configured KB.
        
        Args:
            project_id: Foundry project ID (optional, uses settings if not provided)
            
        Returns:
            List of knowledge base metadata
        """
        if not self.use_foundry_iq:
            logger.warning("Foundry IQ not enabled")
            return []
        
        # TODO: Implement actual Foundry API call to list KBs
        # For now, return configured KB if available
        if self.kb_id:
            return [{
                "id": self.kb_id,
                "name": self.kb_id,  # Placeholder
                "status": "configured",
                "source_count": None,  # Unknown without API call
            }]
        
        return []
    
    async def query_knowledge_base(
        self,
        kb_id: str,
        query: str,
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        search_type: str = "hybrid"  # keyword, vector, hybrid
    ) -> FoundryIQResponse:
        """
        Query a Foundry IQ knowledge base.
        
        Args:
            kb_id: Knowledge base ID
            query: Search query
            limit: Maximum results (default: 5)
            filters: Optional filters (e.g., tenant_id, sensitivity_level)
            search_type: keyword | vector | hybrid (default: hybrid)
            
        Returns:
            FoundryIQResponse with results
        """
        if not self.use_foundry_iq:
            logger.warning("Foundry IQ not enabled")
            return FoundryIQResponse(
                results=[],
                query=query,
                kb_id=kb_id,
                total_results=0
            )
        
        # If we have Azure AI Search client, query directly
        if self.search_client:
            return await self._query_azure_search(kb_id, query, limit, filters, search_type)
        
        # Otherwise, return empty results with note
        logger.warning(
            "Azure AI Search client not configured. "
            "Foundry IQ KBs should be queried via MCP tools in Foundry agents."
        )
        
        return FoundryIQResponse(
            results=[],
            query=query,
            kb_id=kb_id,
            total_results=0
        )
    
    async def _query_azure_search(
        self,
        kb_id: str,
        query: str,
        limit: int,
        filters: Optional[Dict[str, Any]],
        search_type: str
    ) -> FoundryIQResponse:
        """Query Azure AI Search directly."""
        try:
            # Build search options
            search_options = {
                "top": limit,
                "include_total_count": True,
            }
            
            # Add filters if provided
            if filters:
                filter_string = " and ".join([f"{k} eq '{v}'" for k, v in filters.items()])
                search_options["filter"] = filter_string
            
            # Determine search mode based on search_type
            if search_type == "keyword":
                search_mode = "any"  # Match any terms
            elif search_type == "vector":
                # Vector search requires embeddings - would need query vector
                # For now, fall back to hybrid
                search_mode = "any"
            else:  # hybrid
                search_mode = "any"  # Azure AI Search handles hybrid automatically
            
            # Execute search
            results = await asyncio.to_thread(
                self.search_client.search,
                search_text=query,
                search_mode=search_mode,
                **search_options
            )
            
            # Convert results to FoundryIQResult format
            foundry_results = []
            total_count = 0
            
            async for result in results:
                if hasattr(result, '@odata.count'):
                    total_count = result['@odata.count']
                    continue
                
                # Extract content (adjust field names based on your index schema)
                content = result.get('content') or result.get('text') or result.get('chunk_text', '')
                score = result.get('@search.score', 0.0)
                source = result.get('source') or result.get('source_path') or result.get('file_path', '')
                
                # Extract metadata
                metadata = {k: v for k, v in result.items() if not k.startswith('@')}
                
                # Extract citations if available
                citations = result.get('citations', []) or []
                
                foundry_results.append(FoundryIQResult(
                    content=content,
                    score=score,
                    source=source,
                    metadata=metadata,
                    citations=citations
                ))
            
            return FoundryIQResponse(
                results=foundry_results,
                query=query,
                kb_id=kb_id,
                total_results=total_count or len(foundry_results)
            )
            
        except Exception as e:
            logger.error(f"Error querying Azure AI Search: {e}", exc_info=True)
            return FoundryIQResponse(
                results=[],
                query=query,
                kb_id=kb_id,
                total_results=0
            )
    
    async def get_kb_status(self, kb_id: str) -> Dict[str, Any]:
        """
        Get knowledge base status and health.
        
        Args:
            kb_id: Knowledge base ID
            
        Returns:
            Status information
        """
        if not self.use_foundry_iq:
            return {
                "enabled": False,
                "status": "disabled",
                "kb_id": kb_id
            }
        
        # Check if KB is configured
        is_configured = (kb_id == self.kb_id) if self.kb_id else False
        
        # Check if search client is available
        has_search_client = self.search_client is not None
        
        return {
            "enabled": self.use_foundry_iq,
            "configured": is_configured,
            "status": "available" if (is_configured and has_search_client) else "not_configured",
            "kb_id": kb_id,
            "has_search_client": has_search_client,
            "search_endpoint": bool(self.search_endpoint),
        }
