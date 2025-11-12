@echo off
echo ========================================
echo  Simple Batch Screen Capture
echo ========================================
echo.

REM Check if we have a virtual environment
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    echo.
) else (
    echo Warning: No virtual environment found
    echo Using system Python installation...
    echo.
)

echo Prerequisites Check:
echo   - scrcpy must be running with Android device
echo   - Kindle app open on starting page
echo   - ADB connection established
echo.

echo Running simple batch capture tool...
echo.
python simple_batch_capture.py

echo.
echo ========================================
echo  Batch capture finished
echo ========================================
pause