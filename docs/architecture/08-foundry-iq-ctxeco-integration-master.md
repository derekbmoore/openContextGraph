# Foundry IQ + ctxEco Integration Master (Data → Information → Knowledge → Wisdom)

## Purpose

This is the **master integration document** for deeply integrating **ctxEco / OpenContextGraph** with **Microsoft Foundry / Azure AI Foundry**, specifically the **Foundry IQ** knowledge layer and the **Tools** surface (built-in tools + MCP).

Primary goal: ship a **GTM MVP** where customers can adopt ctxEco as a **bring-your-own MCP server** (and optionally a Marketplace offer), while building a Foundry-native **Data → Information → Knowledge → Wisdom (DIKW)** experience in the Foundry portal.

## TL;DR (Executive Summary)

- **We already have**: Foundry-first chat flow, Foundry agents (Elena/Marcus/Sage), an MCP endpoint (`/mcp`) with a tool manifest and working memory/story/diagram tools.
- **Next build focus**: the Foundry portal’s **Knowledge** section (Foundry IQ knowledge bases + source onboarding) and **Tools** section (MCP + Action Groups) with rigorous **gating** (tenant/project/group boundaries + truth/sensitivity classes).
- **GTM MVP**: publish a hardened ctxEco MCP server as “Context Ecology Memory + KeywordVectorGraph” with a small, high-value tool set (search, ingest, evidence, governance), and pair it with a Foundry IQ KB recipe for M365 + OneLake.

## Terminology (Align the Names)

- **Microsoft Foundry / Azure AI Foundry**: Microsoft’s AI platform + portal (models, agents, tools, governance).
- **Foundry IQ**: Foundry’s **multi-source knowledge base** layer (built on Azure AI Search capabilities) for agent grounding across SharePoint/OneLake/etc.
- **MCP (Model Context Protocol)**: JSON-RPC protocol for tool/resource discovery and tool invocation. Spec: `https://spec.modelcontextprotocol.io/`.
- **Foundry MCP Server (Microsoft-managed)**: Microsoft’s hosted MCP endpoint (`https://mcp.ai.azure.com`) that exposes Foundry/Model/Agent/Deployment/Evaluation operations via MCP.
- **Azure MCP Server (Microsoft)**: MCP server(s) exposing Azure resource operations (including PostgreSQL and Marketplace-related tooling) to MCP clients.
- **ctxEco MCP Server (ours)**: the ctxEco endpoint used by Foundry agents as an external MCP tool provider.
- **KeywordVectorGraph (product capability)**: ctxEco’s **Tri-Search™** (keyword + vector + graph) + provenance + graph edges as a publishable “knowledge substrate”.

## What’s Already Implemented (Repo Reality)

### Foundry-first orchestration

- The chat system was refactored to a **“Foundry drives execution”** flow with strict HTTPS handling and a dedicated Foundry client layer.
- MCP tool routing exists server-side, enabling Foundry agents to call back into ctxEco tools.

### MCP server surface (ctxEco)

- **MCP tool registry**: `backend/api/mcp_tools.py`
- **MCP handlers**: `backend/api/mcp_handlers.py`
- **Working tools** (at least):
  - `search_memory` (Tri-Search™ against Zep)
  - `list_episodes`
  - `generate_story` (Temporal → Claude)
  - `generate_diagram` (Gemini)
- **Stubs / placeholders** exist for code search, project status, GitHub issue creation, ingestion trigger (ready for real implementations).

### Knowledge substrate (ctxEco)

- **Tri-Search™** is documented and implemented as hybrid retrieval (keyword + similarity; graph edges available via memory graph endpoint).
- **Antigravity Router** is the ingestion philosophy: A/B/C truth-class routing + metadata for decay, sensitivity, provenance.

## DIKW in Foundry Portal (What We Build Next)

The Foundry portal experience should map cleanly to DIKW. The same sources and artifacts should be usable by:
1) Foundry IQ knowledge bases, and 2) ctxEco’s MCP tools (our “knowledge substrate”).

### Data (Sources)

**Goal**: maximize the number of high-signal enterprise sources connected, while respecting identity and permission boundaries.

- **Targets (MVP)**:
  - M365 SharePoint sites/libraries (high-value docs)
  - OneLake / Lakehouse (structured + semi-structured)
  - Azure Blob Storage (bulk documents)
  - GitHub repos (engineering knowledge)
  - At least one operational telemetry source (Splunk is a real Marketplace example)
  - At least one DB source (PostgreSQL or SQL)

### Information (Normalization)

**Goal**: convert raw data into structured, attributable information with strong metadata.

- **Antigravity ingestion**:
  - Class A (Immutable truth): layout fidelity extraction (Docling)
  - Class B (Ephemeral): semantic chunking (Unstructured)
  - Class C (Operational): structured ingestion (Pandas; preserve numeric fidelity)
