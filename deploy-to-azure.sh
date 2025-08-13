#!/bin/bash

# Azure deployment script for Visual AI Regression Module
# This script deploys the application to Azure App Service

# Configuration
RESOURCE_GROUP_NAME="visual-ai-regression-rg"
APP_NAME="visual-ai-regression-$(date +%Y%m%d%H%M%S)"
LOCATION="East US"
SKU="B2"  # Basic tier with more memory for image processing

echo "Starting deployment of Visual AI Regression Module to Azure App Service..."
echo "Resource Group: $RESOURCE_GROUP_NAME"
echo "App Name: $APP_NAME"
echo "Location: $LOCATION"

# Login to Azure (if not already logged in)
echo "Checking Azure login status..."
az account show > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Please login to Azure:"
    az login
fi

# Create resource group
echo "Creating resource group..."
az group create \
    --name $RESOURCE_GROUP_NAME \
    --location "$LOCATION"

# Deploy the ARM template
echo "Deploying Azure resources..."
az deployment group create \
    --resource-group $RESOURCE_GROUP_NAME \
    --template-file azure-template.json \
    --parameters appName=$APP_NAME location="$LOCATION" sku=$SKU

# Get the web app URL
WEB_APP_URL=$(az webapp show \
    --resource-group $RESOURCE_GROUP_NAME \
    --name $APP_NAME \
    --query defaultHostName \
    --output tsv)

echo "Configuring deployment source..."
# Set up deployment from local git
az webapp deployment source config-local-git \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP_NAME

# Get deployment credentials
DEPLOYMENT_USERNAME=$(az webapp deployment list-publishing-credentials \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP_NAME \
    --query publishingUserName \
    --output tsv)

echo "Setting up Git repository..."
# Initialize git repository if not exists
if [ ! -d ".git" ]; then
    git init
    git add .
    git commit -m "Initial commit for Visual AI Regression Module"
fi

# Add Azure remote
AZURE_GIT_URL="https://$DEPLOYMENT_USERNAME@$APP_NAME.scm.azurewebsites.net/$APP_NAME.git"
git remote remove azure 2>/dev/null
git remote add azure $AZURE_GIT_URL

echo "Deploying code to Azure..."
echo "You will be prompted for deployment credentials."
echo "Use the deployment username and password from the Azure portal."
git push azure main

echo ""
echo "=========================================="
echo "Deployment completed successfully!"
echo "=========================================="
echo "App Name: $APP_NAME"
echo "Resource Group: $RESOURCE_GROUP_NAME"
echo "Web App URL: https://$WEB_APP_URL"
echo ""
echo "Next steps:"
echo "1. Visit the web app URL to test the application"
echo "2. Upload baseline and current images for comparison"
echo "3. Configure any additional settings in the Azure portal"
echo ""
echo "To manage the app:"
echo "az webapp browse --name $APP_NAME --resource-group $RESOURCE_GROUP_NAME"
echo ""
echo "To view logs:"
echo "az webapp log tail --name $APP_NAME --resource-group $RESOURCE_GROUP_NAME"
