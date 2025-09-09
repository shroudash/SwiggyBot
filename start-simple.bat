@echo off
echo.
echo 🚀 Starting SwiggyBot...
echo.

REM Clean up any existing processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Start backend in new window with logging
echo ▶ Starting backend (port 8000)...
start "SwiggyBot Backend" powershell -NoExit -Command "cd backend; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 --log-level info *>&1 | Tee-Object -FilePath '../logs/backend.log'"

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in new window  
echo ▶ Starting frontend (port 3000)...
start "SwiggyBot Frontend" cmd /k "cd frontend && npm start"

REM Create logs directory if it doesn't exist
if not exist logs mkdir logs

REM Wait for backend to generate some logs
timeout /t 8 /nobreak >nul

REM Start Gemini logs window
echo 🔍 Starting Gemini logs monitor...
start "SwiggyBot Gemini Logs" powershell -NoExit -ExecutionPolicy Bypass -File gemini-logs.ps1

REM Wait a moment then open browser
timeout /t 3 /nobreak >nul
echo 🌐 Opening browser...
start http://localhost:3000

echo.
echo ✅ SwiggyBot is running with 3 windows:
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000  
echo 🔍 Gemini Logs: Real-time AI monitoring
echo.
echo Try asking: "How many burgers are left?" to see Gemini in action!
echo.
pause
