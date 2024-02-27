import PySimpleGUI as sg
from Import_audio import Import_audio
from Record_audio import AudioRecorder
from Trim_audio import Trim_audio
from Overwrite_audio import Overwrite_audio
from Abouts import List_about
from User_guide import List_user_guide
from List_all_audio import List_all_audio
from Delete_audio import Delete_Audio
import os
from datetime import time, datetime, timedelta
import threading
# All the stuff inside window.

sg.theme('LightBlue')

audio_directory='./audios'
playing_audio_name='Nothing'
time_constant = time(0,0,0)
os.makedirs("audios", exist_ok=True)
thread_running = False
paused = False


# ------ Menu Definition ------ #
menu_def = [
    ["File", ["Import Files"]],
    ["Editor", ["Trim", "Overwrite"]],
    ["Help", ["User Guide", "About..."]],
]# ------ Frame Definition ------ #
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
                "60%",
                "70%",
                "80%",
                "90%",
                "100%",
                "110%",
                "120%",
                "130%",
                "140%",
                "150%",
                "160%",
                "170%",
                "180%",
                "190%",
                "200%",
            ],
            size=(5, 1),
            initial_value="100%",
            enable_events=True,
            readonly=True,
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
        sg.Frame("", frame_layout_playback_speed, element_justification="center"),
        sg.Frame("", frame_layout_volume, element_justification="center"),
    ]
]

frame_layout_audio_to_visual = [
    [
        sg.Graph(
            (400, 200),
            (-400, -200),
            (400, 200),
            background_color="black",
            key="-GRAPH-",
        )
    ],
    [
        sg.Checkbox("Audio Transcription", default=False),
        sg.StatusBar("", key="-AudiotoText-", background_color="white"),
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
            range=(0, 1000),
            key="-play-length-",
            size=(100, 10),
            orientation="h",
            enable_events=True,
            disable_number_display=True
        ),
    ],
    [sg.Frame("", frame_layout_playback_controls, element_justification="center")],
]

# Create the Window
window = sg.Window("Sound Recorder", layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    window.finalize()
    audio_info_list = List_all_audio(audio_directory)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Import Audio':
        Import_audio()
    elif event == 'Trim':
        Trim_audio()
    elif event == 'Overwrite':
        Trim_audio()
    elif event == 'User Guide':
        List_user_guide()
    elif event == 'About...':
        List_about()
    elif event == 'Record':
        recorder = AudioRecorder()
        recorder.run()
        audio_info_list = List_all_audio(audio_directory)
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == "Delete":
        selected_audio_name = [
            audio_info_list[row][0] for row in values["-TABLE-"]
        ]  # return audio name as list
        Delete_Audio(audio_directory, selected_audio_name)
        window["-TABLE-"].update(List_all_audio(audio_directory))
    elif event == ("Play"):
        paused = False
        
        def update_elapsed_time():
            global thread_running
            thread_running = True
            elapsed_time = datetime.strptime('00:00:00', '%H:%M:%S')
            audio_length = datetime.strptime(selected_audio_length[0], '%H:%M:%S')

            while elapsed_time < audio_length and thread_running:
                if not paused:
                    elapsed_time += timedelta(seconds=1)
                    elapsed_time_str = elapsed_time.strftime('%H:%M:%S')
                    window['-Eplased_Playtime-'].update(elapsed_time_str)

                    elapsed_seconds = (elapsed_time - datetime(1900, 1, 1)).total_seconds()
                    audio_length_seconds = (audio_length - datetime(1900, 1, 1)).total_seconds()
                    slider_position = int((elapsed_seconds / audio_length_seconds) * 1000)
                    window['-play-length-'].update(slider_position)

                sg.time.sleep(1)

            window['-Audio_playing_name-'].update('')
            window['-Eplased_Playtime-'].update(time_constant)
            window['-Audio_Length-'].update(time_constant)
            window['-play-length-'].update(0)
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
                window['-Audio_playing_name-'].update(selected_audio_name)
                window['-Audio_Length-'].update(selected_audio_length[0])
                threading.Thread(target=update_elapsed_time).start()
    elif event == 'Pause':
        paused = True
    elif event == 'Stop':
        window['-Audio_playing_name-'].update('')
        window['-Audio_Length-'].update(time_constant)
        window['-play-length-'].update(0)
        thread_running = False
    elif event == "Muted":
        window["-Volume-"].update(0)
        window["Muted"].update("🔇")
    elif event == "-Volume-":
        volume_value = values["-Volume-"]
        if volume_value == 0:
            window["Muted"].update("🔇")
        elif volume_value > 0 and volume_value <= 33:
            window["Muted"].update("🔈")
        elif volume_value > 33 and volume_value <= 66:
            window["Muted"].update("🔉")
        else:
            window['Muted'].update("🔊")
    else:
        print(event,values) # debug use
        
window.close()
