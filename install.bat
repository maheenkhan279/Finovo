@echo off
echo ========================================
echo FINOVO Installation Script for Windows
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python found!
    set PYTHON_CMD=python
    goto :install
)

py --version >nul 2>&1
if %errorlevel% == 0 (
    echo Python found (using py launcher)!
    set PYTHON_CMD=py
    goto :install
)

echo ERROR: Python is not installed or not in PATH
echo Please install Python from https://www.python.org/downloads/
pause
exit /b 1

:install
echo.
echo Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% == 0 (
    echo.
    echo ========================================
    echo Installation successful!
    echo ========================================
    echo.
    echo To run the application, use:
    echo   %PYTHON_CMD% app.py
    echo.
    echo Then open your browser to:
    echo   http://localhost:5000
    echo.
) else (
    echo.
    echo ERROR: Installation failed
    echo Please check the error messages above
    echo.
)

pause

