# ctxEco Verified MCP: Microsoft Marketplace GTM Master Plan

**Date:** 2026-01-22  
**Status:** GTM Ready - Phase 1 Complete (Incorporates Verified MCP / MCP Security Posture Management)  
**Target:** Microsoft Marketplace SaaS Offer + Azure AI Foundry Tool Catalog  
**Publisher:** Zimax Networks LC (Phoenix, Arizona, USA)  
**OSS Foundation:** `derekbmoore/openContextGraph` (**MIT**) + related OSS components  
**Companion Assets:** SecAI Framework (assessment methodology) + **SecAI Radar: MCP Trust Registry** (governance application)

---

## Executive Summary

Azure AI Foundry is accelerating adoption of **Model Context Protocol (MCP)** tooling, but Microsoft's own documentation warns that **third-party MCP servers are not verified** and customers must **review and track what they connect**.

**ctxEco Verified MCP** turns that warning into a product advantage:

- **Governed Knowledge Substrate:** Hybrid retrieval + **Graph Knowledge (Gk)** with provenance-first outputs
- **Verified MCP (MCP Security Posture Management):** **SecAI Radar: MCP Trust Registry** — A trust registry, risk scoring, approval workflows, and runtime guardrails for MCP servers/tools, plus **MCP Trust Index** (public content program)
- **Audit-Ready Evidence:** Every tool invocation and knowledge claim is attributable, exportable, and defensible for security/compliance reviews
- **Enterprise-Ready Deployment Options:** Customer-hosted ("BYO MCP URL") first, then transactable Marketplace SaaS, plus private tool catalogs via API Center

**Market Position:** Not "yet another RAG connector" but the **only MCP server** offering:
- **Graph Knowledge (Gk)** as the trust substrate (multi-hop traceability, permission-trimmed relationships, provable provenance)
- **Verified MCP governance** (trust registry, scoring, approvals, drift detection)
- **Complete DIKW stack** (Data → Information → Knowledge → Wisdom) with enterprise governance

**GTM Status:** ✅ Phase 1 Complete (Foundry IQ client + 12 MCP tools operational)

---

## Table of Contents

