---
layout: default
title: Configuration Source of Truth (Key Vault)
parent: Foundry (Azure AI Foundry)
nav_order: 6
description: "How ctxEco manages Foundry and platform configuration across Key Vault, GitHub, and runtime."
---

# Configuration Source of Truth (Key Vault)

> **Principle**: Azure Key Vault is the single source of truth for production secrets.  
> **Goal**: enable repeatable customer provisioning for the GTM MVP.

This document consolidates the strategy for how ctxEco configuration flows across:

- **Azure Key Vault** (production)
- **GitHub Secrets** (CI/CD)
- **Container App environment variables** (runtime)
- **Local `.env`** (development only)

## Configuration hierarchy

### 1) Azure Key Vault (production source of truth)

- Store all sensitive values in Key Vault
- Access via Managed Identity (RBAC: *Key Vault Secrets User*)
- Container Apps reference secrets (no plaintext secrets committed)

### 2) GitHub Secrets (deployment-time only)

Used to populate infrastructure during deployment:

```text
GitHub Secrets → Bicep parameters → Key Vault → Container Apps
```

### 3) Runtime environment variables

In production, env vars are **set from Key Vault references** by infra.

### 4) Local `.env` (dev only)

Never committed; used only for local development.

## What to store (minimum for Foundry)

From the PoC provisioning runbook, these Key Vault secret names are the stable interface:

- `azure-foundry-agent-endpoint`
- `azure-foundry-agent-project`
- `azure-foundry-agent-key` (optional if using managed identity)
- `elena-foundry-agent-id` (and `marcus-...`, `sage-...` if used)

See: [Customer Provisioning (PoC)](../../operations/customer-provisioning-poc.md)

## Naming conventions (ctxEco)

For current conventions, see the migration plan:

- `ctxeco-rg`, `ctxecokv`, `ctxeco-api`, `ctxeco-web`, etc.

See: [ctxEco.com Migration Plan](../../migration/ctxeco-migration-plan.md)

