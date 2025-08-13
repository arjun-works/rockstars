@echo off
setlocal enabledelayedexpansion
color 0A

:: ========================================================================
:: Visual AI Regression Module - Simple GUI Launcher v6.1
:: Updated: August 13, 2025 (Fixed GUI Launch Issues)
:: ========================================================================

title Visual AI Regression Module - Simple Launcher v6.1

echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║              Visual AI Regression Module - GUI Launcher              ║
echo ║                        Version 6.1 (Aug 2025)                       ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.

:: Set working directory
cd /d "%~dp0"
echo [INFO] Working directory: %CD%

:: Check Python
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
echo [✓] Python !PYTHON_VERSION! detected

:: Check virtual environment
echo [INFO] Checking virtual environment...
if not exist "venv\Scripts\python.exe" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo [✓] Virtual environment created
) else (
    echo [✓] Virtual environment found
)

:: Check main.py
echo [INFO] Checking application files...
if not exist "main.py" (
    echo [ERROR] main.py not found!
    echo [INFO] Make sure you're running this from the correct directory
    pause
    exit /b 1
)
echo [✓] main.py found

:: Install/update dependencies
echo [INFO] Checking dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip --quiet
venv\Scripts\python.exe -m pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo [WARNING] Some dependencies may have failed to install
    echo [INFO] The application may still work with existing packages
)
echo [✓] Dependencies checked

:: Launch the GUI
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                        LAUNCHING GUI APPLICATION                     ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Starting Visual AI Regression Module...
echo [INFO] If GUI window doesn't appear, check for errors below
echo [INFO] Launch time: %date% %time%
echo.

:: Try to launch the GUI
echo [DEBUG] Executing: venv\Scripts\python.exe main.py
venv\Scripts\python.exe main.py

:: Capture exit code
set "EXIT_CODE=!errorlevel!"

:: Handle exit
echo.
echo ╔══════════════════════════════════════════════════════════════════════╗
echo ║                         APPLICATION CLOSED                           ║
echo ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo [INFO] Application closed at %date% %time%

if !EXIT_CODE! equ 0 (
    echo [✓] Application closed normally
) else (
    echo [ERROR] Application exited with error code: !EXIT_CODE!
    echo [INFO] Common issues and solutions:
    echo        • Missing dependencies: Run 'pip install -r requirements.txt'
    echo        • Import errors: Check that all modules are installed
    echo        • Permission issues: Run as administrator
    echo        • Display issues: Check that GUI display is available
)

echo.
echo [INFO] Press any key to close this window...
pause >nul
