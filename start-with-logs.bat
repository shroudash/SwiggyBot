@echo off
echo.
echo 🚀 SwiggyBot with Live Gemini Logs
echo ================================
echo.

REM Clean processes
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1
timeout /t 2 /nobreak >nul

REM Create logs directory
if not exist logs mkdir logs

echo ▶ Starting Backend with full logging...
start "SwiggyBot Backend" powershell -NoExit -Command "cd backend; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 *>&1 | Tee-Object -FilePath '../logs/backend.log'"

timeout /t 5 /nobreak >nul

echo ▶ Starting Frontend...
start "SwiggyBot Frontend" cmd /k "cd frontend && npm start"

echo ▶ Starting Gemini Logs Monitor...
start "SwiggyBot Gemini Monitor" powershell -NoExit -Command "Write-Host '=== Live Gemini Logs ===' -ForegroundColor Green; Write-Host ''; Get-Content -Path 'logs/backend.log' -Wait -Tail 0 | Where-Object { $_ -match 'GEMINI|POST.*chat' } | ForEach-Object { $time = Get-Date -Format 'HH:mm:ss'; if ($_ -match 'GEMINI') { Write-Host \"[$time] $_\" -ForegroundColor Cyan } else { Write-Host \"[$time] Chat request\" -ForegroundColor Gray } }"

timeout /t 8 /nobreak >nul
start http://localhost:3000

echo.
echo ✅ SwiggyBot running with live Gemini monitoring!
echo 📱 Web: http://localhost:3000
echo 🔍 Watch the "SwiggyBot Gemini Monitor" window for AI calls
echo.
pause
