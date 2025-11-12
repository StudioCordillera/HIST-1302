@echo off
REM Kindle Capture Quick Launch Script
REM Edit the variables below for quick captures

setlocal

REM ========================================
REM CONFIGURATION - Edit these values
REM ========================================
set BOOK_TITLE=My Book
set START_PAGE=1
set END_PAGE=50
REM ========================================

echo.
echo ========================================
echo  Kindle Capture Tool
echo ========================================
echo.
echo Book: %BOOK_TITLE%
echo Pages: %START_PAGE% to %END_PAGE%
echo.
echo Press Ctrl+C to cancel, or
pause

python kindle_capture_cli.py --book "%BOOK_TITLE%" --start %START_PAGE% --end %END_PAGE%

echo.
echo ========================================
echo  Capture Complete!
echo ========================================
echo.
pause
