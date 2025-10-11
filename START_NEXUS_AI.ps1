# Nexus AI - One-Click PowerShell Startup
# Starts Ollama, Backend, and Frontend automatically

$ErrorActionPreference = "Continue"

# Colors
$Host.UI.RawUI.BackgroundColor = "Black"
Clear-Host

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗     █████╗ ██╗" -ForegroundColor Magenta
Write-Host "    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██║" -ForegroundColor Magenta
Write-Host "    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ███████║██║" -ForegroundColor Magenta
Write-Host "    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔══██║██║" -ForegroundColor Magenta
Write-Host "    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║  ██║██║" -ForegroundColor Magenta
Write-Host "    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝" -ForegroundColor Magenta
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "         🚀 ONE-CLICK STARTUP - Starting Everything! 🚀" -ForegroundColor Yellow
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Step 1: Check/Start Ollama
Write-Host "[1/3] 🧠 Checking Ollama..." -ForegroundColor Blue
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -TimeoutSec 2 -ErrorAction Stop
    Write-Host "   ✅ Ollama is already running!" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Ollama is not running!" -ForegroundColor Yellow
    Write-Host "   🚀 Starting Ollama in new window..." -ForegroundColor Cyan
    Start-Process cmd -ArgumentList "/k", "title Ollama Server && color 0E && echo Starting Ollama... && ollama serve"
    Write-Host "   ⏳ Waiting 5 seconds for Ollama to start..." -ForegroundColor Cyan
    Start-Sleep -Seconds 5
}
Write-Host ""

# Step 2: Start Flask Backend
Write-Host "[2/3] 🔧 Starting Flask Backend Server..." -ForegroundColor Blue
$backendPath = Join-Path $scriptDir "backend"
$backendCmd = "title Nexus AI Backend - Keep This Open && color 0A && echo ════════════════════════════════════ && echo    NEXUS AI BACKEND SERVER && echo    http://localhost:5000 && echo    ⚠️  Keep this window OPEN! && echo ════════════════════════════════════ && echo. && cd /d `"$backendPath`" && python app.py"

Start-Process cmd -ArgumentList "/k", $backendCmd
Write-Host "   ✅ Backend server starting on http://localhost:5000" -ForegroundColor Green
Write-Host "   ⏳ Waiting 8 seconds for server to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 8

# Verify backend is running
try {
    $healthCheck = Invoke-RestMethod -Uri "http://localhost:5000/health" -TimeoutSec 3 -ErrorAction Stop
    Write-Host "   ✅ Backend is ready!" -ForegroundColor Green
} catch {
    Write-Host "   ⚠️  Backend is starting... (check backend window for status)" -ForegroundColor Yellow
}
Write-Host ""

# Step 3: Open Frontend
Write-Host "[3/3] 🌐 Opening Frontend Interface..." -ForegroundColor Blue
$frontendPath = Join-Path $scriptDir "frontend\index.html"
Start-Process $frontendPath
Write-Host "   ✅ Frontend opened in browser!" -ForegroundColor Green
Write-Host ""

# Final Status
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "                    ✅ NEXUS AI IS READY! ✅" -ForegroundColor Green -BackgroundColor Black
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "📊 Status:" -ForegroundColor Yellow
Write-Host "   🧠 Ollama Server   : " -NoNewline; Write-Host "Running" -ForegroundColor Green
Write-Host "   🔧 Backend API     : " -NoNewline; Write-Host "http://localhost:5000" -ForegroundColor Cyan -NoNewline; Write-Host " (in separate window)" -ForegroundColor White
Write-Host "   🌐 Frontend        : " -NoNewline; Write-Host "Opened in browser" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Important:" -ForegroundColor Yellow
Write-Host "   • Backend server window is now open (green/black window)"
Write-Host "   • " -NoNewline; Write-Host "⚠️  DO NOT CLOSE " -ForegroundColor Red -NoNewline; Write-Host "the backend window!"
Write-Host "   • The backend must stay running for Nexus AI to work"
Write-Host "   • You can minimize the backend window if needed"
Write-Host ""
Write-Host "🎉 Start asking questions in the browser!" -ForegroundColor Green
Write-Host ""
Write-Host "🛑 To stop Nexus AI:" -ForegroundColor Yellow
Write-Host "   • Close the backend server window"
Write-Host "   • Or press Ctrl+C in the backend window"
Write-Host ""
Write-Host "Press any key to close this startup window (backend will keep running)..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
