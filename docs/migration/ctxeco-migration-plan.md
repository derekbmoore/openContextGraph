# ctxEco.com Migration Plan

**From:** `engram-rg` (Legacy/Deleted) → **To:** `ctxeco-rg` (ctxeco.com)
**Repository:** `/Users/derek/Library/CloudStorage/OneDrive-zimaxnet/code/openContextGraph`
**Date:** 2026-01-16

---

## Current State: engram-rg Inventory (Legacy - Deleted from Azure)

| Resource Type | Resource Name | Purpose | Migration Priority |
|---------------|---------------|---------|-------------------|
| **CIAM Directory** | `engramai.onmicrosoft.com` | Azure AD B2C for authentication | P0 - New tenant required |
| **PostgreSQL** | `staging-env-db` | Primary database (Zep, application data) | P0 - Fresh database |
| **Key Vault** | `stagingenvkvysoxm5` | Secrets management | P0 - New vault |
| **Storage Account** | `stagingenvstore` | File storage, docs, images | P1 - New account |
| **Container Environment** | `staging-env-aca` | Azure Container Apps managed environment | P1 - New environment |
| **Container App** | `staging-env-api` | Backend API | P2 - New container |
| **Container App** | `staging-env-worker` | Temporal Worker | P2 - New container |
| **Container App** | `staging-env-zep` | Zep Memory Service | P2 - New container |
| **Container App** | `staging-env-temporal-server` | Temporal orchestration server | P2 - New container |
| **Container App** | `staging-env-temporal-ui` | Temporal web UI | P3 - Optional |
| **Static Web App** | `staging-env-web` | Frontend (React) | P3 - After backend |
| **Managed Identity** | `staging-env-backend-identity` | API identity | P1 - New identity |
| **Managed Identity** | `staging-env-worker-identity` | Worker identity | P1 - New identity |
| **Log Analytics** | `staging-env-logs` | Centralized logging | P1 - New workspace |
| **Managed Certs** | `*.engram.work` | SSL certificates | P4 - New domain certs |

---

## Target State: ctxeco-rg Naming Convention

| Old Name (engram-rg) | New Name (ctxeco-rg) | Notes |
|----------------------|----------------------|-------|
| `staging-env-db` | `ctxeco-db` | Fresh PostgreSQL Flexible Server |
| `stagingenvkvysoxm5` | `ctxecokv` | Key Vault (clean start) |
| `stagingenvstore` | `ctxecostore` | Storage Account |
| `staging-env-aca` | `ctxeco-aca` | Container Apps Environment |
| `staging-env-api` | `ctxeco-api` | API Container App |
| `staging-env-worker` | `ctxeco-worker` | Temporal Worker Container |
| `staging-env-zep` | `ctxeco-zep` | Zep Memory Service Container |
| `staging-env-temporal-server` | `ctxeco-temporal` | Temporal Server Container |
| `staging-env-temporal-ui` | `ctxeco-temporal-ui` | Temporal UI (optional) |
| `staging-env-web` | `ctxeco-web` | Static Web App |
| `staging-env-backend-identity` | `ctxeco-backend-id` | Managed Identity |
| `staging-env-worker-identity` | `ctxeco-worker-id` | Managed Identity |
| `staging-env-logs` | `ctxeco-logs` | Log Analytics Workspace |
| `engramai.onmicrosoft.com` | **ctxeco.onmicrosoft.com** | New CIAM Tenant ✅ Created |

---

## Confirmed Decisions

| Decision | Answer | Notes |
|----------|--------|-------|
| CIAM Tenant | `ctxeco.onmicrosoft.com` | Created 2026-01-16 |
| Container Registry | GHCR | Free, migrate to ACR if VNet needed |
| Temporal | Self-hosted OSS | Evaluate Temporal Cloud later |
| Database | Migrate from engram | pg_dump/restore |
| PostgreSQL SKU | Standard_B2ms | ~$30/mo, stop when not in use |

---

## Migration Phases

### Phase 1: Foundation (P0/P1)
>
> **Goal:** Create core infrastructure with default Azure domains first

- [ ] **1.1 Create CIAM Tenant**
  - New tenant: `ctxecoai.onmicrosoft.com`
  - Configure Google IdP
  - Create App Registration for ctxEco
  - Define user flows (sign-up, sign-in)

- [ ] **1.2 Create Database**

  ```bash
  az postgres flexible-server create \
    --resource-group ctxeco-rg \
    --name ctxeco-db \
    --location eastus2 \
    --sku-name Standard_B1ms \
    --storage-size 32 \
    --admin-user ctxecoadmin
  ```

- [ ] **1.3 Create Key Vault**

  ```bash
  az keyvault create \
    --resource-group ctxeco-rg \
    --name ctxecokv \
    --location eastus2
  ```

- [ ] **1.4 Create Storage Account**

  ```bash
  az storage account create \
    --resource-group ctxeco-rg \
    --name ctxecostore \
    --location eastus2 \
    --sku Standard_LRS
  ```

- [ ] **1.5 Create Log Analytics**

  ```bash
  az monitor log-analytics workspace create \
    --resource-group ctxeco-rg \
    --workspace-name ctxeco-logs \
    --location eastus2
  ```

