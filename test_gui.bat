@echo off
echo Testing GUI...
cd /d "%~dp0"
.\venv\Scripts\python.exe test_gui.py
pause
