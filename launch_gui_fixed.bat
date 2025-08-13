@echo off
echo ========================================================================
echo Visual AI Regression Module - Simple GUI Launcher
echo ========================================================================
echo.

:: Set working directory to the batch file location
cd /d "%~dp0"

:: Check if Python is available
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo     ✓ Python found

:: Check if virtual environment exists
echo [2/4] Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo     Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo     ✓ Virtual environment ready

:: Install/update dependencies
echo [3/4] Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
venv\Scripts\python.exe -m pip install -r requirements.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Some dependencies may not be installed properly
)
echo     ✓ Dependencies checked

:: Launch the GUI application
echo [4/4] Launching Visual AI Regression Module GUI...
echo.
echo ========================================================================
echo If the GUI window doesn't appear, check for error messages below:
echo ========================================================================
echo.

:: Launch with explicit error handling
venv\Scripts\python.exe main.py
set EXIT_CODE=%errorlevel%

:: Show exit status
echo.
echo ========================================================================
if %EXIT_CODE% equ 0 (
    echo GUI application closed normally
) else (
    echo GUI application exited with code: %EXIT_CODE%
    echo.
    echo Possible solutions:
    echo 1. Make sure main.py exists in this directory
    echo 2. Check that all dependencies are installed
    echo 3. Try running: python main.py directly
    echo 4. Check for error messages above
)
echo ========================================================================
echo.
echo Press any key to close this window...
pause >nul
