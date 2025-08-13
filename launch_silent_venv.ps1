# PowerShell script to launch Visual AI Regression Module silently
Set-Location -Path $PSScriptRoot
Start-Process -FilePath "C:/Users/2052091/OneDrive - Cognizant/Desktop/Suganthi/Vibe/TestProject/venv/Scripts/python.exe" -ArgumentList "main.py" -WindowStyle Hidden
