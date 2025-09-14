@echo off
title Smart Resume Database Integrity Checker
color 0C

echo ========================================
echo   Smart Resume Integrity Checker
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

REM Check if integrity checker exists
if not exist "check_database_integrity.py" (
    echo [ERROR] check_database_integrity.py not found!
    echo Please make sure you're running this from the Smart Resume directory.
    echo.
    pause
    exit /b 1
)

echo [INFO] Running database integrity check...
echo.
echo ========================================
echo    STARTING INTEGRITY CHECK
echo ========================================
echo.

REM Run the integrity checker
python check_database_integrity.py

echo.
echo ========================================
echo    INTEGRITY CHECK COMPLETE
echo ========================================
echo.

REM Check exit code
if errorlevel 1 (
    echo [WARNING] Integrity check found issues!
    echo Please review the results above and fix any problems.
) else (
    echo [SUCCESS] All integrity checks passed!
    echo Your Smart Resume application is healthy.
)

echo.
echo Press any key to exit...
pause >nul
