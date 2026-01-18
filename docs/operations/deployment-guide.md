# OpenContextGraph Deployment Guide

This guide details how to deploy the **OpenContextGraph** platform (formerly Engram/CtxEco) to a new Azure Tenant (e.g., a customer environment).

Before customer demos, run the readiness checklist in [docs/operations/poc-readiness-checklist.md](poc-readiness-checklist.md).

## 1. Prerequisites

Before beginning the deployment, ensure you have the following administrative access and prerequisites:

* **Azure Subscription:** Contributor or Owner access to a valid Azure Subscription.
* **Azure CLI:** Installed and authenticated (`az login`).
* **GitHub CLI:** Installed (`gh auth login`) if deploying from valid source.
* **Domain Name:** A custom domain (e.g., `agency-context.com`) managed via DNS (Cloudflare, GoDaddy, or Azure DNS).
* **CIAM Tenant:** An Azure Entra External ID (CIAM) tenant for handling authentication.

### Regional Requirements

* **Avatar/VoiceLive:** Requires **`westus2`**, `northeurope`, or `southeastasia` for Azure Speech Service (Avatar Realtime).
* **Recommendation:** Deploy all resources in **`westus2`** or **`eastus2`** (if Avatar latency across US is acceptable).

## 2. Infrastructure Overview

The platform consists of the following Azure resources:

| Resource | Purpose | Recommended SKU |
|----------|---------|-----------------|
| **Container Apps Env** | Hosting Backend, Worker, Zep | Consumption |
| **PostgreSQL Flexible** | Main DB + Vector Store (pgvector) | `Standard_B2ms` (or `D4ds_v4` for Prod) |
| **Logic/Storage** | System of Record (Blob/File) | `Standard_LRS` |
| **Key Vault** | Secrets Management | Standard |
| **Log Analytics** | Telemetry & Auditing | PerGB2018 |
| **Azure AI Speech** | Avatar & Voice Capabilities | `S0` (must be in `westus2`) |

## 3. Configuration & Secrets

You must seed the **Key Vault** with these secrets before the Container Apps can start.

### 3.1 Required Secrets (Key Vault)

| Secret Name | Description | Source |
|-------------|-------------|--------|
| `postgres-password` | Admin password for DB | Generated/User defined |
| `zep-api-key` | API Key for Zep Memory Service | Generated (High entropy string) |
| `azure-ai-key` | Key for Azure OpenAI/Foundry | Azure Portal (AI Foundry) |
| `anthropic-api-key` | (Optional) For Anthropic fallback | Anthropic Console |
| `gemini-api-key` | (Optional) For Gemini fallback | Google AI Studio |
| `voicelive-api-key` | Voice live API key (Cognitive Services) | Azure Portal (AI Services) |
| `azure-speech-key` | Azure Speech Service Key | Azure Portal -> Speech Resource (`westus2`) |
| `azure-openai-realtime-endpoint` | Azure OpenAI Realtime endpoint | Azure Portal (OpenAI resource) |
| `azure-openai-realtime-key` | Azure OpenAI Realtime key | Azure Portal (OpenAI resource) |
| `github-token` | PAT for Repo Context Ingestion | GitHub Developer Settings |

### 3.2 Bicep Parameters

The `infra/main.bicep` file controls the specific deployment configuration. Important parameters to override for customers:

```bicep
param envName string = 'customer-app'       // Resource prefix
param environment string = 'prod'           // prod, uat, staging
param azureAdExternalDomain string = ''     // e.g., 'customer-auth.ciamlogin.com'
param azureVoiceLiveEndpoint string = ''    // Default: 'https://zimax.services.ai.azure.com'
param azureAiEndpoint string = ''           // Your AI Foundry Endpoint
```

## 4. Step-by-Step Deployment

### Step 1: Create Resource Group & Core Identity

```bash
# 1. Create Resource Group
az group create --name customer-rg --location westus2

# 2. Create User Assigned Identities (used for initial setup permissions)
az identity create -g customer-rg -n customer-backend-id
az identity create -g customer-rg -n customer-worker-id
```

### Step 2: Provision Infrastructure (Bicep)

Navigate to the `infra/` directory and run the deployment.

```bash
# Example deployment using Azure CLI
az deployment group create \
  --resource-group customer-rg \
  --template-file main.bicep \
  --parameters \
    envName=customer-app \
    environment=prod \
    postgresPassword=<SECURE_PASSWORD> \
    azureSpeechRegion=westus2 \
    deployAks=false
```

### Step 3: Seed Secrets

Once the Key Vault is created (output from Step 2), run a script or manually add the secrets listed in Section 3.1.

```bash
# Example
az keyvault secret set --vault-name customerkv --name azure-speech-key --value "<YOUR_KEY>"
az keyvault secret set --vault-name customerkv --name voicelive-api-key --value "<ZIMAX_PROVIDED_KEY>"
```

### Step 4: Deploy Configuration Updates

After seeding secrets, you may need to redeploy the Bicep template (or specific modules) to ensure the Container Apps pick up the latest secret versions if they failed to start initially.

## 5. Domain & SSL

1. Get the **Static IP** of the Container Apps Environment (if custom VNet) or the default DNS suffix.
2. Configure CNAME records for:
    * `api.customer-domain.com` -> Backend Container App
    * `zep.customer-domain.com` -> Zep Container App
3. Add Custom Domains in the Azure Portal (Container Apps bucket) to provision Managed Certificates.

## 6. Troubleshooting

* **Avatar Video Fails:** Check browser console. If `401 Unauthorized` on ICE candidates, ensure `azure-speech-key` is valid and `azureSpeechRegion` matches the resource region (`westus2`).
* **Database Connection:** Ensure the `backend-id` Managed Identity has access/firewall rules allow the container subnet.
