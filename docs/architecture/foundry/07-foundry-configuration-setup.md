---
layout: default
title: Foundry Configuration Setup (Key Vault + CI/CD)
parent: Foundry (Azure AI Foundry)
nav_order: 7
description: "Step-by-step: configure Foundry endpoint/project/agent IDs for ctxEco deployments."
---

# Foundry Configuration Setup (Key Vault + CI/CD)

This is the **practical setup checklist** to ensure Foundry agents can call ctxEco and vice versa.

## 1) Required values

- Foundry endpoint: `https://<account>.services.ai.azure.com`
- Foundry project: `<project-name>`
- Agent IDs: `ELENA_FOUNDRY_AGENT_ID` (+ Marcus/Sage as needed)

## 2) Store in Key Vault (production)

Example:

```bash
az keyvault secret set --vault-name "ctxecokv" --name "azure-foundry-agent-endpoint" --value "https://<account>.services.ai.azure.com"
az keyvault secret set --vault-name "ctxecokv" --name "azure-foundry-agent-project" --value "<project-name>"
az keyvault secret set --vault-name "ctxecokv" --name "elena-foundry-agent-id" --value "<agent-id>"
```

Optional (only if not using managed identity):

```bash
az keyvault secret set --vault-name "ctxecokv" --name "azure-foundry-agent-key" --value "<api-key>"
```

## 3) Configure GitHub Secrets (CI/CD)

Set these repository secrets to drive deployments (names vary by workflow, but should map into Key Vault secrets):

- `AZURE_FOUNDRY_AGENT_ENDPOINT`
- `AZURE_FOUNDRY_AGENT_PROJECT`
- `AZURE_FOUNDRY_AGENT_KEY` (optional)
- `ELENA_FOUNDRY_AGENT_ID`

## 4) Verify the deployment

Use the provisioning runbook smoke tests:

- [Customer Provisioning (PoC)](../../operations/customer-provisioning-poc.md)

