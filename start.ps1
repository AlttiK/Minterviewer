# Mock Interview Practice - Startup Script
# Run this script to start the backend server

Write-Host "🎯 Starting Mock Interview Practice Backend" -ForegroundColor Cyan
Write-Host ""

# Check if Ollama is installed
Write-Host "Checking dependencies..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version 2>&1
    Write-Host "✓ Ollama found: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama not found!" -ForegroundColor Red
    Write-Host "  Install from: https://ollama.ai/download" -ForegroundColor Yellow
    Write-Host "  Or run: winget install Ollama.Ollama" -ForegroundColor Yellow
    exit 1
}

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Install Python 3.10+ from: https://www.python.org/downloads/" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Check if Ollama is running
Write-Host "Checking Ollama service..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://localhost:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "✓ Ollama is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Ollama is not running!" -ForegroundColor Red
    Write-Host "  Starting Ollama..." -ForegroundColor Yellow
    Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Write-Host "  Waiting for Ollama to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 3
}

# Check if model is downloaded
Write-Host ""
Write-Host "Checking AI model..." -ForegroundColor Yellow
$models = ollama list
if ($models -like "*llama3.2*") {
    Write-Host "✓ llama3.2 model found" -ForegroundColor Green
} else {
    Write-Host "! llama3.2 model not found" -ForegroundColor Yellow
    Write-Host "  Downloading model (this may take a few minutes)..." -ForegroundColor Yellow
    ollama pull llama3.2:latest
}

# Navigate to backend directory
Write-Host ""
Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\backend"

# Check if virtual environment exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Install dependencies if needed
if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Start the server
Write-Host ""
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "  Backend server starting at http://localhost:8000" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Open Chrome and go to chrome://extensions/" -ForegroundColor White
Write-Host "  2. Enable 'Developer mode'" -ForegroundColor White
Write-Host "  3. Click 'Load unpacked'" -ForegroundColor White
Write-Host "  4. Select the 'chrome-extension' folder" -ForegroundColor White
Write-Host "  5. Click the 🎯 icon to start an interview!" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python app.py
