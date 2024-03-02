import PySimpleGUI as sg
from Import_audio import Import_audio
from Record_audio import AudioRecorder
from Trim_audio_GUI import Trim_audio_GUI
from Overwrite_audio_GUI import Overwrite_audio_GUI
from List_all_audio import List_all_audio
from audio_eq import Equalizer
from Delete_audio import Delete_Audio
from audio_to_waveform import Generate_waveform
import os
from datetime import time, datetime, timedelta
import threading
from Play_audio import AudioPlayer
from text_convert_ver2 import TextConverter
from noise_reduction import NoiseReducer
from User_guide import List_user_guide

sg.theme("LightBlue")

audio_directory = "./audios"
playing_audio_name = "Nothing"
time_constant = time(0, 0, 0)
os.makedirs("audios", exist_ok=True)
thread_running = False
paused = False
length_adjusted = False

# ------ Menu Definition ------ #
menu_def = [
    ["File", ["Import Files","Delete"]],
    ["Editor", ["Trim", "Overwrite","Audio_Equalizer"]],
    ["User_Guide",["User_Guide"]]
]  # ------ Frame Definition ------ #
header = [
    "Audio Name",
    "Time Length",
    "Last Modified Date",
]  # ["Name","Time Length","Last Modified Date"]

audio_info_list = List_all_audio(audio_directory)

frame_layout_audio_list = [
    [sg.Text("Recording List:"), sg.Button("Import Files")],
    [
        sg.Table(
            headings=header,
            values=audio_info_list,
            key="-TABLE-",
            auto_size_columns=True,
            enable_events=True,
            starting_row_number=1,
        )
    ],
]

frame_layout_playback_speed = [
    [
        sg.Text("Playback Speed:"),
        sg.Spin(
            [
                "50%",
                "100%",
                "200%",
            ],
            size=(5, 1),
            initial_value="100%",
            enable_events=True,
            readonly=True,
            key="-Speed-",
        ),
    ]
]

frame_layout_volume = [
    [
        sg.Text("Volume"),
        sg.Slider(
            (0, 100),
            orientation="horizontal",
            key="-Volume-",
            enable_events=True,
            default_value=100,
        ),
        sg.Button("🔊", font=(30), key="Muted"),
    ]
]

frame_layout_playback_controls = [
    [
        sg.Button("🎤", font=(40), key="Record"),
        sg.Button("❌", font=(40), key="Delete"),
        sg.Button("▶", font=(40), key="Play"),
        sg.Button("⏸", font=(40), key="Pause"),
        sg.Button("◼", font=(40), key="Stop"),
        sg.Button("Text", key="Text"), 
        sg.Button("NR", key="NR"),  #Noise Reduce
        sg.Frame("", frame_layout_playback_speed, element_justification="center"),
        sg.Frame("", frame_layout_volume, element_justification="center"),
       
    ]
]

frame_layout_audio_to_visual = [
    [
        sg.Graph(
            canvas_size=(400, 200),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 200),
            key="-GRAPH-",
            enable_events=True,
            background_color="black",
        )
    ],
    [
        sg.Checkbox("Audio Transcription", default=False),
        sg.StatusBar("", key="-AudiotoText-", background_color="white", size=(50, 1)),
    ],
]

layout = [
    [sg.Menu(menu_def)],
    [
        sg.Frame("", frame_layout_audio_list, element_justification="center"),
        sg.VerticalSeparator(color="black"),
        sg.Frame("", frame_layout_audio_to_visual, element_justification="center"),
    ],
    [sg.HorizontalSeparator(color="LightBlue")],
    [
        sg.Text("Currently Playing:"),
        sg.StatusBar(
            playing_audio_name,
            key="-Audio_playing_name-",
            text_color="#000000",
            size=(100, 1),
        ),
    ],
    [
        sg.Text(time_constant, key="-Eplased_Playtime-"),
        sg.Text("/"),
        sg.Text(time_constant, key="-Audio_Length-"),
        sg.Slider(
            range=(0, 100),
            key="-Play_Length-",
            size=(100, 10),
            orientation="h",
            enable_events=True,
            disable_number_display=True,
        ),
    ],
    [sg.Frame("", frame_layout_playback_controls, element_justification="center")],
]

# Create the Window
window = sg.Window("Sound Recorder", layout, finalize=True)