1. [Market Analysis & Category Definition](#market-analysis)
2. [Enterprise Value Proposition & ICP](#value-proposition)
3. [Differentiation: Verified MCP + Graph Knowledge](#differentiation)
4. [GTM MVP Requirements](#gtm-mvp)
5. [Implementation Status](#implementation-status)
6. [Marketplace + Foundry Distribution Strategy](#marketplace-strategy)
7. [Pricing & Packaging](#pricing)
8. [Sales Enablement](#sales-enablement)
9. [Technical Architecture](#architecture)
10. [Roadmap](#roadmap)
11. [Success Metrics](#success-metrics)
12. [SecAI Radar: MCP Trust Registry Product Details](#secai-radar)
13. [MCP Trust Index: Content GTM Strategy](#trust-index)
14. [Registry Data Model (Graph-First)](#registry-model)
15. [Appendix: MCP Trust Score (v1)](#appendix-trust-score)
16. [Appendix: MCP Trust Index Scorecard Template](#appendix-scorecard-template)

---

## Market Analysis & Category Definition {#market-analysis}

### The Market Reality (Early 2026)

Most MCP "products" fall into one of these buckets:

1. **Connectors to systems of record**  
   Examples: telemetry platforms, ticketing systems, doc repositories, cloud resources.  
   Value: "My agent can query system X."

2. **Platform-native MCP tools**  
   Examples: vendor-provided cloud operations tooling.  
   Value: "My agent can manage platform resources safely (within vendor patterns)."

3. **Knowledge retrieval MCP tools**  
   Examples: doc search and KB retrieval.  
   Value: "My agent can ground answers in approved content."

**What's missing (and now explicitly called out by Microsoft):**  
A dedicated layer that helps enterprises **verify** MCP endpoints, manage **tool risk**, prevent **excessive agency**, and produce **audit evidence**.

### Category We Will Own: MCP Security Posture Management (MCP-SPM)

**Definition:** A control plane for MCP that provides:

- Inventory of MCP servers and exposed tools
- Risk scoring and security review before enablement
- Runtime guardrails (least privilege + approvals + policy enforcement)
- Monitoring, drift detection, and audit packs

This becomes the natural extension of **SecAI Framework** and **SecAI Radar** into the "agentic integration security" space.

### Competitive Positioning Matrix (Updated)

| Capability | Connector-only MCP | Platform MCP | RAG/Docs MCP | **ctxEco Verified MCP** |
||---|---:|---:|---:|---:|
| Multi-source access | ⚠️ varies | ⚠️ | ⚠️ | ✅ |
| Hybrid retrieval (fusion) | ❌ | ❌ | ⚠️ | ✅ |
| **Graph knowledge (Gk)** | ❌ | ❌ | ❌ | ✅ **core** |
| Evidence bundles / provenance | ❌ | ⚠️ | ⚠️ | ✅ **default** |
| Tool governance (approval gates) | ⚠️ | ⚠️ | ❌ | ✅ |
| **MCP trust registry + scoring** | ❌ | ❌ | ❌ | ✅ **category-defining** |
| Drift detection (tools/permissions changed) | ❌ | ❌ | ❌ | ✅ |
| Compliance export ("audit pack") | ❌ | ❌ | ❌ | ✅ |

**Bottom line:** We are not "another connector." We are the **trusted substrate + security control plane** that makes MCP adoption safe, scalable, and auditable.

---

## Enterprise Value Proposition & ICP {#value-proposition}

### Primary Value: "Safe MCP Adoption at Enterprise Scale"

Enterprises want the productivity of agents + tools, but they need:

- **Control:** What tools exist, who owns them, and what they can do
- **Safety:** Minimized blast radius (least privilege, approvals, policy gates)
- **Assurance:** Evidence for auditors, security teams, and risk owners
- **Truth & provenance:** Outputs that can be traced back to sources

ctxEco Verified MCP delivers this through **Gk graph knowledge** + **MCP-SPM governance**.

### Ideal Customer Profiles (ICP)

1. **CISOs / Security Architecture teams**
   - Need: risk controls, auditability, policy alignment (NIST AI RMF, CIS, NIST 800-53, etc.)
   - Value: repeatable approval & evidence for agent/tool integrations

2. **Platform Engineering / Cloud Center of Excellence**
   - Need: safe self-service tooling, change control, standardized integrations
   - Value: enable agents without opening the floodgates

3. **Compliance, GRC, and Audit**
   - Need: defensible evidence trails and change history
   - Value: "audit pack" exports and consistent control mapping

4. **Engineering leaders adopting agents**
   - Need: speed, reliability, grounded answers, fewer incidents
   - Value: hybrid retrieval + provenance + safer actions

### Top Use Cases (Buying Triggers)

1. **"We want to use MCP in Foundry, but security says no."**  
   → Trust Registry supplies review + tracking + approval + evidence.

2. **"We had a tool misfire / unauthorized action risk."**  
   → Runtime guardrails + approval gates + audit trail.

3. **"We must prove compliance for AI integrations."**  
   → Evidence packs aligned to NIST AI RMF outcomes.

4. **"We need a private tools catalog for internal MCP servers."**  
   → Azure API Center-backed catalog + Trust Registry overlays.

5. **"We need to compare MCP vendors rationally."**  
   → Trust Index scorecards.

---

## Differentiation: Verified MCP + Graph Knowledge {#differentiation}

### 1. Verified MCP (MCP Security Posture Management) — Our Headline

**What it is:**  
**SecAI Radar: MCP Trust Registry** — A dedicated governance layer that treats MCP endpoints and tools as governed assets with lifecycle controls.

**Core features:**
- **MCP Trust Registry:** inventory, ownership, environment scoping, data classification, tool catalog
- **MCP Trust Score:** risk scoring (identity, hosting posture, privileges, data handling, monitoring, maintenance hygiene)
- **Approval workflows:** allowlist/denylist, change approval, time-bound approvals (JIT)
- **Runtime guardrails:** policy checks before tool execution; "destructive tool" gating
- **Drift detection:** alerts when tools, scopes, endpoints, or behaviors change
- **Audit packs:** export everything needed for reviews (who approved what, when, why, and what happened)

**Why it wins:**  
Microsoft explicitly places the burden of verifying and tracking third-party MCP on customers. We productize that requirement through **SecAI Radar: MCP Trust Registry**.

**Product positioning:**
- **SecAI Radar: MCP Trust Registry** = Enterprise SaaS product (inventory, scoring, approvals, evidence)
- **MCP Trust Index** = Public content program (scorecards, rankings, methodology) that drives inbound demand

### 2. Graph Knowledge (Gk) as the Trust Substrate

**What it is:**  
A graph-native knowledge model that links **entities, evidence, and decisions** across tools and data sources.

**Why it matters:**  
Most MCP servers are "flat retrieval." Enterprises need:
- multi-hop traceability,
- permission-trimmed relationships,
- and provable provenance over time.

**What this unlocks:**
- "Show me the evidence trail for this claim."
- "What changed since last week that affects this control?"
- "Which agents/tools can touch regulated data?"

**Competitive advantage:**
- No other MCP server has graph-native knowledge
- Most are flat RAG systems without relationship understanding

### 3. Hybrid Retrieval (Foundry IQ + Tri-Search™)

**What it is:**
- Fuses Foundry IQ knowledge bases (SharePoint, OneLake) with ctxEco Tri-Search™
- Uses Reciprocal Rank Fusion (RRF) for ranking
- Normalizes results from both sources

**Why it matters:**
- Foundry IQ = "my org's documents" (fast, permission-trimmed)
- ctxEco = "operational memory" (conversations, patterns, telemetry)
- Together = complete knowledge picture

**Competitive advantage:**
- No other MCP server offers hybrid fusion
- Most are single-source connectors

### 2. Governed Memory (Decay + Truth + Sensitivity)

**What it is:**
- **Decay rates:** Class A (immutable truth) vs Class B (ephemeral) vs Class C (operational)
- **Truth classes:** Immutable truth, ephemeral data, operational telemetry
- **Sensitivity:** High/moderate/low (NIST-aligned)

**Why it matters:**
- Safety manuals don't decay (Class A)
- Slack messages do decay (Class B)
- Sensor logs are operational (Class C)
- Different retention, different precision

**Competitive advantage:**
- No other MCP server has truth-value classification
- Most treat all data equally

### 3. Evidence-First Answers

**What it is:**
- Every answer includes citations
- Provenance tracking (source URI + immutable ID)
- "Why this result" explanations
- Audit-ready evidence bundles

**Why it matters:**
- Enterprises need to trust AI answers
- Compliance requires citations
- Debugging needs provenance

**Competitive advantage:**
- Most MCP servers don't provide citations
- None provide evidence bundles

### 4. Cross-Source Synthesis

**What it is:**
- Unifies Foundry IQ grounding with operational memory
- Connects documents to conversations to telemetry
- Semantic graph relationships

**Why it matters:**
- Documents alone aren't enough
- Need operational context
- Need relationship understanding

**Competitive advantage:**
- No other MCP server synthesizes across sources
- Most are single-purpose connectors

### 5. DIKW Stack (Data → Information → Knowledge → Wisdom)

**What it is:**
- **Data:** Raw sources (SharePoint, OneLake, telemetry)
- **Information:** Normalized, attributable chunks
- **Knowledge:** Retrievable, graph-connected facts (Gk)
- **Wisdom:** Agentic action with governance

**Why it matters:**
- Enterprises need the full stack
- Not just RAG, but governed knowledge → wisdom

**Competitive advantage:**
- No other MCP server implements DIKW
- Most are flat RAG systems

### 6. SecAI Framework Alignment (Assessment-Ready)

**What it is:**  
We ship a mapping-ready structure (controls, evidence objects, measurement outputs) that plugs into SecAI Framework and can be rendered by SecAI Radar.

**Why it matters:**  
It turns MCP + tools into a measurable security posture program aligned to NIST AI RMF and enterprise control frameworks.

---

## GTM MVP Requirements {#gtm-mvp}

### MVP Scope: Ship Value in 30–45 Days (Customer-Hosted First)

The MVP must prove two things immediately:
1) ctxEco delivers **better answers + safer actions** (hybrid + evidence)  
2) ctxEco reduces MCP adoption risk via a **trust registry + scoring** baseline

### Minimum Viable Toolset (12 Tools - Current + 5 Verified MCP Tools)

**A. Knowledge & Retrieval (5) ✅**
1. ✅ **`search_memory`** / **`search.trisearch`** - Tri-Search™ retrieval (keyword + vector + graph)
2. ✅ **`query_foundry_iq_kb`** / **`search.iq`** - Foundry IQ KB query
3. ✅ **`list_foundry_iq_kbs`** - Discover KBs
4. ✅ **`get_foundry_iq_kb_status`** - KB health
5. ⏳ **`search.hybrid`** - Fusion search across IQ + Tri-Search + Gk

**B. Graph Knowledge (Gk) (1) ⏳**
6. ⏳ **`graph.query`** - Entity/relationship query (Gk)

**C. Verified MCP / Trust Registry (SecAI Radar) (5) ⏳**
7. ⏳ **`mcp.registry.upsert_server`** - Register MCP endpoint + metadata (SecAI Radar)
8. ⏳ **`mcp.registry.list_servers`** - Inventory and filtering (SecAI Radar)
9. ⏳ **`mcp.score.compute`** - Compute trust score (v1 rubric) (SecAI Radar)
10. ⏳ **`mcp.policy.evaluate`** - Policy gate before tool execution (SecAI Radar)
11. ⏳ **`mcp.audit.export`** - Audit pack export (JSON + human summary) (SecAI Radar)

**D. Evidence & Context (1) ⏳**
12. ⏳ **`evidence.bundle`** - Produce citations/provenance pack for an answer

**E. Memory & Context Tools ✅**
13. ✅ **`list_episodes`** - Conversation history
14. ✅ **`read_domain_memory`** - Project patterns
15. ✅ **`update_domain_memory`** - Learn patterns
16. ✅ **`scan_commit_history`** - Git analysis

**F. Story & Visualization Tools ✅**
17. ✅ **`generate_story`** - Narrative generation
18. ✅ **`generate_diagram`** - Visual diagrams

**G. Code & Database Tools ✅**
19. ✅ **`search_codebase`** - Code search
20. ✅ **`query_database`** - SQL queries

**H. Ops Essentials (2) ⏳**
21. ⏳ **`health.status`** - Readiness and dependency checks
22. ⏳ **`admin.config`** - Tenant/project scoping and governance settings

### Non-Negotiable Enterprise Requirements (MVP)

- Entra-friendly auth patterns (customer-hosted: managed identity where possible)
- Tenant/project scoping enforced server-side
- Structured audit logs for tool calls (who/what/when/inputs/outputs hash)
- Clear data handling boundaries (what leaves the tenant, what stays)
- Safety defaults: deny by default for high-risk tools unless approved

### North-Star Metrics

- ✅ **Time-to-first-answer:** < 60 minutes (new tenant → agent answers)
- ✅ **Coverage:** 6+ meaningful sources connected
- ⏳ **Evidence rate:** > 80% answers include citations (Phase 2)
- ✅ **Safety:** Zero cross-tenant leakage

---

## Implementation Status {#implementation-status}

### Phase 1: Foundry IQ Integration ✅ COMPLETE

**Status:** ✅ **Operational**

**Completed:**
- ✅ Foundry IQ client (`backend/integrations/foundry_iq.py`)
- ✅ Azure AI Search integration
- ✅ 3 new MCP tools (list, query, status)
- ✅ Configuration (endpoint, key, index)
- ✅ MCP handlers and routing
- ✅ Dependencies (`azure-search-documents`)

**Tools Available:** 12 MCP tools (9 existing + 3 Foundry IQ)

### Phase 2: Evidence & Hybrid Search ⏳ IN PROGRESS

**Status:** ⏳ **Planned**

**Needed:**
- ⏳ Hybrid search implementation (`backend/memory/hybrid_search.py`)
- ⏳ Evidence bundle tool (`get_evidence_bundle`)
- ⏳ Source management tools (`list_sources`, `get_source_status`, `trigger_ingestion`)
- ⏳ Policy check tool (`policy_check`)

**Target:** Week 2-3

### Phase 3: Testing & Hardening ⏳ PLANNED

**Status:** ⏳ **Planned**

**Needed:**
- ⏳ Integration tests
- ⏳ Security hardening
- ⏳ Performance optimization
- ⏳ Documentation

**Target:** Week 3-4

---

## Marketplace + Foundry Distribution Strategy {#marketplace-strategy}

### Packaging Options

#### Option 1: "Bring Your Own MCP URL" (Fastest GTM) ✅ RECOMMENDED FIRST

**What it is:**
- Customer deploys ctxEco MCP server in their Azure tenant (Container Apps recommended)
- They provide the MCP URL to Foundry agents/tools configuration
- Data stays in customer control; easiest security approval

**Why it works:**
- Minimizes procurement friction
- Maximizes enterprise trust early
- Lets us iterate on registry/scoring with real feedback

**GTM Timeline:** Immediate (can ship now)

#### Option 2: Private Tool Catalog (Azure API Center) ✅ ENTERPRISE DISCOVERY

**What it is:**
- Publish ctxEco tools into customer's private catalog
- Enables curated adoption with centralized governance

**Why it works:**
- Aligns with large-org tool allowlisting
- Establishes "official" tooling presence in enterprise environments

**GTM Timeline:** Month 2

#### Option 3: Microsoft Marketplace Transactable SaaS (Broad Distribution)

**What it is:**
- Managed ctxEco Verified MCP endpoint (SaaS)
- Microsoft procurement + billing pathway for customers
- Requires stronger compliance package and operational maturity

**Why it works:**
- Unlocks enterprise buying motion
- Enables revenue at scale

**GTM Timeline:** Month 3-4

### Recommended Phased Rollout

#### Phase 1 — Land (0–60 days)
- Publish Trust Index methodology + first 10 scorecards
- Ship Trust Registry MVP (customer-hosted first if needed)
- Pilot with 1–3 design partners (AI platform or cloud security teams)

#### Phase 2 — Expand (60–120 days)
- Integrate with Foundry workflows (private tool catalogs; "approved list")
- Launch "Verified Provider" program
- Add evidence packs and drift detection enhancements

#### Phase 3 — Scale (120–240 days)
- Publish Microsoft Marketplace offer(s):
  - SaaS Trust Registry
  - Regulated deployment option
- Pursue Microsoft partner co-sell motions (once referenceable customers exist)

---

## Pricing & Packaging {#pricing}

### Packaging Principle

Price based on:
- **Risk reduction + governance value** (registry/scoring/audit)
- **Usage** (queries/tool calls)
- **Breadth** (sources, MCP endpoints, environments)

### Suggested Tiers (v1)

#### Offer Types

**A) Free: MCP Trust Index (Public)**
- Scorecards + methodology
- Quarterly/Monthly "Top MCP Servers for Enterprise" posts
- "Pattern advisories" (e.g., static API keys vs OIDC; read-only vs write)

**B) Paid: SecAI Radar — MCP Trust Registry (SaaS)**
- Inventory, policy, scoring, approvals, drift, monitoring, evidence exports
- Multi-tenant + customer workspaces
- Optional managed MCP gateway (policy enforcement point)

**C) Paid: Customer-managed deployment (Regulated)**
- Deploy in customer Azure (Container Apps/Functions)
- Private networking options
- Full data residency + customer logs

#### Pricing Tiers

**Tier 1: Developer / OSS**
- Price: Free (self-hosted)  
- Includes: core OSS components + reference deployment + basic hybrid search  
- No hosted SLA; community support

**Tier 2: Verified MCP Starter**
- Price: $199–$499 / month (self-hosted with paid support OR hosted starter)  
- Includes: Trust Registry, Trust Score v1, audit exports, basic policies  
- Ideal for: early teams piloting MCP

**Tier 3: Verified MCP Enterprise**
- Price: $1,500–$5,000 / month (or usage-based)  
- Includes: advanced policy engine, drift detection, SSO/RBAC, retention controls, premium support  
- Ideal for: org-wide rollout

**Tier 4: Regulated / High Assurance**
- Price: custom  
- Includes: private networking, compliance artifacts, custom scoring rubrics, on-prem/isolated deployments, security reviews, optional attestation package

### Sales Motion

**Land:**
- Low-friction: "We'll help you approve MCP safely in 2 weeks"
- Fixed-fee assessment + config + first evidence pack

**Expand:**
- Subscription pricing for:
  - Registry seats (security + platform teams)
  - Number of MCP servers monitored
  - Evidence pack exports / audit module

**Scale:**
- Enterprise: annual contract + support + optional managed enforcement gateway

> Note: For Marketplace transactable SaaS, separate infra costs remain your responsibility—price accordingly.

---

## Sales Enablement {#sales-enablement}

### Core Narrative (Talk Track)

1) MCP adoption is exploding because it makes agents useful.  
2) Microsoft explicitly warns third-party MCP servers aren't verified—customers must review and track.  
3) Enterprises therefore need an MCP control plane: inventory, scoring, approvals, guardrails, and audit evidence.  
4) ctxEco Verified MCP provides that **and** improves answer quality via hybrid retrieval + Gk graph knowledge.

### Key Messages

#### Message 1: "Verified MCP: Make MCP Adoption Safe"
- Microsoft warns third-party MCP servers aren't verified
- We productize that requirement with trust registry + scoring
- Enterprises can adopt MCP with confidence

#### Message 2: "Graph Knowledge (Gk): Multi-Hop Traceability"
- Not flat RAG, but graph-native knowledge
- Multi-hop traceability, permission-trimmed relationships
- Provable provenance over time

#### Message 3: "Hybrid Retrieval = Complete Picture"
- Foundry IQ = enterprise documents
- ctxEco = operational memory + graph knowledge
- Together = complete knowledge with evidence

### Demo Script: "Golden Thread"

**Scenario:** Agent answers question using both Foundry IQ and ctxEco memory

1. **User asks:** "What's our security policy for API keys?"
2. **Agent searches:**
   - Foundry IQ KB (SharePoint docs)
   - ctxEco memory (past conversations, incidents)
3. **Agent responds:**
   - Answer with citations
   - Evidence bundle (provenance, sources)
   - Explanation ("why this result")
4. **User sees:**
   - Answer with citations
   - Source documents
   - Related conversations
   - Audit trail

**Time:** < 60 seconds from question to answer

### Objection Handling

**"We can just build a connector."**  
- Connectors don't solve governance, drift, or auditability.  
- The security burden shifts to the customer; that's where adoption slows.

**"We already have RAG."**  
- RAG doesn't manage tools, approvals, or runtime guardrails.  
- Our differentiator is **evidence + governance**, not just retrieval.

**"MCP is risky; we'll wait."**  
- That's exactly why Verified MCP exists: to make adoption safe and measurable.

### Competitive Battle Cards (High Level)

**vs Connector-only MCP**  
- They offer access. We offer **access + trust + governance + evidence**.

**vs Platform-native MCP**  
- They help with one platform. We unify **cross-source** knowledge and provide **tool governance** across the estate.

**vs Generic GRC tools**  
- They document controls. We generate **live evidence** and enforce runtime guardrails on agent/tool execution.

---

## Technical Architecture {#architecture}

### High-Level Architecture

```
Foundry Agent
   ↓  (MCP JSON-RPC)
ctxEco Verified MCP Server
   ↓
 ├─ Knowledge Plane
 │    ├─ Foundry IQ client (enterprise KB queries)
 │    ├─ Tri‑Search (keyword + vector + graph)
 │    └─ Gk graph knowledge (entities, relationships, provenance)
 │
 ├─ Governance Plane (Verified MCP)
 │    ├─ MCP Trust Registry (inventory, ownership, classification)
 │    ├─ Trust Score (rubric + scoring engine)
 │    ├─ Policy Gate (allowlist/approval/JIT)
 │    └─ Drift + Monitoring (change detection, alerts)
 │
 └─ Evidence Plane
      ├─ Citation & provenance builder
      └─ Audit Pack export (JSON + human summary)
```

### Knowledge Flow

```
Enterprise Sources (SharePoint, OneLake, etc.)
    ↓
Foundry IQ Knowledge Bases
    ↓
Azure AI Search Index
    ↓
ctxEco Hybrid Search
    ↓
    ├── Foundry IQ Results (enterprise docs)
    └── Tri-Search™ Results (operational memory)
    ↓
RRF Fusion
    ↓
Gk Graph Knowledge (entities, relationships, provenance)
    ↓
Evidence Bundle (citations + provenance)
    ↓
Agent Response
```

### Security & Governance Controls (Implementation Targets)

- **Tenant isolation:** strict `tenant_id` / `project_id` scoping  
- **Least privilege:** scoped tokens; deny-by-default tool policies  
- **Approval gates:** high-risk tools require explicit approval or time-bound token  
- **Audit logging:** immutable event logs for tool calls and policy decisions  
- **Data classification:** label sources/outputs and enforce redaction rules  
- **Retention controls:** configurable retention for logs and evidence packs  
- **Secure defaults:** "safe mode" for unknown/low-trust MCP endpoints

---

## Roadmap {#roadmap}

### Q1 2026: Ship Verified MCP MVP (Design Partners)

- Deliver 12-tool MVP including Trust Registry + Trust Score v1
- 3–5 design partners using customer-hosted deployment
- Publish initial "Verified MCP" documentation + onboarding playbooks

**Month 1 (Current):**
- ✅ Phase 1: Foundry IQ client + MCP tools
- ⏳ Phase 2: Hybrid search + evidence bundles + Verified MCP tools
- ⏳ Phase 3: Testing + hardening

**Month 2:**
- ⏳ Marketplace listing (Option 1: BYO MCP URL)
- ⏳ API Center registration (Option 2)
- ⏳ Early customer deployments

**Month 3:**
- ⏳ Marketplace SaaS offer (Option 3)
- ⏳ Production hardening
- ⏳ Sales enablement materials

### Q2 2026: Productize SecAI Radar as MCP Trust Registry

- Launch **SecAI Radar: MCP Trust Registry** SaaS product
- Introduce MCP Trust Registry UI (inventory, scoring, approvals, drift)
- Add scoring dashboards, drift alerts, and approval workflows
- Release exportable compliance artifacts aligned to SecAI Framework
- Launch **MCP Trust Index** public content program (scorecards, rankings, methodology)

### Q3 2026: Category Leadership ("MCP Trust Index")

- Launch **MCP Trust Index** public content program (scorecards, rankings, methodology)
- Publish scoring rubric v2 with stronger coverage (auth, hosting, safety, maintenance)
- Launch "Verified Provider" program for providers who pass validation
- Establish Zimax as the "trust authority" for MCP through content leadership

### Q4 2026: Marketplace Scale

- Transactable Marketplace SaaS offer (hosted)
- Partner motion (consultancies, MSPs) with co-sell packaging
- Expand connectors + integrate with enterprise SIEM/SOAR patterns

---

## Success Metrics {#success-metrics}

### Product Metrics

#### SecAI Radar: MCP Trust Registry
- **Time-to-first-trusted-tool (TTFTT):** minutes/hours to register + approve an MCP server
- **# MCP servers inventoried** per customer
- **% approved vs blocked** (approval rate)
- **Drift alerts / month** per customer
- **Evidence pack exports / quarter** per customer
- **Time-to-approval reduction** (before vs after SecAI Radar)

#### MCP Trust Index (Content Program)
- **Monthly visitors** to Trust Index content
- **Subscriber growth** (newsletter, GitHub stars)
- **Scorecard downloads** per month
- **Provider submissions** (evidence packs received)
- **Inbound demo requests** attributed to Trust Index

#### ctxEco MCP Server
- **% of tool calls with evidence bundles**
- **Reduction in "unattributed answers" and "unsafe tool calls"**
- **Tool Adoption:** % of customers using each tool
- **Query Volume:** Queries/month per customer
- **Evidence Rate:** % of answers with citations
- **Hybrid Usage:** % of queries using hybrid search

### Business Metrics
- **Design partner conversions to paid tiers**
- **Marketplace conversions** (views → trials → paid)
- **Average revenue per tenant and retention**
- **Trust Index → Trust Registry conversions** (content → product)
- **Time-to-Value:** < 60 minutes (new tenant → first answer)
- **Customer Satisfaction:** NPS > 50
- **Retention:** > 90% month-over-month
- **Expansion:** > 30% upgrade to Enterprise

### Technical Metrics
- **P95 tool-call latency**
- **Uptime/SLA achievement** (hosted tier)
- **Audit log integrity + completeness**
- **Uptime:** > 99.9% (Enterprise SLA)
- **Latency:** < 500ms (p95)
- **Error Rate:** < 0.1%
- **Cross-tenant Leakage:** 0 incidents

---

## Conclusion {#conclusion}

Microsoft's guidance makes the situation clear: **MCP is powerful, but trust is the customer's responsibility** when using third-party endpoints. That creates a new category need—**MCP Security Posture Management**—and ctxEco Verified MCP is purpose-built to lead it.

By combining **Gk graph knowledge**, **hybrid retrieval**, and **SecAI Radar: MCP Trust Registry**, we give enterprises a safe path to adopt agents and tools with confidence, evidence, and measurable risk reduction.

**The Complete Offering:**
- **ctxEco Verified MCP Server:** Governed knowledge substrate with hybrid retrieval + Gk
- **SecAI Radar: MCP Trust Registry:** Enterprise governance SaaS (inventory, scoring, approvals, evidence)
- **MCP Trust Index:** Public content program that establishes market authority and drives inbound demand

**ctxEco Verified MCP** is positioned as the **only** MCP server offering:
- ✅ **Graph Knowledge (Gk)** as the trust substrate (multi-hop traceability, permission-trimmed relationships, provable provenance)
- ✅ **Verified MCP governance** (trust registry, scoring, approvals, drift detection)
- ✅ Hybrid retrieval (Foundry IQ + Tri-Search™)
- ✅ Governed memory (decay + truth + sensitivity)
- ✅ Evidence-first answers (citations + provenance)
- ✅ Cross-source synthesis (unified knowledge)
- ✅ DIKW stack (Data → Information → Knowledge → Wisdom)
- ✅ SecAI Framework alignment (assessment-ready)

**Market Opportunity:** Enterprise customers need more than data connectors—they need **governed knowledge substrates** with evidence, compliance, and **MCP security posture management**.

**GTM Status:** ✅ Phase 1 Complete (Foundry IQ client + 12 MCP tools operational), ⏳ Phase 2 In Progress (Verified MCP tools)

**Next Steps:**
1. Complete Phase 2 (hybrid search + evidence + Verified MCP tools)
2. Deploy to design partners (Option 1: BYO MCP URL)
3. Register in API Center (Option 2)
4. Submit to Marketplace (Option 3)

---

## Immediate Next Actions (Next 7–10 Days)

1. **Finalize Trust Score rubric v1** (domains, weights, evidence requirements)
2. **Decide first 10 MCP providers** to score (mix of major + emerging)
3. **Build Trust Registry MVP screens:**
   - Add Server
   - Tool Inventory
   - Trust Score
   - Approval
   - Drift
   - Evidence Export
4. **Publish the first Methodology Post:**
   - "Why MCP Trust Matters"
   - "How We Score MCP Servers"
   - "Minimum Enterprise Requirements for MCP"

---

## SecAI Radar: MCP Trust Registry Product Details {#secai-radar}

### Product Overview

**SecAI Radar: MCP Trust Registry** is the enterprise governance layer for MCP adoption, delivered as:
- **SaaS product:** Multi-tenant registry with scoring, approvals, drift detection, evidence exports
- **Customer-managed deployment:** For regulated orgs (deploy in customer Azure, private networking)
- **Integration:** Works with Foundry private tool catalogs and Azure API Center

### Core Capabilities Roadmap

#### MVP (4–6 weeks)
- **Registry:** MCP server + tool inventory (metadata schema)
- **Trust Score v1:** automated + manual inputs
- **Approval workflow:** allow/deny + justification + expiry
- **Drift detection (basic):** new tools/permissions since last approval
- **Evidence export v1:** PDF/JSON bundle for review boards
- **Foundry integration path:** private tool catalog links + "approved tool list"

#### v1 (8–12 weeks)
- **Runtime telemetry:** tool call logging (hash inputs/outputs; do not over-retain sensitive content)
- **Policy engine:** allowlist + required-approval + environment restrictions
- **Identity posture checks:** token scope analysis, secret hygiene checks
- **Provider attestation support:** SOC2/ISO evidence attachments + SBOM refs
- **"Control mapping":** NIST AI RMF / OWASP LLM Top 10 mapping for each server/tool

#### v2 (3–6 months)
- **Inline enforcement point:** MCP gateway proxy (optional)
- **Anomaly detection:** unusual tool sequences, permission spikes
- **Automated red-team prompts/tests:** prompt injection resilience tests
- **Integration marketplace:** "verified providers" program

### Value Packaging Principle

**Do not sell "an MCP server."**  
Sell **"Verified MCP adoption."** MCP is the transport; trust is the product.

---

## MCP Trust Index: Content GTM Strategy {#trust-index}

### Overview

**MCP Trust Index** is a public content program that ranks MCP providers and patterns, creating inbound demand and establishing Zimax as the "trust authority" for MCP.

### Content Pillars

1. **Provider Scorecards** (repeatable template)
   - Trust Score + risk tier + enterprise fit
   - Evidence-based assessment
   - Transparent methodology
   - See [Appendix: MCP Trust Index Scorecard Template](#appendix-scorecard-template) for template structure

2. **Pattern Advisories** ("What to avoid / what to require")
   - Static API keys vs OIDC
   - Read-only vs write tools
   - Hosting posture recommendations

3. **Foundry Adoption Playbooks** (private catalog, approvals, governance)
   - How to set up private tool catalogs
   - Approval workflows
   - Governance best practices

4. **Incident Retrospectives** (public lessons; anonymized)
   - Tool misfires
   - Unauthorized actions
   - Lessons learned

5. **Reference Architectures** (NIST AI RMF-aligned MCP governance)
   - Control mapping
   - Evidence requirements
   - Compliance alignment

### Seed Backlog & Initial Provider List

**Batch 1 (10 providers — seed scorecards created):**
- Microsoft Learn Docs MCP Server (official Microsoft hosted)
- Microsoft Azure MCP Server (official Microsoft repo; auth/RBAC benchmark)
- GitHub MCP Server (official GitHub; enterprise code/PR automation)
- Splunk MCP Server (Microsoft Marketplace listing; audit/ops anchor)
- Datadog MCP Server (auth posture + logging patterns)
- PagerDuty MCP Server (enterprise incident management)
- Notion MCP (hosted + self-run patterns)
- Cloudflare MCP Server (OAuth, managed remote benchmark)
- Google Official MCP Servers (cross-cloud comparison)
- Celonis MCP Server Asset (process intelligence; graph-shaped differentiation)

**Discovery Sources (long-tail expansion):**
- `modelcontextprotocol/servers` (GitHub reference + community list)
- `habitoai/Awesome-MCP-Servers-directory` (categorized directory)
- `punkpeye/awesome-mcp-servers` (curated list with production tags)
- `mcpservers.org` (searchable catalog; monitoring new entries)

**Workflow:**
1. **Seed:** Create scorecard template with provider metadata + starter evidence list
2. **Assess:** Apply Trust Score v1 rubric, gather evidence, compute scores
3. **Publish:** Release scorecard to MCP Trust Index with Trust Score + findings
4. **Maintain:** Track drift, update scores, publish ranking updates

**Research Round Output:**
- Structured data: [CSV inventory](../mcp-trust-index-seed-backlog.csv) + [Markdown analysis](../mcp_trust_index_seed/mcp-trust-index-research-round-structured-data.md)
- **10 providers** across 10 categories (Observability, Cloud/Infrastructure, Dev/Version Control, etc.)
- **Deployment patterns:** Mix of Remote (5), Local (3), Hybrid (1), Collection/Asset (2)
- **Enterprise anchors:** Splunk (Marketplace), Microsoft (official), GitHub (official)

**Batch 1 Scoring Results (Initial Pass):**
- **Scored:** 10 providers using Trust Score v1 rubric (evidence-light, public docs only)
- **Top Performers (Tier B):**
  - Cloudflare: 73.5 (OAuth, managed remote, strong hosting)
  - GitHub: 70.0 (enterprise policy gating, push protection)
  - Datadog: 65.5 (preview, auth posture)
  - Celonis: 65.5 (enterprise asset, graph-shaped)
- **Key Insights:**
  - Managed/hosted remote endpoints score higher (better UX, faster adoption)
  - OAuth + explicit consent patterns score better than static keys
  - Enterprise governance hooks (allowlisting, policy gates, audit trails) are differentiators
  - Clear read/write tool separation + guardrails are critical
- **Market Gap:** Industry needs trust registry for continuous risk assessment (what changed since yesterday?)
- **Differentiation:** Trust Graph (Gk) + Verified MCP as security control plane
- **Scored Data:** [Batch 1 Scored Report](../mcp_trust_index_seed%202/batch1-scored-report.md) | [Scored CSV](../mcp_trust_index_seed%202/mcp-trust-index-seed-backlog.scored.csv)

### Content Cadence

- **Weekly:** Short "Trust Note" (1–2 pages)
- **Monthly:** 3–5 provider scorecards + ranking update (starting with Batch 1)
- **Quarterly:** "State of MCP Security" report

### Distribution Channels

- SecAI Radar site + wiki
- GitHub repo + issues as feedback loop
- LinkedIn long-form
- Microsoft community channels (where appropriate)
- Security / AI governance newsletters

### "Verified Provider" Program (Monetization + Flywheel)

Offer MCP providers a way to:
- Submit evidence (SOC2, SBOM, auth posture, hosting details)
- Receive a verified badge / score boost once validated
- Sponsor deeper assessments (optional, clearly labeled)

---

## Registry Data Model (Graph-First) {#registry-model}

### Entities (Nodes)

- **MCPServer:** id, name, endpoint, hostingType, provider, region, SLA, docsLink
- **Tool:** name, description, category, capability (read/write/destructive), requiredScopes
- **IdentityAuth:** authType (OIDC/OAuth/API key/mTLS), tokenTTL, rotation, JIT/JEA support
- **DataDomain:** PII, PHI, PCI, IP, logs, tickets, source code, secrets
- **Policy:** allow/deny, approvals, environment, redaction, rate limits
- **Approval:** approver, reason, date, expiry, conditions
- **EvidenceArtifact:** file/link, timestamp, source, checksum
- **RunEvent:** timestamp, actor, tool, outcome, risk flags

### Relationships (Edges)

- MCPServer **EXPOSES** Tool  
- Tool **TOUCHES** DataDomain  
- Tool **REQUIRES** IdentityAuth  
- MCPServer **HAS_SCORE** TrustScore  
- Policy **GOVERNS** Tool/MCPServer  
- Approval **APPROVES** Policy  
- RunEvent **INVOKED** Tool  
- EvidenceArtifact **SUPPORTS** TrustScore/Approval/Policy

### Graph Knowledge (Gk) Integration

This graph enables:
- **Provenance** (every claim has a source + timestamp)
- **Drift detection** (tools/permissions changed since last approval)
- **Policy-aware access** (decisioning + redaction by classification)
- **Audit packs** (exports for risk committees)

---

## Appendix: MCP Trust Score (v1) {#appendix-trust-score}

**Version:** v1.0 (public draft)  
**Date:** 2026-01-22  
**Publisher:** Zimax Networks LC (Phoenix, Arizona)  
**Programs:** SecAI Radar • MCP Trust Registry • MCP Trust Index  
**Alignment:** NIST AI RMF (GOVERN / MAP / MEASURE / MANAGE), OWASP Top 10 for LLM Apps (selected)

---

### Purpose & Non‑Goals

#### Purpose
Provide a **repeatable**, **evidence-backed** way to evaluate the enterprise security posture of:
- MCP servers (remote endpoints)
- The tools they expose
- The authentication, data handling, and operational controls surrounding them

#### Non‑Goals
- This score is **not** a certification or guarantee of safety.
- This score does **not** replace a customer's vendor risk management process.
- This score focuses on **operational risk and governance**, not feature completeness.

---

### Trust Index Ratings & Labels

#### Score Output
- **Trust Score (0–100)** — weighted total
- **Risk Tier**  
  - **A (85–100):** Enterprise-ready, strong evidence and controls  
  - **B (70–84):** Generally enterprise-usable with some gaps / compensating controls  
  - **C (50–69):** Limited enterprise fit; significant controls missing  
  - **D (0–49):** High risk / unfit for enterprise use without major changes
- **Enterprise Fit Flag**  
  - **Regulated** / **Standard Enterprise** / **Experimental**

#### Evidence Confidence
Separately report **Evidence Confidence (0–3)**:
- **0 — Unknown:** no evidence provided
- **1 — Self‑attested:** vendor statements only (docs / claims)
- **2 — Verifiable:** evidence artifacts provided (configs, logs, screenshots, SBOM, pen test letter)
- **3 — Independently validated:** third-party assurance (SOC 2 report, ISO cert, external pentest report, bug bounty, signed attestations)

> Trust Score answers "how strong are the controls?"  
> Evidence Confidence answers "how confident are we in the claims?"

---

### Evaluation Method

#### Domain Weights (v1)
| Domain | Weight | Why it matters |
|---|---:|---|
| D1. Identity & Authentication | 25 | Prevents credential misuse and supports least privilege |
| D2. Hosting & Supply Chain | 20 | Reduces compromise risk and enables secure operations |
| D3. Tool Agency & Permission Safety | 20 | Limits damage from prompt injection and tool misuse |
| D4. Data Handling & Privacy | 15 | Controls data leakage, retention, and residency |
| D5. Observability & Auditability | 15 | Enables detection, response, and compliance evidence |
| D6. Safety & Abuse Resistance | 5 | Minimizes exploitability and downstream impact |

#### Scoring Scale per Control
Each control is scored:
- **0 = missing**
- **1 = present but weak / undocumented**
- **2 = partial**
- **3 = implemented (baseline)**
- **4 = strong**
- **5 = best-in-class**

#### Computing the Trust Score
1) For each domain, compute average control score (0–5).  
2) Normalize to a 0–100 domain score: `domain_pct = (avg/5) * 100`  
3) Weighted total: `TrustScore = Σ(domain_pct * weight)` / 100

---

### Control Set (v1)

#### D1) Identity & Authentication (25)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D1.1 Modern auth | OAuth2/OIDC; no static keys required for core flows | Auth docs; supported grant types; sample config |
| D1.2 Token minimization | Short-lived tokens; scoped permissions; no broad scopes by default | Token TTL policies; scope list; least-priv templates |
| D1.3 Secret hygiene | Secrets avoided; if used, rotated + stored in HSM/KV; no hardcoding | Rotation policy; code scan results; key vault ref |
| D1.4 Strong client identity | mTLS supported/optional; client allowlists; issuer validation | TLS/mTLS config; cert chain practices |
| D1.5 Tenant isolation | Clear boundaries; per-tenant auth contexts; no cross-tenant leakage | Architecture diagram; tenancy model; test results |
| D1.6 Human break-glass | Controlled admin access; audited; JIT/JEA patterns | RBAC model; access logs; admin procedures |

**Notes:** Prefer Entra-friendly patterns where possible.

---

#### D2) Hosting & Supply Chain (20)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D2.1 Trusted hosting posture | Endpoint operated by provider; avoids opaque proxy relays | Hosting docs; domain ownership; network design |
| D2.2 Patch & vuln mgmt | Documented patch SLAs; scanning + remediation workflow | SLA; CVE workflow; scanner output summary |
| D2.3 Signed artifacts | Signed container images/binaries; provenance attestations | Signing proof (cosign, sigstore, etc.) |
| D2.4 SBOM & dependency transparency | SBOM published; dependency risk tracked | SBOM artifact; dependency inventory |
| D2.5 Secure defaults | Hardened config; least open ports; secure headers | Baseline config; security scan results |
| D2.6 Incident response readiness | IR plan, contact path, disclosure policy | IR doc; vuln disclosure; status page |

---

#### D3) Tool Agency & Permission Safety (20)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D3.1 Read-only by default | Write tools are separate and opt-in; strong scoping | Tool catalog; capability labels |
| D3.2 Destructive operations guardrails | Explicit confirmation, dry-run, and safety checks | Tool specs; "dry-run" examples |
| D3.3 Approval gates | Supports required human approval for high-risk tools/actions | Workflow docs; approval settings |
| D3.4 Scope containment | Tools constrained to resource subsets; idempotent patterns | Scope configs; examples; RBAC mapping |
| D3.5 Rate limits / abuse controls | Rate limiting; anomaly thresholds; lockouts | Rate limit config; telemetry |
| D3.6 Tool output constraints | Outputs bounded; schema validated; no arbitrary code execution | Response schema; validation layer |

---

#### D4) Data Handling & Privacy (15)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D4.1 Clear data flows | Precise description of what data is sent/received | Data flow diagram; data dictionary |
| D4.2 Minimization & redaction | Redaction supported; avoid exporting secrets/PII | Redaction rules; examples; tests |
| D4.3 Retention & deletion | Retention settings; delete workflows; customer control | Retention policy; delete API |
| D4.4 Residency options | Region selection; customer-managed storage option | Region list; storage model |
| D4.5 Encryption | TLS in transit; encryption at rest; key mgmt practices | TLS config; KMS/KV docs |
| D4.6 Privacy & compliance posture | DPA/ToS clarity; privacy policy; subprocessors list | Policy docs; DPA; subprocessors |

---

#### D5) Observability & Auditability (15)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D5.1 Audit trails | Tamper-evident logs for tool calls (who/what/when) | Sample logs; schema; export |
| D5.2 Correlation IDs | End-to-end trace IDs for requests and tool invocations | Log examples; trace docs |
| D5.3 Drift detection | Detects tool/schema/permission changes since approval | Diff reports; alerts |
| D5.4 Security monitoring hooks | SIEM integration; alerting; severity taxonomy | Integration docs; alert samples |
| D5.5 Evidence export | One-click "audit pack" (policy + approvals + logs) | Export sample; format spec |

---

#### D6) Safety & Abuse Resistance (5)

| Control | What "5" looks like | Evidence required (examples) |
|---|---|---|
| D6.1 Prompt-injection aware design | Treat untrusted input as data; avoid instruction mixing | Design notes; tests; red-team prompts |
| D6.2 Output validation | Validate tool outputs before downstream use | Validation logic; schemas |
| D6.3 Least privilege as mitigation | Tool permissions minimized to reduce blast radius | RBAC mapping; scope constraints |
| D6.4 Abuse testing | Repeatable adversarial tests; regression suite | Test harness; results |

---

### Minimum Enterprise Requirements (Fail-Fast Rules)

If any of the following are true, assign **Enterprise Fit = Experimental** (even if total score is high):

1) **Static API keys required** for core operations without rotation guidance  
2) **Write/destructive tools enabled by default** without approvals  
3) **No audit trail** for tool invocations  
4) **Opaque hosting** (unknown operators / proxy relays with unclear custody)  
5) **Unclear data handling** (no data flow, retention, or deletion story)

