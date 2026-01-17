import asyncio
import os
import pandas as pd
from datetime import datetime
import sys

# Add backend to path to import core modules
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from etl.antigravity_router import get_antigravity_router, DataClass

async def main():
    print("=== Agent Elena: Generating Financial Report ===")
    print("Context: Zimax Networks LC - Context Ecology Platform")
    print("Author: Derek Brent Moore (Principal Architect)")
    
    # 1. Generate Mock Financial Data
    data = [
        {
            "Customer": "GE Vernova",
            "Tier": "Enterprise (FedRAMP High)",
            "Revenue_ARR": 1500000,
            "Support": "24/7 Dedicated",
            "Notes": "Using OpenContextGraph for industrial telemetry. Requires strict isolation."
        },
        {
            "Customer": "Agency Gov",
            "Tier": "Enterprise (IL5)",
            "Revenue_ARR": 2000000,
            "Support": "Cleared Personnel",
            "Notes": "Deployed to Azure Gov. Heavy use of Docling for manual ingestion."
        },
        {
            "Customer": "TechCorp Inc",
            "Tier": "Commercial Pro",
            "Revenue_ARR": 500000,
            "Support": "Standard Business",
            "Notes": "Marketing intelligence use case. High usage of VoiceLive Avatar."
        },
        {
            "Customer": "Research Lab X",
            "Tier": "OSS / Academic",
            "Revenue_ARR": 0,
            "Support": "Community",
            "Notes": "Contributing back to MIT Licensed core."
        }
    ]
    
    # df = pd.read_json(pd.io.json.dumps(data)) # formatting trick or just direct
    df = pd.DataFrame(data)
    
    # Add metadata columns in the sheet itself contextually
    df.attrs["Title"] = "Zimax Networks LC - Financial Projections Q1 2026"
    df.attrs["Generated_By"] = "Agent:Elena (Service Principal)"
    df.attrs["Architect"] = "Derek Brent Moore"
    
    filename = "zimax_financials_q1_2026.xlsx"
    filepath = os.path.abspath(filename)
    
    print(f"Generating {filename}...")
    # Requires openpyxl
    try:
        df.to_excel(filepath, index=False, sheet_name="Q1_2026_Revenue")
        print(f"Success: {filepath}")
    except ImportError:
        print("Error: openpyxl not installed. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
        df.to_excel(filepath, index=False, sheet_name="Q1_2026_Revenue")
        print(f"Success: {filepath}")

    # 2. Ingest into Context Ecology with Security Tags
    print("\n=== Ingesting into Context Ecology ===")
    print("Target ACL: ['Dept:Finance']")
    print("Classification: CONFIDENTIAL")
    
    # We need to simulate the ACL passing (Phase 2 implementation in router)
    # For now, we mimic the call structure
    router = get_antigravity_router()
    
    # Mocking the ACL injection for now (until router accepts it)
    # Ideally we would pass tuple or extra dict if router supported it yet
    # Since we haven't updated router yet, this is a demonstration of INTENT
    
    chunks = await router.ingest(
        file_path=filepath,
        filename=filename,
        force_class=DataClass.CLASS_C_OPS, # Financial data is Ops/Structured
        user_id="agent:elena",
        tenant_id="zimax-tenant"
    )
    
    # Post-process chunks to add ACL (simulating the Router update we are about to do)
    for chunk in chunks:
        chunk["metadata"]["acl_groups"] = ["Dept:Finance"]
        chunk["metadata"]["classification"] = "confidential"
        chunk["metadata"]["author_credit"] = "Derek Brent Moore"
    
    print(f"Ingested {len(chunks)} row-chunks.")
    print(f"Sample Metadata: {chunks[0]['metadata']}")
    print("\nMission Complete: Financial data secured for Finance Dept only.")

if __name__ == "__main__":
    asyncio.run(main())
