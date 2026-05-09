@echo off
echo ========================================
echo Starting FINOVO Application
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :run
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto :run
)

echo ERROR: Python is not installed or not in PATH
echo Please install Python from https://www.python.org/downloads/
pause
exit /b 1

:run
echo Starting Flask server...
echo.
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
%PYTHON_CMD% app.py

