@echo off
echo ============================================
echo Starting Nexus AI with NVIDIA GPU
echo ============================================
echo.
echo GPU: NVIDIA (GPU 1) - Moderate Load
echo Backend: http://localhost:5000
echo Frontend: http://localhost:8000
echo Target Response Time: 30 seconds or less
echo.
echo ============================================
echo.

REM Set NVIDIA GPU
set CUDA_VISIBLE_DEVICES=1

REM Start Backend
cd "d:\Nexus AI\backend"
start "Nexus AI Backend (NVIDIA)" cmd /k "set CUDA_VISIBLE_DEVICES=1 && python app.py"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start Frontend
cd "d:\Nexus AI\frontend"
start "Nexus AI Frontend" cmd /k "python -m http.server 8000"

REM Wait for frontend to start
timeout /t 2 /nobreak >nul

REM Open browser
start "" "http://localhost:8000"

echo.
echo ============================================
echo All services started!
echo ============================================
