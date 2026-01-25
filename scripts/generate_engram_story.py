#!/usr/bin/env python3
"""
Generate Engram evolution story via MCP tool.

This script calls the generate_story MCP tool to have Sage create a story
about Engram's evolution based on the ingested commit history.
"""

import json
import sys
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def generate_story_via_mcp(api_url: str = "http://localhost:8000") -> dict:
    """Generate story via MCP tool."""
    mcp_url = f"{api_url}/mcp"
    
    payload = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "generate_story",
            "arguments": {
                "topic": "The Evolution of Engram: A Journey Through Commit History",
                "style": "informative",
                "length": "long"
            }
        },
        "id": 1
    }
    
    logger.info(f"Calling MCP tool: {mcp_url}")
    logger.info(f"Topic: {payload['params']['arguments']['topic']}")
    
    try:
        async with httpx.AsyncClient(timeout=600.0) as client:
            response = await client.post(mcp_url, json=payload)
            response.raise_for_status()
            result = response.json()
            
            if "error" in result:
                logger.error(f"MCP error: {result['error']}")
                return {"success": False, "error": result["error"]}
            
            if "result" in result:
                content = result["result"].get("content", [])
                if content and len(content) > 0:
                    text_content = content[0].get("text", "")
                    try:
                        story_data = json.loads(text_content)
                        return {"success": True, "data": story_data}
                    except:
                        return {"success": True, "raw": text_content}
            
            return {"success": True, "result": result}
            
    except httpx.ConnectError:
        logger.error(f"Could not connect to API at {api_url}")
        logger.error("Make sure the API server is running: cd backend && uvicorn api.main:app --reload")
        return {"success": False, "error": "API server not running"}
    except Exception as e:
        logger.error(f"Error calling MCP tool: {e}")
        return {"success": False, "error": str(e)}


async def main():
    """Main execution."""
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    logger.info("Generating Engram evolution story via Sage...")
    logger.info(f"API URL: {api_url}")
    
    result = await generate_story_via_mcp(api_url)
    
    if result.get("success"):
        print("\n" + "="*80)
        print("STORY GENERATION RESULT")
        print("="*80)
        print(json.dumps(result, indent=2))
        print("="*80)
    else:
        print("\n" + "="*80)
        print("ERROR")
        print("="*80)
        print(f"Failed to generate story: {result.get('error')}")
        print("\nTo start the API server:")
        print("  cd backend && uvicorn api.main:app --reload")
        print("="*80)
        sys.exit(1)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
