from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any, Optional
import networkx as nx
import logging

from api.middleware.auth import get_current_user
from core import SecurityContext
from memory import get_memory_client

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("", response_model=Dict[str, Any])
async def get_memory_graph(
    query: Optional[str] = None,
    limit: int = 50,
    user: SecurityContext = Depends(get_current_user)
):
    """
    Generate a dynamic knowledge graph from Zep memory.
    Returns nodes (Episodes, Facts) and edges.
    
    Nodes:
    - User (Central)
    - Episodes (Sessions)
    - Facts (Extracted knowledge)
    """
    try:
        client = get_memory_client()
        graph = nx.MultiDiGraph()
        
        # 1. Add User Node
        user_node_id = f"user:{user.user_id}"
        graph.add_node(
            user_node_id, 
            type="meta", 
            content=f"User: {user.user_id}", 
            degree=0,
            metadata={}
        )

        # 2. Fetch Episodes (Sessions)
        # Note: list_sessions returns list of dicts based on client.py
        sessions = await client.list_sessions(user_id=user.user_id, limit=limit)
        
        session_ids = set()
        
        for session in sessions:
            session_id = session.get("session_id")
            session_ids.add(session_id)
            
            # Create Episode Node
            summary = session.get("metadata", {}).get("summary", f"Episode {session_id[:8]}...")
            if len(summary) > 50:
                 summary = summary[:47] + "..."
                 
            graph.add_node(
                session_id, 
                type="memory", 
                content=summary, 
                metadata=session.get("metadata", {}),
                degree=0
            )
            # Link to User
            graph.add_edge(user_node_id, session_id, label="participated_in", weight=1)

        # 3. Fetch Facts
        # get_facts returns List[Fact] objects
        facts = await client.get_facts(user_id=user.user_id, query=query, limit=limit)
        
        for fact in facts:
            fact_content = fact.content
            # Deduplicate facts by hash
            fact_id = f"fact:{hash(fact_content)}"
            
            if not graph.has_node(fact_id):
                graph.add_node(
                    fact_id, 
                    type="fact", 
                    content=fact_content, 
                    degree=0,
                    metadata={"confidence": fact.confidence}
                )
            
            # Link to Source Session if available and exists in graph
            source_session = fact.source
            
            if source_session and source_session in session_ids:
                graph.add_edge(source_session, fact_id, label="established", weight=1)
            else:
                # If source session not loaded (limit) or missing, link to User
                graph.add_edge(user_node_id, fact_id, label="knows", weight=0.5)

        # 4. Calculate Degrees
        for node in graph.nodes():
            graph.nodes[node]['degree'] = graph.degree(node)

        # Convert to node-link data
        data = nx.node_link_data(graph)
        
        # Calculate stats
        data["stats"] = {
            "total_nodes": graph.number_of_nodes(),
            "total_edges": graph.number_of_edges(),
            "max_degree": max([d for n, d in graph.degree()]) if graph.number_of_nodes() > 0 else 0,
            "node_types": {} # Frontend creates this too, but we can populate if needed
        }
        
        return data

    except Exception as e:
        logger.error(f"Failed to generate memory graph: {e}")
        raise HTTPException(status_code=500, detail=str(e))
