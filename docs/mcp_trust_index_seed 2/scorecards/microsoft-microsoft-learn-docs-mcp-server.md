# MCP Provider Scorecard
**Provider:** Microsoft  
**Server / Product:** Microsoft Learn Docs MCP Server  
**Endpoint(s):** https://learn.microsoft.com/api/mcp  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 54.0 (**Tier:** C)  
**Enterprise fit:** Standard

---

## 1) Summary
Official Microsoft-hosted remote MCP endpoint for Microsoft Learn documentation search and retrieval. It is designed for programmatic Streamable HTTP access by MCP clients.

## 2) Quick Flags (Unverified)
- **Auth:** No authentication required (public endpoint).
- **Tool agency:** Read-only tools (search + fetch docs), lower blast radius.
- **Data risk:** Primarily public documentation; low sensitivity by default.
- **Governance gap:** Customer-side allowlisting/logging still required in Foundry (third‑party MCP servers not verified).

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 1.0 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.0 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 4.0 | TBD |
| D4 — Data Handling & Privacy | 15 | 4.0 | TBD |
| D5 — Observability & Auditability | 15 | 2.0 | TBD |
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
- https://learn.microsoft.com/en-us/training/support/mcp
- https://learn.microsoft.com/en-us/training/support/mcp/get-started

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.