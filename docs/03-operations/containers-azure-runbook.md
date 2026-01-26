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

### Zep: "password authentication failed for user \"ctxecoadmin\""

Zep is trying to connect to PostgreSQL with a user that doesn’t match the Flexible Server admin, or the password is wrong.

- **Template default**: `main.bicep` uses Postgres admin `cogadmin` and passes it to Zep via `zepPostgresUser`. The Flex Server is created with `administratorLogin: 'cogadmin'`.
- **If you see `ctxecoadmin`**: The Zep app was likely deployed with a different config (different params, older template, or manual env/secret). The Flex Server may have been created with `administratorLogin: 'ctxecoadmin'` elsewhere.

**Fix:**

1. **Redeploy with aligned credentials**  
   Use the `postgresAdminUser` parameter so it matches the actual Postgres admin:
   - If the server uses **cogadmin**: no change; default is correct.
   - If the server uses **ctxecoadmin**: pass `postgresAdminUser=ctxecoadmin` in the Bicep/ARM deploy (or set it in your environment’s `parameters.json`, e.g. `infra/environments/ctxeco/parameters.json` already sets it for the shared ctxeco-db) and use that server’s admin password for `postgresPassword`. Zep and Temporal will then use `ctxecoadmin`, and the Key Vault secret **`zep-postgres-dsn`** will be seeded with the correct DSN on deploy.

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

### Fix Zep in Azure (steps you can run now)

If Zep is failing with a Postgres auth error and you want to fix it without a full redeploy:

1. **Set variables** (adjust for your environment; example uses `ctxeco-rg`, `ctxecokv`, `ctxeco-db`, `ctxeco-zep`):

   ```bash
   RG=ctxeco-rg
   KV=ctxecokv
   PG_USER=ctxecoadmin
   PG_HOST=ctxeco-db.postgres.database.azure.com
   ZEP_APP=ctxeco-zep
   ```

2. **Get the Postgres password** (must match the Flexible Server admin):

   ```bash
   PG_PASS=$(az keyvault secret show --vault-name "$KV" --name postgres-password --query value -o tsv)
   ```

   If that secret is wrong or missing, set the correct password in the vault or use the value you have:  
   `PG_PASS='your-actual-postgres-admin-password'`

3. **Build the DSN** (escape `@` and `%` in the password if needed; below assumes no special chars):

   ```bash
   DSN="postgresql://${PG_USER}:${PG_PASS}@${PG_HOST}:5432/zep?sslmode=require"
   ```

4. **Update the Key Vault secret** so Zep picks it up on next start:

   ```bash
   az keyvault secret set --vault-name "$KV" --name zep-postgres-dsn --value "$DSN" --output none
   ```

5. **Restart the Zep container app** (force a new revision so it re-reads KV):

   ```bash
   az containerapp revision restart --resource-group "$RG" --name "$ZEP_APP" --revision $(az containerapp revision list -g "$RG" -n "$ZEP_APP" --query '[0].name' -o tsv)
   ```

   Or scale to 0 and back to 1:

   ```bash
   az containerapp update --resource-group "$RG" --name "$ZEP_APP" --min-replicas 0 --max-replicas 2 --output none
   az containerapp update --resource-group "$RG" --name "$ZEP_APP" --min-replicas 1 --max-replicas 2 --output none
   ```

6. **Check logs** to confirm Zep connects:

   ```bash
   az containerapp logs show --resource-group "$RG" --name "$ZEP_APP" --tail 50
   ```

### Zep revision Unhealthy / container will not run

If the Zep revision shows **Unhealthy** or the container keeps restarting:

1. **Confirm DSN and KV**  
   Run the “Fix Zep in Azure (steps you can run now)” above: set **`zep-postgres-dsn`** in Key Vault to the correct full DSN, then restart (scale to 0 then back to 1, or revision restart).

