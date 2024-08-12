
# Sam's AI-Powered Audio Enhancement Tool v1.0

Welcome to **Sam's AI-Powered Audio Enhancement Tool**, a custom-built solution designed specifically for audio producers, particularly those working on *Mirchi promos* and other time-sensitive audio projects. This tool streamlines your workflow by automatically processing audio files, removing silences, and adjusting their duration to meet your exact needs.

## Features

- **Silence Removal**: Automatically removes silent parts from your audio files.
- **Time Stretching**: Adjusts the duration of the audio to a specified target duration.
- **Batch Processing**: Supports multiple files at once for efficient batch processing.
- **Easy Access**: Automatically opens the folder where processed files are saved.
- **User Control**: Allows you to stop processes and clear the output folder with ease.
- **User-Friendly Interface**: A sleek, modern interface with easy-to-use controls.

## Requirements

Before you can use this tool, you'll need to install the following dependencies:

- [Python 3.8.0](https://www.python.org/downloads/release/python-380/)
- [Pydub](https://github.com/jiaaro/pydub) - `pip install pydub`
- [ffmpeg](https://ffmpeg.org/download.html) - Make sure `ffmpeg` is installed and added to your PATH.
- [Gradio](https://gradio.app/) - `pip install gradio`

## Installation

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/sam4muzix/audio-enhancement-tool.git 
    cd audio-enhancement-tool
    ```

2. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure that `ffmpeg` is installed and accessible via your system's PATH. For instructions, check [here](https://ffmpeg.org/download.html).

## Usage

Run the following command to start the Gradio interface:

```bash
python app.py
```

The tool will launch a local web server, and you can access the user interface via your web browser. If you wish to share the interface externally, the app provides a shareable link.

### Interface Overview

- **Upload Audio Files**: Upload one or more WAV files for processing.
- **Target Duration**: Set the desired duration (in seconds) for the output files.
- **Process Files**: Start processing the uploaded files.
- **Open Output Folder**: Open the folder where the processed files are stored.
- **Clear Output Folder**: Delete all files in the output folder.
- **Stop**: Stop the current audio processing task.
- **Refresh**: Refresh the interface to clear the displayed messages.

## Output

Processed audio files will be saved in the `audio_outputs` folder located in the root directory of the project. Each file will be named using a unique identifier based on the target duration and the timestamp of processing.

## Known Issues

- The tool currently only supports WAV files. Future versions may include support for additional audio formats.
- The silence threshold is hardcoded; customizable thresholds may be added in future versions.

## Contribution

Contributions are welcome! If you have suggestions for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by [Shyam L Raj](https://github.com/yourusername).

---

This README should now accurately reflect your project setup.
