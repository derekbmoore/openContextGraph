# MCP Trust Index Research Round — Structured Data

**Generated:** 2026-01-22  
**Source:** Research round output (CSV)  
**Purpose:** Structured inventory of Batch 1 providers for MCP Trust Index assessment

---

## Provider Inventory (Batch 1)

| Provider | Server | Category | Type | Docs | Endpoint | Repo | Notes |
|---|---|---|---|---|---|---|---|
| Microsoft | Microsoft Learn Docs MCP Server | Docs / Knowledge | Remote (hosted) | [Docs](https://developer.microsoft.com/blog/10-microsoft-mcp-servers-to-accelerate-your-development-workflow) | https://learn.microsoft.com/api/mcp | (docs only; endpoint documented) | Official Microsoft hosted MCP endpoint for Microsoft Learn docs search/retrieval. |
| Microsoft | Azure MCP Server | Cloud / Infrastructure | Local (official) + IDE integrations | [Docs](https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/) | Local server; connects via MCP client (e.g., VS Code/GitHub Copilot). | [Repo](https://github.com/microsoft/mcp) | Official Microsoft repo includes Azure MCP; important benchmark for auth/RBAC guidance. |
| GitHub | GitHub MCP Server | Dev / Version Control | Server (runs locally or hosted by integrators) | [Docs](https://github.com/github/github-mcp-server) | Depends on deployment; typically STDIO/local transport | [Repo](https://github.com/github/github-mcp-server) | Official GitHub MCP server; enterprise relevance for code, issues, PR automation. |
| Splunk | Splunk MCP Server | Observability / SecOps | Remote (marketplace/managed) | [Docs](https://marketplace.microsoft.com/hi-in/product/saas/splunk.splunk_mcp_server?tab=overview) | Managed remote (see offer docs); supports Splunk Enterprise & Cloud | (vendor-managed; see offer + Splunk docs) | Microsoft Marketplace listing; strong enterprise anchor for audit/ops use cases. |
| Datadog | Datadog MCP Server | Observability | Remote (preview) | [Docs](https://docs.datadoghq.com/bits_ai/mcp_server/) | Remote MCP server (preview) per Datadog docs | (vendor-managed; docs + blog) | Good for scoring auth posture + logging and guardrails patterns. |
| PagerDuty | PagerDuty MCP Server | Incident Response | Local (official) | [Docs](https://support.pagerduty.com/main/docs/pagerduty-mcp-server-integration-guide) | Local server (STDIO); connects to PagerDuty account | [Repo](https://github.com/PagerDuty/pagerduty-mcp-server) | Strong enterprise incident mgmt use case; repo includes security and license details. |
| Notion | Notion MCP (hosted) / Notion MCP Server (official) | Productivity / Knowledge | Remote hosted + local/HTTP modes | [Docs](https://developers.notion.com/docs/mcp) | Hosted server (per Notion docs) + HTTP transport option in official server repo | [Repo](https://github.com/makenotion/notion-mcp-server) | Shows both hosted and self-run patterns; includes HTTP transport with auth token options. |
| Cloudflare | Cloudflare MCP Server(s) | Cloud / Edge / Security | Remote managed catalog + OSS servers | [Docs](https://developers.cloudflare.com/agents/model-context-protocol/mcp-servers-for-cloudflare/) | Remote managed MCP servers via OAuth (catalog) + deploy-your-own guide | [Repo](https://github.com/cloudflare/mcp-server-cloudflare) | Great benchmark for OAuth, managed remote, and deployment guidance. |
| Google | Google Official MCP Servers | Cloud / Productivity | Collection (official) | [Docs](https://github.com/google/mcp) | Varies by server; see repo list | [Repo](https://github.com/google/mcp) | Official Google collection; good for cross-cloud comparisons. |
| Celonis | Celonis MCP Server Asset (Process Intelligence) | Process Intelligence / Graph | Vendor asset (enterprise) | [Docs](https://developer.celonis.com/mcp-server-asset/overview/) | (see Celonis asset docs; depends on customer Celonis environment) | (vendor docs) | Direct comparator for 'graph-shaped' differentiation (PI Graph context). |

---

## Discovery Sources (Long-Tail Expansion)

| Source | Type | Link | Notes |
|---|---|---|---|
| modelcontextprotocol — Reference + community servers list | Directory | [Link](https://github.com/modelcontextprotocol/servers) | Use as long-tail expansion source. |
| habitoai — Awesome MCP Servers directory | Directory | [Link](https://github.com/habitoai/Awesome-MCP-Servers-directory) | Categorized directory for discovery. |
| punkpeye — awesome-mcp-servers | Directory | [Link](https://github.com/punkpeye/awesome-mcp-servers) | Curated list; production vs experimental tags. |
| mcpservers.org — Awesome MCP Servers (website) | Directory | [Link](https://mcpservers.org/) | Searchable catalog; useful for monitoring new entries. |

---

## Research Insights

### Category Distribution

- **Observability / SecOps:** 1 provider (Splunk)
- **Observability:** 1 provider (Datadog)
- **Cloud / Infrastructure:** 1 provider (Microsoft Azure)
- **Cloud / Edge / Security:** 1 provider (Cloudflare)
- **Cloud / Productivity:** 1 provider (Google)
- **Dev / Version Control:** 1 provider (GitHub)
- **Docs / Knowledge:** 1 provider (Microsoft Learn)
- **Productivity / Knowledge:** 1 provider (Notion)
- **Incident Response:** 1 provider (PagerDuty)
- **Process Intelligence / Graph:** 1 provider (Celonis)

### Deployment Type Distribution

- **Remote (hosted):** 1 provider (Microsoft Learn)
- **Remote (marketplace/managed):** 1 provider (Splunk)
- **Remote (preview):** 1 provider (Datadog)
- **Remote hosted + local/HTTP modes:** 1 provider (Notion)
- **Remote managed catalog + OSS servers:** 1 provider (Cloudflare)
- **Local (official) + IDE integrations:** 1 provider (Microsoft Azure)
- **Local (official):** 1 provider (PagerDuty)
- **Server (runs locally or hosted by integrators):** 1 provider (GitHub)
- **Collection (official):** 1 provider (Google)
- **Vendor asset (enterprise):** 1 provider (Celonis)

### Key Findings

- **Total Providers Researched:** 10 (Batch 1)
- **Discovery Sources:** 4 directories/catalogs
- **Primary Categories:** Observability (2), Cloud/Infrastructure (3), Dev/Version Control (1), Knowledge/Productivity (2), Incident Response (1), Process Intelligence (1)
- **Deployment Patterns:** 
  - **Remote:** 5 providers (hosted, marketplace, preview, managed catalog)
  - **Local:** 3 providers (official, IDE integrations)
  - **Hybrid:** 1 provider (Notion — hosted + local/HTTP)
  - **Collection/Asset:** 2 providers (Google collection, Celonis enterprise asset)
- **Enterprise Anchors:** 
  - Splunk (Microsoft Marketplace listing)
  - Microsoft (official, multiple servers)
  - GitHub (official, enterprise code/PR automation)
- **OSS vs Managed:** Mix of open-source repos and vendor-managed solutions

---

## Next Steps

1. **Assess:** Apply Trust Score v1 rubric to each provider
2. **Gather Evidence:** Collect auth configs, SBOMs, hosting details, audit logs
3. **Score:** Compute Trust Scores and Evidence Confidence levels
4. **Publish:** Release scorecards to MCP Trust Index
5. **Expand:** Use discovery sources to identify Batch 2 providers
