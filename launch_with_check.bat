@echo off
echo ========================================
echo Visual AI Regression Module
echo ========================================
echo Testing dependencies...

.\venv\Scripts\python.exe test_dependencies.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Starting application...
    .\venv\Scripts\python.exe main.py
) else (
    echo.
    echo ❌ Dependency check failed!
    echo Please install missing dependencies first.
    pause
)
