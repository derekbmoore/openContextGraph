# MCP Trust Index — Seed Batch 1 (Scored)
**Run date:** 2026-01-22

This report contains an initial, evidence-light scoring pass over 10 widely referenced MCP providers/servers. Scores reflect **public docs and repos only**; treat them as a starting point for deeper verification.

## 1) Ranking (initial)
| Rank | Provider | Server | Trust Score | Tier | Evidence confidence | Enterprise fit |
|---:|---|---|---:|:---:|:---:|---|
| 1 | Cloudflare | Cloudflare MCP Server(s) | 73.5 | B | 1 | Standard/Regulated |
| 2 | GitHub | GitHub MCP Server | 70.0 | B | 1 | Standard/Regulated |
| 3 | Datadog | Datadog MCP Server | 65.5 | B | 1 | Standard (Preview) |
| 4 | Celonis | Celonis MCP Server Asset (Process Intelligence) | 65.5 | B | 1 | Standard/Regulated |
| 5 | Splunk | Splunk MCP Server | 64.5 | C | 1 | Standard/Regulated |
| 6 | Microsoft | Azure MCP Server | 59.0 | C | 1 | Standard/Regulated (local) |
| 7 | PagerDuty | PagerDuty MCP Server | 59.0 | C | 1 | Standard |
| 8 | Notion | Notion MCP (hosted) / Notion MCP Server | 56.5 | C | 1 | Standard |
| 9 | Google | Google Official MCP Servers | 56.5 | C | 1 | Experimental→Standard (varies) |
| 10 | Microsoft | Microsoft Learn Docs MCP Server | 54.0 | C | 1 | Standard |

## 2) What the best-positioned offerings have in common
- **Managed/hosted “remote” endpoints** with clear onboarding and stable URLs (better UX and faster adoption).
- **OAuth or strong identity passthrough** + explicit consent (avoids static keys and supports least privilege).
- **Enterprise governance hooks:** allowlisting, policy gates, and audit trails (or at least a path to get them).
- **Clear separation of read vs write tools** + guardrails for destructive actions.

## 3) Where the marketplace gap is (your opening)
- Vendor docs increasingly admit that **third‑party MCP servers aren’t verified** and customers must manage risk themselves.
- The industry needs a **trust registry** that continuously answers: *What is this tool allowed to do? What data can it touch? What changed since yesterday?*

## 4) Differentiation play: “Trust Graph (GK) + Verified MCP”
Your strongest differentiator isn’t another MCP server — it’s a **security control plane**:
- Build a **Graph Knowledge (GK) model** that links: `Provider → Server → Tools → Permissions/Scopes → Data classes → Deployment model → Assurance artifacts → Known risks/CVEs → Customer controls`.
- Use the graph to power: **impact analysis**, **drift detection**, **least-privilege recommendations**, and **comparative rankings**.
- Package it as: **SecAI Radar Verified MCP** (verification workflow) + **ctxeco MCP Gateway** (API / proxy / APIM templates) + **Trust Index** (public scoring + content).

## 5) Daily automation concept (agent-driven)
Minimum daily jobs (automatable):
1. **Change detection:** monitor docs/repos/marketplace listings; diff tool schemas + endpoints.
2. **Health checks:** endpoint availability, TLS/certs, auth flows, rate limits.
3. **Security signals:** CVEs, advisories, repo security alerts, breaking changes.
4. **Re-score + publish:** update Trust Scores, generate a daily “Top movers” post, and refresh leaderboards.
5. **Evidence requests:** auto-generate vendor questionnaires and evidence-pack checklists to raise confidence to 2/3.

## 6) Next actions
- Promote **OAuth identity passthrough + APIM governance** as the enterprise-safe integration path.
- Add a **Verified MCP Badge** program (Tiered): Bronze (docs), Silver (verifiable evidence), Gold (independent assurance).
- Prioritize scoring additions for: credential handling, audit log accessibility, signed artifacts/SBOM, and tool-level permission scoping.