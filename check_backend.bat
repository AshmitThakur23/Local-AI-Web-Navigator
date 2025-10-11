@echo off
echo Viewing Backend Logs...
echo Press Ctrl+C to stop
echo.
tasklist | findstr python
echo.
netstat -ano | findstr :5000
