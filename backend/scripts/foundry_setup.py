import os
import asyncio
from openai import AzureOpenAI

# Define Agent Specs
AGENTS = {
    "elena": {
        "name": "Elena",
        "model": "gpt-4o",
        "instructions": """You are Elena, a Senior System Architect with deep expertise in:
- Distributed systems and microservices architecture
- Security architecture and compliance (NIST, FedRAMP)
- Enterprise integration patterns
- AI/ML system design and deployment

You are precise, authoritative, and detail-oriented.
"""
    },
    "marcus": {
        "name": "Marcus",
        "model": "gpt-4o",
        "instructions": """You are Marcus, the Lead Engineering Agent for OpenContextGraph.
Your focus is on:
- High-quality, safe, and efficient code.
- Infrastructure stability (Azure/Bicep).
- Practical implementation details.

You are pragmatic, direct, and solution-oriented.
"""
    },
    "sage": {
        "name": "Sage",
        "model": "gpt-4o",
        "instructions": """You are Sage, the Creative Storyteller for OpenContextGraph.
Your goals are:
- Translate technical/complex data into clear, engaging narratives.
- Create visual representations (diagrams, images) to aid understanding.
- Connect disparate facts into coherent episodes.

You are empathetic, articulate, and insightful.
"""
    }
}

async def main():
    # Read from environment variables
    endpoint_url = os.getenv("AZURE_OPENAI_ENDPOINT", "https://zimax.cognitiveservices.azure.com/")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = "2024-05-01-preview" # Recent API version supporting Assistants v2
    
    if not key:
        print("ERROR: AZURE_OPENAI_API_KEY environment variable not set")
        return
    
    print(f"Connecting to Azure OpenAI Endpoint: {endpoint_url} (Version: {api_version})")
    
    try:
        client = AzureOpenAI(
            api_key=key,
            azure_endpoint=endpoint_url,
            api_version=api_version,
        )
    except Exception as e:
        print(f"Failed to initialize AzureOpenAI Client: {e}", flush=True)
        return

    # List existing assistants
    print("Checking existing assistants...", flush=True)
    existing = {}
    try:
        # Use sync List (openai sdk is sync by default unless AsyncAzureOpenAI used)
        # But we can iterate properly.
        assistants_list = client.beta.assistants.list()
        for a in assistants_list:
            existing[a.name] = a.id
            print(f"Found: {a.name} ({a.id})", flush=True)
    except Exception as e:
        print(f"Error listing assistants: {e}", flush=True)
        return

    # Provision
    for key, spec in AGENTS.items():
        name = spec["name"]
        if name in existing:
            print(f"Skipping {name} (Already exists: {existing[name]})", flush=True)
            continue
            
        print(f"Creating Assistant: {name}...", flush=True)
        try:
            # Note: Azure OpenAI requires 'model' to be the Deployment Name usually.
            # Assuming "gpt-4o" is the deployment name on 'zimax'.
            agent = client.beta.assistants.create(
                model=spec["model"],
                name=name,
                instructions=spec["instructions"],
                tools=[] 
            )
            print(f"Created {name}: {agent.id}", flush=True)
        except Exception as e:
            print(f"Failed to create {name}: {e}", flush=True)

if __name__ == "__main__":
    # main is technically sync with AzureOpenAI (unless Async client used)
    # But wrapper was async. Let's just run it.
    import asyncio
    # Redefine running logic
    asyncio.run(main())
