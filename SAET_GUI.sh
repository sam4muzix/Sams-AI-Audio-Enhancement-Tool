#!/bin/bash

# Set the directory where your script and dependencies are located
SCRIPT_DIR="$(dirname "$0")"

# Change to the script directory
cd "$SCRIPT_DIR" || { echo "Failed to change directory"; exit 1; }

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed or not in the system PATH."
    echo "Please install Python before running this script."
    exit 1
fi

# Upgrade pip and install required Python packages
echo "Installing/upgrading Python packages..."
python3 -m pip install --upgrade pip
python3 -m pip install pydub gradio

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "FFmpeg is not installed. Installing FFmpeg..."

    # Download and install FFmpeg using Homebrew
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. Please install Homebrew first."
        exit 1
    fi

    echo "Installing FFmpeg using Homebrew..."
    brew install ffmpeg

    if [ $? -ne 0 ]; then
        echo "Failed to install FFmpeg."
        exit 1
    fi

    echo "FFmpeg installed."
fi

# Run the Python script and capture its output
echo "Running the Python script..."
python3 SAET_GUI.py &

# Wait a moment to ensure the Python script starts up
sleep 5

# Launch the default web browser and open the web UI
open "http://localhost:7860"

echo "Script finished. Press any key to exit."
read -n 1 -s
