#!/bin/bash
# Installation script for Navi Assistant

set -e  # Exit on error

NAVI_VERSION="0.1.1"
NAVI_WHL="navi_assistant-${NAVI_VERSION}-py3-none-any.whl" 

# Check if the script is run as root
if [ "$EUID" -eq 0 ]; then
  echo "You should not run this script as root. Please run it as a normal user."
  exit 1
fi

# Check if the required commands are available
for cmd in python3 curl; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "Error: '$cmd' is not installed. Please install it first."
    exit 1
  fi
done

# Check the OS
echo "Checking OS..."
if [ "$(uname)" == "Darwin" ]; then
  echo "macOS detected"
  echo "Please note that Navi has not been thoroughly tested on macOS."
elif [ "$(uname)" == "Linux" ]; then
  echo "Linux detected"
else
  echo "Unsupported OS. Windows support is planned for the future."
  exit 1
fi

echo "Installing Navi Assistant..."

# Set the app directory based on XDG_DATA_HOME or default to ~/.local/share/navi
if [ -z "${XDG_DATA_HOME+x}" ]; then
  APP_DIR="$HOME/.local/share/navi"
else
  APP_DIR="$XDG_DATA_HOME/navi"
fi

mkdir -p "$APP_DIR"

# Create a virtual environment for the app
python3 -m venv "$APP_DIR/venv"

# Download the latest release
echo "Downloading the latest release..."
RELEASE_URL="https://github.com/NixonInnes/Navi-Assistant/releases/download/v$NAVI_VERSION/$NAVI_WHL"
curl -L "$RELEASE_URL" -o "$APP_DIR/$NAVI_WHL"

# Activate the virtual environment and install the package
source "$APP_DIR/venv/bin/activate"
pip install "$APP_DIR/$NAVI_WHL" --force-reinstall

# Set the bin directory based on XDG_BIN_HOME or default to ~/.local/bin
if [ -z "${XDG_BIN_HOME+x}" ]; then
  BIN_DIR="$HOME/.local/bin"
else
  BIN_DIR="$XDG_BIN_HOME"
fi

mkdir -p "$BIN_DIR"

# Create the executable script for 'navi'
echo "#!/bin/bash
${APP_DIR}/venv/bin/python -m navi_assistant \"\$@\"" > "$BIN_DIR/navi"
chmod +x "$BIN_DIR/navi"

python3 -m navi_assistant.install

echo "Navi Assistant has been installed successfully. You can now run it by typing 'navi' in your terminal."
echo "Note: You may need to add '$BIN_DIR' to your PATH to run 'navi'."
