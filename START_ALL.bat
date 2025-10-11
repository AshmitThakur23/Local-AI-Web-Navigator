@echo off
echo ========================================
echo Starting Nexus AI - Complete Application
echo ========================================
echo.

echo Starting Backend Server...
start "Nexus AI Backend" cmd /k "cd /d %~dp0backend && python app.py"

echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

echo Opening Frontend Pages...
start "" "%~dp0frontend\index.html"
timeout /t 1 /nobreak >nul
start "" "%~dp0frontend\table_view.html"
timeout /t 1 /nobreak >nul
start "" "%~dp0frontend\scraper.html"

echo.
echo ========================================
echo Nexus AI is now running!
echo ========================================
echo Backend: http://localhost:5000
echo.
echo Close the Backend window to stop the server.
echo Press any key to exit this launcher...
pause >nul
