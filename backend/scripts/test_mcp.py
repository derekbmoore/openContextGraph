"""
Test MCP Endpoint
Quick verification that the MCP JSON-RPC router works.
"""
import json
import asyncio
import httpx

MCP_URL = "http://localhost:8000/mcp"

async def main():
    async with httpx.AsyncClient() as client:
        # 1. Test initialize
        print("Testing initialize...")
        response = await client.post(MCP_URL, json={
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {"clientInfo": {"name": "test-client"}},
            "id": 1
        })
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # 2. Test tools/list
        print("\nTesting tools/list...")
        response = await client.post(MCP_URL, json={
            "jsonrpc": "2.0",
            "method": "tools/list",
            "id": 2
        })
        print(f"Status: {response.status_code}")
        data = response.json()
        if "result" in data and "tools" in data["result"]:
            print(f"Tools available: {len(data['result']['tools'])}")
            for tool in data["result"]["tools"]:
                print(f"  - {tool['name']}: {tool['description'][:50]}...")
        else:
            print(json.dumps(data, indent=2))
        
        # 3. Test tools/call (search_memory)
        print("\nTesting tools/call (search_memory)...")
        response = await client.post(MCP_URL, json={
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "search_memory",
                "arguments": {"query": "test", "limit": 3}
            },
            "id": 3
        })
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(main())
