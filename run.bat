@echo off
REM Shopping Basket Extractor - Windows Launcher
REM This script runs the Flask web app locally

echo.
echo ========================================
echo  Shopping Basket Extractor
echo ========================================
echo.

cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -q -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Starting Shopping Basket Extractor...
echo.
echo Your browser will open automatically at http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.

start http://localhost:5000
python app.py

pause
