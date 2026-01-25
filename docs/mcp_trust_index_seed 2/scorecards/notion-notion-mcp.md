# MCP Provider Scorecard
**Provider:** Notion  
**Server / Product:** Notion MCP (hosted) / Notion MCP Server  
**Endpoint(s):** (Notion-hosted remote MCP server), (self-hosted option)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 56.5 (**Tier:** C)  
**Enterprise fit:** Standard

---

## 1) Summary
Notion’s MCP integration supports connecting an MCP client to a Notion workspace via OAuth. Notion warns that the integration may have full access to the workspace and requires careful review of what tools can do.

## 2) Quick Flags (Unverified)
- **Auth:** OAuth with user consent; scope and workspace permissions must be reviewed.
- **Tool agency:** High-risk by default (workspace write operations). Push for read-only modes and scoped workspaces.
- **Data risk:** Contains sensitive knowledge-base content; ensure retention and audit expectations are met.

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 4.0 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.0 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 2.5 | TBD |
| D4 — Data Handling & Privacy | 15 | 2.0 | TBD |
| D5 — Observability & Auditability | 15 | 2.0 | TBD |
| D6 — Safety & Abuse Resistance | 5 | 2.5 | TBD |

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
- https://developers.notion.com/docs/get-started-with-mcp

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.