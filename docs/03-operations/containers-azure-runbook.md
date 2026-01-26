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

4. **Zep — "password authentication failed for user ctxEco"**  
   Zep must use the same Postgres password as the `postgres` service. The compose file passes `ZEP_STORE_POSTGRES_DSN` and `ZEP_STORE_TYPE` from the environment so the DSN always uses `${POSTGRES_PASSWORD:-changeme}`. If you use a custom password, set `POSTGRES_PASSWORD` (e.g. in `.env`) so both postgres and Zep see it. If the postgres volume was created with a different password earlier, set `POSTGRES_PASSWORD` to that value when running `docker compose up`, or remove the volume and start fresh.

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


### Zep in Azure (single flow)

Zep runs as a Container App and gets its **Postgres DSN only from Key Vault** when the template is used with `keyVaultUri` and a user-assigned identity. The config file has **no** `store.postgres.dsn` in that case so the env var `ZEP_STORE_POSTGRES_DSN` (from the KV secret **`zep-postgres-dsn`**) is the single source of truth.

**You need:**

1. **Key Vault** (e.g. `ctxecokv`) with secret **`zep-postgres-dsn`** = full DSN  
   `postgresql://<admin_user>:<password>@<postgres_fqdn>:5432/zep?sslmode=require`  
   User must match the Flex Server admin (e.g. `ctxecoadmin` for ctxeco-db).

2. **User-assigned identity** (e.g. `ctxeco-zep-id`) with **Key Vault Secrets User** on that vault, attached to the Zep app.

3. **Restart** after any DSN or identity change so the app pulls the updated secret.

---

**Fix when you see `password authentication failed for user "ctxecoadmin"`**

The password in **ctxecokv** `postgres-password` must match what **ctxeco-db** uses for `ctxecoadmin`. If it doesn’t, use one of these:

- **You know the correct server password** — from this repo (ctxEco) run:
  ```bash
  POSTGRES_PASSWORD='the-actual-server-password' ./scripts/fix-zep-db-auth.sh
  ```
  Or run `./scripts/fix-zep-db-auth.sh` and enter the password when prompted. The script updates ctxecokv (`postgres-password`, `zep-postgres-dsn`, `postgres-connection-string`) and forces a new Zep revision.

- **You’re not sure of the password** — reset it on the server, then run the script with the new value:
  1. Azure Portal → **ctxeco-db** → Settings → **Reset password**, or:
     `az postgres flexible-server update -g ctxeco-rg -n ctxeco-db --admin-password 'YourNewPassword'`
  2. `POSTGRES_PASSWORD='YourNewPassword' ./scripts/fix-zep-db-auth.sh`

- **Update both ctxEco and secai-radar** — from the secai-radar repo run `./scripts/update-db-credentials-secai-ctxeco.sh` (see **INTEGRATED-WORKSPACE-DATABASE.md** at the workspace root). That updates both vaults and restarts Zep.

**If Zep still fails after running the fix** (revision still logs `password authentication failed`):

1. **Verify the DSN** — ensure the vault value matches the server and works locally:
   ```bash
   KV=ctxecokv
   # Inspect (host/user/db only; password is redacted in practice)
   az keyvault secret show --vault-name "$KV" --name zep-postgres-dsn --query value -o tsv
   # Test connectivity (requires psql; replace with actual DSN from above or from portal)
   # psql "<paste-DSN-here>" -c "SELECT 1"
   ```
   If you reset the server password with `az postgres flexible-server update --admin-password`, that value must be in **ctxecokv** `postgres-password`; `fix-zep-db-auth.sh` builds `zep-postgres-dsn` from it.

