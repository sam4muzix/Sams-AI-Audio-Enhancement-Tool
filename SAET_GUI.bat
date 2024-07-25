@echo off
setlocal enabledelayedexpansion

REM Set the directory where your script and dependencies are located
set "SCRIPT_DIR=%~dp0"

REM Change to the script directory
cd /d "%SCRIPT_DIR%"

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not in the system PATH.
    echo Please install Python before running this script.
    pause
    exit /b
)

REM Upgrade pip and install required Python packages
echo Installing/upgrading Python packages...
python -m pip install --upgrade pip
python -m pip install pydub gradio

REM Check if FFmpeg is installed
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
    echo FFmpeg is not installed. Installing FFmpeg...

    REM Download and install FFmpeg
    if "%os%"=="Windows_NT" (
        REM Download FFmpeg
        powershell -Command "Invoke-WebRequest -Uri https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z -OutFile ffmpeg-release-full.7z"
        if %errorlevel% neq 0 (
            echo Failed to download FFmpeg.
            pause
            exit /b
        )

        REM Extract FFmpeg
        powershell -Command "Expand-Archive -Path ffmpeg-release-full.7z -DestinationPath ."
        if %errorlevel% neq 0 (
            echo Failed to extract FFmpeg.
            pause
            exit /b
        )

        REM Add FFmpeg to PATH
        for /d %%d in (ffmpeg-*) do set "FFmpeg_DIR=%%d"
        set "PATH=%PATH%;%SCRIPT_DIR%\%FFmpeg_DIR%\bin"
        echo FFmpeg installed and added to PATH.
    ) else (
        echo Unsupported OS. Please install FFmpeg manually.
        pause
        exit /b
    )
)

REM Run the Python script and capture its output
echo Running the Python script...
start "" python SAET_GUI.py

REM Wait a moment to ensure the Python script starts up
timeout /t 5 /nobreak >nul

REM Launch the default web browser and open the web UI
start "" "http://localhost:7860"

REM Pause to view any error messages
pause
