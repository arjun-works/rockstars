@echo off
echo Starting Visual AI Regression Module...
echo.

:: Set working directory
cd /d "%~dp0"

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment!
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install requirements
echo Installing requirements...
pip install -r requirements.txt --quiet

:: Launch the GUI
echo.
echo Launching Visual AI Regression Module GUI...
echo.
venv\Scripts\python.exe main.py

:: Check exit code
if errorlevel 1 (
    echo.
    echo Application exited with an error.
    echo Press any key to close...
    pause >nul
) else (
    echo.
    echo Application closed successfully.
)
