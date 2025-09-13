@echo off
color 0A
title AarogyaLink - Starting Backend Server
echo ========================================
echo   Starting AarogyaLink Backend Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ and try again.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python version:
python --version
echo.

REM Check if .env file exists
if not exist .env (
    echo [WARNING] .env file not found!
    echo Please create .env file with your API keys
    echo See .env.example for reference
    echo.
)

REM Check if required files exist
if not exist app.py (
    echo [ERROR] app.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

if not exist run.py (
    echo [ERROR] run.py not found!
    echo Make sure you're running this from the correct directory.
    pause
    exit /b 1
)

REM Check if required Python packages are installed
echo [INFO] Checking required packages...
python -c "import flask, requests, google.generativeai, PIL, dotenv" 2>nul
if %errorLevel% neq 0 (
    echo [WARNING] Some required packages may be missing!
    echo Installing required packages...
    pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to install packages!
        echo Please run: pip install -r requirements.txt
        pause
        exit /b 1
    )
)

REM Start the Flask server with auto-browser opening
echo [INFO] Starting server with auto-browser opening...
echo [INFO] Microsoft Edge will open automatically...
echo [INFO] Press Ctrl+C to stop the server
echo ========================================
python run.py

REM Check exit code
if %errorLevel% neq 0 (
    echo.
    echo [ERROR] Server failed to start! Error code: %errorLevel%
    echo.
    echo Common solutions:
    echo 1. Check if port 5000 is already in use
    echo 2. Verify your .env file configuration
    echo 3. Ensure all dependencies are installed
    echo 4. Check the error messages above
    echo.
else (
    echo.
    echo [INFO] Server stopped successfully.
)

pause