# MCP Provider Scorecard
**Provider:** Google  
**Server / Product:** Google Official MCP Servers  
**Endpoint(s):** (Google-managed remote endpoints), (open-source servers you deploy)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 56.5 (**Tier:** C)  
**Enterprise fit:** Experimental→Standard (varies)

---

## 1) Summary
Google’s official MCP collection lists both Google-managed remote MCP servers (e.g., Maps Grounding Lite, BigQuery) and a large set of open-source MCP servers you can run locally or deploy on Google Cloud.

## 2) Quick Flags (Unverified)
- **Adoption signal:** Repository popularity indicates ecosystem traction (stars/forks).
- **Variance:** Security posture varies widely across servers; treat as a portfolio rather than one product.
- **Disclaimer:** Some items are demo/not-officially-supported, which impacts regulated enterprise suitability.

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 3.0 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.5 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 2.5 | TBD |
| D4 — Data Handling & Privacy | 15 | 2.5 | TBD |
| D5 — Observability & Auditability | 15 | 2.5 | TBD |
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
- https://github.com/google/mcp

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.