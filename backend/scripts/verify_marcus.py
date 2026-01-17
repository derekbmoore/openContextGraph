"""
Verify Marcus Agent (Foundry/Assistants API)
Smoke test for the refactored FoundryAgentWrapper and MarcusAgent.
"""
import asyncio
import os
import logging
from agents.marcus import MarcusAgent
from core.context import EnterpriseContext

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # 1. Setup Environment 
    # Ensure AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT are set in your environment
    if not os.getenv("AZURE_OPENAI_API_KEY"):
        print("ERROR: AZURE_OPENAI_API_KEY environment variable not set")
        return
    if not os.getenv("AZURE_OPENAI_ENDPOINT"):
        os.environ["AZURE_OPENAI_ENDPOINT"] = "https://zimax.cognitiveservices.azure.com/"
    
    # 2. Initialize Agent
    print("Initializing Marcus Agent...")
    marcus = MarcusAgent()
    
    from core.context import EnterpriseContext, SecurityContext, OperationalContext
    
    # 3. Create Context
    sec_ctx = SecurityContext(
        user_id="derek",
        tenant_id="zimax",
        groups=["Proj:CtxEcoDev"],
        roles=["developer"],
        scopes=["read", "write"]
    )
    
    ctx = EnterpriseContext(
        security=sec_ctx,
        operational=OperationalContext(trace_id="verify-run-1")
    )
    
    # 4. Execute Test Query (Should trigger tool)
    query = "Please search the codebase for 'error' handling in the agents directory."
    print(f"\nSending Query: {query}")
    
    response, logs = await marcus._execute(query, ctx)
    
    print("\n--- Response ---")
    print(response)
    print("\n--- Tool Logs ---")
    for log in logs:
        print(f"Tool: {log.get('name')} | Result: {log.get('result')}")

if __name__ == "__main__":
    asyncio.run(main())
