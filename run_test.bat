@echo off
REM System Test and Verification Script

echo.
echo ========================================
echo  Kindle Capture System Test
echo ========================================
echo.
echo This will verify:
echo  - Python packages installed
echo  - External tools (ADB, Tesseract, scrcpy)
echo  - Device connection
echo  - OCR functionality
echo.

python test_system.py

echo.
pause
