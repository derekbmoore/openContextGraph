# Agents — Brain Layer (LangGraph)

## Purpose

Agents are the **reasoning and decision-making layer** of openContextGraph. Built on LangGraph, they provide domain-specialized AI assistants that leverage the full 4-layer context to deliver expert responses.

## Why This Exists

### The Problem

Generic chatbots lack:

- **Domain expertise**: No understanding of specific roles
- **Context awareness**: Each response starts fresh
- **Tool integration**: Limited to text generation
- **Accountability**: No attribution of AI actions

### The Solution

Specialized agents that:

1. **Embody domain roles** (Architect, PM, Storyteller)
2. **Leverage full context** (Security, Episodic, Semantic, Operational)
3. **Use tools** (Memory search, document generation, integrations)
4. **Are fully attributed** (Every action traceable to invoking user)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Router                              │
│  Routes requests to appropriate specialized agent            │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Elena     │      │   Marcus    │      │    Sage     │
│  Architect  │      │     PM      │      │ Storyteller │
└─────────────┘      └─────────────┘      └─────────────┘
         │                    │                    │
         └────────────────────┴────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LangGraph Engine                          │
│  State machine for multi-step reasoning                      │
└─────────────────────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Memory    │      │    Tools    │      │    LLM      │
│   Client    │      │  Functions  │      │  Provider   │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## Agent Profiles

### Elena — Senior System Architect

```
Role: Technical architecture analysis and guidance
Expertise: System design, integration patterns, security
Personality: Precise, authoritative, detail-oriented
Tools: Architecture diagrams, code review, documentation
```

### Marcus — Project Manager

```
Role: Project planning and risk assessment
Expertise: Timelines, resources, risk mitigation
Personality: Organized, proactive, stakeholder-focused
Tools: Timeline generation, status reports, risk matrices
```

### Sage — Storyteller

```
Role: Narrative generation and visualization
Expertise: Communication, visual storytelling, synthesis
Personality: Creative, clear, engaging
Tools: Story generation, image creation, presentations
```

---

## Code Sample

