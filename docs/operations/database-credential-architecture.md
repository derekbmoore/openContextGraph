---
title: "Database Credential Architecture Reference"
summary: "Complete reference for the unified database credential architecture across ctxEco, Zep, and secai-radar systems"
date: 2026-01-30
status: active
category: operations
tags:
  - database
  - credentials
  - azure
  - postgresql
  - architecture
  - reference
---

# Database Credential Architecture Reference

This document provides the definitive reference for database credential management across the integrated workspace.

---

## Architecture Overview

### Shared PostgreSQL Server

All systems share a single Azure Database for PostgreSQL Flexible Server:

```
Server: ctxeco-db.postgres.database.azure.com
Port: 5432
SSL: Required (sslmode=require)
Admin User: ctxecoadmin
```

### Database Topology

| Database | System | Purpose |
|----------|--------|---------|
| `zep` | ctxEco | Zep memory service - vector store, sessions, facts |
| `ctxEco` | ctxEco | Backend application data, workflows |
| `temporal` | ctxEco | Temporal orchestration engine state |
| `temporal_visibility` | ctxEco | Temporal search and visibility |
| `secairadar` | secai-radar | MCP trust scores, drift events, daily briefs |

---

## Credential Flow

```
┌────────────────────────────────────────────────────────────────┐
│                 AZURE KEY VAULT (ctxecokv)                     │
│                    SOURCE OF TRUTH                              │
│                                                                 │
│  Secrets:                                                      │
│  • postgres-password     → Raw password for ctxecoadmin        │
│  • database-url          → Full connection string              │
│  • zep-config-yaml       → Zep configuration with embedded DSN │
└──────────────────────────────┬─────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ CONTAINER APPS      │ │ GITHUB SECRETS  │ │ LOCAL .env      │
│ (Runtime)           │ │ (CI/CD)         │ │ (Development)   │
│                     │ │                 │ │                 │
│ Managed Identity    │ │ DATABASE_URL    │ │ DATABASE_URL    │
│ reads from KV       │ │ (sync from KV)  │ │ (manual sync)   │
└─────────────────────┘ └─────────────────┘ └─────────────────┘
```

---

## Connection String Format

```
postgresql://ctxecoadmin:{PASSWORD}@ctxeco-db.postgres.database.azure.com:5432/{DATABASE}?sslmode=require
```

### Per-Database Examples

| Database | Connection String |
|----------|-------------------|
| zep | `postgresql://ctxecoadmin:***@ctxeco-db...5432/zep?sslmode=require` |
| ctxEco | `postgresql://ctxecoadmin:***@ctxeco-db...5432/ctxEco?sslmode=require` |
| secairadar | `postgresql://ctxecoadmin:***@ctxeco-db...5432/secairadar?sslmode=require` |

---

## Service Credential Sources

| Service | Location | Credential Source | Secret Name |
|---------|----------|-------------------|-------------|
| Zep Memory | Container App | Key Vault | `zep-config-yaml` (DSN embedded) |
| ctxEco Backend | Container App | Key Vault | `database-url` |
| Daily Pipeline | GitHub Actions | GitHub Secrets | `DATABASE_URL` |
| Local Dev | .env file | Manual | `DATABASE_URL` |

---

## Password Rotation Protocol

When rotating the database password:

### Step 1: Update Key Vault (Source of Truth)
```bash
az keyvault secret set \
  --vault-name ctxecokv \
  --name postgres-password \
  --value "NEW_PASSWORD"

az keyvault secret set \
  --vault-name ctxecokv \
  --name database-url \
  --value "postgresql://ctxecoadmin:NEW_PASSWORD@ctxeco-db.postgres.database.azure.com:5432/secairadar?sslmode=require"
```

### Step 2: Update GitHub Secrets
```bash
# Get new password from Key Vault
NEW_PASSWORD=$(az keyvault secret show --vault-name ctxecokv --name postgres-password --query value -o tsv)

# Update GitHub secret (via GitHub CLI or UI)
gh secret set DATABASE_URL --body "postgresql://ctxecoadmin:${NEW_PASSWORD}@ctxeco-db.postgres.database.azure.com:5432/secairadar?sslmode=require"
```

### Step 3: Update Local .env Files
Update `.env` in:
- `/ctxEco/.env`
- `/ctxEco/backend/.env`
- `/secai-radar/.env` (if applicable)

### Step 4: Restart Container Apps
```bash
az containerapp revision restart --name zep --resource-group ctxEco-rg
az containerapp revision restart --name ctxeco-backend --resource-group ctxEco-rg
```

---

## Verification Commands

### Test Connection Locally
```bash
psql "postgresql://ctxecoadmin:PASSWORD@ctxeco-db.postgres.database.azure.com:5432/zep?sslmode=require" -c "SELECT 1"
```

### Check Container App Health
```bash
# Zep health
curl https://zep.{region}.azurecontainerapps.io/api/v1/health

# Check container status
az containerapp show --name zep --resource-group ctxEco-rg --query "properties.runningStatus"
```

### Verify Key Vault Secrets
```bash
az keyvault secret show --vault-name ctxecokv --name postgres-password --query value -o tsv
```

---

## Troubleshooting

### Error: `password authentication failed for user "ctxecoadmin"`

**Cause**: Credential mismatch between source and consumer

**Resolution**:
1. Get correct password from Key Vault
2. Update the failing service's credential source
3. Restart/redeploy the service

### Error: `FATAL: database "xxx" does not exist`

**Cause**: Wrong database name in connection string

**Resolution**: Verify database name matches one of the five databases listed above

### Error: `SSL connection is required`

**Cause**: Missing `?sslmode=require` in connection string

**Resolution**: Append `?sslmode=require` to connection string

---

## Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| Database Credentials Guide | [DATABASE-CREDENTIALS-GUIDE.md](../../../DATABASE-CREDENTIALS-GUIDE.md) | Navigation hub |
| Operations Runbook | [DATABASE-OPERATIONS-RUNBOOK.md](../../../DATABASE-OPERATIONS-RUNBOOK.md) | Step-by-step procedures |
| Authentication Inventory | [DATABASE-AUTHENTICATION-INVENTORY.md](../../../DATABASE-AUTHENTICATION-INVENTORY.md) | Service status |
| Working Memory | [database-access-journey-2026-01-30.md](../working-memory/database-access-journey-2026-01-30.md) | Journey record |

---

## Memory Classification

- **Type**: Knowledge Document
- **Classification**: Class A (Operational Reference)
- **Retention**: Permanent (update as architecture changes)
- **Owner**: Platform Team