- [ ] **1.6 Create Azure AI Speech (Avatar Requirement)**
  > **Note:** Real-time Avatar features require `westus2`, `northeurope`, or `southeastasia`.

  ```bash
  az cognitiveservices account create \
    --resource-group ctxeco-rg \
    --name ctxeco-speech \
    --location westus2 \
    --kind SpeechServices \
    --sku S0
  ```

- [ ] **1.6 Create Managed Identities**

  ```bash
  az identity create -g ctxeco-rg -n ctxeco-backend-id
  az identity create -g ctxeco-rg -n ctxeco-worker-id
  ```

---

### Phase 2: Container Environment (P1/P2)
>
> **Goal:** Deploy container apps with default Azure URLs

- [ ] **2.1 Create Container Apps Environment**

  ```bash
  az containerapp env create \
    --resource-group ctxeco-rg \
    --name ctxeco-aca \
    --location eastus2 \
    --logs-workspace-id <workspace-id>
  ```

- [ ] **2.2 Deploy Zep Container**
  - Image: `ghcr.io/getzep/zep-cloud:latest` (or self-hosted)
  - Environment variables from Key Vault
  - Connect to PostgreSQL

- [ ] **2.3 Deploy Temporal Server**
  - Image: `temporalio/server:latest`
  - Configure PostgreSQL visibility store

- [ ] **2.4 Deploy API Container**
  - Image: From GitHub Container Registry
  - Environment: CIAM, Zep, Temporal endpoints
  - Initial URL: `ctxeco-api.<env>.azurecontainerapps.io`

- [ ] **2.5 Deploy Worker Container**
  - Image: From GitHub Container Registry
  - Connect to Temporal

---

### Phase 3: Frontend & Domain (P3)
>
> **Goal:** Deploy frontend and configure custom domain

- [ ] **3.1 Deploy Static Web App**
  - Connect to openContextGraph GitHub repo
  - Build command: `npm run build`
  - Initial URL: `*.azurestaticapps.net`

- [ ] **3.2 Configure ctxeco.com DNS**
  - A/CNAME records for:
    - `ctxeco.com` → Static Web App
    - `api.ctxeco.com` → API Container App
    - `zep.ctxeco.com` → Zep Container App (if exposed)

- [ ] **3.3 Managed Certificates**
  - Create managed certificates for each custom domain

---

### Phase 4: Freeze engram-rg (P4)
>
> **Goal:** Stop all containers in engram-rg

- [ ] **4.1 Stop All Container Apps**

  ```bash
  az containerapp stop -g engram-rg -n staging-env-api
  az containerapp stop -g engram-rg -n staging-env-worker
  az containerapp stop -g engram-rg -n staging-env-zep
  az containerapp stop -g engram-rg -n staging-env-temporal-server
  az containerapp stop -g engram-rg -n staging-env-temporal-ui
  ```

- [ ] **4.2 Stop PostgreSQL** (if not sharing)

  ```bash
  az postgres flexible-server stop -g engram-rg -n staging-env-db
  ```

- [ ] **4.3 Document Final State**
  - Archive final environment variables
  - Export Key Vault secrets (encrypted)
  - Document DNS records

---

## Infrastructure as Code

### Required Updates in openContextGraph

The following files need to be created/updated:

1. **`infra/main.bicep`** - Copy from ctxEco and update:
   - Resource group: `ctxeco-rg`
   - Naming prefix: `ctxeco` instead of `staging-env`
   - CIAM tenant: `ctxecoai.onmicrosoft.com`

2. **`infra/environments/production.bicepparam`** - New parameters:
   - Domain: `ctxeco.com`
   - Subscription: Same
   - Location: `eastus2`

3. **`.github/workflows/deploy.yml`** - Update GitHub Actions:
   - New resource group targets
   - New secrets (AZURE_CREDENTIALS for ctxeco-rg)

---

## Key Decisions Required

> [!IMPORTANT]
> The following require user input before proceeding:

1. **CIAM Tenant Name:** `ctxecoai.onmicrosoft.com` - Confirm this name
2. **PostgreSQL SKU:** `Standard_B1ms` (dev) or larger for production?
3. **Database Migration:** Fresh start or migrate data from engram?
4. **Container Registry:** Use existing `ghcr.io` or create Azure ACR?
5. **Temporal:** Self-hosted or consider Temporal Cloud?

---

## Cost Considerations (FinOps)

| Resource | Estimated Monthly Cost |
|----------|----------------------|
| PostgreSQL (B1ms) | ~$15 |
| Container Apps (5 apps) | ~$50-100 |
| Static Web App (Standard) | ~$9 |
| Key Vault | ~$3 |
| Storage | ~$2 |
| Log Analytics | ~$5 |
| **Total** | **~$85-135/month** |

---

## Next Steps

1. [ ] Review and approve this plan
2. [ ] Create CIAM tenant (manual in Azure Portal)
3. [ ] Copy/adapt Bicep templates from ctxEco to openContextGraph
4. [ ] Execute Phase 1 provisioning
5. [ ] Stop engram-rg containers
6. [ ] Update openContextGraph codebase with new endpoints
7. [ ] Deploy and test
