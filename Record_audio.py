import PySimpleGUI as sg
import sounddevice as sd
import datetime
import struct
import wave
import numpy as np


def write_wav_file(file_path, data, sample_rate):
    with wave.open(file_path, "wb") as wav_file:
        wav_file.setnchannels(1)  # Mono audio
        wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(data)


def Record_audio():
    # Define the recording parameters
    sample_rate = 44100  # Sample rate (Hz)
    duration = 3  # Duration of recording (seconds)
    file_name = f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

    # Start the recording
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)

    # Open a window to show the recording progress
    layout = [
        [sg.Text("Recording in progress...")],
        [
            sg.ProgressBar(
                1800, orientation="h", size=(20, 20), key="-PROGRESS_BAR-"
            )
        ],
    ]

    window = sg.Window("Recording", layout)

    # Start the event loop for updating the progress bar
    for i in range(1800):
        event, values = window.read(timeout=1)
        if event == sg.WINDOW_CLOSED:
            break
        window["-PROGRESS_BAR-"].update(i + 1)

    # Stop the recording
    sd.stop()

    # Scale the recording data and convert to integers
    scaled_data = np.int16(recording.flatten() * (2**15 - 1))

    # Convert the recording data to bytes
    data_bytes = b"".join(struct.pack("<h", sample) for sample in scaled_data)

    # Write the WAV file
    write_wav_file(file_name, data_bytes, sample_rate)

    # Close the window
    window.close()

    # Show a message box with the file path
    sg.popup(f"Recording saved:\n{file_name}", title="Recording Saved")
