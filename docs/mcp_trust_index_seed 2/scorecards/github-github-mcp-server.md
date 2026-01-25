# MCP Provider Scorecard
**Provider:** GitHub  
**Server / Product:** GitHub MCP Server  
**Endpoint(s):** (remote hosted by GitHub), (local option)  
**Last assessed:** 2026-01-22  
**Evidence confidence:** 1 (Self-attested)  
**Trust Score:** 70.0 (**Tier:** B)  
**Enterprise fit:** Standard/Regulated

---

## 1) Summary
GitHub-maintained MCP server that lets Copilot/agents perform GitHub actions (issues/PRs/repo info). Supports remote hosted and local deployments; enterprise policy gating exists for Copilot orgs; includes interactions with GitHub security features like push protection.

## 2) Quick Flags (Unverified)
- **Auth:** GitHub account auth; org/enterprise policies can gate MCP use.
- **Safety:** Push protection/secret scanning can block secrets during agent-driven workflows.
- **Tool agency:** Includes write actions (issues/branches/merges). Permission scoping + confirmations are critical.

## 3) Domain Scores (v1)
| Domain | Weight | Score (0–5) | Notes |
|---|---:|---:|---|
| D1 — Identity & Authentication | 25 | 4.0 | TBD |
| D2 — Hosting & Supply Chain | 20 | 3.5 | TBD |
| D3 — Tool Agency & Permission Safety | 20 | 3.5 | TBD |
| D4 — Data Handling & Privacy | 15 | 3.0 | TBD |
| D5 — Observability & Auditability | 15 | 3.0 | TBD |
| D6 — Safety & Abuse Resistance | 5 | 4.0 | TBD |

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
- https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/set-up-the-github-mcp-server
- https://docs.github.com/en/copilot/how-tos/provide-context/use-mcp/use-the-github-mcp-server
- https://github.com/github/github-mcp-server

## 7) Disclosure / Disclaimer
This scorecard reflects observed evidence at the time of assessment and is not a certification or guarantee of security.