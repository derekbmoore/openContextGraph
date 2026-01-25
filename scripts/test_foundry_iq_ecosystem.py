#!/usr/bin/env python3
"""
Test Foundry IQ Ecosystem Integration Maturity

Tests what Foundry IQ components are available, configured, and functional.
"""

import asyncio
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from core.config import Settings

# ANSI colors for output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


class FoundryIQTester:
    """Test Foundry IQ ecosystem components."""
    
    def __init__(self):
        self.settings = Settings()
        self.results: Dict[str, Any] = {}
        
    def print_header(self, text: str):
        """Print a section header."""
        print(f"\n{BOLD}{BLUE}{'='*80}{RESET}")
        print(f"{BOLD}{BLUE}{text}{RESET}")
        print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
    
    def print_status(self, component: str, status: str, details: str = ""):
        """Print component status."""
        if status == "✅":
            color = GREEN
        elif status == "⚠️":
            color = YELLOW
        else:
            color = RED
        
        print(f"{color}{status}{RESET} {BOLD}{component}{RESET}")
        if details:
            print(f"    {details}")
    
    def test_configuration(self) -> Dict[str, Any]:
        """Test 1: Configuration Check"""
        self.print_header("Test 1: Configuration Check")
        
        config_status = {
            "foundry_agent_endpoint": bool(self.settings.azure_foundry_agent_endpoint),
            "foundry_agent_key": bool(self.settings.azure_foundry_agent_key),
            "foundry_agent_project": bool(self.settings.azure_foundry_agent_project),
            "use_foundry_iq": self.settings.use_foundry_iq,
            "foundry_iq_kb_id": bool(self.settings.foundry_iq_knowledge_base_id),
        }
        
        # Print results
        if config_status["foundry_agent_endpoint"]:
            self.print_status("Foundry Agent Endpoint", "✅", 
                            f"Configured: {self.settings.azure_foundry_agent_endpoint[:50]}...")
        else:
            self.print_status("Foundry Agent Endpoint", "❌", "Not configured")
        
        if config_status["foundry_agent_key"]:
            self.print_status("Foundry Agent Key", "✅", "Configured (hidden)")
        else:
            self.print_status("Foundry Agent Key", "❌", "Not configured")
        
        if config_status["foundry_agent_project"]:
            self.print_status("Foundry Agent Project", "✅", 
                            f"Configured: {self.settings.azure_foundry_agent_project}")
        else:
            self.print_status("Foundry Agent Project", "❌", "Not configured")
        
        if config_status["use_foundry_iq"]:
            self.print_status("Foundry IQ Enabled", "✅", "USE_FOUNDRY_IQ=True")
        else:
            self.print_status("Foundry IQ Enabled", "⚠️", "USE_FOUNDRY_IQ=False (disabled)")
        
        if config_status["foundry_iq_kb_id"]:
            self.print_status("Foundry IQ KB ID", "✅", 
                            f"Configured: {self.settings.foundry_iq_knowledge_base_id}")
        else:
            self.print_status("Foundry IQ KB ID", "⚠️", "Not configured")
        
        return config_status
    
    def test_foundry_client(self) -> Dict[str, Any]:
        """Test 2: Foundry Client Availability"""
        self.print_header("Test 2: Foundry Client Implementation")
        
        try:
            from integrations.foundry import FoundryClient
            
            client_status = {
                "foundry_client_exists": True,
                "can_instantiate": False,
            }
            
            # Try to instantiate
            try:
                client = FoundryClient(self.settings)
                client_status["can_instantiate"] = True
                self.print_status("Foundry Client", "✅", "Can instantiate")
            except Exception as e:
                self.print_status("Foundry Client", "⚠️", f"Exists but can't instantiate: {e}")
            
            return client_status
            
        except ImportError as e:
            self.print_status("Foundry Client", "❌", f"Not found: {e}")
            return {"foundry_client_exists": False, "can_instantiate": False}
    
    def test_foundry_iq_client(self) -> Dict[str, Any]:
        """Test 3: Foundry IQ Client"""
        self.print_header("Test 3: Foundry IQ Client Implementation")
        
        foundry_iq_path = Path(__file__).parent.parent / "backend" / "integrations" / "foundry_iq.py"
        
        if foundry_iq_path.exists():
            self.print_status("Foundry IQ Client", "✅", f"File exists: {foundry_iq_path}")
            return {"foundry_iq_client_exists": True}
        else:
            self.print_status("Foundry IQ Client", "❌", 
                            f"File missing: {foundry_iq_path}")
            self.print_status("", "", "💡 Create: backend/integrations/foundry_iq.py")
            return {"foundry_iq_client_exists": False}
    
    def test_mcp_tools(self) -> Dict[str, Any]:
        """Test 4: MCP Tools Available"""
        self.print_header("Test 4: MCP Tools Registry")
        
        try:
            from api.mcp_tools import TOOLS
            
            tools_list = list(TOOLS.keys())
            tools_status = {
                "mcp_tools_registry_exists": True,
                "tool_count": len(tools_list),
                "tools": tools_list,
            }
            
            self.print_status("MCP Tools Registry", "✅", 
                            f"Found {len(tools_list)} tools")
            
            # List key tools
            key_tools = ["search_memory", "generate_story", "read_domain_memory"]
            for tool in key_tools:
                if tool in tools_list:
                    self.print_status(f"  - {tool}", "✅", "Available")
                else:
                    self.print_status(f"  - {tool}", "❌", "Missing")
            
            return tools_status
            
        except ImportError as e:
            self.print_status("MCP Tools Registry", "❌", f"Not found: {e}")
            return {"mcp_tools_registry_exists": False}
    
    async def test_mcp_endpoint(self) -> Dict[str, Any]:
        """Test 5: MCP Endpoint Availability"""
        self.print_header("Test 5: MCP Endpoint Test")
        
        api_url = os.getenv("API_BASE_URL", "https://api.ctxeco.com")
        mcp_url = f"{api_url}/mcp"
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Test tools/list
                payload = {
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "id": 1
                }
                
                try:
                    response = await client.post(mcp_url, json=payload)
                    if response.status_code == 200:
                        result = response.json()
                        tools = result.get("result", {}).get("tools", [])
                        
                        self.print_status("MCP Endpoint", "✅", 
                                        f"Responding at {mcp_url}")
                        self.print_status("", "", f"Found {len(tools)} tools via MCP")
                        
                        return {
                            "mcp_endpoint_available": True,
                            "tool_count": len(tools),
                            "url": mcp_url,
                        }
                    else:
                        self.print_status("MCP Endpoint", "⚠️", 
                                        f"HTTP {response.status_code}: {response.text[:100]}")
                        return {"mcp_endpoint_available": False, "status_code": response.status_code}
                        
                except httpx.ConnectError:
                    self.print_status("MCP Endpoint", "⚠️", 
                                    f"Could not connect to {mcp_url}")
                    self.print_status("", "", "💡 Is the API server running?")
                    return {"mcp_endpoint_available": False, "error": "connection_error"}
                    
        except Exception as e:
            self.print_status("MCP Endpoint", "❌", f"Error: {e}")
            return {"mcp_endpoint_available": False, "error": str(e)}
    
    def test_hybrid_search(self) -> Dict[str, Any]:
        """Test 6: Hybrid Search Implementation"""
        self.print_header("Test 6: Hybrid Search (Foundry IQ + Tri-Search™)")
        
        hybrid_search_path = Path(__file__).parent.parent / "backend" / "memory" / "hybrid_search.py"
        
        if hybrid_search_path.exists():
            self.print_status("Hybrid Search", "✅", f"File exists: {hybrid_search_path}")
            return {"hybrid_search_exists": True}
        else:
            self.print_status("Hybrid Search", "❌", 
                            f"File missing: {hybrid_search_path}")
            self.print_status("", "", "💡 Create: backend/memory/hybrid_search.py")
            return {"hybrid_search_exists": False}
    
    def test_m365_integration(self) -> Dict[str, Any]:
        """Test 7: M365 Integration Status"""
        self.print_header("Test 7: M365 Integration")
        
        m365_doc = Path(__file__).parent.parent / "docs" / "knowledge" / "03-m365-integration.md"
        
        status = {
            "documentation_exists": m365_doc.exists(),
            "implementation_exists": False,
        }
        
        if m365_doc.exists():
            self.print_status("M365 Documentation", "✅", "Documentation exists")
        else:
            self.print_status("M365 Documentation", "❌", "Documentation missing")
        
        # Check for SharePoint connector
        sharepoint_path = Path(__file__).parent.parent / "backend" / "integrations" / "sharepoint.py"
        if sharepoint_path.exists():
            self.print_status("SharePoint Connector", "✅", "Implementation exists")
            status["implementation_exists"] = True
        else:
            self.print_status("SharePoint Connector", "❌", "Not implemented")
        
        return status
    
    def generate_maturity_report(self) -> Dict[str, Any]:
        """Generate overall maturity assessment."""
        self.print_header("Maturity Assessment Report")
        
        maturity = {
            "foundry_iq": {
                "level": 1 if self.results.get("config", {}).get("use_foundry_iq") else 0,
                "status": "Configured but not operational",
                "components": {
                    "config": self.results.get("config", {}).get("use_foundry_iq", False),
                    "client": self.results.get("foundry_iq_client", {}).get("foundry_iq_client_exists", False),
                    "hybrid_search": self.results.get("hybrid_search", {}).get("hybrid_search_exists", False),
                }
            },
            "fabric_iq": {
                "level": 0,
                "status": "Not explored",
                "components": {}
            },
            "work_iq": {
                "level": 0,
                "status": "Not explored",
                "components": {}
            },
            "m365_copilot": {
                "level": 1 if self.results.get("m365", {}).get("documentation_exists") else 0,
                "status": "Documented but not operational",
                "components": {
                    "documentation": self.results.get("m365", {}).get("documentation_exists", False),
                    "implementation": self.results.get("m365", {}).get("implementation_exists", False),
                }
            }
        }
        
        # Print summary
        for component, data in maturity.items():
            level = data["level"]
            status_icon = "✅" if level >= 2 else "⚠️" if level >= 1 else "❌"
            print(f"{status_icon} {BOLD}{component.upper()}{RESET}: Level {level} - {data['status']}")
        
        return maturity
    
    async def run_all_tests(self):
        """Run all tests."""
        print(f"{BOLD}{BLUE}{'='*80}{RESET}")
        print(f"{BOLD}{BLUE}Foundry IQ Ecosystem Maturity Test{RESET}")
        print(f"{BOLD}{BLUE}{'='*80}{RESET}\n")
        
        # Run tests
        self.results["config"] = self.test_configuration()
        self.results["foundry_client"] = self.test_foundry_client()
        self.results["foundry_iq_client"] = self.test_foundry_iq_client()
        self.results["mcp_tools"] = self.test_mcp_tools()
        self.results["mcp_endpoint"] = await self.test_mcp_endpoint()
        self.results["hybrid_search"] = self.test_hybrid_search()
        self.results["m365"] = self.test_m365_integration()
        
        # Generate report
        self.results["maturity"] = self.generate_maturity_report()
        
        # Save results
        output_file = Path(__file__).parent.parent / "docs" / "research" / "foundry-iq-test-results.json"
        with open(output_file, "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n{BOLD}Results saved to: {output_file}{RESET}\n")
        
        return self.results


async def main():
    """Main execution."""
    tester = FoundryIQTester()
    results = await tester.run_all_tests()
    
    # Exit with error code if critical components missing
    if not results.get("foundry_client", {}).get("foundry_client_exists"):
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    asyncio.run(main())