class Updater:
    def __init__(self, elapsed_time, audio_length, speed):
        self.elapsed_time = elapsed_time
        self.audio_length = audio_length
        self.speed = speed

    def update(self):
        while self.elapsed_time < self.audio_length and thread_running:
            if not paused:
                self.elapsed_time += timedelta(seconds=1)
                elapsed_time_str = self.elapsed_time.strftime("%H:%M:%S")
                window.write_event_value("-Update_Elapsed_Time-", elapsed_time_str)

                elapsed_seconds = (
                    self.elapsed_time - datetime(1900, 1, 1)
                ).total_seconds()
                audio_length_seconds = (
                    self.audio_length - datetime(1900, 1, 1)
                ).total_seconds()
                slider_position = int((elapsed_seconds / audio_length_seconds) * 100)
                window.write_event_value("-Update_Slider_Position-", slider_position)

            if self.speed == "50%":
                sg.time.sleep(2)
            elif self.speed == "200%":
                sg.time.sleep(0.5)
            else:
                sg.time.sleep(1)

        window.write_event_value("-End_Play-", "end")

    def update_elapsed_time(self, time):
        self.elapsed_time = time


def get_time(selected_audio_length):
    audio_length = datetime.strptime(selected_audio_length, "%H:%M:%S")
    hours, minutes, seconds = selected_audio_length.split(":")
    total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    current_second = int(values["-Play_Length-"] / 100 * total_seconds)
    elapsed_hours = current_second // 3600
    elapsed_minutes = (current_second % 3600) // 60
    elapsed_seconds = current_second % 60
    elapsed_time_str = (
        f"{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_seconds:02d}"
    )
    elapsed_time = datetime.strptime(elapsed_time_str, "%H:%M:%S")
    return elapsed_time, audio_length

