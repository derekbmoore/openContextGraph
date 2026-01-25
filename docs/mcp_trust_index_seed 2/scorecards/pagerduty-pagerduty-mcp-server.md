# MCP Provider Scorecard
**Provider:** PagerDuty  
**Server / Product:** PagerDuty MCP Server  
**Endpoint(s):** (open-source server; runs where you host it)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 59.0 (**Tier:** C)  
**Enterprise fit:** Standard

---

## 1) Summary
PagerDuty’s MCP server integration enabling agents to interact with PagerDuty incident management via API token–based access (hosting depends on how you deploy).

## 2) Quick Flags (Unverified)
- **Auth:** API-token based (confirm scopes + rotation).
- **Tool agency:** Potentially includes acknowledgement/trigger actions; require confirmations and least privilege.
- **Hosting:** If self-hosted, your org must handle patching, logging, and supply-chain controls.

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 3.5 | TBD |
| D2 — Hosting & Supply Chain | 20 | 2.5 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 3.0 | TBD |
| D4 — Data Handling & Privacy | 15 | 2.5 | TBD |
| D5 — Observability & Auditability | 15 | 3.0 | TBD |
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
- https://github.com/PagerDuty/pagerduty-mcp-server

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.