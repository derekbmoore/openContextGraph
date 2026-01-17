# Deployment Checklist for Azure Container Apps

## Prerequisites Check

### 1. GitHub Secrets (Required)

**Minimum required for deployment:**
- ✅ `AZURE_CREDENTIALS` - Service Principal JSON (or individual secrets)
  - Contains: `clientId`, `clientSecret`, `subscriptionId`, `tenantId`

**Optional (with defaults):**
- `AZURE_RESOURCE_GROUP` - Default: `ctxeco-rg`
- `AZURE_BACKEND_APP_NAME` - Default: `ctxeco-api`
- `AZURE_WORKER_APP_NAME` - Default: `ctxeco-worker`

### 2. Verify Container App Names

Check your actual deployed Container App names:
```bash
az containerapp list --resource-group ctxeco-rg --query "[].{Name:name}" -o table
```

The workflow uses these defaults, but your actual names may differ if they follow the Bicep pattern:
- Bicep pattern: `${envName}-api` and `${envName}-worker` (where `envName` defaults to `ctxEco-env`)
- Possible actual names: `ctxEco-env-api` and `ctxEco-env-worker`

**Fix:** Set `AZURE_BACKEND_APP_NAME` and `AZURE_WORKER_APP_NAME` secrets if your names differ.

### 3. Service Principal Permissions

Ensure the service principal has:
- **Contributor** role on the resource group
- Access to Container Apps to update revisions

```bash
# Check service principal roles
az role assignment list \
  --assignee <SERVICE_PRINCIPAL_CLIENT_ID> \
  --scope /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/ctxeco-rg \
  --query "[].{Role:roleDefinitionName}" -o table
```

## Deployment Process

1. **Push code to main branch** → Triggers CI workflow
2. **Build Images job** → Builds and pushes to `ghcr.io/derekbmoore/opencontextgraph/backend:latest`
3. **Deploy Azure job** → Updates Container Apps with new image

## Verify Deployment

After pushing:
1. Check GitHub Actions: https://github.com/derekbmoore/openContextGraph/actions
2. Verify build succeeded
3. Verify deployment step updated Container Apps
4. Check Container App revisions:
   ```bash
   az containerapp revision list \
     --name ctxeco-api \
     --resource-group ctxeco-rg \
     --query "[0].{Name:name,Image:properties.template.containers[0].image,Active:properties.active}" -o table
   ```

## Troubleshooting

### "Container App not found"
- Verify the app name matches your actual deployment
- Set `AZURE_BACKEND_APP_NAME` and `AZURE_WORKER_APP_NAME` secrets

### "Authorization failed"
- Verify `AZURE_CREDENTIALS` is set correctly
- Check service principal has Contributor role

### "Image pull failed"
- Verify image was pushed to GHCR: `ghcr.io/derekbmoore/opencontextgraph/backend:latest`
- Check Container App has access to GHCR (if private)
