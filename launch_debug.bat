@echo off
echo ========================================
echo Visual AI Regression Module - Debug Mode
echo ========================================
cd /d "%~dp0"

echo Current directory: %CD%
echo Python executable: .\venv\Scripts\python.exe
echo.

echo Testing Python executable...
.\venv\Scripts\python.exe --version
echo.

echo Testing imports...
.\venv\Scripts\python.exe -c "import tkinter; print('Tkinter: OK')"
.\venv\Scripts\python.exe -c "import sklearn; print('Sklearn: OK')"
.\venv\Scripts\python.exe -c "import cv2; print('OpenCV: OK')"
.\venv\Scripts\python.exe -c "import PIL; print('PIL: OK')"
echo.

echo Starting main application...
echo If the GUI doesn't appear, check for error messages below:
echo.
.\venv\Scripts\python.exe main.py

echo.
echo Application ended. Press any key to close...
pause > nul
