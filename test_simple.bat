@echo off
echo ========================================
echo  Testing Simple Capture Setup  
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

echo This will test:
echo   [1] Required Python packages
echo   [2] ADB connection to Android device  
echo   [3] Window capture functionality
echo.
echo Make sure scrcpy is running before the test!
echo.

python test_simple_capture.py

pause