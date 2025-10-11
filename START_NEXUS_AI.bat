@echo off
echo ========================================
echo    Starting Nexus AI...
echo ========================================
echo.

REM Run PowerShell script with execution policy bypass
powershell.exe -ExecutionPolicy Bypass -File "%~dp0START_NEXUS_AI.ps1"

REM If PowerShell script fails, try batch version
if %errorlevel% neq 0 (
    echo.
    echo PowerShell script failed, using batch version...
    echo.
    goto BATCH_START
)

exit /b 0

:BATCH_START
color 0A
echo ════════════════════════════════════════════════════════════════
echo     ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗     █████╗ ██╗
echo     ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██║
echo     ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ███████║██║
echo     ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔══██║██║
echo     ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║  ██║██║
echo     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝
echo ════════════════════════════════════════════════════════════════
echo            🚀 ONE-CLICK STARTUP - Starting Everything! 🚀
echo ════════════════════════════════════════════════════════════════
echo.

REM Check if Ollama is running
echo [1/3] 🧠 Checking Ollama...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo    ⚠️  Ollama is not running!
    echo    🚀 Starting Ollama in new window...
    start "Ollama Server" cmd /k "echo Starting Ollama... && ollama serve"
    echo    ⏳ Waiting 5 seconds for Ollama to start...
    timeout /t 5 /nobreak >nul
) else (
    echo    ✅ Ollama is already running!
)
echo.

REM Start Flask Backend
echo [2/3] 🔧 Starting Flask Backend Server...
cd /d "%~dp0backend"
start "Nexus AI Backend - Keep This Open" cmd /k "color 0A && echo ════════════════════════════════════ && echo    NEXUS AI BACKEND SERVER && echo    http://localhost:5000 && echo    Keep this window OPEN && echo ════════════════════════════════════ && echo. && python app.py"
echo    ✅ Backend server starting on http://localhost:5000
echo    ⏳ Waiting 5 seconds for server to initialize...
timeout /t 5 /nobreak >nul
echo.

REM Open Frontend
echo [3/3] 🌐 Opening Frontend Interface...
cd /d "%~dp0frontend"
start "" index.html
echo    ✅ Frontend opened in browser!
echo.

echo ════════════════════════════════════════════════════════════════
echo                    ✅ NEXUS AI IS READY! ✅
echo ════════════════════════════════════════════════════════════════
echo.
echo 📊 Status:
echo    🧠 Ollama Server   : Running
echo    🔧 Backend API     : http://localhost:5000 (Running in separate window)
echo    🌐 Frontend        : Opened in browser
echo.
echo 💡 Important:
echo    • Backend server window is now open (green text)
echo    • ⚠️  DO NOT CLOSE the backend window!
echo    • The backend must stay running for Nexus AI to work
echo    • You can minimize the backend window if needed
echo.
echo 🎉 Start asking questions in the browser!
echo.
echo 🛑 To stop Nexus AI:
echo    • Close the backend server window
echo    • Or press Ctrl+C in the backend window
echo.
pause