---

### Provider Submission: Evidence Pack (Recommended)

#### Evidence Checklist (Minimum)
- Architecture diagram (endpoint, identity flow, data flows)
- Tool catalog export (tools + read/write classification)
- Auth configuration (supported flows, scopes, TTL)
- Logging schema + example logs (with sensitive fields redacted)
- Vulnerability management statement + patch cadence
- SBOM (if available)
- IR + vulnerability disclosure policy

#### Evidence Pack Formats
- PDF (human-readable)
- JSON export (machine-readable)
- Links to public docs + signed attestations

---

### Output Formats

- **Trust Score (0–100)** — weighted total across all domains
- **Risk tier:** A (85–100) / B (70–84) / C (50–69) / D (0–49)
- **Enterprise Fit:** Regulated / Standard Enterprise / Experimental
- **Evidence Confidence:** 0 (Unknown) / 1 (Self-attested) / 2 (Verifiable) / 3 (Independently validated)
- **Flags:** static secrets, write tools without approvals, missing audit trail, unclear hosting, proxy relays

### Output Artifacts (What Customers Get)

- Trust Score + explanation ("why this score")
- Domain-level breakdown (D1–D6 scores)
- Control-level details (which controls passed/failed)
- Allowed environments and scopes
- Approval history and reviewers
- Drift report (changes since last approval)
- Audit Pack export (JSON + summary PDF)

