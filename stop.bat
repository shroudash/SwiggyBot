@echo off
echo.
echo 🛑 Stopping SwiggyBot servers...
echo.

REM Kill processes using ports 8000 and 3000
for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process on port 8000 (PID: %%p)
    taskkill /F /PID %%p >nul 2>&1
)

for /f "tokens=5" %%p in ('netstat -ano 2^>nul ^| findstr :3000 ^| findstr LISTENING') do (
    echo Killing process on port 3000 (PID: %%p)
    taskkill /F /PID %%p >nul 2>&1
)

echo.
echo ✅ SwiggyBot servers stopped.
echo.
pause