- **Minimum metadata for every chunk**:
  - `provenance_id` (source URI + immutable ID)
  - `data_class` (A/B/C)
  - `decay_rate`
  - `sensitivity_level` (high/moderate/low)
  - `tenant_id`, `project_id`, `acl_groups` (gating controls)

### Knowledge (Retrieve + Graph + Evidence)

**Goal**: make knowledge queryable as a product surface inside Foundry: reliable retrieval, citations, and relationship context.

Two parallel “knowledge planes” can coexist (and should):

- **Foundry IQ plane** (Foundry-native KBs):
  - Multi-source retrieval across configured sources.
  - Best for “my org’s docs” with built-in permission trimming.
- **ctxEco KeywordVectorGraph plane** (our MCP server):
  - Tri-Search™ + graph edges + episodic memory + operational telemetry.
  - Best for “context ecology” (governed memory, decay, provenance, and cross-system synthesis).

### Wisdom (Agentic action + governance)

**Goal**: guided action with safe autonomy.

- **Wisdom behaviors**:
  - “Ask before acting” for destructive operations
  - policy-driven tool allowlists by agent persona (Elena/Marcus/Sage)
  - audit logs + evidence bundles + golden-thread validations
- **Wisdom artifacts**:
  - evaluation datasets, baselines, and regression tests (Foundry evals + our golden-thread suite)
  - governance docs: what is allowed, by whom, in which tenant/project

## Foundry Integration Architecture (Target)

### Pattern A (Recommended MVP): Foundry Agent + Foundry IQ KB + ctxEco MCP tools

- **Foundry Agent**:
  - uses **Foundry IQ KB** for grounding (SharePoint/OneLake/etc.)
  - uses **ctxEco MCP** for:
    - cross-source retrieval when KB coverage is incomplete
    - episodic memory and evidence bundles
    - ingestion triggers and metadata enforcement
    - specialized graph traversal / “why” explanations

### Pattern B: Foundry IQ KB is primary; ctxEco is the ingestion + governance layer

- ctxEco runs ingestion pipelines and writes to an indexable store (e.g., Azure AI Search / OneLake),
  then Foundry IQ becomes the main retrieval engine.
- ctxEco MCP remains the **governance, provenance, and operations** layer.

### Pattern C: ctxEco is primary; Foundry IQ is optional

- For customers who can’t adopt Foundry IQ yet, Foundry agents still get “knowledge” through ctxEco MCP (`search_memory`, `list_episodes`, graph endpoints).

## Knowledge: What To Build in Foundry IQ (Now)

### 1) Knowledge base strategy

- **KB-1 (M365 Knowledge)**: SharePoint (primary), plus whatever is supported in the tenant (OneLake if available).
- **KB-2 (Engineering Knowledge)**: GitHub repos + runbooks + architecture docs.
- **KB-3 (Operations Knowledge)**: telemetry (Splunk) + incident runbooks + known issues.

### 2) Gating model (permission trimming + ctxEco “context ecology”)

We need two layers of gating:

- **Foundry IQ gating**: built-in permission trimming where supported by the source.
- **ctxEco gating** (always-on):
  - tenant isolation (`tenant_id`)
  - project isolation (`project_id`)
  - group-based access (`acl_groups`)
  - truth/sensitivity gating (A/B/C + high/moderate/low)

### 3) Known platform gaps to design around

- SharePoint remote knowledge sources exist (preview), but **OneDrive is not included** in the “remote SharePoint” pathway.
- Plan for OneDrive via:
  - ingestion into Blob/OneLake, or
  - a custom MCP tool that fetches and ingests OneDrive content with proper delegated auth.

## Tools: What To Build in Foundry (Now)

### Tool surfaces we should support

- **MCP tool** (preferred for GTM): a single MCP server URL that exposes multiple tools with discoverability.
- **Action Group / HTTP tools** (still useful): simple REST endpoints for narrower enterprise integration.

### Minimum viable ctxEco MCP toolset (GTM MVP)

These are the “we can sell this” tools that map directly to Foundry portal “Tools”:

1. **`search_memory`** (already live): Tri-Search™ retrieval with evidence metadata.
2. **`trigger_ingestion`**: create/refresh a source; route via Antigravity (A/B/C).
3. **`get_evidence_bundle`** (new): return citations + provenance + why-this-result (auditable).
4. **`list_sources` / `get_source_status`** (new): “are we connected, indexed, fresh?”
5. **`policy_check`** (new): explain if a tool action is allowed for this agent/user context.

### “Source unlockers” (high GTM leverage)

Build MCP tools that unlock sources Foundry IQ can’t reach easily (or can’t gate how we need):

- OneDrive ingestion (delegated)
- Teams chat exports (policy-controlled)
- GitHub issues/PRs (Marcus)
- Jira/ServiceNow tickets (operations)
- Splunk queries (either via Splunk MCP Server, or via ctxEco if we want one surface)

## Marketplace / Catalog Research (What Exists in Early 2026)

### 1) Microsoft-managed MCP servers exist (not our product, but important context)

