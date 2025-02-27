#!/bin/bash

# Define the repository URL and the project directory
REPO_URL="https://github.com/phillippZZ/aaron.git"
PROJECT_DIR="aaron"

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
pip install -r requirements.txt || { echo "Failed to install required packages"; exit 1; }

# Install pytesseract-ocr
echo "Installing pytesseract-ocr..."
sudo apt-get install -y tesseract-ocr || { echo "Failed to install pytesseract-ocr"; exit 1; }

# Run the main program
echo "Running the main program..."
python src/main.py || { echo "Failed to run the main program"; exit 1; }

# Deactivate the virtual environment
deactivate
