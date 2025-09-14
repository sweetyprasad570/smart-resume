@echo off
echo Copying video file to project directory...
echo.

REM Check if the video exists in Downloads
if exist "C:\Users\Lenovo\Downloads\background.mp4" (
    echo Found video in Downloads folder
    copy "C:\Users\Lenovo\Downloads\background.mp4" ".\background.mp4" /Y
    echo Video copied successfully!
) else (
    echo Video not found in Downloads folder.
    echo Please make sure your background.mp4 file is in:
    echo C:\Users\Lenovo\Downloads\
    echo.
    echo Or manually copy your video file to this directory:
    echo %CD%
)

echo.
echo Video location: %CD%\background.mp4
echo.
echo Press any key to exit...
pause > nul
