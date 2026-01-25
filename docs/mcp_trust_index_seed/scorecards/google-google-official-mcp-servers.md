# MCP Provider Scorecard
**Provider:** Google  
**Server / Product:** Google Official MCP Servers  
**Endpoint(s):** Varies by server; see repo list  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested) → 2 (Verifiable) pending evidence pack  
**Trust Score:** TBD (**Tier:** TBD)  
**Enterprise fit:** TBD (likely Standard/Regulated depending on controls)

---

## 1) Summary
Official Google collection; good for cross-cloud comparisons.

## 2) Quick Flags (Unverified)
- Static API keys required: Unknown  
- Write tools enabled by default: Unknown  
- Approval gates supported: Unknown  
- Audit trail for tool calls: Unknown  
- Clear data retention/deletion: Unknown  
- Opaque proxy relay: Unknown  

---

## 3) Domain Scores (v1) — placeholders

| Domain | Weight | Score (0–5) | Domain % | Notes |
|---|---:|---:|---:|---|
| D1 Identity & Authentication | 25 |  |  |  |
| D2 Hosting & Supply Chain | 20 |  |  |  |
| D3 Tool Agency & Permission Safety | 20 |  |  |  |
| D4 Data Handling & Privacy | 15 |  |  |  |
| D5 Observability & Auditability | 15 |  |  |  |
| D6 Safety & Abuse Resistance | 5 |  |  |  |

**Computed Trust Score:** TBD

---

## 4) Evidence List (starter)
| Evidence artifact | Type | Date | Confidence | Notes |
|---|---|---|---:|---|
| https://github.com/google/mcp | Docs | 2026-01-22 | 1 | Primary documentation / listing |
| https://github.com/google/mcp | Repo / Source | 2026-01-22 | 1 | If OSS; otherwise N/A |

---

## 5) Findings (draft)
### Strengths (hypotheses)
- TBD based on auth, hosting, and audit evidence.

### Gaps / risks (hypotheses)
- TBD based on token model, write-tool separation, logging, and data handling disclosures.

### Recommended remediation / requirements (for enterprise buyers)
- Provide an Evidence Pack (SBOM, auth scopes/TTL, audit logging schema, data handling/retention, IR policy).
- Demonstrate approval gating and least-privilege tool scoping.

---

## 6) NIST AI RMF mapping (high-level)
- GOVERN: Registry, ownership, approvals (TBD)  
- MAP: tool + data-flow inventory (TBD)  
- MEASURE: Trust Score + test evidence (TBD)  
- MANAGE: drift detection + remediation (TBD)  

---

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.
