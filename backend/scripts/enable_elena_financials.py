
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from core.config import get_settings
from openai import AzureOpenAI

def setup_elena_financials():
    load_dotenv()
    settings = get_settings()
    
    # 1. Initialize Client
    client = AzureOpenAI(
        azure_endpoint=settings.azure_foundry_agent_endpoint,
        api_key=settings.azure_foundry_agent_key,
        api_version=settings.azure_foundry_agent_api_version,
    )
    
    elena_id = settings.elena_foundry_agent_id
    if not elena_id:
        print("Error: ELENA_FOUNDRY_AGENT_ID not set.")
        return

    # 2. Locate File
    file_path = Path("/Users/derek/Library/CloudStorage/OneDrive-zimaxnet/code/openContextGraph/zimax_financials_q1_2026.xlsx")
    if not file_path.exists():
        print(f"Error: File not found at {file_path}")
        return

    print(f"Uploading {file_path.name}...")
    
    # 3. Upload File
    with open(file_path, "rb") as f:
        uploaded_file = client.files.create(
            file=f,
            purpose="assistants"
        )
    
    print(f"File uploaded. ID: {uploaded_file.id}")
    
    # 4. Update Elena
    print(f"Updating Elena ({elena_id}) with Code Interpreter and File...")
    
    assistant = client.beta.assistants.update(
        assistant_id=elena_id,
        tools=[{"type": "code_interpreter"}], # Ensure code_interpreter is enabled
        tool_resources={
            "code_interpreter": {
                "file_ids": [uploaded_file.id]
            }
        }
    )
    
    print("Success! Elena now has access to the financials file via Code Interpreter.")
    print("She can analyze, plot, and modify this data.")

if __name__ == "__main__":
    setup_elena_financials()
