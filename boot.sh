#!/bin/bash

# Define the repository URL and the project directory
REPO_URL="https://github.com/phillippZZ/aaron.git"
PROJECT_DIR="aaron"

# Check if Homebrew is installed, install if not
if ! command -v brew &>/dev/null; then
    echo "Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" || { echo "Failed to install Homebrew"; exit 1; }
else
    echo "Homebrew is already installed."
fi

# Ensure Homebrew is in the path (for Apple Silicon Macs)
eval "$(/opt/homebrew/bin/brew shellenv)" 2>/dev/null || eval "$(/usr/local/bin/brew shellenv)"

# Check if Python 3 is installed, install if not
if ! command -v python3 &>/dev/null; then
    echo "Python3 not found. Installing Python3 via Homebrew..."
    brew install python || { echo "Failed to install Python3"; exit 1; }
else
    echo "Python3 is already installed."
fi

# Clone the repository if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Cloning repository..."
    git clone "$REPO_URL" "$PROJECT_DIR" || { echo "Failed to clone repository"; exit 1; }
else
    echo "Repository already exists. Pulling latest changes..."
    cd "$PROJECT_DIR" || { echo "Failed to change directory"; exit 1; }
    git pull || { echo "Failed to pull latest changes"; exit 1; }
    cd ..
fi

# Change to the project directory
cd "$PROJECT_DIR" || { echo "Failed to change directory"; exit 1; }

# Create a virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv || { echo "Failed to create virtual environment"; exit 1; }
fi

# Activate the virtual environment
source .venv/bin/activate || { echo "Failed to activate virtual environment"; exit 1; }

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip || { echo "Failed to upgrade pip"; exit 1; }
pip install -r requirements.txt || { echo "Failed to install required packages"; exit 1; }

# Install Tesseract-OCR using Homebrew
echo "Installing Tesseract-OCR..."
brew install tesseract || { echo "Failed to install Tesseract-OCR"; exit 1; }

echo "Installing poppler..."
brew install poppler || { echo "Failed to install poppler"; exit 1; }
# Run the main program
echo "Running the main program..."
python src/main.py || { echo "Failed to run the main program"; exit 1; }

# Deactivate the virtual environment
deactivate

cd .. #leave the project directory