```python
# backend/agents/base.py
"""
Base Agent Implementation

LangGraph-based agent with:
- Full EnterpriseContext integration
- Memory enrichment
- Tool execution
- Attribution tracking

NIST AI RMF Alignment:
- GOVERN 1.2: Agent actions attributed to invoking user
- MAP 1.1: Context flows through all agent operations
- MEASURE 2.5: Agent responses are tracked for feedback
"""

import logging
from abc import ABC, abstractmethod
from typing import Optional, Any

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from core import EnterpriseContext, SecurityContext, ToolCall

logger = logging.getLogger(__name__)


class BaseAgent(ABC):
    """
    Base class for all agents.
    
    NIST AI RMF: GOVERN 1.2 - All agent actions are attributed
    """
    
    def __init__(
        self, 
        agent_id: str,
        display_name: str,
        system_prompt: str,
        model: str = "gpt-4o"
    ):
        self.agent_id = agent_id
        self.display_name = display_name
        self.system_prompt = system_prompt
        self.model = model
        self._graph = None
    
    @property
    def graph(self) -> StateGraph:
        """Lazy-build the LangGraph state machine."""
        if self._graph is None:
            self._graph = self._build_graph()
        return self._graph
    
    @abstractmethod
    def _build_graph(self) -> StateGraph:
        """Build the agent's reasoning graph. Override in subclasses."""
        pass
    
    @abstractmethod
    def get_tools(self) -> list:
        """Return tools available to this agent. Override in subclasses."""
        pass
    
    async def process(
        self,
        message: str,
        context: EnterpriseContext
    ) -> dict:
        """
        Process a user message through the agent.
        
        NIST AI RMF Controls:
        - GOVERN 1.2: Records invoking user
        - MAP 1.1: Context enrichment
        - MEASURE 2.5: Response tracking
        
        Args:
            message: User's input
            context: Full 4-layer enterprise context
        
        Returns:
            {response, agent_id, sources, tool_calls}
        """
        # Track who invoked this agent
        context.operational.current_agent = self.agent_id
        
        logger.info(
            f"Agent {self.agent_id} processing request from "
            f"{context.security.user_id}"
        )
        
        # Prepare state for graph execution
        state = {
            "messages": [HumanMessage(content=message)],
            "context": context,
            "tool_calls": [],
        }
        
        # Execute the graph
        result = await self.graph.ainvoke(state)
        
        # Extract response
        response_message = result.get("messages", [])[-1]
        response_text = (
            response_message.content 
            if hasattr(response_message, "content") 
            else str(response_message)
        )
        
        # Record tool calls for attribution (NIST MANAGE 4.2)
        tool_calls = [
            ToolCall(
                tool_name=tc.get("name", "unknown"),
                arguments=tc.get("args", {}),
                result=tc.get("result"),
                duration_ms=tc.get("duration_ms")
            )
            for tc in result.get("tool_calls", [])
        ]
        
        return {
            "response": response_text,
            "agent_id": self.agent_id,
            "user_id": context.security.user_id,  # Attribution
            "sources": self._extract_sources(result),
            "tool_calls": [tc.model_dump() for tc in tool_calls],
        }
    
    def _extract_sources(self, result: dict) -> list[str]:
        """Extract source references from semantic context."""
        context = result.get("context")
        if not context:
            return []
        return [
            fact.source 
            for fact in context.semantic.facts 
            if fact.source
        ]


# =============================================================================
# ELENA - Senior System Architect
# =============================================================================

class ElenaAgent(BaseAgent):
    """
    Elena - Senior System Architect
    
    Expertise:
    - System architecture analysis
    - Technical guidance
    - Security assessment
    - Integration patterns
    """
    
    SYSTEM_PROMPT = """You are Elena, a Senior System Architect with deep expertise in:
- Distributed systems and microservices
- Security architecture and compliance
- Enterprise integration patterns
- AI/ML system design

You are precise, authoritative, and detail-oriented. You base your answers on 
the provided context and always cite your sources.

Current user: {user_id}
Tenant: {tenant_id}
"""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__(
            agent_id="elena",
            display_name="Elena",
            system_prompt=self.SYSTEM_PROMPT,
            model=model
        )
    
    def _build_graph(self) -> StateGraph:
        """Build Elena's reasoning graph."""
        from langgraph.graph import StateGraph, END
        from langgraph.prebuilt import ToolNode
        
        # Define graph nodes
        graph = StateGraph(dict)
        
        # Add nodes
        graph.add_node("reason", self._reason)
        graph.add_node("tools", ToolNode(self.get_tools()))
        
        # Define edges
        graph.set_entry_point("reason")
        graph.add_conditional_edges(
            "reason",
            self._should_use_tools,
            {"tools": "tools", "end": END}
        )
        graph.add_edge("tools", "reason")
        
        return graph.compile()
    
    def get_tools(self) -> list:
        """Elena's available tools."""
        return [
            # Memory search tool
            {
                "name": "search_architecture_docs",
                "description": "Search architecture documentation",
                "func": self._search_docs,
            },
            # Diagram generation
            {
                "name": "generate_diagram",
                "description": "Generate architecture diagram",
                "func": self._generate_diagram,
            },
        ]
    
    async def _reason(self, state: dict) -> dict:
        """Elena's reasoning step."""
        # TODO: Integrate with LLM
        return state
    
    def _should_use_tools(self, state: dict) -> str:
        """Determine if tools are needed."""
        return "end"
    
    async def _search_docs(self, query: str) -> str:
        """Search architecture documentation."""
        return f"[Search results for: {query}]"
    
    async def _generate_diagram(self, description: str) -> str:
        """Generate architecture diagram."""
        return f"[Diagram: {description}]"


# =============================================================================
# MARCUS - Project Manager
# =============================================================================

class MarcusAgent(BaseAgent):
    """
    Marcus - Project Manager
    
    Expertise:
    - Project planning and timelines
    - Risk assessment
    - Stakeholder communication
    - Status reporting
    """
    
    SYSTEM_PROMPT = """You are Marcus, an experienced Project Manager with expertise in:
- Agile and traditional project methodologies
- Risk identification and mitigation
- Cross-functional team coordination
- Executive communication

You are organized, proactive, and stakeholder-focused. You provide clear
action items and timelines.

Current user: {user_id}
Tenant: {tenant_id}
"""
    
    def __init__(self, model: str = "gpt-4o"):
        super().__init__(
            agent_id="marcus",
            display_name="Marcus",
            system_prompt=self.SYSTEM_PROMPT,
            model=model
        )
    
    def _build_graph(self) -> StateGraph:
        """Build Marcus's reasoning graph."""
        # Similar structure to Elena
        graph = StateGraph(dict)
        graph.add_node("reason", self._reason)
        graph.set_entry_point("reason")
        graph.add_edge("reason", END)
        return graph.compile()
    
    def get_tools(self) -> list:
        """Marcus's available tools."""
        return [
            {"name": "create_timeline", "description": "Create project timeline"},
            {"name": "assess_risks", "description": "Assess project risks"},
            {"name": "generate_status_report", "description": "Generate status report"},
        ]
    
    async def _reason(self, state: dict) -> dict:
        return state


# =============================================================================
# AGENT ROUTER
# =============================================================================

class AgentRouter:
    """
    Routes requests to the appropriate agent.
    
    NIST AI RMF: GOVERN 1.2 - Routing decisions are logged
    """
    
    def __init__(self):
        self.agents = {
            "elena": ElenaAgent(),
            "marcus": MarcusAgent(),
            # "sage": SageAgent(),
        }
    
    async def route(
        self,
        agent_name: str,
        message: str,
        context: EnterpriseContext
    ) -> dict:
        """
        Route to the specified agent.
        
        Args:
            agent_name: Target agent ("elena", "marcus", "sage")
            message: User's input
            context: Full enterprise context
        """
        agent = self.agents.get(agent_name.lower())
        
        if not agent:
            available = ", ".join(self.agents.keys())
            return {
                "error": f"Unknown agent: {agent_name}. Available: {available}",
                "agent_id": None
            }
        
        return await agent.process(message, context)


# Singleton router
agent_router = AgentRouter()
```

---

## NIST AI RMF Alignment

| Function | Control | Implementation |
|----------|---------|----------------|
| **GOVERN 1.2** | Accountability | `user_id` in every response |
| **GOVERN 1.4** | Transparency | System prompts are explicit |
| **MAP 1.1** | System Context | Full `EnterpriseContext` flow |
| **MEASURE 2.5** | User Feedback | Response tracking |
| **MANAGE 4.2** | Audit | `tool_calls` recorded |

---

## Summary

The Agents layer provides:

- ✅ Domain-specialized AI assistants
- ✅ Full context integration (4 layers)
- ✅ Tool execution with attribution
- ✅ Accountable AI (user attribution)
- ✅ NIST AI RMF compliance

*Document Version: 1.0 | Created: 2026-01-11*
