# Deploy Azure AI Foundry Infrastructure
param(
    [string]$ResourceGroupName = "rg-studentadvisor-dev",
    [string]$Location = "eastus"
)

Write-Host "Deploying Student Advisor Chatbot Infrastructure" -ForegroundColor Cyan

# Create resource group
Write-Host "Creating resource group: $ResourceGroupName" -ForegroundColor Yellow
az group create --name $ResourceGroupName --location $Location

# Deploy Bicep template
Write-Host "Deploying Azure AI Foundry resources..." -ForegroundColor Yellow
az deployment group create --resource-group $ResourceGroupName --template-file "./infra/main.bicep" --parameters "./infra/parameters.json" --output table

if ($LASTEXITCODE -eq 0) {
    Write-Host "Deployment completed successfully!" -ForegroundColor Green
    
    # Get deployment outputs
    $deployment = az deployment group show --resource-group $ResourceGroupName --name main --query properties.outputs --output json | ConvertFrom-Json
    
    Write-Host "`nDeployment Outputs:" -ForegroundColor Cyan
    Write-Host "  AI Hub Name: $($deployment.aiHubName.value)" -ForegroundColor White
    Write-Host "  AI Project Name: $($deployment.aiProjectName.value)" -ForegroundColor White
    Write-Host "  OpenAI Endpoint: $($deployment.openAIEndpoint.value)" -ForegroundColor White
    Write-Host "  Model Deployment: $($deployment.modelDeploymentName.value)" -ForegroundColor White
    
    Write-Host "`nSaving configuration to .env file..." -ForegroundColor Yellow
    
    $envContent = "# Azure Configuration`n"
    $envContent += "AZURE_SUBSCRIPTION_ID=$($deployment.subscriptionId.value)`n"
    $envContent += "AZURE_RESOURCE_GROUP_NAME=$($deployment.resourceGroupName.value)`n"
    $envContent += "AZURE_PROJECT_NAME=$($deployment.aiProjectName.value)`n"
    $envContent += "AZURE_OPENAI_ENDPOINT=$($deployment.openAIEndpoint.value)`n"
    $envContent += "AZURE_OPENAI_DEPLOYMENT=$($deployment.modelDeploymentName.value)`n"
    $envContent += "AZURE_LOCATION=$($deployment.location.value)`n"
    
    $envContent | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "Configuration saved to .env file" -ForegroundColor Green
    
    Write-Host "`nSetup complete! Run: python chatbot.py" -ForegroundColor Cyan
}
else {
    Write-Host "Deployment failed. Check error messages above." -ForegroundColor Red
    exit 1
}
