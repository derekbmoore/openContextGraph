"""
Azure AI Foundry Integration Client

Handles communication with Azure AI Foundry agents (Assistants API).
Encapsulates thread creation, run execution, and tool output handling.
"""

import logging
import asyncio
from typing import Optional, Dict, Any, List
from openai import AzureOpenAI
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FoundryResponse(BaseModel):
    response: str
    thread_id: str
    run_id: str
    status: str
    error: Optional[str] = None
    tool_calls: List[Dict[str, Any]] = []

class FoundryClient:
    def __init__(self, settings: Any):
        """
        Initialize Foundry Client with application settings.
        
        Args:
            settings: App settings containing azure_foundry_agent_* config
        """
        # Debug: Log credential presence (not values!)
        logger.info(f"FoundryClient init: endpoint={bool(settings.azure_foundry_agent_endpoint)}, key={bool(settings.azure_foundry_agent_key)}, api_version={settings.azure_foundry_agent_api_version}")
        
        self.client = AzureOpenAI(
            azure_endpoint=settings.azure_foundry_agent_endpoint,
            api_key=settings.azure_foundry_agent_key,
            api_version=settings.azure_foundry_agent_api_version,
        )
        self.settings = settings

    async def chat(
        self, 
        agent_id: str, 
        message: str, 
        thread_id: Optional[str] = None,
        memory_context: str = ""
    ) -> FoundryResponse:
        """
        Send a message to a Foundry Agent.
        
        Args:
            agent_id: The Assistant ID (e.g. asst_...)
            message: User's message
            thread_id: Optional existing thread ID
            memory_context: Context derived from memory/RAG to inject
            
        Returns:
            FoundryResponse object
        """
        try:
            # 1. Create or Retrieve Thread
            if not thread_id:
                thread = await asyncio.to_thread(self.client.beta.threads.create)
                thread_id = thread.id
                logger.info(f"Created new Foundry thread: {thread_id}")
            
            # 2. Inject Memory Context (if new thread or relevant)
            # Note: We inject this as a separate user message just before the actual query
            # to ensure it's in context but distinct.
            if memory_context:
                await asyncio.to_thread(
                    self.client.beta.threads.messages.create,
                    thread_id=thread_id,
                    role="user",
                    content=f"Context from memory:\n{memory_context}"
                )

            # 3. Add User Message
            await asyncio.to_thread(
                self.client.beta.threads.messages.create,
                thread_id=thread_id,
                role="user",
                content=message
            )

            # 4. Create Run
            run = await asyncio.to_thread(
                self.client.beta.threads.runs.create,
                thread_id=thread_id,
                assistant_id=agent_id
            )
            logger.info(f"Started Foundry run: {run.id} on thread {thread_id}")

            # 5. Poll for Completion
            # We use a loop with asyncio.sleep to avoid blocking the event loop
            # Max wait: 60 seconds
            final_run = await self._poll_run(thread_id, run.id)

            if final_run.status == "completed":
                # Retrieve the latest message
                messages = await asyncio.to_thread(
                    self.client.beta.threads.messages.list,
                    thread_id=thread_id,
                    order="desc",
                    limit=1
                )
                
                if not messages.data:
                    return FoundryResponse(
                        response="No response generated.",
                        thread_id=thread_id,
                        run_id=final_run.id,
                        status="completed"
                    )

                # Extract text content
                content_blocks = messages.data[0].content
                text_response = ""
                for block in content_blocks:
                    if hasattr(block, "text"):
                        text_response += block.text.value
                
                return FoundryResponse(
                    response=text_response,
                    thread_id=thread_id,
                    run_id=final_run.id,
                    status="completed"
                )

            elif final_run.status == "requires_action":
                # Handle cases where the agent wants to call a generic tool
                # that wasn't handled by the server-side Action Group.
                # In this architecture, we expect Azure to handle HTTP tools internally.
                # If we get here, it implies a misconfiguration or a local function definition.
                logger.warning(f"Foundry run {final_run.id} requires action: {final_run.required_action}")
                
                # Attempt to cancel to clean up
                await asyncio.to_thread(
                    self.client.beta.threads.runs.cancel,
                    thread_id=thread_id,
                    run_id=final_run.id
                )
                
                return FoundryResponse(
                    response="Error: Agent tried to execute a local function. This agent should uses server-side Action Groups (MCP).",
                    thread_id=thread_id,
                    run_id=final_run.id,
                    status="error",
                    error="requires_action_unhandled"
                )

            else:
                return FoundryResponse(
                    response=f"Agent execution failed with status: {final_run.status}",
                    thread_id=thread_id,
                    run_id=final_run.id,
                    status="failed",
                    error=str(final_run.last_error) if final_run.last_error else "Unknown error"
                )

        except Exception as e:
            logger.error(f"Foundry Client Error: {e}", exc_info=True)
            return FoundryResponse(
                response=f"System Error: {str(e)}",
                thread_id=thread_id or "unknown",
                run_id="unknown",
                status="error",
                error=str(e)
            )

    async def _poll_run(self, thread_id: str, run_id: str, timeout: int = 60, interval: float = 0.5):
        """Poll the run status until terminal state or timeout."""
        start_time = asyncio.get_event_loop().time()
        
        while True:
            run = await asyncio.to_thread(
                self.client.beta.threads.runs.retrieve,
                thread_id=thread_id,
                run_id=run_id
            )
            
            if run.status in ["completed", "failed", "cancelled", "expired", "requires_action"]:
                return run
            
            if asyncio.get_event_loop().time() - start_time > timeout:
                # Timeout - attempt to cancel
                try:
                    await asyncio.to_thread(
                        self.client.beta.threads.runs.cancel,
                        thread_id=thread_id,
                        run_id=run_id
                    )
                except:
                    pass
                raise TimeoutError(f"Foundry run {run_id} timed out after {timeout}s")
                
            await asyncio.sleep(interval)
