@echo off
REM Visual AI Regression Module - Batch Launcher
REM This batch file sets up the environment and runs the Visual AI Regression Module

echo ========================================
echo Visual AI Regression Module Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and add it to your PATH
    pause
    exit /b 1
)

echo Python found. Checking version...
python --version

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing required packages...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install requirements
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found
    echo Installing basic requirements...
    pip install selenium opencv-python Pillow numpy scikit-image webdriver-manager matplotlib reportlab requests beautifulsoup4
)

REM Create necessary directories
echo Creating directories...
if not exist "screenshots" mkdir screenshots
if not exist "reports" mkdir reports
if not exist "visualizations" mkdir visualizations

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please ensure you are running this batch file from the project directory
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting Visual AI Regression Module...
echo ========================================
echo.

REM Run the main application
python main.py

REM Check if the application ran successfully
if errorlevel 1 (
    echo.
    echo ERROR: Application encountered an error
    echo Please check the console output above for details
) else (
    echo.
    echo Application completed successfully!
)

echo.
echo Press any key to exit...
pause >nul

REM Deactivate virtual environment
deactivate
