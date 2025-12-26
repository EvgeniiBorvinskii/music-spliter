@echo off
echo Music Splitter - Starting Application...
echo =====================================

REM Use the full Python path
set PYTHON_PATH=C:\Users\KeyWest\AppData\Local\Programs\Python\Python313\python.exe

REM Check if Python exists
if not exist "%PYTHON_PATH%" (
    echo Error: Python not found at %PYTHON_PATH%
    echo Trying to find Python in PATH...
    python --version >nul 2>&1
    if errorlevel 1 (
        echo Error: Python is not installed or not in PATH
        echo Please install Python 3.8 or higher from https://python.org
        pause
        exit /b 1
    )
    set PYTHON_PATH=python
)

REM Run the main application
echo Starting Music Splitter GUI...
"%PYTHON_PATH%" main.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application ended with an error.
    pause
)
