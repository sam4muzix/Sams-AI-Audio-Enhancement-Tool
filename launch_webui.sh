#!/bin/bash

# Set up the environment
echo "Setting up the Python environment..."

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Ensure ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed. Please install it to continue."
    exit 1
fi

# Launch the application
echo "Launching the application..."
python aipp.py

# Deactivate the virtual environment after use
deactivate
