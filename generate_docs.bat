@echo off
echo ========================================
echo Visual AI Regression Module
echo PDF Documentation Generator
echo ========================================
echo.
echo Generating comprehensive PDF documentation...
echo.

.\venv\Scripts\python.exe generate_documentation_pdf.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ PDF documentation generated successfully!
    echo 📁 Check the project directory for the PDF file.
    echo.
    echo Opening file location...
    start .
) else (
    echo.
    echo ❌ PDF generation failed!
    echo Please check the error messages above.
)

echo.
pause
