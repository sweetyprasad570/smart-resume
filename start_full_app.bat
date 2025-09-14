@echo off
title Smart Resume Full Application Launcher
color 0B

echo ========================================
echo  Smart Resume Full Application Launcher
echo     (Requires MongoDB Database)
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
if not exist "app.py" (
    echo [ERROR] app.py not found!
    echo Please make sure you're running this from the Smart Resume directory.
    echo.
    pause
    exit /b 1
)

echo [INFO] Installing/updating required packages...
pip install -r requirements.txt
echo.

echo [WARNING] This version requires MongoDB to be installed and running!
echo If you don't have MongoDB, use "start_smart_resume.bat" instead.
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.

echo [INFO] Starting Full Smart Resume Application...
echo.
echo ========================================
echo    FULL APPLICATION READY!
echo ========================================
echo.
echo Your Smart Resume app is starting...
echo.
echo Access your application at:
echo   - Local:    http://localhost:5000
echo   - Network:  http://0.0.0.0:5000
echo.
echo Features available:
echo   - Complete Database Integration
echo   - User Authentication (JWT)
echo   - Resume Management
echo   - Job Management
echo   - User Profiles
echo   - API Endpoints
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

REM Start the Flask application
python app.py

echo.
echo [INFO] Application stopped.
pause
