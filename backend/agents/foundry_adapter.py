"""
Foundry Agent Adapter
Implementation of the Azure AI Foundry Agent (Hybrid PoC) Blueprint.
Aligns with SDK 2.0 Patterns (Project Endpoint, Agent ID, Async).

Ref: docs/research/foundry-agent-integration.md
"""
import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional

from openai import AzureOpenAI
from openai.types.beta.threads import Run
from openai.types.beta.thread import Thread

from agents.base import BaseAgent
from core.context import EnterpriseContext

logger = logging.getLogger(__name__)

class FoundryAgentWrapper(BaseAgent):
    """
    Adapter for Azure AI Foundry Agents (via Azure OpenAI Assistants API).
    
    This wrapper handles:
    1. Managing OpenContextGraph -> OpenAI Thread mapping (via DB)
    2. executing Tools locally (requires_action)
    3. Polling for Run completion
    """
    
    def __init__(
        self, 
        agent_id: str, 
        foundry_agent_id: str,
        display_name: str,
        system_prompt: str,
        model: str = "gpt-4o"
    ):
        super().__init__(agent_id, display_name, system_prompt, model)
        self.foundry_agent_id = foundry_agent_id
        self._registered_tools = {}
        
        # Initialize Azure OpenAI Client
        # We use standard env vars or 'zimax' hardcoded fallbacks for this context if needed
        # ideally env vars: AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version="2024-05-01-preview",
        )

    def get_tools(self) -> List[str]:
        """Return list of registered local tools."""
        return list(self._registered_tools.keys())

    def register_tool(self, name: str, func: callable):
        """Register a local function tool."""
        self._registered_tools[name] = func

    async def _execute(
        self, 
        message: str, 
        context: EnterpriseContext
    ) -> tuple[str, list[dict]]:
        """
        Execute the Agent loop:
        1. Get/Create Thread
        2. Add Message
        3. Create Run
        4. Poll for Completion / Tool Calls
        5. Return Response
        """
        try:
            # 1. Thread Management
            thread_id = await self._get_or_create_thread(context.security.user_id)
            
            # 2. Add Message
            await asyncio.to_thread(
                self.client.beta.threads.messages.create,
                thread_id=thread_id,
                role="user",
                content=message
            )
            
            # 3. Create Run
            run = await asyncio.to_thread(
                self.client.beta.threads.runs.create,
                thread_id=thread_id,
                assistant_id=self.foundry_agent_id,
                # instruction_override=... could pass dynamic context here
            )
            
            # 4. Poll Loop
            while True:
                # Retrieve Run Status
                run = await asyncio.to_thread(
                    self.client.beta.threads.runs.retrieve,
                    thread_id=thread_id,
                    run_id=run.id
                )
                
                status = run.status
                logger.info(f"Run {run.id} status: {status}")
                
                if status == "completed":
                    break
                elif status == 'requires_action':
                    await self._handle_requires_action(run, thread_id)
                elif status in ["failed", "cancelled", "expired"]:
                    error_msg = f"Run failed with status: {status}"
                    if run.last_error:
                         error_msg += f" ({run.last_error.code}: {run.last_error.message})"
                    raise Exception(error_msg)
                
                await asyncio.sleep(1.0) # Polling interval
            
            # 5. Retrieve Messages
            response_text = await self._get_latest_response(thread_id, run.id)
            return response_text, [] # TODO: Extract executed tools for audit trail

        except Exception as e:
            logger.error(f"Foundry Agent execution failed: {e}")
            return f"I encountered an error executing that request: {str(e)}", []

    async def _get_or_create_thread(self, user_id: str) -> str:
        """
        Retrieve existing thread for user or create new one.
        TODO: Persist in `user_threads` table.
        """
        # Placeholder: Always create new thread for now
        thread = await asyncio.to_thread(self.client.beta.threads.create)
        return thread.id

    async def _handle_requires_action(self, run: Run, thread_id: str):
        """
        Handle 'requires_action' state by executing local tools.
        """
        tool_outputs = []
        
        required_actions = run.required_action.submit_tool_outputs.tool_calls
        
        for tool_call in required_actions:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            call_id = tool_call.id
            
            logger.info(f"Executing Tool: {func_name} args={args}")
            
            if func_name in self._registered_tools:
                try:
                    # Execute local tool
                    # Note: Tools might be async, handle accordingly
                    result = self._registered_tools[func_name](**args)
                    if asyncio.iscoroutine(result):
                        result = await result
                    
                    output_str = json.dumps(result) if not isinstance(result, str) else result
                except Exception as e:
                    output_str = f"Error: {str(e)}"
            else:
                output_str = f"Error: Tool {func_name} not found locally."
            
            tool_outputs.append({
                "tool_call_id": call_id,
                "output": output_str
            })
            
        # Submit Outputs
        if tool_outputs:
            await asyncio.to_thread(
                self.client.beta.threads.runs.submit_tool_outputs,
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

    async def _get_latest_response(self, thread_id: str, run_id: str) -> str:
        """Extract the assistant's response from the thread."""
        messages = await asyncio.to_thread(
            self.client.beta.threads.messages.list,
            thread_id=thread_id,
            order="desc",
            limit=1
        )
        
        if not messages.data:
            return "No response received."
            
        latest = messages.data[0]
        if latest.role == "assistant":
             # Combine text content
             text_content = []
             for c in latest.content:
                 if c.type == 'text':
                     text_content.append(c.text.value)
             return "\n".join(text_content)
        
        return "No assistant response found."
