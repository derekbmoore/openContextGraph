# Kubernetes (optional)

**derekbmoore/opencontextgraph** is a **container-based** OSS (MIT) system. The standard ways to run it are:

| Path | Use case |
|------|----------|
| **Docker Compose** | Local dev and testing (`docker compose up` from repo root). |
| **Azure Container Apps** | Managed containers in Azure via `infra/main.bicep` (default: no Kubernetes). |

This **`infra/k8s/`** folder is an **optional, reference** deployment for running the same container images on **Kubernetes** (AKS or on-prem). You do not need it for the default container-based flow.

## When to use k8s

- You want to run OpenContextGraph on **your own Kubernetes** (on-prem or any cloud).
- You use **Azure** with `environment=prod` and the main Bicep deploys AKS; these manifests can serve as a reference for workload shape, not as the single source of truth (Bicep/ACA are primary for Azure).

## What’s in this folder

| Path | Purpose |
|------|---------|
| `backend/` | API deployment, service, service account (and CSI secret store for Azure Key Vault). |
| `worker/` | Temporal worker deployment. |
| `zep/` | Zep deployment. |
| `temporal/` | Helm values for Temporal Server. |
| `namespaces/` | Example namespace (e.g. prod). |
| `network-policies/` | Example network policies. |

Image references use `ghcr.io/derekbmoore/opencontextgraph/backend` and `.../worker` (same images as Compose and ACA).

## Summary

- **Primary (OSS, container-based):** Docker Compose + Azure Container Apps.  
- **Optional:** Use `infra/k8s/` when you need a Kubernetes-based deployment; it is a reference, not required for the standard container workflow.
