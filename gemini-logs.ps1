# SwiggyBot Gemini Logs Monitor
Write-Host "=== SwiggyBot Gemini Logs (Live) ===" -ForegroundColor Green
Write-Host "Monitoring backend logs for [GEMINI] entries..." -ForegroundColor Yellow
Write-Host ""

# Create logs directory if it doesn't exist
if (!(Test-Path "logs")) { 
    New-Item -ItemType Directory -Path "logs" -Force | Out-Null 
}

# Create backend.log if it doesn't exist
$logPath = "logs/backend.log"
if (!(Test-Path $logPath)) { 
    Write-Host "Creating backend.log file..." -ForegroundColor Cyan
    New-Item -ItemType File -Path $logPath -Force | Out-Null
    Start-Sleep 2
}

Write-Host "Waiting for Gemini API calls..." -ForegroundColor Magenta
Write-Host "NOTE: Gemini logs appear in the backend console window." -ForegroundColor Yellow
Write-Host "This window shows when log entries are detected." -ForegroundColor Yellow
Write-Host ""

# Monitor the log file for Gemini-related entries
$lastSize = 0
while ($true) {
    Start-Sleep -Seconds 1
    
    if (Test-Path $logPath) {
        $content = Get-Content -Path $logPath -Raw
        if ($content -and $content.Length -gt $lastSize) {
            $newContent = $content.Substring($lastSize)
            $lines = $newContent -split "`n"
            
            foreach ($line in $lines) {
                if ($line -match "GEMINI") {
                    $time = Get-Date -Format "HH:mm:ss"
                    Write-Host "[$time] $line" -ForegroundColor Cyan
                }
                elseif ($line -match "INFO.*POST /chat") {
                    $time = Get-Date -Format "HH:mm:ss"
                    Write-Host "[$time] Chat request received" -ForegroundColor Gray
                }
            }
            
            $lastSize = $content.Length
        }
    }
    
    # Also show a heartbeat
    $time = Get-Date -Format "HH:mm:ss"
    Write-Host "[$time] Monitoring... (Ask a question in the web interface)" -ForegroundColor DarkGray
}
