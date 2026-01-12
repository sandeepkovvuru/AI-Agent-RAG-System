#!/bin/bash

# Azure Deployment Script for AI Agent RAG System
# This script automates the deployment of the AI Agent to Azure App Service

set -e

echo "========================================"
echo "AI Agent RAG System - Azure Deployment"
echo "========================================"
echo ""

# Variables
RESOURCE_GROUP="ai-agent-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="ai-agent-plan"
WEB_APP_NAME="ai-agent-rag-$(date +%s)"
REPO_URL="https://github.com/sandeepkovvuru/AI-Agent-RAG-System.git"

echo "Setting variables:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  App Service Plan: $APP_SERVICE_PLAN"
echo "  Web App Name: $WEB_APP_NAME"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "Error: Azure CLI is not installed. Please install it first."
    exit 1
fi

echo "Step 1: Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION
echo "✓ Resource group created"
echo ""

echo "Step 2: Creating App Service Plan..."
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux
echo "✓ App Service Plan created"
echo ""

echo "Step 3: Creating Web App..."
az webapp create \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON|3.10"
echo "✓ Web App created"
echo ""

echo "Step 4: Configuring deployment..."
az webapp config appsettings set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AZURE_OPENAI_KEY="your-azure-openai-key" \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4" \
    ENVIRONMENT="production" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=true
echo "✓ App Settings configured"
echo ""

echo "Step 5: Deploying application..."
az webapp up \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION
echo "✓ Application deployed"
echo ""

echo "========================================"
echo "Deployment Complete!"
echo "========================================"
echo "Web App URL: https://$WEB_APP_NAME.azurewebsites.net"
echo ""
echo "IMPORTANT: Update these Azure App Settings with your actual values:"
echo "  - AZURE_OPENAI_KEY: Your Azure OpenAI API key"
echo "  - AZURE_OPENAI_ENDPOINT: Your Azure OpenAI endpoint URL"
echo ""
echo "To update settings manually:"
echo "  az webapp config appsettings set --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP --settings AZURE_OPENAI_KEY=your-key AZURE_OPENAI_ENDPOINT=your-endpoint"
echo ""
echo "To view application logs:"
echo "  az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP"
echo ""
echo "To delete all resources:"
echo "  az group delete --name $RESOURCE_GROUP --yes --no-wait"
echo ""
