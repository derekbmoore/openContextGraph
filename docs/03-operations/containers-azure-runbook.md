# CtxEco Containers: Local & Azure Runbook

**derekbmoore/opencontextgraph** is container-based (OSS, MIT). Standard run paths are **Docker Compose** (local) and **Azure Container Apps** (Azure). Kubernetes is optional — see `infra/k8s/README.md` if you run on K8s/AKS.

This runbook covers the API, worker, and Temporal containers locally and in Azure.

---

## Local (Docker Compose)

### Prerequisites

- Docker Desktop running
- Optional: `.env` in repo root (or use `.env.azure`) for Azure/VoiceLive; safe defaults exist so the stack can start without it

### Start order

From the **opencontextgraph** repo root (this repo):

```bash
# Data and orchestration first
docker compose up -d postgres temporal zep

# Wait until temporal and zep are healthy (temporal can take ~60s)
docker compose ps

# Then API and worker (depend on temporal + zep)
docker compose up -d api worker
```

Or in one go:

```bash
docker compose up -d postgres temporal zep api worker
```

### Useful commands

| Command | Purpose |
|---------|---------|
| `docker compose ps` | See status of all services |
| `docker compose logs -f api` | Follow API logs |
| `docker compose logs -f worker` | Follow worker logs |
| `docker compose logs -f temporal` | Follow Temporal logs |
| `docker compose down` | Stop and remove containers |

### Ports

| Service    | Port | Notes                    |
|-----------|------|--------------------------|
| Postgres  | 5432 | CtxEco DB                |
| Zep       | 8000 | Memory / CtxGraph        |
| Temporal  | 7233 | gRPC                     |
| Temporal UI | 8080 | Web UI                 |
| API       | 8082 | FastAPI (mapped from 8080) |

### If API / worker / temporal fail

1. **Worker**  
   Built from `backend/workflows/Dockerfile` (Compose). Image must have layout `/app/backend/` and `PYTHONPATH=/app` so `python -m backend.workflows.worker` works.  
   If you changed the worker Dockerfile, rebuild:  
   `docker compose build worker --no-cache && docker compose up -d worker`

2. **Temporal**  
   Healthcheck uses `tctl --address 127.0.0.1:7233 cluster health`. If it stays unhealthy, check logs and ensure Postgres is up; auto-setup can take 60s+.

3. **API**  
   Depends on Temporal and Zep being healthy. Check `docker compose logs api` for connection or config errors.

---

## Azure (Container Apps)

API, worker, and Temporal run as Azure Container Apps. Images come from GitHub Container Registry (GHCR).

### How images get built and deployed

1. **CI** (on push to `main` or `develop`, or workflow_dispatch with “Skip tests”):
   - Builds `backend` and `worker` from `backend/Dockerfile`
   - Worker is built with `WORKER_MODE=true` (same Dockerfile, entrypoint runs the worker)
- Pushes to `ghcr.io/<owner>/opencontextgraph/backend:latest` and `:${GITHUB_SHA}`
  - Same for `worker` (opencontextgraph is the GH repo used for images)

2. **Deploy** (after successful CI on `main`, or manually via workflow_dispatch):
   - When triggered by **CI completion**: uses images tagged with the **commit SHA** that CI built
   - When triggered by **workflow_dispatch**: uses `:latest`
   - Deploys Bicep (Temporal, Zep, backend API, worker, SWA, etc.) to the chosen environment (default `staging`)

### Getting containers running in Azure

**Option A – Full pipeline (recommended)**  
1. Push (or merge) to `main`.  
2. Wait for **CI** to finish (builds and pushes backend + worker).  
3. **Deploy** runs automatically and deploys the SHA that CI just built.

**Option B – Manual deploy**  
1. Ensure **CI** has run at least once on `main` so `backend:latest` and `worker:latest` exist in GHCR.  
2. In GitHub: **Actions → Deploy → Run workflow**.  
3. Choose **Environment** (e.g. staging) and **Auth required** (e.g. false for POC).  
4. Run. This deploys whatever is currently `:latest`.

**Option C – Build then deploy from a branch**  
1. In **CI**, use “Run workflow” and check “Skip tests and force build images” so it builds and pushes from the current branch.  
2. Run **Deploy** via “Run workflow” and pick the environment.  
   Note: Deploy will use `:latest` (or the default ref the workflow uses). For strict “this commit in Azure” you’d temporarily point Deploy at a branch or SHA; the default automation prefers “CI on main → deploy that SHA”.

### Required GitHub secrets (for Deploy)

