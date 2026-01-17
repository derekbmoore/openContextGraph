# GitHub Secrets and Azure Key Vault Configuration

This document describes how secrets are managed for the OpenContextGraph CI/CD pipeline.

## Secret Management Strategy

### GitHub Secrets (Repository Settings → Secrets and variables → Actions)

**Required for CI/CD:**

**Option 1: AZURE_CREDENTIALS (Recommended - matches engram pattern)**
- `AZURE_CREDENTIALS` - Service Principal JSON containing clientId, clientSecret, subscriptionId, tenantId

**Option 2: Individual Secrets (Alternative)**
- `AZURE_CLIENT_ID` - Service Principal Client ID
- `AZURE_TENANT_ID` - Azure AD Tenant ID
- `AZURE_SUBSCRIPTION_ID` - Azure Subscription ID
- `AZURE_CLIENT_SECRET` - Service Principal Client Secret

**Creating AZURE_CREDENTIALS:**
```bash
# Login to Azure
az login

# Set variables
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
RESOURCE_GROUP="ctxeco-rg"
SP_NAME="opencontextgraph-github-actions"

# Create service principal with contributor role
az ad sp create-for-rbac \
  --name "$SP_NAME" \
  --role contributor \
  --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP" \
  --sdk-auth

# Output JSON should be saved as AZURE_CREDENTIALS secret
```

**Note:** If you prefer using OpenID Connect (federated credentials) instead of service principal secrets, you can configure it in Azure AD. See [Azure Federated Identity Credentials](https://learn.microsoft.com/en-us/azure/active-directory/develop/workload-identity-federation-create-trust-github) for setup instructions.

**Required for Deployment (passed to Bicep templates):**
- `POSTGRES_PASSWORD` - PostgreSQL admin password (stored in Key Vault during deployment)
- `CR_PAT` - GitHub Container Registry Personal Access Token

**Optional for CI/CD (with defaults):**
- `AZURE_RESOURCE_GROUP` - Resource group name (default: `ctxeco-rg`)
- `AZURE_BACKEND_APP_NAME` - Backend Container App name (default: `ctxeco-api`)
- `AZURE_WORKER_APP_NAME` - Worker Container App name (default: `ctxeco-worker`)
- `AZURE_KEY_VAULT_NAME` - Key Vault name for fetching config (optional)

**Optional for Deployment (passed to Bicep templates):**
- `ZEP_API_KEY` - Zep API key (stored in Key Vault, optional)
- `AZURE_AI_ENDPOINT` or `AZURE_OPENAI_ENDPOINT` - Azure AI endpoint URL
- `AZURE_OPENAI_KEY` - Azure OpenAI API key (alternative to APIM key)
- `AZURE_AI_PROJECT_NAME` - Azure AI project name (optional)
- `AZURE_AD_TENANT_ID` - Azure AD tenant ID for authentication
- `AZURE_AD_CLIENT_ID` - Azure AD client ID for frontend app
- `AZURE_AD_EXTERNAL_ID` - Whether using Entra External ID (CIAM), set to 'true' if using
- `AZURE_AD_EXTERNAL_DOMAIN` - Entra External ID tenant domain
- `AZURE_FOUNDRY_AGENT_ENDPOINT` - Azure AI Foundry agent endpoint
- `AZURE_FOUNDRY_AGENT_PROJECT` - Azure AI Foundry agent project
- `AZURE_FOUNDRY_AGENT_KEY` - Azure AI Foundry agent API key
- `ELENA_FOUNDRY_AGENT_ID` - Elena Foundry agent ID

### Azure Key Vault

**Application Secrets** (automatically referenced by Container Apps via Bicep):
- `postgres-password` - PostgreSQL admin password
- `zep-api-key` - Zep API key
- `azure-ai-key` - Azure AI Services API key
- `anthropic-api-key` - Anthropic Claude API key (for Sage agent)
- `gemini-api-key` - Google Gemini API key (for Sage agent)
- `voicelive-api-key` - Azure VoiceLive API key
- `github-token` - GitHub token for repository access
- `azure-foundry-agent-endpoint` - Azure AI Foundry agent endpoint
- `azure-foundry-agent-project` - Azure AI Foundry agent project
- `azure-foundry-agent-key` - Azure AI Foundry agent API key
- `elena-foundry-agent-id` - Elena Foundry agent ID

**How it works:**
1. Secrets are stored in Azure Key Vault (created via `infra/main.bicep`)
2. Container Apps are configured with Managed Identity access to Key Vault
3. Bicep templates reference secrets via `keyVaultUrl` (e.g., `${keyVaultUri}secrets/postgres-password`)
4. Container Apps pull secrets at runtime using Managed Identity authentication

**Key Vault Configuration:**
- Key Vault name pattern: `${envName}kv` (e.g., `ctxEco-envkv`)
- Managed Identity has "Key Vault Secrets User" role on Key Vault
- Secrets are referenced via `AZURE_KEYVAULT_URL` environment variable in Container Apps

## Setting Up Secrets

### GitHub Secrets
1. Go to Repository Settings → Secrets and variables → Actions
2. Add required secrets listed above
3. Use environment-specific secrets for `production` vs `staging` environments if needed

### Azure Key Vault
Secrets are managed via Infrastructure as Code (`infra/main.bicep` and `infra/modules/keyvault-secrets.bicep`):
- Initial secrets are seeded during Bicep deployment
- Updates can be made via Azure Portal, Azure CLI, or by updating Bicep parameters

```bash
# Example: Update a secret via Azure CLI
az keyvault secret set \
  --vault-name ctxEco-envkv \
  --name postgres-password \
  --value "new-password"
```

## Security Best Practices

1. **Never commit secrets to git** - All secrets must be in GitHub Secrets or Key Vault
2. **Use Managed Identity** - Container Apps authenticate to Key Vault using Managed Identity (no credentials stored)
3. **Principle of Least Privilege** - Grant only required permissions to service principals and managed identities
4. **Environment Isolation** - Use separate Key Vaults and secrets for production vs staging
5. **Rotation** - Regularly rotate secrets, especially in production

## Troubleshooting

### CI/CD Authentication Failures
- Verify `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_SUBSCRIPTION_ID` are set correctly
- Ensure service principal has required permissions (Container Apps Contributor, Key Vault Secrets User)

### Container App Secret Access Failures
- Verify Managed Identity is assigned to Container App
- Check Managed Identity has "Key Vault Secrets User" role on Key Vault
- Verify `AZURE_KEYVAULT_URL` environment variable is set correctly in Container App

