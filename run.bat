@echo off
echo.
echo 🚀 SwiggyBot - Single Terminal Runner
echo ===================================
echo.

REM Create logs directory
if not exist logs mkdir logs

REM Quick dependency check
echo 🔎 Checking dependencies...
cd backend
python -c "import fastapi, uvicorn, google.generativeai" 2>nul || (
    echo 📦 Installing backend deps...
    pip install -r requirements.txt >nul
)
cd ..

if not exist frontend\node_modules (
    echo 📦 Installing frontend deps...
    cd frontend
    npm install >nul 2>&1
    cd ..
)

echo.
echo ▶ Starting servers in THIS terminal...
echo.

REM Kill any processes on our ports
echo 🧹 Cleaning up existing servers...
for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr :8000 ^| findstr LISTENING 2^>nul') do (
    echo   Stopping process on port 8000 (PID: %%p)
    taskkill /F /PID %%p >nul 2>&1
)
for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr :3000 ^| findstr LISTENING 2^>nul') do (
    echo   Stopping process on port 3000 (PID: %%p)
    taskkill /F /PID %%p >nul 2>&1
)

REM Start backend with logging
echo [INFO] Starting backend server...
start /b cmd /c "cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 > ../logs/backend.log 2>&1"

REM Wait for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend with logging
echo [INFO] Starting frontend server...
start /b cmd /c "cd frontend && npm start > ../logs/frontend.log 2>&1"

REM Wait for frontend to compile
echo [INFO] Waiting for servers to start (10 seconds)...
timeout /t 10 /nobreak >nul

REM Open browser
echo 🌐 Opening http://localhost:3000...
start http://localhost:3000

echo.
echo 📜 Want to see Gemini logs in a separate window?
choice /c YN /m "Open Gemini logs window (Y/N)?"
if errorlevel 2 goto SHOW_STATUS

echo 🔍 Opening Gemini logs...
start powershell -NoExit -Command "Write-Host '=== Gemini Logs (Live) ==='; Get-Content -Path 'logs/backend.log' -Wait -Tail 10 | Where-Object { $_ -match 'GEMINI' }"

:SHOW_STATUS
echo.
echo ✅ SwiggyBot is running!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📜 Logs: logs/backend.log, logs/frontend.log
echo.
echo Press Ctrl+C to stop or any key to view live logs...
pause >nul

REM Show live backend logs with filtering
echo.
echo === Live Backend Logs (Press Ctrl+C to stop) ===
powershell -Command "Get-Content -Path 'logs/backend.log' -Wait -Tail 20"
