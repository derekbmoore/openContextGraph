# GitHub Secrets and Azure Key Vault Configuration

This document describes how secrets are managed for the OpenContextGraph CI/CD pipeline.

## Secret Management Strategy

### GitHub Secrets (Repository Settings → Secrets and variables → Actions)

**Required for CI/CD:**
- `AZURE_CLIENT_ID` - Service Principal Client ID for Azure authentication
- `AZURE_TENANT_ID` - Azure AD Tenant ID
- `AZURE_SUBSCRIPTION_ID` - Azure Subscription ID

**Optional for CI/CD (with defaults):**
- `AZURE_RESOURCE_GROUP` - Resource group name (default: `ctxeco-rg`)
- `AZURE_BACKEND_APP_NAME` - Backend Container App name (default: `ctxeco-api`)
- `AZURE_WORKER_APP_NAME` - Worker Container App name (default: `ctxeco-worker`)
- `AZURE_KEY_VAULT_NAME` - Key Vault name for fetching config (optional)

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

