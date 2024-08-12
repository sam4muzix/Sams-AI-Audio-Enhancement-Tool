import os
import subprocess
import io
from pydub import AudioSegment, silence
from datetime import datetime
import gradio as gr

# Global variable to store the process object for stopping
process_to_stop = None

def generate_unique_filename(base_path, duration):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    duration_str = f"{round(duration)}"
    base_name = os.path.basename(base_path)
    name, ext = os.path.splitext(base_name)
    return f"mirchi_{duration_str}_{timestamp}{ext}"

def remove_silences_and_stretch(audio_binary, output_folder, target_duration):
    global process_to_stop

    try:
        audio = AudioSegment.from_wav(audio_binary)
        non_silent_chunks = silence.split_on_silence(audio, silence_thresh=-40)
        non_silent_audio = sum(non_silent_chunks)
        
        original_duration = len(non_silent_audio) / 1000
        stretch_ratio = original_duration / target_duration

        unique_filename = generate_unique_filename("audio.wav", target_duration)
        output_path_with_extension = os.path.join(output_folder, unique_filename)

        in_memory_audio = io.BytesIO()
        non_silent_audio.export(in_memory_audio, format="wav")
        in_memory_audio.seek(0)

        command = [
            'ffmpeg',
            '-i', 'pipe:0',
            '-filter:a', f'atempo={stretch_ratio}',
            output_path_with_extension
        ]
        
        process = subprocess.Popen(command, stdin=subprocess.PIPE)
        process_to_stop = process
        process.communicate(input=in_memory_audio.read())
        process.wait()

        return output_path_with_extension

    except Exception as e:
        return f"An error occurred: {e}"

def process_multiple_files(files, target_duration):
    output_folder = os.path.join(os.getcwd(), 'audio_outputs')
    os.makedirs(output_folder, exist_ok=True)
    output_paths = []

    if not files:
        return ["Excuse me, I cannot process the AIR or your FACE. Better put in the audio file."]

    for file in files:
        file_binary = io.BytesIO(file)
        result_path = remove_silences_and_stretch(file_binary, output_folder, target_duration)
        output_paths.append(result_path)
    
    return output_paths

def open_audio_outputs_folder():
    output_folder = os.path.join(os.getcwd(), 'audio_outputs')
    if os.path.exists(output_folder):
        try:
            files = os.listdir(output_folder)
            if not files:
                return "Looks like the output folder is on a diet—no audio files to be found!.", []

            if os.name == 'nt':  # For Windows
                subprocess.Popen(f'explorer "{output_folder}"')
                return "Output folder opened successfully.", []
            elif os.name == 'posix':  # For Unix-like systems
                # Try different commands to open the folder
                for cmd in ['xdg-open', 'nautilus', 'thunar', 'pcmanfm', 'dolphin', 'nemo']:
                    try:
                        subprocess.Popen([cmd, output_folder])
                        return "Output folder opened successfully.", []
                    except FileNotFoundError:
                        continue
                # If no suitable command is found, return a status message
                return "I'm really frustrated—no command to open the folder. The processed audio is placed in audio_outputs folder. please check.", []
        except Exception as e:
            return f"An error occurred: {e}", []
    else:
        return "Output folder does not exist.", []

def clear_output_folder():
    output_folder = os.path.join(os.getcwd(), 'audio_outputs')
    if os.path.exists(output_folder):
        try:
            for filename in os.listdir(output_folder):
                file_path = os.path.join(output_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return "Boom! The output folder is now as empty as my motivation on a Monday morning!."
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "Output folder does not exist."

def stop_process():
    global process_to_stop
    if process_to_stop:
        try:
            process_to_stop.terminate()
            process_to_stop.wait()
            return "Process stopped successfully."
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return "Well, look at that—no process running. It’s just you and me, keeping things nice and quiet."

def refresh_gui():
    # Return empty values to refresh the displayed content
    return "", "", ""  # Adjust according to the actual components

css = """
<style>
    body {
        font-family: 'Arial', sans-serif;
        font-size: 18px;
        line-height: 1.6;
        color: #e0e0e0;
        background: #333;
        text-align: center;
    }
    .container {
        padding: 20px;
        margin: auto;
        max-width: 1200px; /* Increased width */
        background: rgba(0, 0, 0, 0.7);
        border-radius: 15px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
    }
    .title {
        font-size: 40px;
        font-family: 'Copperplate', 'Papyrus', fantasy;
        color: red;
        margin-bottom: 30px;
        text-align: center;
    }
    .section {
        font-size: 28px;
        margin-bottom: 30px;
        font-family: Arial, Helvetica, sans-serif;
        color: #ecf0f1;
        text-align: center;
    }
    .button {
        padding: 15px 30px;
        font-size: 18px;
        margin: 10px;
        border-radius: 10px;
        background-color: #3498db;
        color: #fff;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .button:hover {
        background-color: #2980b9;
    }
</style>
"""

def gradio_interface():
    with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.HTML(css)

        with gr.Column(elem_classes="container"):
            gr.Markdown("<div class='title'>Sam's AI-Powered Audio Enhancement Tool v1.0</div>")
            gr.Markdown("<div class='section'>Tailor-Made for Sound Designers and Audio Innovators: Revolutionize Your Workflow and Save Time!</div>")

            file_input = gr.File(label="Upload Audio Files", type="binary", file_count="multiple")
            duration_input = gr.Slider(minimum=1, maximum=60, value=15, step=1, label="Target Duration (seconds)")

            with gr.Row():
                process_button = gr.Button("Process Files", elem_classes="button")
                open_folder_button = gr.Button("Open Output Folder", elem_classes="button")
                clear_folder_button = gr.Button("Clear Output Folder", elem_classes="button")
                stop_button = gr.Button("Stop", elem_classes="button")
                refresh_button = gr.Button("Refresh", elem_classes="button")

            output_markdown = gr.Markdown()
            folder_contents_markdown = gr.Markdown()
            refresh_markdown = gr.Markdown()

            def process_and_display(files, target_duration):
                if not files:
                    # Return the specific message if no files are provided
                    return "Excuse me, I cannot process the AIR or your FACE. Better put in the audio file.", "", ""
                
                output_paths = process_multiple_files(files, target_duration)
                if len(output_paths) == 1 and "Am I a Joke to you dear???" in output_paths[0]:
                    return output_paths[0], "", ""  # Return status and empty strings for folder contents and refresh section
                
                # Refresh the folder contents
                status, _ = open_audio_outputs_folder()
                return "", status, ""

            process_button.click(
                fn=process_and_display, 
                inputs=[file_input, duration_input], 
                outputs=[output_markdown, folder_contents_markdown, refresh_markdown]
            )
            
            def open_folder_and_display():
                status, _ = open_audio_outputs_folder()
                return status, ""
            
            open_folder_button.click(
                fn=open_folder_and_display,
                outputs=[folder_contents_markdown, output_markdown]
            )
            
            def clear_and_reload():
                result = clear_output_folder()
                return result, "", ""  # Return status and empty strings to refresh sections
            
            clear_folder_button.click(
                fn=clear_and_reload,
                outputs=[folder_contents_markdown, output_markdown, refresh_markdown]
            )
            
            stop_button.click(
                fn=stop_process,
                outputs=folder_contents_markdown
            )
            
            refresh_button.click(
                fn=refresh_gui,
                outputs=[output_markdown, folder_contents_markdown, refresh_markdown]
            )
    
    demo.launch(share=True)

if __name__ == "__main__":
    gradio_interface()
