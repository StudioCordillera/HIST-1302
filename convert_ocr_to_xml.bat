@echo off
REM OCR to XML Batch Conversion Script
REM =====================================

echo.
echo ========================================
echo  OCR to XML Conversion for CH21-24
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

echo [1/4] Checking dependencies...
python -c "import PIL, pytesseract" 2>nul
if errorlevel 1 (
    echo.
    echo Missing required packages. Installing...
    pip install Pillow pytesseract
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)
echo      Dependencies OK

echo.
echo [2/4] Converting images to XML...
python ocr_to_xml_converter.py --input-dir 01_TEXTBOOK/OCR/00_IMPORT/tmp/CH21-24 --output-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

if errorlevel 1 (
    echo.
    echo ERROR: Conversion failed
    pause
    exit /b 1
)

echo.
echo [3/4] Validating XML output...
python validate_xml_output.py --input-dir 01_TEXTBOOK/OCR/01_XML_OUTPUT

echo.
echo [4/4] Complete!
echo.
echo Output files are in: 01_TEXTBOOK\OCR\01_XML_OUTPUT
echo.
pause
