@echo off
cls
color 0A
echo ========================================
echo    NEXUS AI - ONE CLICK START (FIXED)
echo ========================================
echo.

REM Check if backend directory exists
if not exist "%~dp0backend" (
    echo ERROR: Backend directory not found!
    pause
    exit /b 1
)

REM Navigate to backend
cd /d "%~dp0backend"

REM Create agent_state directory if needed
if not exist "agent_state" (
    echo 📁 Creating agent_state directory...
    mkdir agent_state
    echo    ✅ Created successfully
) else (
    echo    ✅ agent_state directory exists
)

echo.
echo [1/2] 🔧 Starting Backend Server...
echo.

REM Start backend in new window
start "Nexus AI Backend - Keep This Open" cmd /k "color 0A && cd /d "%~dp0backend" && echo ════════════════════════════════════ && echo    NEXUS AI BACKEND SERVER && echo    http://localhost:5000 && echo    Keep this window OPEN && echo ════════════════════════════════════ && echo. && python app.py"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

echo    ✅ Backend started!
echo.
echo [2/2] 🌐 Opening Frontend...

REM Open frontend
cd /d "%~dp0frontend"
start "" index.html

echo    ✅ Frontend opened!
echo.
echo ════════════════════════════════════
echo    ✅ NEXUS AI IS READY!
echo ════════════════════════════════════
echo.
echo 📊 Status:
echo    🔧 Backend: http://localhost:5000
echo    🌐 Frontend: Opened in browser
echo.
echo ⚠️  IMPORTANT:
echo    • Keep the backend window open
echo    • Don't close the green terminal
echo.
echo 🎉 Start asking questions!
echo.
pause
