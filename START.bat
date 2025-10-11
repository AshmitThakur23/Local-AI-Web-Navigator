@echo off
color 0B
cls
echo ═══════════════════════════════════════════════════════════════
echo     ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗     █████╗ ██╗
echo     ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝    ██╔══██╗██║
echo     ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗    ███████║██║
echo     ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║    ██╔══██║██║
echo     ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║    ██║  ██║██║
echo     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝
echo ═══════════════════════════════════════════════════════════════
echo          🚀 STARTING EVERYTHING - ONE COMMAND! 🚀
echo ═══════════════════════════════════════════════════════════════
echo.

REM Kill any old Python processes to avoid conflicts
echo [0/3] 🧹 Cleaning up old processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 1 /nobreak >nul
echo    ✅ Cleanup done
echo.

REM Check if Ollama is running, start if not
echo [1/3] 🧠 Checking Ollama...
curl -s http://127.0.0.1:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo    ⚠️  Ollama is not running!
    echo    🚀 Starting Ollama in background...
    start /min "Ollama Server" cmd /k "title Ollama Server && color 0E && ollama serve"
    echo    ⏳ Waiting 5 seconds for Ollama to start...
    timeout /t 5 /nobreak >nul
    echo    ✅ Ollama started!
) else (
    echo    ✅ Ollama is already running!
)
echo.

REM Start Flask Backend in new window
echo [2/3] 🔧 Starting Backend Server...
cd /d "%~dp0backend"
start "Nexus AI Backend - KEEP THIS OPEN" cmd /k "color 0A && title Nexus AI Backend - KEEP THIS OPEN && echo ════════════════════════════════════ && echo    NEXUS AI BACKEND SERVER && echo    http://localhost:5000 && echo. && echo    ⚠️  KEEP THIS WINDOW OPEN! && echo    Backend will stay running && echo    You can search multiple times && echo ════════════════════════════════════ && echo. && python app.py"
echo    ✅ Backend starting at http://localhost:5000
echo    ⏳ Waiting 8 seconds for server to start...
timeout /t 8 /nobreak >nul
echo.

REM Verify backend is running
curl -s http://localhost:5000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Backend is ready and responding!
) else (
    echo    ⚠️  Backend is starting... (check backend window)
)
echo.

REM Open Frontend in browser
echo [3/3] 🌐 Opening Frontend...
cd /d "%~dp0frontend"
start "" index.html
echo    ✅ Frontend opened in browser!
echo.

REM Final instructions
cls
color 0A
echo ═══════════════════════════════════════════════════════════════
echo                    ✅ NEXUS AI IS READY! ✅
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📊 Status:
echo    🧠 Ollama Server   : Running
echo    🔧 Backend API     : http://localhost:5000 (in separate window)
echo    🌐 Frontend        : Opened in browser
echo.
echo ═══════════════════════════════════════════════════════════════
echo                    ⚡ IMPORTANT INSTRUCTIONS ⚡
echo ═══════════════════════════════════════════════════════════════
echo.
echo ✅ BACKEND IS NOW RUNNING!
echo    • A GREEN window titled "Nexus AI Backend" is now open
echo    • ⚠️  DO NOT CLOSE that window!
echo    • Backend will stay running - search as many times as you want!
echo.
echo ✅ HOW TO USE:
echo    1. Go to the browser (already opened)
echo    2. Type your question in the chat box
echo    3. Click Send button
echo    4. Get answer!
echo    5. Ask another question (no need to restart!)
echo    6. Keep asking questions - backend stays running!
echo.
echo ✅ MULTIPLE SEARCHES:
echo    • Backend is PERSISTENT - stays running
echo    • Search → Get Answer → Search Again!
echo    • No need to come back here and run commands
echo    • Just keep using the browser!
echo.
echo 🛑 TO STOP NEXUS AI:
echo    • Close the GREEN backend window
echo    • Or press Ctrl+C in backend window
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🎉 Start asking questions in your browser NOW!
echo.
echo Press any key to close this window (backend keeps running)...
pause >nul
