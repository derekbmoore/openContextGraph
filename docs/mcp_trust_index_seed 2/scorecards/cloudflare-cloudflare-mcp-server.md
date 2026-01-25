# MCP Provider Scorecard
**Provider:** Cloudflare  
**Server / Product:** Cloudflare MCP Server(s)  
**Endpoint(s):** (Cloudflare managed remote servers), (your own remote server behind Cloudflare)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 73.5 (**Tier:** B)  
**Enterprise fit:** Standard/Regulated

---

## 1) Summary
Cloudflare provides both managed MCP servers and guidance for building remote MCP servers. Their ecosystem emphasizes OAuth, access control, and managed connectivity for agent workloads.

## 2) Quick Flags (Unverified)
- **Auth:** Strong OAuth + platform access controls; can pair with Cloudflare Access/Zero Trust patterns.
- **Hosting:** Mature edge platform; good benchmark for managed remote model.
- **Tool agency:** Depending on server, may control infrastructure (DNS/WAF/workers) → require guardrails.

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 4.5 | TBD |
| D2 — Hosting & Supply Chain | 20 | 4.0 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 3.0 | TBD |
| D4 — Data Handling & Privacy | 15 | 3.0 | TBD |
| D5 — Observability & Auditability | 15 | 3.5 | TBD |
| D6 — Safety & Abuse Resistance | 5 | 3.5 | TBD |

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
- https://developers.cloudflare.com/agents/guides/remote-mcp-server/
- https://developers.cloudflare.com/agents/guides/managed-mcp-servers/

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.