#!/bin/bash
set -e

# Azure Migration Phase 3 Deployment Script
# Deploys ctxEco/frontend to ctxeco-web Static Web App

SWA_NAME="ctxeco-web"
RG_NAME="ctxeco-rg"
FRONTEND_PATH="../ctxEco/frontend"

echo "Checking if SWA resource exists..."
EXISTS=$(az resource list --resource-group $RG_NAME --name $SWA_NAME --resource-type Microsoft.Web/staticSites --query "length(@)" -o tsv)

if [ "$EXISTS" == "0" ]; then
  echo "Error: Static Web App '$SWA_NAME' not found in '$RG_NAME'. Run Phase 2 deployment first."
  exit 1
fi

echo "Fetching Deployment Token..."
TOKEN=$(az staticwebapp secrets list --name $SWA_NAME --resource-group $RG_NAME --query "properties.apiKey" -o tsv)

if [ -z "$TOKEN" ]; then
    echo "Error: Could not fetch deployment token."
    exit 1
fi

echo "Building Frontend in $FRONTEND_PATH..."
cd $FRONTEND_PATH || exit
npm install
npm run build

echo "Deploying to Azure Static Web App..."
# Assuming build output is in 'dist' (Vite default)
deployment_folder="./dist"
if [ -d "build" ]; then
    deployment_folder="./build"
fi

echo "Deploying from $deployment_folder..."
npx -y @azure/static-web-apps-cli deploy $deployment_folder --deployment-token $TOKEN --env production --app-name $SWA_NAME

echo "Phase 3 Deployment Complete."