- **Foundry MCP Server (preview)**: `https://mcp.ai.azure.com` for model/agent/deployment/evaluation operations.
- **Azure MCP Server (preview)**: exposes Azure resource operations; includes tooling for PostgreSQL and Marketplace discovery.

### 2) Third-party MCP servers on Microsoft Marketplace (real example)

- **Splunk MCP Server** is listed as an Azure Marketplace SaaS offer and exposes Splunk data/query tools (e.g., run SPL queries, list indexes, knowledge objects).
  - Marketplace listing: `https://marketplace.microsoft.com/en-us/product/saas/splunk.splunk_mcp_server`

### 3) What “made it” so far (pattern recognition)

The MCP offerings that show up are typically:

- **Data/Telemetry access** (Splunk-style)
- **Database access** (PostgreSQL/SQL patterns) via Microsoft MCP servers or reference implementations
- **Implementation services** (consulting offers that build MCP servers for customers)

Implication: our best Marketplace story is **“Knowledge substrate + governance + evidence”** (not just “yet another RAG connector”).

## How ctxEco / KeywordVectorGraph Should Be Positioned for Foundry

### “KeywordVectorGraph” as a publishable capability

In Foundry terms, KeywordVectorGraph should be marketed as:

- **Hybrid retrieval**: keyword + vector + graph fusion (Tri-Search™)
- **Governed memory**: decay + truth classes + sensitivity controls
- **Evidence-first answers**: provenance links + metadata + explainability
- **Cross-source synthesis**: unify Foundry IQ grounding with operational memory

### Packaging options (practical)

- **Option 1 (fastest GTM)**: “Bring your own MCP URL” + reference deployment templates (Azure Container Apps).
- **Option 2 (enterprise distribution)**: register ctxEco MCP in **Azure API Center** for discovery inside customer tenants.
- **Option 3 (broader GTM)**: Microsoft commercial marketplace offer (likely SaaS or Managed App) that provisions a hosted MCP endpoint per tenant.

## GTM MVP Plan (Elena + Marcus + Sage)

### MVP definition (what we ship)

- **A Foundry Agent bundle** (Elena/Marcus/Sage) configured with:
  - 1–3 Foundry IQ KBs (M365 + Eng + Ops)
  - ctxEco MCP server attached with the MVP toolset
- **A “Sources” playbook**: how to connect the first 10–16 sources quickly and safely
- **A demo “Golden Thread”**: repeatable proof-of-life scenario that shows DIKW end-to-end

### Roles

- **Elena (Knowledge + Sources)**:
  - define KB templates and “source gating” defaults
  - prioritize connectors (M365 first)
  - drive permission trimming and sensitivity alignment
- **Marcus (Tools + Ops + DevEx)**:
  - implement real `search_codebase`, GitHub, ingestion triggers, source status tools
  - harden auth (Entra/OBO), audit logging, and rate limiting
- **Sage (Narrative + Demo + GTM content)**:
  - produce the demo story + demo scripts
  - craft “why ctxEco vs generic RAG” narrative with evidence screenshots/metrics

### North-star metrics (MVP)

- **Time-to-first-answer**: from “new tenant” → “agent answers from SharePoint + ctxEco memory” in < 60 minutes
- **Coverage**: at least 6 meaningful sources connected (with gating) in the MVP demo tenant
- **Evidence rate**: > 80% of answers include provenance links/citations
- **Safety**: no cross-tenant leakage; project boundaries verified via tests

## Azure CLI (Current Reference, macOS)

### Required baseline

- Azure CLI should be current for provisioning and automation.
- As of **Jan 2026**, Azure CLI stable is **2.82.0**.
  - Release notes: `https://learn.microsoft.com/en-us/cli/azure/release-notes-azure-cli`
  - Homebrew formula: `https://formulae.brew.sh/formula/azure-cli`

### Install / upgrade (Homebrew)

```bash
brew update
brew install azure-cli
brew upgrade azure-cli
az --version
az login
```

## Key Reference Links (Keep These Handy)

- Azure AI Foundry Agents: `https://learn.microsoft.com/en-us/azure/ai-foundry/agents/`
- Foundry Agents MCP tool (BYO MCP server): `https://learn.microsoft.com/azure/ai-foundry/agents/how-to/tools/model-context-protocol`
- Foundry MCP Server preview (Microsoft-managed): `https://devblogs.microsoft.com/foundry/announcing-foundry-mcp-server-preview-speeding-up-ai-dev-with-microsoft-foundry/`
- Azure MCP Server overview: `https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/overview`
- SharePoint remote knowledge source (Azure AI Search): `https://learn.microsoft.com/en-us/azure/search/agentic-knowledge-source-how-to-sharepoint-remote`
- Foundry IQ overview (blog): `https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/foundry-iq-unlocking-ubiquitous-knowledge-for-agents/4470812`
- Azure API Center register/discover MCP servers: `https://learn.microsoft.com/en-us/azure/api-center/register-discover-mcp-server`

