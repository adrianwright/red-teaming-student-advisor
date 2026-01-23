# PowerShell setup script for Red Teaming Framework
# Run this once to set up your Python environment

param(
    [switch]$Force  # Force recreate venv even if it exists
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Red Teaming Framework - Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "[1/4] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Python not found. Please install Python 3.10-3.13" -ForegroundColor Red
    exit 1
}
Write-Host "      Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
$venvPath = ".venv"
if ((Test-Path $venvPath) -and -not $Force) {
    Write-Host "[2/4] Virtual environment already exists at $venvPath" -ForegroundColor Green
    Write-Host "      Use -Force to recreate" -ForegroundColor Gray
} else {
    if (Test-Path $venvPath) {
        Write-Host "[2/4] Removing existing virtual environment..." -ForegroundColor Yellow
        Remove-Item $venvPath -Recurse -Force
    }
    Write-Host "[2/4] Creating virtual environment at $venvPath..." -ForegroundColor Yellow
    python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
    Write-Host "      Created successfully" -ForegroundColor Green
}

# Activate and install dependencies
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
& "$venvPath\Scripts\pip.exe" install -r requirements.txt --pre
Write-Host "      Dependencies installed" -ForegroundColor Green

# Check for .env file and populate from azd
Write-Host "[4/4] Configuring environment from Azure deployment..." -ForegroundColor Yellow

# Check if azd environment exists (filter out warnings)
$azdOutput = azd env get-values 2>&1 | Where-Object { $_ -notmatch '^WARNING:' }
$azdCheck = $azdOutput -join "`n"

if ($azdCheck -match 'AZURE_SUBSCRIPTION_ID') {
    # Parse azd env values
    $subscriptionId = ($azdCheck | Select-String 'AZURE_SUBSCRIPTION_ID="([^"]+)"').Matches.Groups[1].Value
    $resourceGroup = ($azdCheck | Select-String 'AZURE_RESOURCE_GROUP="([^"]+)"').Matches.Groups[1].Value
    $location = ($azdCheck | Select-String 'AZURE_LOCATION="([^"]+)"').Matches.Groups[1].Value
    
    if ($subscriptionId -and $resourceGroup) {
        # Get AI Services account name - filter warnings and get first line
        $azOutput = az resource list -g $resourceGroup --query "[?type=='Microsoft.CognitiveServices/accounts' && kind=='AIServices'].name" -o tsv 2>&1
        $aiAccount = ($azOutput | Where-Object { $_ -notmatch '^WARNING:' -and $_ -notmatch '^ERROR' -and $_.Trim() -ne '' } | Select-Object -First 1)
        
        if ($aiAccount -and $aiAccount.Trim() -ne '') {
            # Create .env file with real values
            $envContent = @"
# Azure Configuration
# Auto-populated from azd deployment: $resourceGroup

# Required for all scripts
AZURE_SUBSCRIPTION_ID=$subscriptionId
AZURE_RESOURCE_GROUP_NAME=$resourceGroup
AZURE_AI_PROJECT_ENDPOINT=https://$aiAccount.services.ai.azure.com/api/projects/project
AZURE_AI_MODEL_DEPLOYMENT_NAME=gpt-4.1
AZURE_AI_AGENT_NAME=StudentAdvisor
AZURE_LOCATION=$location

# PyRIT configuration (for demos)
OPENAI_CHAT_ENDPOINT=https://$aiAccount.cognitiveservices.azure.com/openai/v1
OPENAI_CHAT_MODEL=gpt-4.1
"@
            $envContent | Out-File -FilePath ".env" -Encoding UTF8 -Force
            Write-Host "      Created .env with deployed Azure resources" -ForegroundColor Green
            Write-Host "      Resource group: $resourceGroup" -ForegroundColor Gray
            Write-Host "      AI Services: $aiAccount" -ForegroundColor Gray
            
            # Create pyrit_tests/.env file
            $pyritEnvContent = @"
# Azure OpenAI Configuration (REQUIRED for PyRIT 0.10.0)
# Auto-populated from Azure deployment

# Your Azure OpenAI endpoint
OPENAI_CHAT_ENDPOINT=https://$aiAccount.cognitiveservices.azure.com/openai/v1

# Model deployment name
OPENAI_CHAT_MODEL=gpt-4.1

# GPT-4o deployment (for vision-aware multimodal tests)
OPENAI_VISION_MODEL=gpt-4o

# Azure region where your resources are deployed
AZURE_LOCATION=$location

# AI Foundry agent name
AZURE_AI_AGENT_NAME=StudentAdvisor
"@
            
            $pyritEnvContent | Out-File -FilePath "pyrit_tests\.env" -Encoding UTF8 -Force
            Write-Host "      Created pyrit_tests\.env for PyRIT demos" -ForegroundColor Green
        } else {
            Write-Host "      WARNING: Could not find AI Services account in $resourceGroup" -ForegroundColor Yellow
            if (Test-Path ".env.template") {
                Copy-Item ".env.template" ".env" -Force
                Write-Host "      Created .env from template - please fill in values manually" -ForegroundColor Yellow
            }
        }
    } else {
        Write-Host "      WARNING: Could not parse azd environment values" -ForegroundColor Yellow
        if (Test-Path ".env.template") {
            Copy-Item ".env.template" ".env" -Force
            Write-Host "      Created .env from template" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "      No azd deployment found" -ForegroundColor Yellow
    if (Test-Path ".env.template") {
        Copy-Item ".env.template" ".env" -Force
        Write-Host "      Created .env from template - run 'azd provision' first" -ForegroundColor Yellow
    } else {
        Write-Host "      WARNING: No .env.template found" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Activate the environment:" -ForegroundColor Gray
Write-Host "     .\.venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "  2. Configure .env with your Azure values" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Deploy infrastructure (if not done):" -ForegroundColor Gray
Write-Host "     azd provision" -ForegroundColor Cyan
Write-Host ""
Write-Host "  4. Run the chatbot:" -ForegroundColor Gray
Write-Host "     python chatbot.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  5. Run red teaming tests:" -ForegroundColor Gray
Write-Host "     cd pyrit_tests; python quickstart.py" -ForegroundColor Cyan
Write-Host ""
