# ASTRA Service Launcher
# This script starts all ASTRA microservices in separate PowerShell windows

Write-Host "🚀 Starting ASTRA - AI Security Assistant" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$pythonExe = "C:/Users/akesh/AppData/Local/Programs/Python/Python313/python.exe"
$projectRoot = "c:\Users\akesh\OneDrive\Desktop\Projects\Astra"

# Check if Python exists
if (-not (Test-Path $pythonExe)) {
    Write-Host "❌ Python not found at: $pythonExe" -ForegroundColor Red
    Write-Host "Please update the pythonExe variable in this script" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "✅ Python found" -ForegroundColor Green

# Function to start a service in a new window
function Start-Service {
    param(
        [string]$ServiceName,
        [string]$ServicePath,
        [string]$Port,
        [string]$MainFile = "main_local:app"
    )
    
    Write-Host "Starting $ServiceName on port $Port..." -ForegroundColor Yellow
    
    $servicePath = Join-Path $projectRoot $ServicePath
    $command = "cd '$servicePath'; $pythonExe -m uvicorn $MainFile --host 0.0.0.0 --port $Port --reload"
    
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $command
    Start-Sleep -Seconds 2
}

Write-Host ""
Write-Host "🔄 Launching services..." -ForegroundColor Cyan
Write-Host ""

# Start Gateway (Port 8000)
Start-Service -ServiceName "API Gateway" -ServicePath "backend\gateway" -Port "8000" -MainFile "main:app"

# Start NLP Service (Port 8001)
Start-Service -ServiceName "NLP Service" -ServicePath "backend\nlp_service" -Port "8001" -MainFile "main:app"

# Start SIEM Service (Port 8002)
Start-Service -ServiceName "SIEM Service" -ServicePath "backend\siem_service" -Port "8002"

# Start Reporting Service (Port 8003)
Start-Service -ServiceName "Reporting Service" -ServicePath "backend\reporting_service" -Port "8003"

# Start Blockchain Service (Port 8004)
Start-Service -ServiceName "Blockchain Service" -ServicePath "backend\blockchain_service" -Port "8004"

Write-Host ""
Write-Host "✅ All services started!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Service Status:" -ForegroundColor Cyan
Write-Host "  Gateway Service:     http://localhost:8000" -ForegroundColor White
Write-Host "  NLP Service:         http://localhost:8001" -ForegroundColor White
Write-Host "  SIEM Service:        http://localhost:8002" -ForegroundColor White
Write-Host "  Reporting Service:   http://localhost:8003" -ForegroundColor White
Write-Host "  Blockchain Service:  http://localhost:8004" -ForegroundColor White
Write-Host ""
Write-Host "🌐 Open the frontend:" -ForegroundColor Cyan
Write-Host "  File: $projectRoot\frontend\index.html" -ForegroundColor White
Write-Host ""
Write-Host "💡 Test queries:" -ForegroundColor Cyan
Write-Host "  - Show me failed login attempts" -ForegroundColor White
Write-Host "  - Initiate 'Ransomware Hunt'" -ForegroundColor White
Write-Host "  - Look for lateral movement" -ForegroundColor White
Write-Host "  - Generate an incident report" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  To stop all services, close all PowerShell windows" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Open frontend in default browser
$frontendPath = Join-Path $projectRoot "frontend\index.html"
Start-Process $frontendPath

Write-Host ""
Write-Host "🎉 ASTRA is ready! Happy investigating!" -ForegroundColor Green
Write-Host ""
