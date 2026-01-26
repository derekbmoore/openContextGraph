#!/bin/bash
# Fix Zep "password authentication failed for user ctxecoadmin" by setting the
# correct Postgres password in ctxecokv and forcing a new Zep revision.
#
# The password MUST be the one that ctxeco-db currently accepts for ctxecoadmin.
# If you don't know it: reset it in Azure Portal (ctxeco-db → Reset password)
# or: az postgres flexible-server update -g ctxeco-rg -n ctxeco-db --admin-password 'NewPass'
# then run this script with that new password.
#
# Usage:
#   POSTGRES_PASSWORD='the-actual-server-password' ./scripts/fix-zep-db-auth.sh
#   # Or prompt (hidden):
#   ./scripts/fix-zep-db-auth.sh
#
# Requires: az login, read/write on ctxecokv, access to ctxeco-zep app.

set -e

urlencode_password() { python3 -c "import sys, urllib.parse; print(urllib.parse.quote(sys.stdin.read().strip(), safe=''))"; }

CTXECO_KV="${CTXECO_KV:-ctxecokv}"
CTXECO_RG="${CTXECO_RG:-ctxeco-rg}"
ZEP_APP="${ZEP_APP:-ctxeco-zep}"
PG_USER="${PG_USER:-ctxecoadmin}"
PG_HOST="${PG_HOST:-ctxeco-db.postgres.database.azure.com}"
PG_DB_CTXECO="${PG_DB_CTXECO:-ctxEco}"

if [ -n "${POSTGRES_PASSWORD:-}" ]; then
  PG_PASS="$POSTGRES_PASSWORD"
else
  echo "Enter PostgreSQL admin password for $PG_USER on ctxeco-db (input hidden):"
  read -s -p "Password: " PG_PASS
  echo ""
  if [ -z "$PG_PASS" ]; then
    echo "No password provided. Set POSTGRES_PASSWORD or enter at prompt."
    exit 1
  fi
fi

PG_PASS_ENC=$(printf '%s' "$PG_PASS" | urlencode_password)
echo "Updating ctxecokv ($CTXECO_KV)..."
az keyvault secret set --vault-name "$CTXECO_KV" --name postgres-password --value "$PG_PASS" --output none
ZEP_DSN="postgresql://${PG_USER}:${PG_PASS_ENC}@${PG_HOST}:5432/zep?sslmode=require"
POSTGRES_CS="postgresql://${PG_USER}:${PG_PASS_ENC}@${PG_HOST}:5432/${PG_DB_CTXECO}?sslmode=require"
az keyvault secret set --vault-name "$CTXECO_KV" --name zep-postgres-dsn --value "$ZEP_DSN" --output none
az keyvault secret set --vault-name "$CTXECO_KV" --name postgres-connection-string --value "$POSTGRES_CS" --output none
echo "  postgres-password, zep-postgres-dsn, postgres-connection-string updated."

echo "Forcing new Zep revision and scaling 0→1..."
az containerapp update -g "$CTXECO_RG" -n "$ZEP_APP" --revision-suffix "dsn-$(date +%s)" --output none
az containerapp update -g "$CTXECO_RG" -n "$ZEP_APP" --min-replicas 0 --max-replicas 2 --output none
az containerapp update -g "$CTXECO_RG" -n "$ZEP_APP" --min-replicas 1 --max-replicas 2 --output none
echo ""
echo "Done. Zep will start a new revision and pull the updated DSN from Key Vault."
echo "Check logs: az containerapp logs show -g $CTXECO_RG -n $ZEP_APP --tail 50"
