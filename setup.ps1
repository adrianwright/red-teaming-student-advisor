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
& "$venvPath\Scripts\pip.exe" install --upgrade pip | Out-Null
& "$venvPath\Scripts\pip.exe" install -r requirements.txt --pre
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    exit 1
}
Write-Host "      Dependencies installed" -ForegroundColor Green

# Check for .env file
Write-Host "[4/4] Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.template") {
        Copy-Item ".env.template" ".env"
        Write-Host "      Created .env from template - please fill in your values" -ForegroundColor Yellow
    } else {
        Write-Host "      WARNING: No .env file found" -ForegroundColor Yellow
    }
} else {
    Write-Host "      .env file exists" -ForegroundColor Green
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
