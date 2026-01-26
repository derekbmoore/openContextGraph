# Infrastructure

This folder contains the Bicep templates and optional K8s manifests for the Cognitive Enterprise Architecture. **The OSS system is container-based:** default run paths are Docker Compose (local) and Azure Container Apps (here). For Kubernetes (AKS or on‑prem), see [infra/k8s/README.md](k8s/README.md).

## Resources Deployed (Bicep → ACA)
- **Azure Container Apps Environment**: For hosting Zep, Temporal, and Agents.
- **Postgres Flexible Server (B1ms)**: Shared database for Zep and Temporal.
- **Storage Account**: For Unstructured.io data ingestion (Data Lake).
- **Log Analytics**: Observability.

## Deployment

```bash
az group create --name cogai-rg --location eastus
az deployment group create --resource-group cogai-rg --template-file main.bicep --parameters postgresPassword='<YOUR_SECURE_PASSWORD>'
```
