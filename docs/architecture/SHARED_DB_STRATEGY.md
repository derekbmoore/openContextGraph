# Shared Database Access Strategy: CtxEco & SecAI Radar

## Overview

This document defines the production authentication and authorization strategy for the shared PostgreSQL resource (`ctxeco-db`). As `ctxEco` (Enterprise Agentic Platform) and `secai-radar` (Security Auditing) converge, they must share infrastructure while maintaining security isolation and operational robustness.

## Core Principles

1. **Identity Over Passwords**: Wherever possible (i.e., for code we control), we accept **Managed Identity (MI)** authentication. This eliminates password management, rotation, and leakage risks.
2. **Least Privilege**: Each application/container connects as a specific identity with permissions limited strictly to its required scope (specific database and schema).
3. **Isolation**: Third-party services (like Zep) that do not natively support Azure MI will use **Dedicated Service Accounts** with unique, strong passwords stored in Key Vault. They will NEVER share the `admin` credentials.

## Access Architecture by Container

### 1. CtxEco Platform (Core)

| Container | Type | Database | Auth Method (Target) | Why? |
| :--- | :--- | :--- | :--- | :--- |
| **ctxeco-worker** | Python (Custom) | `ctxEco` | **Managed Identity** | Application reads/writes core platform data. MI allows granular RBAC without managing secrets. |
| **ctxeco-api** | Python (Custom) | `ctxEco` | **Managed Identity** | Same as worker. Uses `DefaultAzureCredential` to acquire tokens for `oss-rdbms`. |
| **ctxeco-zep** | Go (Third-Party) | `zep` | **Service Account** (`zep_user`) | Zep is a pre-built image. We provision a dedicated Postgres user `zep_user` with access ONLY to the `zep` database. Credentials injected via Key Vault. |

### 2. SecAI Radar (Auditing)

| Container | Type | Database | Auth Method (Target) | Why? |
| :--- | :--- | :--- | :--- | :--- |
| **secai-radar-public-api** | Python (Custom) | `secairadar` | **Managed Identity** | Reads/writes security audit logs. MI allows strict separation from `ctxEco` data while sharing the server. |
| **secai-radar-registry-api**| Python (Custom) | `secairadar` | **Managed Identity** | Same as public API. |

## Production Integration Strategy

As we move to production, `ctxEco` agents may need to query `secai` data (e.g., "Show me the security posture of this repo").

**Cross-Application Access:**
Instead of sharing passwords, we simply **GRANT** the `ctxeco-worker` Managed Identity access to specific tables in the `secairadar` database.

- *Example*: `GRANT SELECT ON ALL TABLES IN SCHEMA public TO "ctxeco-worker-identity";` (executed in `secairadar` DB).

**Benefits:**

- **No credential sharing**: CtxEco never sees SecAI's secrets.
- **Audit Trail**: Database logs show exactly *which* identity accessed the data.
- **Revocability**: We can revoke CtxEco's access to SecAI data instantly without breaking SecAI's own operations.

## Implementation Roadmap

### Phase 1: Stabilization (Immediate)

- [x] Reset `ctxecoadmin` password to a safe alphanumeric baseline.
- [x] Create dedicated `zep_user` for Zep.
- [x] Update `secai-radar` to use the new Admin password (Temporary fix).

### Phase 2: Managed Identity Migration (High Priority)

- [ ] **CtxEco**: Update `backend` code (Tortoise/SQLAlchemy) to use `azure-identity` for token generation.
- [ ] **SecAI**: Update `public-api` code to use `azure-identity`.
- [ ] **Infrastructure**: Grant `PostgreSQL User` role to the User Assigned Identities of both apps.

### Phase 3: Zep Isolation

- [ ] Ensure `zep_user` has `NOINHERIT` and strictly limited permissions (cannot read `ctxEco` or `secairadar` DBs).
