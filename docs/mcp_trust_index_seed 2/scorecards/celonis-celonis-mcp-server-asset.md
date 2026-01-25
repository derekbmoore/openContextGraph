# MCP Provider Scorecard
**Provider:** Celonis  
**Server / Product:** Celonis MCP Server Asset (Process Intelligence)  
**Endpoint(s):** (Celonis platform MCP server asset)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 65.5 (**Tier:** B)  
**Enterprise fit:** Standard/Regulated

---

## 1) Summary
Celonis’ Process Intelligence MCP Server asset provides AI agents with operational/process context (a graph-shaped enterprise data lens) and can potentially trigger actions via their platform APIs; auth options include OAuth.

## 2) Quick Flags (Unverified)
- **Auth:** OAuth-based auth options described for Celonis APIs.
- **Graph-like context:** Direct comparator to your GK pitch: process graphs as operational grounding.
- **Enterprise scale:** Celonis positions itself as used by a large number of enterprises (verify).

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 4.0 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.5 | TBD |
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
- https://developer.celonis.com/process-intelligence-apis/agents-api/
- https://developer.celonis.com/process-intelligence-apis/agents-api/get-started/getting-started/

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.