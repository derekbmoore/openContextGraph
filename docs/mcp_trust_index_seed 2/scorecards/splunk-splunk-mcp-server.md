# MCP Provider Scorecard
**Provider:** Splunk  
**Server / Product:** Splunk MCP Server  
**Endpoint(s):** (managed service; marketplace deploys into Splunk Cloud envs)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 64.5 (**Tier:** C)  
**Enterprise fit:** Standard/Regulated

---

## 1) Summary
Splunk’s fully-managed MCP server bridging AI agents to Splunk Enterprise and Splunk Cloud Platform data and operations. Available via Microsoft Azure Marketplace and other marketplaces; positioned as secure, scalable connectivity to Splunk data.

## 2) Quick Flags (Unverified)
- **Auth:** Likely leverages Splunk platform auth/RBAC; specifics not fully detailed publicly.
- **Data risk:** Splunk often contains highly sensitive telemetry/security data; governance and logging are essential.
- **Enterprise strength:** Managed service + deep observability/audit controls available in Splunk ecosystem (verify MCP-specific logging).

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 3.5 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.5 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 3.0 | TBD |
| D4 — Data Handling & Privacy | 15 | 2.5 | TBD |
| D5 — Observability & Auditability | 15 | 3.5 | TBD |
| D6 — Safety & Abuse Resistance | 5 | 3.0 | TBD |

## 4) Evidence Needed to Raise Confidence (1 → 2/3)
- Provide an **evidence pack**: auth config + tool catalog + sample logs + security/IR contacts.
- Publish **SBOM + signed artifacts** (container/image signatures) where applicable.
- Provide **audit evidence**: what is logged, where it’s stored, retention, and how customers access it.
- Provide **pen test / SOC2 / ISO / bug bounty** artifacts where available.

## 5) NIST AI RMF mapping (high-level)
- **GOVERN:** ownership, approval workflow, third-party risk treatment, tool allowlisting
- **MAP:** tool + data-flow inventory; classify data handled by tools
- **MEASURE:** Trust Score + continuous checks; vulnerability + drift monitoring
- **MANAGE:** remediation SLAs; revocation/rotation; incident response + user comms

## 6) Sources (public)
- https://marketplace.microsoft.com/en-us/product/saas/splunk.splunk_mcp_server?tab=overview
- https://help.splunk.com/en/splunk-cloud-platform/mcp-server-for-splunk-platform/about-the-mcp-server-for-splunk-platform
- https://classic.splunkbase.splunk.com/app/7931/

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.