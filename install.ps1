# install.ps1
#
# Windows installation script for Navi-Assistant

# Exit immediately if a command exits with a non-zero status
$SetActionPreference = "Stop"

$NAVI_VERSION = "0.1.3"
$NAVI_WHL = "navi_assistant-$NAVI_VERSION-py3-none-any.whl"

# Check if the script is runnind as admin
# install.ps1
# Installation script for Navi Assistant (Windows Version)

# Exit immediately if a command exits with a non-zero status
$ErrorActionPreference = "Stop"

$NAVI_VERSION = "0.1.1"
$NAVI_WHL = "navi_assistant-$NAVI_VERSION-py3-none-any.whl"

# Check if the script is run as Administrator
$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if ($isAdmin) {
    Write-Host "You should not run this script as Administrator. Please run it as a normal user." -ForegroundColor Red
    exit 1
}

# Check if required commands are available
$requiredCommands = @("python", "curl")
foreach ($cmd in $requiredCommands) {
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "Error: '$cmd' is not installed. Please install it first." -ForegroundColor Red
        exit 1
    }
}

# Define directories
$APP_DIR = Join-Path $env:LOCALAPPDATA "navi"

$BIN_DIR = Join-Path $env:LOCALAPPDATA "navi\bin"

# Create directories
New-Item -ItemType Directory -Force -Path $APP_DIR | Out-Null
New-Item -ItemType Directory -Force -Path $BIN_DIR | Out-Null

# Create a virtual environment
python -m venv "$APP_DIR\venv"

# Download the latest release
Write-Host "Downloading the latest release..."
$RELEASE_URL = "https://github.com/NixonInnes/Navi-Assistant/releases/download/v$NAVI_VERSION/$NAVI_WHL"
$wheelPath = "$APP_DIR\$NAVI_WHL"
curl -L $RELEASE_URL -o $wheelPath

# Activate the virtual environment and install the package
$activateScript = Join-Path $APP_DIR "venv\Scripts\Activate.ps1"
& $activateScript

pip install "$wheelPath" --force-reinstall

# Create the executable script for 'navi'
$naviScriptPath = Join-Path $BIN_DIR "navi.ps1"
$scriptContent = @"
& `"$APP_DIR\venv\Scripts\python.exe`" -m navi_assistant `\$args
"@

Set-Content -Path $naviScriptPath -Value $scriptContent -Force

# Ensure the bin directory is in PATH
$envPath = [System.Environment]::GetEnvironmentVariable("PATH", "User")
if (-not ($envPath -split ";" | Where-Object { $_ -ieq $BIN_DIR })) {
    [System.Environment]::SetEnvironmentVariable("PATH", "$envPath;$BIN_DIR", "User")
    Write-Host "Added '$BIN_DIR' to your PATH. Please restart your PowerShell or terminal session to apply the changes." -ForegroundColor Green
} else {
    Write-Host "'$BIN_DIR' is already in your PATH." -ForegroundColor Green
}

# Run the install module
python -m navi_assistant.install

Write-Host "Navi Assistant has been installed successfully. You can now run it by typing 'navi' in your terminal." -ForegroundColor Green

