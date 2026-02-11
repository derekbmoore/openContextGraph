---
title: "Database Access Journey: Unified Credential Architecture"
summary: "Memory of the multi-day process to establish, debug, and unify database access across ctxEco, Zep, and secai-radar systems on shared Azure PostgreSQL"
date: 2026-01-30
status: complete
classification: Class A (Immutable Truth)
ingest_to_zep: true
session_id: working-memory
tags:
  - database
  - credentials
  - azure
  - postgresql
  - zep
  - ctxeco
  - secai-radar
  - architecture
  - journey
author: Derek Moore
provenance:
  source: multi-day debugging and architecture effort
  verified_by: system
  date_range: 2026-01-23 to 2026-01-30
---

# Database Access Journey: Unified Credential Architecture

**Date Completed:** January 30, 2026  
**Duration:** Multi-day effort (January 23-30, 2026)  
**Status:** ✅ Complete

---

## Executive Summary

This memory documents the journey to establish unified database access across the integrated workspace. The effort involved:

1. **Diagnosing credential fragmentation** — Multiple services using different credential sources with inconsistent passwords
2. **Mapping the architecture** — Understanding how ctxEco, Zep, and secai-radar share a single Azure PostgreSQL server
3. **Creating comprehensive documentation** — Building runbooks, guides, and inventories for future reference
4. **Establishing single source of truth** — Azure Key Vault as authoritative credential store

---

## The Challenge

### Initial State
When we began, the workspace had:
- **Three systems** (ctxEco, secai-radar, Zep) needing database access
- **Multiple credential locations** with inconsistent values:
  - `.env` files (local development)
  - GitHub Secrets (CI/CD pipelines)
  - Azure Key Vault (container runtime)
- **Cascading authentication failures** — Some services worked, others failed with `password authentication failed`
- **No unified documentation** — Each system had partial, conflicting information

### Root Cause Analysis
The failures stemmed from:
1. Password rotation that didn't propagate to all credential stores
2. GitHub Secrets containing stale DATABASE_URL values
3. Different services reading from different sources without fallback
4. No single document showing the complete credential flow

---

## The Solution

### Shared PostgreSQL Architecture
```
ctxeco-db.postgres.database.azure.com
├─ Database: zep          → Zep memory service
├─ Database: ctxEco       → ctxEco backend/worker
├─ Database: temporal     → Temporal orchestration
├─ Database: temporal_visibility → Temporal state
└─ Database: secairadar   → secai-radar apps & pipelines

Single admin user: ctxecoadmin
```

### Three-Location Credential Strategy
```
┌─────────────────────────────────────────────────────────┐
│                    CREDENTIAL FLOW                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Azure Key Vault (ctxecokv)                            │
│  ═══════════════════════════                           │
│  SOURCE OF TRUTH                                        │
│  • postgres-password secret                            │
│  • database-url secret                                 │
│                                                         │
│           │                                             │
│           ▼                                             │
│  ┌────────────────────┐    ┌────────────────────┐     │
│  │ Container Apps     │    │ GitHub Secrets     │     │
│  │ (Runtime)          │    │ (CI/CD Deploy)     │     │
│  │                    │    │                    │     │
│  │ • Zep reads KV     │    │ • DATABASE_URL     │     │
│  │ • ctxEco reads KV  │    │ • Sync from KV     │     │
│  └────────────────────┘    └────────────────────┘     │
│                                                         │
│           │                        │                    │
│           ▼                        ▼                    │
│  ┌────────────────────────────────────────────────┐   │
│  │         .env (Local Development)                │   │
│  │         Mirror values for local testing         │   │
│  └────────────────────────────────────────────────┘   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Documentation Created

| Document | Purpose |
|----------|---------|
| [DATABASE-CREDENTIALS-GUIDE.md](../../../DATABASE-CREDENTIALS-GUIDE.md) | Navigation hub — "Start Here" |
| [DATABASE-MANAGEMENT-UNIFIED.md](../../../DATABASE-MANAGEMENT-UNIFIED.md) | Complete strategy & architecture |
| [DATABASE-OPERATIONS-RUNBOOK.md](../../../DATABASE-OPERATIONS-RUNBOOK.md) | Step-by-step fix procedures |
| [DATABASE-AUTHENTICATION-INVENTORY.md](../../../DATABASE-AUTHENTICATION-INVENTORY.md) | Service status tracking |
| [DB-CREDENTIALS-FIX.md](../../../DB-CREDENTIALS-FIX.md) | Quick credential update scripts |
| [INTEGRATED-WORKSPACE-DATABASE.md](../../../INTEGRATED-WORKSPACE-DATABASE.md) | Technical architecture deep-dive |

---

## Service Status After Fix

### ✅ Working Services
| Service | Location | Credential Source | Status |
|---------|----------|-------------------|--------|
| Zep Memory | Azure Container Apps | Key Vault → `postgres-password` | Healthy |
| ctxEco Backend | Azure Container Apps | Key Vault → `database-url` | Operational |
| Local Development | .env files | Manual sync from KV | Working |

### ⚠️ Services Needing Attention
| Service | Issue | Fix |
|---------|-------|-----|
| GitHub Actions Daily Pipeline | Stale DATABASE_URL in secrets | Update GitHub secret from KV value |

---

## Key Learnings

### 1. Single Source of Truth
Azure Key Vault must be the authoritative source. All other locations (GitHub Secrets, .env) are mirrors that sync from it.

### 2. Password Rotation Protocol
When rotating passwords:
1. Update Azure Key Vault first
2. Pull new value and update GitHub Secrets
3. Update local .env files
4. Restart affected container apps

### 3. Connection String Format
```
postgresql://ctxecoadmin:PASSWORD@ctxeco-db.postgres.database.azure.com:5432/DATABASE?sslmode=require
```

### 4. Verification Commands
```bash
# Test from local machine
psql "postgresql://ctxecoadmin:PASSWORD@ctxeco-db.postgres.database.azure.com:5432/zep?sslmode=require"

# Check container app health
az containerapp show --name zep --resource-group ctxEco-rg --query "properties.runningStatus"
```

---

## Artifacts Created

### Scripts
- `scripts/sync_credentials.sh` — Synchronize credentials across all locations
- `scripts/test_db_connection.py` — Verify database connectivity

### Architecture Diagrams
- Database topology diagram
- Credential flow diagram
- Service dependency map

---

## Next Steps for Future Reference

1. **Automate credential sync** — GitHub Action to pull from Key Vault on rotation
2. **Add monitoring** — Alert on authentication failures
3. **Document runbook in Sage** — Have Sage create a story about this journey

---

## Memory Classification

- **Type:** Working Memory → Episodic
- **Classification:** Class A (Immutable Truth)
- **Retention:** Permanent
- **Searchable Tags:** database, credentials, authentication, azure, postgresql, zep, architecture, troubleshooting

---

*This memory was created to preserve the knowledge gained during the database access unification effort. It serves as both a historical record and a reference for future credential management tasks.*