2. **Force a new revision and scale** — sometimes scale 0→1 reuses the same revision; create a new one explicitly so the container cold-starts and refetches from Key Vault:
   ```bash
   az containerapp update -g ctxeco-rg -n ctxeco-zep --revision-suffix "dsn-$(date +%s)" --output none
   az containerapp update -g ctxeco-rg -n ctxeco-zep --min-replicas 0 --max-replicas 2 --output none
   az containerapp update -g ctxeco-rg -n ctxeco-zep --min-replicas 1 --max-replicas 2 --output none
   ```

3. **Confirm identity** — `az containerapp show -g ctxeco-rg -n ctxeco-zep --query 'identity.userAssignedIdentities' -o json` should list the Zep identity, and that identity must have **Key Vault Secrets User** on **ctxecokv**.

---

**If the app has no managed identity** (`az containerapp show -g ctxeco-rg -n ctxeco-zep --query 'identity.type' -o tsv` → `None`):

```bash
RG=ctxeco-rg
KV=ctxecokv
ZEP_APP=ctxeco-zep
IDENTITY_NAME=ctxeco-zep-id

az identity create -g "$RG" -n "$IDENTITY_NAME" --output none
PRINCIPAL_ID=$(az identity show -g "$RG" -n "$IDENTITY_NAME" --query principalId -o tsv)
IDENTITY_ID=$(az identity show -g "$RG" -n "$IDENTITY_NAME" --query id -o tsv)
KV_ID=$(az keyvault show -g "$RG" -n "$KV" --query id -o tsv)
az role assignment create --role "Key Vault Secrets User" --assignee "$PRINCIPAL_ID" --scope "$KV_ID" --output none
az containerapp identity assign -g "$RG" -n "$ZEP_APP" --user-assigned "$IDENTITY_ID" --output none
```

Then run **`./scripts/fix-zep-db-auth.sh`** (or the “Update both” script from secai-radar) to set **`zep-postgres-dsn`** and restart.  
Prefer a full Bicep deploy so identity and KV role stay in code; this is for one-off repair when the app was created without them.

---

**Checks when Zep is unhealthy**

- **Log stream:** Container Apps → **ctxeco-zep** → Log stream. Look for `password authentication failed`, Key Vault/secret errors, or `SASL: FATAL`.
- **Identity:** `identity.type` must be `UserAssigned` and the identity must have **Key Vault Secrets User** on the vault.
- **Startup:** The template allows ~7 minutes (60s + 36×10s) for startup; after fixing DSN or identity, force a new revision (`--revision-suffix "dsn-$(date +%s)"`) then scale 0→1 so the new revision pulls the secret from Key Vault.

### Shared database (integrated workspace)

When ctxEco and **secai-radar** use the same Postgres server (e.g. `ctxeco-db` with `envName: "ctxeco"`), see **`INTEGRATED-WORKSPACE-DATABASE.md`** at the workspace root. That doc covers:

- Which databases live on the server (`ctxEco`, `zep`, `temporal`, `temporal_visibility`, `secairadar`) and who creates them
- Security: ctxEco uses the server admin and **ctxecokv**; secai-radar uses a dedicated user **`secairadar_app`** and **secai-radar-kv**
- One-time steps for secai-radar (create `secairadar_app` via `create-secairadar-db-user.py`, store the connection string in secai-radar-kv)

The Bicep in this repo creates the **`secairadar`** database on the shared server so secai-radar only needs to run migrations and the user-creation script.

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

- **Zep (Azure)**  
  - Zep module now depends on **keyVaultSecrets** so the **`zep-postgres-dsn`** secret exists in Key Vault before the Zep app starts.  
  - **ctxeco** environment: `postgresAdminUser` set to `ctxecoadmin` in `infra/environments/ctxeco/parameters.json` so the DSN aligns with the existing ctxeco-db server.  
  - Runbook: added **“Fix Zep in Azure (steps you can run now)”** with AZ CLI to set `zep-postgres-dsn` and restart the Zep app.

More detail: [ctxeco-deployment-issues-january-2026.md](../05-knowledge-base/ctxeco-deployment-issues-january-2026.md) (“Local container fixes” section).
