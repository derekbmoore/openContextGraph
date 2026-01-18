#!/bin/bash
# Manual Deployment / Force Update Script
# Usage: ./scripts/manual_deploy.sh

APP_NAME="ctxeco-api"
WORKER_NAME="ctxeco-worker"
RESOURCE_GROUP="ctxeco-rg"
IMAGE="ghcr.io/derekbmoore/opencontextgraph/backend:latest"

echo "============================================="
echo "Force Updating Azure Container Apps"
echo "Apps: $APP_NAME, $WORKER_NAME"
echo "Group: $RESOURCE_GROUP"
echo "Image: $IMAGE"
echo "============================================="

# Login check
if ! az account show > /dev/null 2>&1; then
    echo "⚠️  Please login to Azure first: 'az login'"
    exit 1
fi

echo "🚀 sending update command for API..."

# Update API
az containerapp update \
  --name "$APP_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --image "$IMAGE"

echo "🚀 sending update command for Worker..."

# Update Worker
az containerapp update \
  --name "$WORKER_NAME" \
  --resource-group "$RESOURCE_GROUP" \
  --image "$IMAGE"


echo "✅ Update initiated. The new revision should be provisioning."
echo "   Monitor status with: az containerapp revision list -n $APP_NAME -g $RESOURCE_GROUP -o table"
