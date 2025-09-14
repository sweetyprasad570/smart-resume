@echo off
title MongoDB Connection Fixer
color 0D

echo ========================================
echo     MongoDB Connection Troubleshooter
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

REM Check if fixer script exists
if not exist "fix_mongodb_connection.py" (
    echo [ERROR] fix_mongodb_connection.py not found!
    echo Please make sure you're running this from the Smart Resume directory.
    echo.
    pause
    exit /b 1
)

echo [INFO] Running MongoDB connection troubleshooter...
echo.
echo ========================================
echo    STARTING MONGODB DIAGNOSIS & FIX
echo ========================================
echo.

REM Run the MongoDB fixer
python fix_mongodb_connection.py

echo.
echo ========================================
echo    MONGODB TROUBLESHOOTING COMPLETE
echo ========================================
echo.

REM Check exit code
if errorlevel 1 (
    echo [INFO] MongoDB connection could not be fixed automatically.
    echo This is normal if you don't have MongoDB installed.
    echo.
    echo Recommendations:
    echo 1. Continue using simple mode: start_smart_resume.bat
    echo 2. Install local MongoDB for full functionality
    echo 3. Check your MongoDB Atlas credentials
) else (
    echo [SUCCESS] MongoDB connection has been fixed!
    echo You can now use the full application with: start_full_app.bat
)

echo.
echo Press any key to exit...
pause >nul
