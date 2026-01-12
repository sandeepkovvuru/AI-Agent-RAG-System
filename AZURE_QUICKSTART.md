# Azure Deployment Quick Start Guide

This is the fastest way to deploy the AI Agent RAG System to Azure.

## Prerequisites

- Azure CLI installed: `curl https://aka.ms/InstallAzureCLIDeb | bash` (Linux/Mac) or download from Azure website (Windows)
- Active Azure subscription
- Azure OpenAI API key and endpoint
- Git installed

## One-Command Deployment

The easiest way to deploy is to run the automated deployment script:

```bash
# Clone the repository
git clone https://github.com/sandeepkovvuru/AI-Agent-RAG-System.git
cd AI-Agent-RAG-System

# Make the script executable
chmod +x deploy-azure.sh

# Run the deployment script
./deploy-azure.sh
```

The script will:
1. Create an Azure resource group
2. Create an App Service plan
3. Create a Python 3.10 Web App
4. Configure environment variables
5. Deploy your application
6. Display the public URL

## Manual Steps (Alternative)

If you prefer manual control:

```bash
# Login to Azure
az login

# Create resource group
az group create --name ai-agent-rg --location eastus

# Create App Service plan
az appservice plan create --name ai-agent-plan --resource-group ai-agent-rg --sku B1 --is-linux

# Create Web App
az webapp create --name ai-agent-rag --resource-group ai-agent-rg --plan ai-agent-plan --runtime "PYTHON|3.10"

# Configure settings
az webapp config appsettings set --name ai-agent-rag --resource-group ai-agent-rg --settings \
  AZURE_OPENAI_KEY="your-key" \
  AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/" \
  AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4"

# Deploy
az webapp up --name ai-agent-rag --resource-group ai-agent-rg
```

## Accessing Your Application

After deployment:

```bash
# View the URL
echo "https://ai-agent-rag.azurewebsites.net"

# API Documentation (Swagger UI)
https://ai-agent-rag.azurewebsites.net/docs

# Test the API
curl -X POST https://ai-agent-rag.azurewebsites.net/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the annual leave policy?"}'
```

## Monitoring & Logs

```bash
# View real-time logs
az webapp log tail --name ai-agent-rag --resource-group ai-agent-rg

# View application settings
az webapp config appsettings list --name ai-agent-rag --resource-group ai-agent-rg

# Restart the app
az webapp restart --name ai-agent-rag --resource-group ai-agent-rg
```

## Updating Configuration

```bash
# Update environment variables
az webapp config appsettings set --name ai-agent-rag --resource-group ai-agent-rg --settings \
  AZURE_OPENAI_KEY="new-key"

# Redeploy (after code changes)
az webapp up --name ai-agent-rag --resource-group ai-agent-rg
```

## Troubleshooting

### Application won't start
```bash
# Check logs
az webapp log tail --name ai-agent-rag --resource-group ai-agent-rg

# Restart app
az webapp restart --name ai-agent-rag --resource-group ai-agent-rg
```

### Azure OpenAI connection error
- Verify AZURE_OPENAI_KEY and AZURE_OPENAI_ENDPOINT are correct
- Check that API key has not expired
- Ensure API version matches: `2024-02-15-preview`

### Slow performance
- Upgrade to S1 tier: `az appservice plan update --sku S1`
- Check Azure OpenAI quota and rate limits

## Cost Optimization

- **B1 tier**: $13/month (good for dev/test)
- **S1 tier**: $75/month (recommended for production)
- **Premium tier**: Higher performance and SLA

## Clean Up

To delete all resources and stop incurring costs:

```bash
az group delete --name ai-agent-rg --yes --no-wait
```

## Continuous Deployment (CI/CD)

We have a GitHub Actions workflow set up. To enable:

1. Generate Azure credentials:
   ```bash
   az ad sp create-for-rbac --name ai-agent-rag --role contributor --sdk-auth
   ```

2. Add the output as a GitHub secret named `AZURE_CREDENTIALS`

3. Add `AZURE_APP_NAME` secret with your app name

Now, every push to main branch will automatically deploy!

## Support

For more detailed information, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive deployment guide
- [README.md](README.md) - Project documentation
- [Azure App Service docs](https://docs.microsoft.com/en-us/azure/app-service/)
