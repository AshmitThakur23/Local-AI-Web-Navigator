@echo off
echo ============================================
echo Starting Nexus AI with Local Web Server
echo ============================================
echo.
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Press Ctrl+C to stop
echo ============================================
echo.

cd "d:\Nexus AI\backend"
start "Nexus AI Backend" cmd /k "python app.py"

timeout /t 3 /nobreak >nul

cd "d:\Nexus AI\frontend"
start "Nexus AI Frontend" cmd /k "python -m http.server 8000"

timeout /t 2 /nobreak >nul

start "" "http://localhost:8000"