- `AZURE_CREDENTIALS` – Azure login (e.g. app registration or federated credentials)
- `POSTGRES_PASSWORD` – Admin password for Postgres
- `CR_PAT` – GitHub PAT with `write:packages` (so workflow can pull from GHCR)
- Optional: `AZURE_OPENAI_KEY` or `AZURE_AI_ENDPOINT`, `ZEP_API_KEY`, `AZURE_AD_*`, etc. (see [GitHub Secrets](github-secrets.md))

### Resource group and locations

- Default resource group: `ctxEco-rg`
- Default location: `eastus2`  
Both are set in the Deploy workflow env.

### After deploy

- **Backend API**: URL comes from Bicep outputs (e.g. custom domain or ACA FQDN).
- **Temporal UI**: From Bicep output `temporalUIFqdn`.
- **Worker**: No ingress; it runs in the same ACA environment and talks to Temporal and Zep internally.

If the API or worker fail in Azure, check:

1. **Logs**: Container Apps → your app (e.g. `staging-env-api`, `staging-env-worker`) → Log stream / Log Analytics.  
2. **Images**: That the correct image:tag is deployed (SHA when deployed from CI, or `latest` when run manually).  
3. **Secrets**: Key Vault references and managed identity for the backend/worker (see [deployment](deployment.md) and Bicep).

### Zep: "password authentication failed for user \"ctxecoadmin\""

Zep is trying to connect to PostgreSQL with a user that doesn’t match the Flexible Server admin, or the password is wrong.

- **Template default**: `main.bicep` uses Postgres admin `cogadmin` and passes it to Zep via `zepPostgresUser`. The Flex Server is created with `administratorLogin: 'cogadmin'`.
- **If you see `ctxecoadmin`**: The Zep app was likely deployed with a different config (different params, older template, or manual env/secret). The Flex Server may have been created with `administratorLogin: 'ctxecoadmin'` elsewhere.

**Fix:**

1. **Redeploy with aligned credentials**  
   Use the `postgresAdminUser` parameter so it matches the actual Postgres admin:
   - If the server uses **cogadmin**: no change; default is correct.
   - If the server uses **ctxecoadmin**: pass `postgresAdminUser=ctxecoadmin` in the Bicep/ARM deploy and use that server’s admin password for `postgresPassword`. Zep and Temporal will then use `ctxecoadmin`.

2. **One-off fix in Azure**  
   In the Zep Container App, update the secret that holds the config (or the revision’s env) so the DSN uses the real Postgres admin user and password for that Flex Server. The DSN is in the mounted `config.yaml` (from secret `zep-config-yaml`). Ensure it matches the server’s `administratorLogin` and password.

3. **Confirm the Postgres user**  
   In Azure Portal: Flex Server → Overview or Settings → check the admin login. Use that exact value for `postgresAdminUser` (and in any manual Zep config).

### "The password was updated in KV" — Zep still failing

Zep reads its Postgres connection from Key Vault when the app is configured with a managed identity and the **`zep-postgres-dsn`** secret.

- **What to do**
  1. In Key Vault, create or update the secret **`zep-postgres-dsn`** with the **full** Postgres connection string, including the new password.  
     Example:  
     `postgresql://ctxecoadmin:YOUR_NEW_PASSWORD@your-server.postgres.database.azure.com:5432/zep?sslmode=require`
  2. User and host must match your Flex Server admin login and FQDN; `zep` is the database name.
  3. Restart the Zep container app (new revision or scale to 0 then back to 1) so it pulls the updated secret from Key Vault.

- **Why**  
  Zep is configured to use Key Vault for `ZEP_STORE_POSTGRES_DSN`. The template also seeds **`zep-postgres-dsn`** at deploy time from the same password. If you change only **`postgres-password`** in KV, Zep does not see that; it uses **`zep-postgres-dsn`**. So after a password change, update **`zep-postgres-dsn`** with the new full DSN, then restart Zep.

---

## Changes made for integrated workspace (Jan 2026)

- **Worker (local)**  
  - `backend/workflows/Dockerfile`: copy app into `/app/backend/`, set `PYTHONPATH=/app`, healthcheck `pgrep -f "backend.workflows.worker"`.

- **Temporal (local)**  
  - Healthcheck: `tctl --address 127.0.0.1:7233 cluster health`, longer `start_period` and more retries.

- **API (local)**  
  - Compose env defaults for `AUTH_REQUIRED`, `AZURE_VOICELIVE_*`, `AZURE_AD_*` so the stack can start without a full `.env`.

- **Deploy (Azure)**  
  - When Deploy is triggered by CI completion, it uses backend and worker images tagged with the CI commit SHA instead of `:latest`.  
  - Deploy job’s `environment` is set correctly when triggered by `workflow_run` (no manual inputs).

More detail: [ctxeco-deployment-issues-january-2026.md](../05-knowledge-base/ctxeco-deployment-issues-january-2026.md) (“Local container fixes” section).
