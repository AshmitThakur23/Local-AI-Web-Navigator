@echo off
echo ========================================
echo    Opening Nexus AI Frontend
echo ========================================
echo.

cd /d "%~dp0frontend"

echo Opening index.html in your default browser...
start index.html

echo.
echo ✅ Frontend opened!
echo.
echo Make sure the backend is running on http://localhost:5000
echo If not, run start_backend.bat first
echo.
pause