---

### Compliance Mapping

#### NIST AI RMF (GOVERN / MAP / MEASURE / MANAGE)
- **GOVERN:** ownership, policies, approvals, accountability, audit evidence
- **MAP:** inventory of tools/servers; data domains; trust graph relationships
- **MEASURE:** Trust Score, Evidence Confidence, tests, validation results
- **MANAGE:** enforcement, drift alerts, remediation plans, incident response

#### OWASP Top 10 for LLM Applications (Selected)
- **LLM01 Prompt Injection:** treat inputs as data; tool permissions; approvals (D3, D6)
- **LLM02 Insecure Output Handling:** validate outputs; restrict execution paths (D3.6, D6.2)
- **Tool misuse patterns:** guardrails, allowlists, response constraints (D3.1–D3.6)

---

### Publishing Rules for the MCP Trust Index (Risk + Fairness)

- Always show **Last assessed date** and **Evidence Confidence**
- Vendors can submit evidence for re-score ("right to respond")
- Label entries clearly: **Unverified** vs **Verified**
- Do not imply certification; keep "risk posture assessment" language
- Keep a public changelog for scoring rubric updates

---

### Scorecard Template Reference

See companion scorecard template for consistent publishing format.

---

## Appendix: MCP Trust Index Scorecard Template {#appendix-scorecard-template}