while True:
    event, values = window.read()
    window.finalize()
    audio_info_list = List_all_audio(audio_directory)
    selected_audio_name = [audio_info_list[row][0] for row in values["-TABLE-"]]
    selected_audio_length = [audio_info_list[row][1] for row in values["-TABLE-"]]
    if selected_audio_name != []:
        player = AudioPlayer(audio_directory, selected_audio_name[0])

    if event == sg.WINDOW_CLOSED:
        player.stop_audio()
        os.remove("temp_plot.png")
        break
    elif event == "Import Files":
        Import_audio(audio_directory)
        window["-TABLE-"].update(List_all_audio(audio_directory))

    elif event == "Trim":
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        selected_audio_length = [
            audio_info_list[row][1] for row in values["-TABLE-"]
        ]  # return audio length as list
        Trim_audio_GUI(audio_directory, selected_audio_name, selected_audio_length)
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == "Overwrite":
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        selected_audio_length = [
            audio_info_list[row][1] for row in values["-TABLE-"]
        ]  # return audio length as list
        Overwrite_audio_GUI(audio_directory, selected_audio_name, selected_audio_length)
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == "Audio_Equalizer":
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        selected_audio_length = [
            audio_info_list[row][1] for row in values["-TABLE-"]
        ]  # return audio length as list
        if selected_audio_name!=[] and selected_audio_length!=[]:
            equalizer = Equalizer(audio_directory,selected_audio_name[0],selected_audio_length[0])
            equalizer.run()
            window["-TABLE-"].update(List_all_audio(audio_directory))
        else:
            pass
    elif event == "User_Guide":
        List_user_guide()
    elif event == "Record":
        recorder = AudioRecorder(audio_directory)
        recorder.run()
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == "Delete":
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        Delete_Audio(audio_directory, selected_audio_name)
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == ("Play"):
        paused = False
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        if selected_audio_name != []:
            waveform_image = Generate_waveform(
                audio_directory + "/" + selected_audio_name[0]
            )
            graph = window["-GRAPH-"]
            # Display the image on the graph
            graph.draw_image(data=waveform_image, location=(0, 200))

        def stop_play():
            window["-Audio_playing_name-"].update("")
            window["-Eplased_Playtime-"].update(time_constant)
            window["-Audio_Length-"].update(time_constant)
            window["-Play_Length-"].update(0)
            graph.erase()
            global thread_running
            thread_running = False

        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        selected_audio_length = [
            audio_info_list[row][1] for row in values["-TABLE-"]
        ]  # return audio length as list

        if selected_audio_name == [] and selected_audio_length == []:
            window["-Audio_playing_name-"].update("No audio Selected")
        else:
            if not thread_running:
                window["-Audio_playing_name-"].update(selected_audio_name)
                window["-Audio_Length-"].update(selected_audio_length[0])
                thread_running = True

                # args=speed
                player.set_current_sample(values["-Play_Length-"] / 100)
                threading.Thread(
                    target=player.play_audio,
                    args=(
                        values["-Speed-"],
                        values["-Volume-"] / 100,
                    ),
                ).start()

                elapsed_time, audio_length = get_time(selected_audio_length[0])
                updater = Updater(elapsed_time, audio_length, values["-Speed-"])
                threading.Thread(target=updater.update).start()

                while True:
                    event, values = window.read()

                    if event == sg.WINDOW_CLOSED:
                        player.stop_audio()
                        graph.erase()
                        break

                    if event == "-Update_Elapsed_Time-":
                        elapsed_time_str = values[event]
                        window["-Eplased_Playtime-"].update(elapsed_time_str)

                    if event == "-Update_Slider_Position-":
                        slider_position = values[event]
                        window["-Play_Length-"].update(slider_position)

                    if event == "-End_Play-":
                        stop_play()
                        os.remove("temp_plot.png")
                        window["-GRAPH-"].update("#000000")
                        break

                    if event == "Pause":
                        paused = True
                        player.pause_audio()
                        length_adjusted = False
                        while paused:
                            event, values = window.read()
                            if event == sg.WINDOW_CLOSED:
                                player.stop_audio()
                                break
                            if event == "Play":
                                player.resume_audio()
                                paused = False
                                if length_adjusted:
                                    threading.Thread(
                                        target=player.play_audio,
                                        args=(
                                            values["-Speed-"],
                                            values["-Volume-"] / 100,
                                        ),
                                    ).start()
                                break
                            if event == "Stop":
                                player.stop_audio()
                                stop_play()
                                break
                            if event == "Muted":
                                window["-Volume-"].update(0)
                                window["Muted"].update("🔇")
                                player.set_volume(0)
                            if event == "-Volume-":
                                volume_value = values["-Volume-"]
                                player.set_volume(volume_value / 100)
                                if volume_value == 0:
                                    window["Muted"].update("🔇")
                                elif volume_value > 0 and volume_value <= 33:
                                    window["Muted"].update("🔈")
                                elif volume_value > 33 and volume_value <= 66:
                                    window["Muted"].update("🔉")
                                else:
                                    window["Muted"].update("🔊")
                            if event == "-Play_Length-":
                                length_adjusted = True
                                elapsed_time, audio_length = get_time(
                                    selected_audio_length[0]
                                )
                                updater.update_elapsed_time(elapsed_time)
                                player.stop_audio()
                                player = AudioPlayer(
                                    audio_directory, selected_audio_name[0]
                                )
                                player.set_current_sample(values["-Play_Length-"] / 100)

                    if event == "Stop":
                        player.stop_audio()
                        stop_play()
                        os.remove("temp_plot.png")
                        graph.erase()
                        break

                    if event == "Muted":
                        window["-Volume-"].update(0)
                        window["Muted"].update("🔇")
                        player.set_volume(0)

                    if event == "-Volume-":
                        volume_value = values["-Volume-"]
                        player.set_volume(volume_value / 100)
                        if volume_value == 0:
                            window["Muted"].update("🔇")
                        elif volume_value > 0 and volume_value <= 33:
                            window["Muted"].update("🔈")
                        elif volume_value > 33 and volume_value <= 66:
                            window["Muted"].update("🔉")
                        else:
                            window["Muted"].update("🔊")

                    if event == "-Play_Length-":
                        elapsed_time, audio_length = get_time(selected_audio_length[0])
                        updater.update_elapsed_time(elapsed_time)
                        player.stop_audio()
                        player = AudioPlayer(audio_directory, selected_audio_name[0])
                        player.set_current_sample(values["-Play_Length-"] / 100)
                        threading.Thread(
                            target=player.play_audio,
                            args=(
                                values["-Speed-"],
                                values["-Volume-"] / 100,
                            ),
                        ).start()
    elif event == "Pause":
        paused = True
    elif event == "Muted":
        window["-Volume-"].update(0)
        window["Muted"].update("🔇")
        if selected_audio_name != []:
            player.set_volume(0)
    elif event == "-Volume-":
        volume_value = values["-Volume-"]
        if selected_audio_name != []:
            player.set_volume(volume_value / 100)
        if volume_value == 0:
            window["Muted"].update("🔇")
        elif volume_value > 0 and volume_value <= 33:
            window["Muted"].update("🔈")
        elif volume_value > 33 and volume_value <= 66:
            window["Muted"].update("🔉")
        else:
            window["Muted"].update("🔊")
    elif event == "Text":
        if selected_audio_name != []:
            audio_path = audio_directory + "/" + selected_audio_name[0]
            converter = TextConverter(audio_path)
            text = converter.process_audio_files()
            if type(text) == str:
                window["-AudiotoText-"].update(text)
            else:
                window["-AudiotoText-"].update("Speech recognition could not understand audio")
    elif event == "NR":
        if not values["-TABLE-"]:
            print("Please select a file.")
            continue

        selected_audio_name = audio_info_list[values["-TABLE-"][0]][0]
        audio_path = os.path.join(audio_directory, selected_audio_name)
        print(f"Reducing...{audio_path}")
        reducer = NoiseReducer(audio_path)
        output_file = os.path.join(audio_directory, selected_audio_name.split(".")[0] + "_reduced.wav")
        print(f"Outputing{output_file}")
        reducer.reduce_noise(output_file)
        window["-TABLE-"].update(values["-TABLE-"].clear())
        window["-TABLE-"].update(List_all_audio(audio_directory))
window.close()