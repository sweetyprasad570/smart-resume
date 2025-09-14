@echo off
title Test MongoDB Atlas Connection - Smart Resume
color 0A

echo ========================================
echo    Testing Smart Resume with MongoDB
echo ========================================
echo.

cd /d "%~dp0"

echo [INFO] Starting MongoDB Atlas application test...
echo.

echo [INFO] Configuration: MongoDB Atlas (fixed)
echo [INFO] Connection: smart-resume-jobmatch.iewebgp.mongodb.net
echo.

echo [TEST] Starting application for 10 seconds...
echo.

REM Start the app in the background and test endpoints
start /B python app.py > app_output.log 2>&1

echo [WAIT] Waiting for app to start...
timeout /t 5 /nobreak > nul

echo [TEST] Testing API endpoints...

REM Test the health endpoint
echo.
echo [TEST 1/3] Health Check:
curl -s http://localhost:5000/health || echo "   [ERROR] Health check failed"

echo.
echo [TEST 2/3] Database Connection:
curl -s http://localhost:5000/test-db || echo "   [ERROR] Database test failed"

echo.
echo [TEST 3/3] API Status:
curl -s http://localhost:5000/api/status || echo "   [ERROR] API status failed"

echo.
echo.
echo ========================================
echo          TEST RESULTS
echo ========================================

if exist app_output.log (
    echo [LOG] Application output:
    type app_output.log
    del app_output.log
)

echo.
echo [INFO] Stopping test application...
taskkill /F /IM python.exe /T > nul 2>&1

echo.
echo Test completed! 
echo.
echo If tests passed, use: start_full_app.bat
echo If tests failed, use:  start_smart_resume.bat
echo.
pause