**Version:** v1.0  
**Date:** 2026-01-22  
**Publisher:** Zimax Networks LC (Phoenix, Arizona)  
**Program:** MCP Trust Index (Public Content Program)

---

### Template Structure

Use this template for all MCP provider scorecards published in the MCP Trust Index.

---

**Provider:** <Name>  
**Server / Product:** <Name>  
**Endpoint(s):** <URL / domains>  
**Last assessed:** <YYYY-MM-DD>  
**Evidence confidence:** <0–3> (Unknown / Self-attested / Verifiable / Independently validated)  
**Trust Score:** <0–100> (**Tier:** A/B/C/D)  
**Enterprise fit:** Regulated / Standard / Experimental

---

### 1) Summary (1–2 paragraphs)
- What this MCP server does
- Where it fits (Foundry, developer tooling, observability, etc.)
- High-level risk posture and standout strengths/concerns

---

### 2) Quick Flags
- Static API keys required: Yes/No  
- Write tools enabled by default: Yes/No  
- Approval gates supported: Yes/No  
- Audit trail for tool calls: Yes/No  
- Clear data retention/deletion: Yes/No  
- Opaque proxy relay: Yes/No  

---

### 3) Domain Scores (v1)

| Domain | Weight | Score (0–5) | Domain % | Notes |
|---|---:|---:|---:|---|
| D1 Identity & Authentication | 25 |  |  |  |
| D2 Hosting & Supply Chain | 20 |  |  |  |
| D3 Tool Agency & Permission Safety | 20 |  |  |  |
| D4 Data Handling & Privacy | 15 |  |  |  |
| D5 Observability & Auditability | 15 |  |  |  |
| D6 Safety & Abuse Resistance | 5 |  |  |  |

