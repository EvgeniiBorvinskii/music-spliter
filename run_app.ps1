# Music Splitter - PowerShell Launcher
Write-Host "Music Splitter - Starting Application..." -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if Python is available
try {
    $pythonVersion = python --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the main application
try {
    python main.py
} catch {
    Write-Host "❌ Error running application: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Application ended with an error." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
}
