@echo off
echo ========================================
echo    NEXUS AI - Quick Start (Fixed)
echo ========================================
echo.

REM Navigate to backend directory
cd /d "%~dp0backend"

REM Ensure agent_state directory exists
if not exist "agent_state" (
    echo Creating agent_state directory...
    mkdir agent_state
    echo ✅ Directory created
) else (
    echo ✅ agent_state directory exists
)

echo.
echo Starting backend server...
echo.

REM Start backend in this window
python app.py

pause