**Computed Trust Score:** <Σ weighted>

---

### 4) Evidence List (with confidence)
| Evidence artifact | Type | Date | Confidence | Notes |
|---|---|---|---:|---|
|  | Docs / Config / Logs / Report |  |  |  |

---

### 5) Findings (what to fix next)
#### Strengths
- <bullet>
#### Gaps / risks
- <bullet>
#### Recommended remediation
- <bullet>

---

### 6) NIST AI RMF mapping (high-level)
- GOVERN: <notes>  
- MAP: <notes>  
- MEASURE: <notes>  
- MANAGE: <notes>  

---

### 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.

---

## References

- [GTM MVP Readiness](./foundry-iq-gtm-mvp-readiness.md)
- [Implementation Status](./foundry-iq-implementation-status.md)
- [API Research](./foundry-iq-api-research.md)
- [Ecosystem Exploration](./foundry-iq-ecosystem-exploration.md)
- [Foundry IQ + ctxEco Integration Master](../architecture/08-foundry-iq-ctxeco-integration-master.md)
- [Graph Knowledge (Gk) + Tri-Search™](../knowledge/01-graph-knowledge-tri-search.md)
- OSS Foundation: `derekbmoore/openContextGraph` (MIT)
- SecAI Framework: security assessment methodology (public)
- SecAI Radar: application wiki (public)
- [SecAI Radar MCP Trust Registry GTM Plan](./ctxeco-verified-mcp-marketplace-gtm-master.md) (internal reference)
- [SecAI Radar MCP Trust Registry GTM Plan #2](../secai-radar-mcp-trust-registry-gtm-plan-2.md) (content GTM strategy)
- [MCP Trust Score Rubric v1](../secai-radar-mcp-trust-score-rubric-v1.md) (detailed scoring methodology)
- [MCP Trust Index Scorecard Template](../mcp-trust-index-scorecard-template.md) (scorecard publishing template)
- [MCP Trust Index Seed Content](../mcp_trust_index_seed/) (production examples: backlog + 10 seed scorecards)
- [MCP Trust Index Research Round Structured Data](../mcp_trust_index_seed/mcp-trust-index-research-round-structured-data.md) (CSV inventory + analysis)
- [MCP Trust Index Batch 1 Scored](../mcp_trust_index_seed%202/) (scored report + 10 scored scorecards with Trust Scores)
