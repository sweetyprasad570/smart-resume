@echo off
title Smart Resume Setup
color 0E

echo ========================================
echo      Smart Resume Application Setup
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
    echo.
    echo Please install Python 3.7+ from: https://python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo [INFO] Python version:
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available!
    echo Please reinstall Python with pip included.
    echo.
    pause
    exit /b 1
)

echo [INFO] pip version:
pip --version
echo.

REM Upgrade pip
echo [INFO] Upgrading pip to latest version...
python -m pip install --upgrade pip
echo.

REM Install requirements
if exist "requirements.txt" (
    echo [INFO] Installing required packages from requirements.txt...
    pip install -r requirements.txt
    echo.
    
    if errorlevel 1 (
        echo [ERROR] Failed to install some packages!
        echo Trying to install core packages individually...
        echo.
        
        echo [INFO] Installing Flask...
        pip install Flask==2.3.3
        
        echo [INFO] Installing Flask-CORS...
        pip install Flask-CORS==4.0.0
        
        echo [INFO] Installing other core packages...
        pip install requests python-dotenv Werkzeug
        
        echo.
        echo [WARNING] Some packages might have failed to install.
        echo The simple app should still work with basic functionality.
    ) else (
        echo [SUCCESS] All packages installed successfully!
    )
) else (
    echo [WARNING] requirements.txt not found!
    echo Installing core packages manually...
    
    pip install Flask Flask-CORS requests python-dotenv Werkzeug
    echo.
)

echo ========================================
echo           SETUP COMPLETE!
echo ========================================
echo.
echo Your Smart Resume application is ready to use!
echo.
echo Available launchers:
echo   - start_smart_resume.bat  (Recommended - No database required)
echo   - start_full_app.bat      (Advanced - Requires MongoDB)
echo.
echo To start your application:
echo   1. Double-click "start_smart_resume.bat"
echo   2. Wait for the server to start
echo   3. Open http://localhost:5000 in your browser
echo.
echo Press any key to exit...
pause >nul
