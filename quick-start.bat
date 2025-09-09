@echo off
echo.
echo 🚀 Quick SwiggyBot Start (3 Windows)
echo.

REM Clean processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Create logs directory
if not exist logs mkdir logs

echo ▶ Starting Backend...
start "Backend" cmd /k "cd backend && python -m uvicorn main:app --reload"

timeout /t 5 /nobreak >nul

echo ▶ Starting Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

echo ▶ Starting Gemini Monitor...
start "Gemini Logs" powershell -NoExit -ExecutionPolicy Bypass -File gemini-logs.ps1

timeout /t 8 /nobreak >nul
start http://localhost:3000

echo.
echo ✅ All started! 
echo 📱 http://localhost:3000
echo 🔍 Watch the Gemini logs window when you chat!
pause
