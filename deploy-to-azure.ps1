# Azure deployment script for Visual AI Regression Module (PowerShell)
# This script deploys the application to Azure App Service

# Configuration
$ResourceGroupName = "visual-ai-regression-rg"
$AppName = "visual-ai-regression-$(Get-Date -Format 'yyyyMMddHHmmss')"
$Location = "East US"
$Sku = "B2"  # Basic tier with more memory for image processing

Write-Host "Starting deployment of Visual AI Regression Module to Azure App Service..." -ForegroundColor Green
Write-Host "Resource Group: $ResourceGroupName"
Write-Host "App Name: $AppName"
Write-Host "Location: $Location"

# Check if Azure CLI is installed
try {
    az --version | Out-Null
} catch {
    Write-Error "Azure CLI is not installed. Please install it from https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Login to Azure (if not already logged in)
Write-Host "Checking Azure login status..." -ForegroundColor Yellow
$loginStatus = az account show 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Please login to Azure:" -ForegroundColor Yellow
    az login
}

# Create resource group
Write-Host "Creating resource group..." -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location

# Deploy the ARM template
Write-Host "Deploying Azure resources..." -ForegroundColor Yellow
az deployment group create `
    --resource-group $ResourceGroupName `
    --template-file azure-template.json `
    --parameters appName=$AppName location=$Location sku=$Sku

# Get the web app URL
$WebAppUrl = az webapp show `
    --resource-group $ResourceGroupName `
    --name $AppName `
    --query defaultHostName `
    --output tsv

Write-Host "Configuring deployment source..." -ForegroundColor Yellow
# Set up deployment from local git
az webapp deployment source config-local-git `
    --name $AppName `
    --resource-group $ResourceGroupName

# Get deployment credentials
$DeploymentUsername = az webapp deployment list-publishing-credentials `
    --name $AppName `
    --resource-group $ResourceGroupName `
    --query publishingUserName `
    --output tsv

Write-Host "Setting up Git repository..." -ForegroundColor Yellow
# Initialize git repository if not exists
if (-not (Test-Path ".git")) {
    git init
    git add .
    git commit -m "Initial commit for Visual AI Regression Module"
}

# Add Azure remote
$AzureGitUrl = "https://$DeploymentUsername@$AppName.scm.azurewebsites.net/$AppName.git"
git remote remove azure 2>$null
git remote add azure $AzureGitUrl

Write-Host "Deploying code to Azure..." -ForegroundColor Yellow
Write-Host "You will be prompted for deployment credentials." -ForegroundColor Cyan
Write-Host "Use the deployment username and password from the Azure portal." -ForegroundColor Cyan
git push azure main

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "App Name: $AppName"
Write-Host "Resource Group: $ResourceGroupName"
Write-Host "Web App URL: https://$WebAppUrl"
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Visit the web app URL to test the application"
Write-Host "2. Upload baseline and current images for comparison"
Write-Host "3. Configure any additional settings in the Azure portal"
Write-Host ""
Write-Host "To manage the app:" -ForegroundColor Yellow
Write-Host "az webapp browse --name $AppName --resource-group $ResourceGroupName"
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "az webapp log tail --name $AppName --resource-group $ResourceGroupName"
