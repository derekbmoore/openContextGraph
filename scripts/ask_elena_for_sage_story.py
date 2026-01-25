#!/usr/bin/env python3
"""
Ask Elena to have Sage write a story about Engram's evolution.

This script calls Elena via the chat API, and she will delegate to Sage
to write the story based on the ingested commit history.
"""

import asyncio
import json
import sys
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def ask_elena_for_story(api_url: str = "http://localhost:8000") -> dict:
    """Ask Elena to have Sage write the story."""
    chat_url = f"{api_url}/api/v1/chat/"
    
    message = """Please have Sage write a comprehensive story about the evolution of Engram based on the commit history we just ingested. The story should:

1. Synthesize the 3,122 commits from the engram repository into a compelling narrative
2. Highlight major architectural decisions and their rationale
3. Show the progression from initial concept to production-ready system
4. Include how the project demonstrates recursive self-awareness and context engineering
5. Create a visual architecture diagram showing the progression

The commit history has been ingested into memory (2,314 chunks), so Sage can search for it. Please delegate this to Sage and have her generate both the story and a visual diagram."""
    
    payload = {
        "message": message,
        "agent": "elena",
        "session_id": None,  # Create new session
    }
    
    logger.info(f"Calling Elena via chat API: {chat_url}")
    logger.info(f"Message: {message[:100]}...")
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(chat_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            logger.info("✅ Response received from Elena")
            return {
                "success": True,
                "response": result.get("response", ""),
                "session_id": result.get("session_id", ""),
                "agent": result.get("agent", "elena"),
                "sources": result.get("sources", []),
                "tool_calls": result.get("tool_calls", []),
            }
            
    except httpx.ConnectError:
        logger.error(f"Could not connect to API at {api_url}")
        return {"success": False, "error": "API server not running"}
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        return {"success": False, "error": f"HTTP {e.response.status_code}"}
    except Exception as e:
        logger.error(f"Error calling chat API: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Main execution."""
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    logger.info("Asking Elena to have Sage write the Engram evolution story...")
    logger.info(f"API URL: {api_url}")
    
    result = await ask_elena_for_story(api_url)
    
    if result.get("success"):
        print("\n" + "="*80)
        print("ELENA'S RESPONSE")
        print("="*80)
        print(f"Session ID: {result.get('session_id')}")
        print(f"Agent: {result.get('agent')}")
        print(f"\nResponse:\n{result.get('response', '')}")
        
        if result.get("tool_calls"):
            print(f"\nTool Calls: {len(result.get('tool_calls', []))}")
            for tool in result.get("tool_calls", [])[:3]:
                print(f"  - {tool.get('name', 'unknown')}")
        
        if result.get("sources"):
            print(f"\nSources: {len(result.get('sources', []))}")
        
        print("="*80)
    else:
        print("\n" + "="*80)
        print("ERROR")
        print("="*80)
        print(f"Failed to get response: {result.get('error')}")
        print("\nMake sure the API server is running:")
        print("  cd backend && uvicorn api.main:app --reload")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
