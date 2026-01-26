# Infrastructure

This folder contains the Bicep templates and optional K8s manifests for the Cognitive Enterprise Architecture. **The OSS system is container-based:** default run paths are Docker Compose (local) and Azure Container Apps (here). For Kubernetes (AKS or on‑prem), see [infra/k8s/README.md](k8s/README.md).

When used in the integrated workspace with **secai-radar**, the same Postgres server (`ctxeco-db` when `envName: "ctxeco"`) hosts the `secairadar` database. See **INTEGRATED-WORKSPACE-DATABASE.md** at the workspace root for the shared-database layout and security model.

## Resources Deployed (Bicep → ACA)
- **Azure Container Apps Environment**: For hosting Zep, Temporal, and Agents.
- **Postgres Flexible Server (B1ms)**: Shared database for Zep, Temporal, and (when integrated) secai-radar (`secairadar` DB).
- **Storage Account**: For Unstructured.io data ingestion (Data Lake).
- **Log Analytics**: Observability.

## Deployment

```bash
az group create --name cogai-rg --location eastus
az deployment group create --resource-group cogai-rg --template-file main.bicep --parameters postgresPassword='<YOUR_SECURE_PASSWORD>'
```
