@echo off
echo ===================================================
echo   Testing Fixed Window Capture
echo ===================================================
echo.

REM Check if venv exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
    echo Using system Python...
)

echo Running capture test...
python test_fixed_capture.py

pause
