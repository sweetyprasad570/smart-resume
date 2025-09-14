@echo off
title Smart Resume Application Launcher
color 0A

echo ========================================
echo    Smart Resume Application Launcher
echo ========================================
echo.

REM Change to the correct directory
cd /d "%~dp0"

echo [INFO] Current directory: %CD%
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.7+ and try again.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python version:
python --version
echo.

REM Check if required files exist
if not exist "simple_app.py" (
    echo [ERROR] simple_app.py not found!
    echo Please make sure you're running this from the Smart Resume directory.
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo [WARNING] requirements.txt not found!
    echo Will try to start anyway...
    echo.
) else (
    echo [INFO] Installing/updating required packages...
    pip install -r requirements.txt
    echo.
)

echo [INFO] Starting Smart Resume Application...
echo.
echo ========================================
echo    APPLICATION READY!
echo ========================================
echo.
echo Your Smart Resume app is starting...
echo.
echo Access your application at:
echo   - Local:    http://localhost:5000
echo   - Network:  http://0.0.0.0:5000
echo.
echo Features available:
echo   - Resume Creation & Management
echo   - Job Browsing & Applications
echo   - User Dashboard
echo   - API Endpoints
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Flask application
python simple_app.py

echo.
echo [INFO] Application stopped.
pause
