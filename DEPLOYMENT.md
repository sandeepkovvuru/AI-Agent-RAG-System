# Azure Deployment Guide

This guide provides step-by-step instructions for deploying the AI Agent RAG System to Azure.

## Option 1: Azure App Service (Recommended for Web Apps)

### Prerequisites
- Azure CLI installed (`az` command)
- An active Azure subscription
- Appropriate Azure permissions to create resources

### Steps

1. **Clone and navigate to the repository**:
```bash
git clone https://github.com/yourusername/AI-Agent-RAG-System.git
cd AI-Agent-RAG-System
```

2. **Set variables**:
```bash
RESOURCE_GROUP="ai-agent-rg"
LOCATION="eastus"
APP_SERVICE_PLAN="ai-agent-plan"
WEB_APP_NAME="ai-agent-rag-$(date +%s)"
```

3. **Create a resource group**:
```bash
az group create --name $RESOURCE_GROUP --location $LOCATION
```

4. **Create an App Service Plan**:
```bash
az appservice plan create \
  --name $APP_SERVICE_PLAN \
  --resource-group $RESOURCE_GROUP \
  --sku B1 \
  --is-linux
```

5. **Create a Web App with Python runtime**:
```bash
az webapp create \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --plan $APP_SERVICE_PLAN \
  --runtime "PYTHON|3.10"
```

6. **Configure Azure OpenAI credentials**:
```bash
az webapp config appsettings set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings \
    AZURE_OPENAI_KEY="your-azure-openai-key" \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4" \
    ENVIRONMENT="production"
```

7. **Deploy the application**:
```bash
az webapp up \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --runtime PYTHON:3.10
```

8. **Access your application**:
```bash
echo "https://$WEB_APP_NAME.azurewebsites.net"
```

## Option 2: Azure Container Instances (Docker)

### Prerequisites
- Docker installed
- Azure Container Registry (ACR) account
- Azure CLI

### Steps

1. **Build and push Docker image**:
```bash
# Login to ACR
az acr login --name <your-acr-name>

# Build and push
az acr build \
  --registry <your-acr-name> \
  --image ai-agent-rag:latest .
```

2. **Create Container Instance**:
```bash
az container create \
  --resource-group $RESOURCE_GROUP \
  --name ai-agent-container \
  --image <your-acr-name>.azurecr.io/ai-agent-rag:latest \
  --ports 8000 \
  --environment-variables \
    AZURE_OPENAI_KEY="your-key" \
    AZURE_OPENAI_ENDPOINT="your-endpoint" \
  --registry-login-server <your-acr-name>.azurecr.io \
  --registry-username <your-acr-username> \
  --registry-password <your-acr-password>
```

## Option 3: Azure Functions

### Prerequisites
- Azure Functions Core Tools
- Azure CLI

### Steps

1. **Create Function App**:
```bash
az functionapp create \
  --resource-group $RESOURCE_GROUP \
  --consumption-plan-location $LOCATION \
  --name ai-agent-functions \
  --storage-account <your-storage-account> \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4
```

2. **Deploy using Func CLI**:
```bash
func azure functionapp publish <function-app-name>
```

## Configuration Management

### Using Azure Key Vault

1. **Create Key Vault**:
```bash
az keyvault create \
  --name ai-agent-kv \
  --resource-group $RESOURCE_GROUP
```

2. **Add secrets**:
```bash
az keyvault secret set \
  --vault-name ai-agent-kv \
  --name AZURE-OPENAI-KEY \
  --value "your-api-key"

az keyvault secret set \
  --vault-name ai-agent-kv \
  --name AZURE-OPENAI-ENDPOINT \
  --value "your-endpoint"
```

3. **Grant access to App Service**:
```bash
az keyvault set-policy \
  --name ai-agent-kv \
  --object-id <app-service-principal-id> \
  --secret-permissions get list
```

## Monitoring and Logging

### Application Insights

1. **Create Application Insights resource**:
```bash
az monitor app-insights component create \
  --app ai-agent-insights \
  --location $LOCATION \
  --resource-group $RESOURCE_GROUP
```

2. **Configure for your App Service**:
```bash
az webapp config appsettings set \
  --name $WEB_APP_NAME \
  --resource-group $RESOURCE_GROUP \
  --settings APPINSIGHTS_INSTRUMENTATIONKEY="<instrumentation-key>"
```

## Cleanup

To remove all resources:
```bash
az group delete --name $RESOURCE_GROUP --yes --no-wait
```

## Troubleshooting

### Application won't start
- Check logs: `az webapp log tail --name $WEB_APP_NAME --resource-group $RESOURCE_GROUP`
- Verify environment variables are set correctly
- Ensure Python dependencies are installed

### Azure OpenAI connection fails
- Verify API key and endpoint in Key Vault or App Settings
- Check network connectivity and firewall rules
- Ensure API version matches your deployment

### Performance issues
- Scale up the App Service Plan (B1 -> S1)
- Enable application insights for monitoring
- Check Azure OpenAI rate limits

## Next Steps

1. Set up continuous deployment from GitHub
2. Configure auto-scaling based on traffic
3. Implement Azure Application Insights for monitoring
4. Set up backup and disaster recovery
