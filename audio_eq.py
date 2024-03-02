import numpy as np
from scipy.io import wavfile
from scipy import signal
import PySimpleGUI as sg
from datetime import time
from audio_to_waveform import Generate_waveform
import os


class Equalizer:
    def __init__(self, audio_directory, selected_audio_name, selected_audio_length):
        self.time_constant = time(0, 0, 0)
        self.filter = "low"
        self.selected_audio_name = selected_audio_name
        self.selected_audio_length = selected_audio_length
        self.audio_directory = audio_directory
        button_size = (45, 32)
        sg.theme("LightBlue")
        self.audioName = self.audio_directory + "/" + self.selected_audio_name
        self.fs, self.data = wavfile.read(self.audioName)
        self.original_data = self.data.copy()
        frame_20hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-20hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("20-40Hz")],
        ]
        frame_40hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-40hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("40-80Hz")],
        ]
        frame_80hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-80hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("80-160Hz")],
        ]
        frame_160hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-160hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("160-320Hz")],
        ]
        frame_320hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-320hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("320-640Hz")],
        ]
        frame_640hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-640hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("640-1280Hz")],
        ]
        frame_1280hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-1280hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("1280-2560Hz")],
        ]
        frame_2560hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-2560hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("2560-5120Hz")],
        ]
        frame_5120hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-5120hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("5120-10240Hz")],
        ]
        frame_10240hz = [
            [
                sg.Slider(
                    range=(0, 100),
                    orientation="v",
                    size=(10, 20),
                    default_value=50,
                    key="-10240hz-",
                    enable_events=True,
                )
            ],
            [sg.Text("10240-20480Hz")],
        ]
        frame_preamp = [
            [
                sg.Slider(
                    range=(-100, 20),
                    orientation="v",
                    size=(10, 20),
                    default_value=0,
                    key="-preamp-",
                )
            ],
            [sg.Text("Preamp")],
            [sg.Image("low.png", size=button_size, enable_events=True, key="-low-")],
            [sg.Image("band.png", size=button_size, enable_events=True, key="-band-")],
        ]
        frame_width = [
            [
                sg.Slider(
                    range=(0.0, 5.0),
                    orientation="v",
                    size=(10, 20),
                    default_value=0.0,
                    key="-width-",
                )
            ],
            [sg.Text("Width")],
            [sg.Image("high.png", size=button_size, enable_events=True, key="-high-")],
            [sg.Image("stop.png", size=button_size, enable_events=True, key="-stop-")],
        ]
        frame_freq_macro = [
            [
                sg.Image(
                    "default.png", size=button_size, enable_events=True, key="-default-"
                ),
                sg.Image("up1.png", size=button_size, enable_events=True, key="-up1-"),
                sg.Image("up2.png", size=button_size, enable_events=True, key="-up2-"),
                sg.Image("up3.png", size=button_size, enable_events=True, key="-up3-"),
                sg.Image("up4.png", size=button_size, enable_events=True, key="-up4-"),
            ],
            [
                sg.Image(
                    "reset.png", size=button_size, enable_events=True, key="-clear-"
                ),
                sg.Image(
                    "down1.png", size=button_size, enable_events=True, key="-down1-"
                ),
                sg.Image(
                    "down2.png", size=button_size, enable_events=True, key="-down2-"
                ),
                sg.Image(
                    "down3.png", size=button_size, enable_events=True, key="-down3-"
                ),
                sg.Image(
                    "down4.png", size=button_size, enable_events=True, key="-down4-"
                ),
            ],
        ]
        frame_buttons = [
            [sg.Button("Preview Changes")],
            [sg.Button("Save & Exit")],
            [sg.Button("Discard & Exit")],
        ]
        layout = [
            [
                sg.Text("Selected Audio to Equalize:"),
                sg.Text(self.selected_audio_name),
                sg.Text("               "),
                sg.Text("Current applied Filter:"),
                sg.Text("None", key="-filter-name-"),
            ],
            [
                sg.Frame(
                    "", frame_20hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_40hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_80hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_160hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_320hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_640hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_1280hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_2560hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_5120hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_10240hz, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_preamp, element_justification="center", border_width=0
                ),
                sg.Frame(
                    "", frame_width, element_justification="center", border_width=0
                ),
            ],
            [
                sg.Frame(
                    "", frame_freq_macro, element_justification="center", border_width=0
                )
            ],
            [
                sg.Frame(
                    "", frame_buttons, element_justification="center", border_width=0
                ),
                sg.Graph(
                    canvas_size=(400, 200),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(400, 200),
                    key="-GRAPH1-",
                    enable_events=True,
                    background_color="black",
                ),
                sg.Graph(
                    canvas_size=(400, 200),
                    graph_bottom_left=(0, 0),
                    graph_top_right=(400, 200),
                    key="-GRAPH2-",
                    enable_events=True,
                    background_color="black",
                ),
            ],
        ]

        self.window = sg.Window("Equalizer", layout)

    def changeValue(self, value, key, filter):
        if "hz" in key:
            band = int(key.strip("-hz-"))
            lowcut = band
            highcut = band * 2
            self.data = self.apply_filter(lowcut, highcut, value / 50, filter)
        elif key == "-preamp-":
            self.data = self.data * (value / 50)
        elif key == "-width-":
            self.width = value

    def apply_filter(self, lowcut, highcut, gain, filter_type):
        nyquist = 0.5 * self.fs
        low = lowcut / nyquist
        high = highcut / nyquist
        if filter_type == "low":
            b, a = signal.butter(1, low, btype="low")
        elif filter_type == "high":
            b, a = signal.butter(1, high, btype="high")
        elif filter_type == "band":
            b, a = signal.butter(1, [low, high], btype="band")
        elif filter_type == "stop":
            b, a = signal.butter(1, [low, high], btype="bandstop")
        else:
            raise ValueError(f"Invalid filter type: {filter_type}")
        return signal.lfilter(b, a, self.data) * gain

    def run(self):
        while True:
            event, values = self.window.read()
            self.window.finalize()
            if event == sg.WINDOW_CLOSED or event == "Discard & Exit":
                break

            elif event == "-default-":
                default_value = 50
                self.window["-20hz-"].update(default_value)
                self.window["-40hz-"].update(default_value)
                self.window["-80hz-"].update(default_value)
                self.window["-160hz-"].update(default_value)
                self.window["-320hz-"].update(default_value)
                self.window["-640hz-"].update(default_value)
                self.window["-1280hz-"].update(default_value)
                self.window["-2560hz-"].update(default_value)
                self.window["-5120hz-"].update(default_value)
                self.window["-10240hz-"].update(default_value)
                self.window["-preamp-"].update(default_value - default_value)
                self.window["-width-"].update(default_value - default_value)

            elif event == "-clear-":
                self.data = self.original_data.copy()
                graph1 = self.window["-GRAPH1-"]
                graph2 = self.window["-GRAPH2-"]
                graph1.erase()
                graph2.erase()
                self.window["-GRAPH1-"].update("#000000")
                self.window["-GRAPH2-"].update("#000000")

            elif event == "-up1-":
                self.window["-20hz-"].update(values["-20hz-"] + 1)
                self.window["-40hz-"].update(values["-40hz-"] + 1)
                self.window["-80hz-"].update(values["-80hz-"] + 1)
                self.window["-160hz-"].update(values["-160hz-"] + 1)
                self.window["-320hz-"].update(values["-320hz-"] + 1)
                self.window["-640hz-"].update(values["-640hz-"] + 1)
                self.window["-1280hz-"].update(values["-1280hz-"] + 1)
                self.window["-2560hz-"].update(values["-2560hz-"] + 1)
                self.window["-5120hz-"].update(values["-5120hz-"] + 1)
                self.window["-10240hz-"].update(values["-10240hz-"] + 1)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-down1-":
                self.window["-20hz-"].update(values["-20hz-"] - 1)
                self.window["-40hz-"].update(values["-40hz-"] - 1)
                self.window["-80hz-"].update(values["-80hz-"] - 1)
                self.window["-160hz-"].update(values["-160hz-"] - 1)
                self.window["-320hz-"].update(values["-320hz-"] - 1)
                self.window["-640hz-"].update(values["-640hz-"] - 1)
                self.window["-1280hz-"].update(values["-1280hz-"] - 1)
                self.window["-2560hz-"].update(values["-2560hz-"] - 1)
                self.window["-5120hz-"].update(values["-5120hz-"] - 1)
                self.window["-10240hz-"].update(values["-10240hz-"] - 1)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-up2-":
                self.window["-20hz-"].update(10)
                self.window["-40hz-"].update(20)
                self.window["-80hz-"].update(30)
                self.window["-160hz-"].update(40)
                self.window["-320hz-"].update(50)
                self.window["-640hz-"].update(60)
                self.window["-1280hz-"].update(70)
                self.window["-2560hz-"].update(80)
                self.window["-5120hz-"].update(90)
                self.window["-10240hz-"].update(100)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-down2-":
                self.window["-10240hz-"].update(10)
                self.window["-5120hz-"].update(20)
                self.window["-2560hz-"].update(30)
                self.window["-1280hz-"].update(40)
                self.window["-640hz-"].update(50)
                self.window["-320hz-"].update(60)
                self.window["-160hz-"].update(70)
                self.window["-80hz-"].update(80)
                self.window["-40hz-"].update(90)
                self.window["-20hz-"].update(100)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-up3-":
                self.window["-20hz-"].update(100)
                self.window["-40hz-"].update(80)
                self.window["-80hz-"].update(60)
                self.window["-160hz-"].update(40)
                self.window["-320hz-"].update(20)
                self.window["-640hz-"].update(20)
                self.window["-1280hz-"].update(40)
                self.window["-2560hz-"].update(60)
                self.window["-5120hz-"].update(80)
                self.window["-10240hz-"].update(100)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-down3-":
                self.window["-20hz-"].update(20)
                self.window["-40hz-"].update(40)
                self.window["-80hz-"].update(60)
                self.window["-160hz-"].update(80)
                self.window["-320hz-"].update(100)
                self.window["-640hz-"].update(100)
                self.window["-1280hz-"].update(80)
                self.window["-2560hz-"].update(60)
                self.window["-5120hz-"].update(40)
                self.window["-10240hz-"].update(20)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-up4-":
                self.window["-10240hz-"].update(10 - 5)
                self.window["-5120hz-"].update(20 - 5)
                self.window["-2560hz-"].update(30 - 5)
                self.window["-1280hz-"].update(40 - 5)
                self.window["-640hz-"].update(50 - 5)
                self.window["-320hz-"].update(60 - 5)
                self.window["-160hz-"].update(70 - 5)
                self.window["-80hz-"].update(80 - 5)
                self.window["-40hz-"].update(90 - 5)
                self.window["-20hz-"].update(100 - 5)
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
                self.changeValue(values["-10240hz-"], "-10420hz-", self.filter)

            elif event == "-down4-":
                self.window["-20hz-"].update(10 - 5)
                self.window["-40hz-"].update(20 - 5)
                self.window["-80hz-"].update(30 - 5)
                self.window["-160hz-"].update(40 - 5)
                self.window["-320hz-"].update(50 - 5)
                self.window["-640hz-"].update(60 - 5)
                self.window["-1280hz-"].update(70 - 5)
                self.window["-2560hz-"].update(80 - 5)
                self.window["-5120hz-"].update(90 - 5)
                self.window["-10240hz-"].update(100 - 5)

            elif event == "-low-":
                self.filter = "low"
                self.window["-filter-name-"].update("low")

            elif event == "-high-":
                self.filter = "high"
                self.window["-filter-name-"].update("high")

            elif event == "-band-":
                self.filter = "band"
                self.window["-filter-name-"].update("band")

            elif event == "-stop-":
                self.filter = "stop"
                self.window["-filter-name-"].update("stop")

            elif event == "-20hz-":
                self.changeValue(values["-20hz-"], "-20hz-", self.filter)
            elif event == "-40hz-":
                self.changeValue(values["-40hz-"], "-40hz-", self.filter)
            elif event == "-80hz-":
                self.changeValue(values["-80hz-"], "-80hz-", self.filter)
            elif event == "-160hz-":
                self.changeValue(values["-160hz-"], "-160hz-", self.filter)
            elif event == "-320hz-":
                self.changeValue(values["-320hz-"], "-320hz-", self.filter)
            elif event == "-640hz-":
                self.changeValue(values["-640hz-"], "-640hz-", self.filter)
            elif event == "-1280hz-":
                self.changeValue(values["-1280hz-"], "-1280hz-", self.filter)
            elif event == "-2560hz-":
                self.changeValue(values["-2560hz-"], "-2560hz-", self.filter)
            elif event == "-5120hz-":
                self.changeValue(values["-5120hz-"], "-5120hz-", self.filter)
            elif event == "-10240hz-":
                self.changeValue(values["-10240hz-"], "-10240hz-", self.filter)

            elif event == "Preview Changes":
                wavfile.write("equalized.wav", self.fs, self.data.astype(np.int16))
                waveform_image1 = Generate_waveform("test.wav")
                graph1 = self.window["-GRAPH1-"]
                graph1.draw_image(data=waveform_image1, location=(0, 200))
                waveform_image2 = Generate_waveform("equalized.wav")
                graph2 = self.window["-GRAPH2-"]
                graph2.draw_image(data=waveform_image2, location=(0, 200))

            elif event == "Save & Exit":
                os.remove("temp_plot.png")
                os.remove("equalized.wav")
                result_file_path = (
                    "./"
                    + self.audio_directory
                    + "/equalized_"
                    + self.selected_audio_name
                )
                wavfile.write(result_file_path, self.fs, self.data.astype(np.int16))
                break

            elif event == "Discard & Exit":
                self.data = self.original_data.copy()
                os.remove("equalized.wav")

        self.window.close()
