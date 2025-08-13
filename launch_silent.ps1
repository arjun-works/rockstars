# Visual AI Regression Module - Silent Launcher
# This script launches the application without showing a console window

$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Launch with pythonw to avoid console window
Start-Process "pythonw" -ArgumentList "main.py" -WindowStyle Hidden
