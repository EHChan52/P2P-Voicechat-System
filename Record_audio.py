import PySimpleGUI as sg
import datetime
import wave
import pyaudio
import threading
import os
import struct


class AudioRecorder:
    def __init__(self):
        self.sample_rate = 44100
        self.frames = []
        self.recording = False
        self.file_name = ""
        self.audio = pyaudio.PyAudio()

        # Create PySimpleGUI layout
        layout = [
            [sg.Text("Recording in progress...")],
            [sg.Text("Time: ", key="TIMER")],
            [sg.Button("Start Recording", key="START"),sg.Button("Stop Recording", key="STOP", disabled=True)]            
        ]

        # Create PySimpleGUI window
        self.window = sg.Window("Recording", layout)

    def start_recording(self):
        self.file_name = os.path.join(f"./audios/recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav")

        # Open audio stream
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=1024
        )

        # Start recording
        self.recording = True
        start_time = datetime.datetime.now()

        while self.recording:
            # Handle closing window when recording
            event, _ = self.window.read(timeout=0)
            if event == sg.WINDOW_CLOSED:
                return
            
            data = stream.read(1024)
            self.frames.append(data)

            # Update time in the GUI
            time = datetime.datetime.now() - start_time
            time = str(time).split(".")[0]  # Remove milliseconds
            self.window["TIMER"].update(f"Time: {time}")

        # Stop recording and close audio stream
        stream.stop_stream()
        stream.close()

        # Terminate PyAudio
        self.audio.terminate()

        # Write WAV file
        self.write_wav_file()

    def write_wav_file(self):
        with wave.open(self.file_name, "wb") as wav_file:
            wav_file.setnchannels(1)  # Mono audio
            wav_file.setsampwidth(2)  # 2 bytes per sample (16-bit)
            wav_file.setframerate(self.sample_rate)

            fmt_chunk_data = struct.pack("<HHIIHH", 1, 1, self.sample_rate, self.sample_rate * 2, 2, 16)
            wav_file.writeframes(b"fmt ")
            wav_file.writeframes(struct.pack("<I", len(fmt_chunk_data)))
            wav_file.writeframes(fmt_chunk_data)

            data_chunk_data = struct.pack("<I", len(self.frames))
            wav_file.writeframes(b"data")
            wav_file.writeframes(data_chunk_data)
            wav_file.writeframes(b"".join(self.frames))

    def stop_recording(self):
        self.recording = False

    def record(self):
        while True:
            event, _ = self.window.read()
            if event == sg.WINDOW_CLOSED:
                break
            elif event == "START":
                self.window["START"].update(disabled=True)
                self.window["STOP"].update(disabled=False)
                threading.Thread(target=self.start_recording).start()
            elif event == "STOP":
                self.stop_recording()
                self.window["STOP"].update(disabled=True)
                self.window["START"].update(disabled=False)
                sg.popup(f"Recording saved:\n{self.file_name}", title="Recording Saved")
                break

    def run(self):
        self.record()
        self.window.close()
