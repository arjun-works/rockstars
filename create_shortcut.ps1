# Create Desktop Shortcut for Visual AI Regression Module
# Run this PowerShell script as Administrator to create a desktop shortcut

$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$([Environment]::GetFolderPath('Desktop'))\Visual AI Regression.lnk")
$Shortcut.TargetPath = "pythonw"
$Shortcut.Arguments = "main.py"
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.IconLocation = "shell32.dll,23"  # Camera icon
$Shortcut.Description = "Visual AI Regression Testing Module"
$Shortcut.Save()

Write-Host "Desktop shortcut created successfully!" -ForegroundColor Green
