"""
Update Marcus Agent Tools
Adds the 'search_codebase' function tool definition to the existing Marcus Assistant.
"""
import asyncio
import os
from openai import AzureOpenAI

async def main():
    # Read from environment variables
    endpoint_url = os.getenv("AZURE_OPENAI_ENDPOINT", "https://zimax.cognitiveservices.azure.com/")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = "2024-05-01-preview"
    
    if not key:
        print("ERROR: AZURE_OPENAI_API_KEY environment variable not set")
        return
    
    # Marcus ID (Provisioned)
    marcus_id = "asst_pGd3gsS2ujEAIkKfkIm1JRep"
    
    print(f"Connecting to Azure OpenAI Endpoint: {endpoint_url}")
    
    client = AzureOpenAI(
        api_key=key,
        azure_endpoint=endpoint_url,
        api_version=api_version,
    )

    # Define Tool
    search_tool = {
        "type": "function",
        "function": {
            "name": "search_codebase",
            "description": "Search the local codebase for a query string. Use this whenever the user asks to find code or search for patterns.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string", 
                        "description": "The string pattern to search for."
                    }
                },
                "required": ["query"]
            }
        }
    }

    print(f"Updating Marcus ({marcus_id}) with tools...")
    
    try:
        updated_agent = client.beta.assistants.update(
            assistant_id=marcus_id,
            tools=[search_tool]
        )
        print(f"Successfully updated Marcus. Tools: {len(updated_agent.tools)}")
        print([t.function.name for t in updated_agent.tools if t.type == 'function'])
    except Exception as e:
        print(f"Failed to update Marcus: {e}")

if __name__ == "__main__":
    asyncio.run(main())