2. **Confirm Zep can read Key Vault**  
   The Zep app uses a user-assigned identity with **Key Vault Secrets User** on the vault. If that role was missing or the identity wrong, Zep can’t resolve `zep-postgres-dsn` and may crash or hang. Redeploy the main Bicep so the Zep identity and `zepKvRole` are correct.

3. **Give Zep more time to start**  
   The template’s startup probe allows ~7 minutes (60s initial delay + 36×10s). If Zep still doesn’t pass before that, check Log stream for errors (e.g. failed DB connect, missing secret). After fixing causes, trigger a new revision (scale 0→1 or redeploy) so the new probe limits apply.

4. **Force a new revision**  
   After changing **`zep-postgres-dsn`** or fixing identity/KV, force a new revision so the app pulls the updated secret and probe config:
   ```bash
   az containerapp update -g ctxeco-rg -n ctxeco-zep --min-replicas 0 --max-replicas 2 --output none
   az containerapp update -g ctxeco-rg -n ctxeco-zep --min-replicas 1 --max-replicas 2 --output none
   ```
   Or create a new revision with a suffix:  
   `az containerapp update -g ctxeco-rg -n ctxeco-zep --revision-suffix "fix-$(date +%H%M)" --output none`

5. **See why it’s unhealthy (no response on /healthz)**  
   - **Portal → Log stream:** Azure Portal → Container Apps → **ctxeco-zep** → **Log stream**. Watch for `level=error`, `level=fatal`, `password authentication failed`, or `secret`/Key Vault errors.
   - **Zep has no managed identity (common cause):** The app needs a user-assigned identity to read **`zep-postgres-dsn`** from Key Vault. Check: `az containerapp show -g ctxeco-rg -n ctxeco-zep --query 'identity.type' -o tsv`. If it returns `None`, and `az identity list -g ctxeco-rg` shows no **ctxeco-zep-id**, use the steps in **“Apply the Zep identity fix (manual)”** below, or redeploy the ctxEco main Bicep so the template creates the identity and role.
   - **Key Vault access:** Portal → Key Vault **ctxecokv** → **Access control**. The Zep managed identity (e.g. **ctxeco-zep-id**) must have **Key Vault Secrets User**. The Bicep role `zepKvRole` does this at deploy time.
   - **Redeploy Bicep:** To fix identity, probes, and KV wiring in one go, redeploy the ctxEco infra (e.g. run the deployment workflow or `az deployment group create` for the main Bicep).

#### Apply the Zep identity fix (manual)

When the Zep app has **no managed identity** (`identity.type` is `None`) and there is no **ctxeco-zep-id** in the resource group, you can create the identity, grant it access to the vault, and attach it to the app with these steps. Use the same resource group, vault, and app names as in “Fix Zep in Azure” (e.g. `ctxeco-rg`, `ctxecokv`, `ctxeco-zep`).

1. **Create the user-assigned identity and assign Key Vault Secrets User:**

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
   ```

2. **Attach the identity to the Zep app:**

   ```bash
   az containerapp identity assign -g "$RG" -n "$ZEP_APP" --user-assigned "$IDENTITY_ID" --output none
   ```

3. **Ensure the app uses the DSN from Key Vault**  
   The Bicep config uses **`zep-postgres-dsn`** from the vault when `keyVaultUri` and `identityResourceId` are set. If this app was created without that, either redeploy the ctxEco Bicep or update the app so its secret/container config resolves `ZEP_STORE_POSTGRES_DSN` from the Key Vault secret **`zep-postgres-dsn`** (and the app uses the identity you just attached). Run **“Fix Zep in Azure (steps you can run now)”** to set **`zep-postgres-dsn`** in the vault if it’s missing or wrong.

4. **Restart Zep** so it picks up identity and secrets:

   ```bash
   az containerapp update -g "$RG" -n "$ZEP_APP" --min-replicas 0 --max-replicas 2 --output none
   az containerapp update -g "$RG" -n "$ZEP_APP" --min-replicas 1 --max-replicas 2 --output none
   az containerapp logs show -g "$RG" -n "$ZEP_APP" --tail 50
   ```

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
