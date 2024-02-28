import PySimpleGUI as sg
import datetime
import pyaudio
import threading
import struct
import sys


class AudioRecorder:
    def __init__(self, audio_directory):
        self.audio_directory = audio_directory
        self.sample_rate = 44100
        self.frames = []
        self.recording = False
        self.file_name = ""
        self.audio = pyaudio.PyAudio()
        self.nchannels = 1
        self.sampwidth = 2
        self.framerate = 44100

        # Create PySimpleGUI layout
        layout = [
            [sg.Text("Recording in progress...")],
            [sg.Text("Time: ", key="TIMER")],
            [
                sg.Button("Start Recording", key="START"),
                sg.Button("Stop Recording", key="STOP", disabled=True),
            ],
        ]

        # Create PySimpleGUI window
        self.window = sg.Window("Recording", layout)

    def start_recording(self):
        self.file_name = self.audio_directory + f"/recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"

        # Open audio stream
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=1024,
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
        self.write_wav_file(self.file_name, b"".join(self.frames))

    def write_wav_file(self, file_name, data):
        with open(file_name, "wb") as wav_file:
            wav_file.write(b"RIFF")

            nframes = len(data) // (self.nchannels * self.sampwidth)

            datalength = nframes * self.nchannels * self.sampwidth

            wav_file.write(
                struct.pack(
                    "<L4s4sLHHLLHH4s",
                    36 + datalength,
                    b"WAVE",
                    b"fmt ",
                    16,
                    1,
                    self.nchannels,
                    self.framerate,
                    self.nchannels * self.framerate * self.sampwidth,
                    self.nchannels * self.sampwidth,
                    self.sampwidth * 8,
                    b"data",
                )
            )

            wav_file.write(struct.pack("<L", datalength))

            if self.sampwidth != 1 and sys.byteorder == "big":
                swapped_data = bytearray(len(data))
                width = self.sampwidth

                for i in range(0, len(data), width):
                    for j in range(width):
                        swapped_data[i + width - 1 - j] = data[i + j]

                data = bytes(swapped_data)

            wav_file.write(data)

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
