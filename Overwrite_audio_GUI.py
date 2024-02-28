import PySimpleGUI as sg
from Overwrite_audio import Overwrite_audio

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_time(total_seconds):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)


def Overwrite_audio_GUI(audio_directory,selected_audio_name,selected_audio_length):
    valid=False
    total_seconds=0
    if selected_audio_name!=[]:
        selected_audio_name=selected_audio_name[0]
        valid=True
    if selected_audio_length!=[]:
        selected_audio_length=selected_audio_length[0]
        total_seconds = time_to_seconds(selected_audio_length)

    layout_audio_overwrite=[[sg.Text('Selected Audio to be overwritten:'),sg.Text(selected_audio_name)],
                    [sg.Text('Original Starting Time:'),sg.Text('00:00:00'),sg.Text('Original Ending Time:'),sg.Text(selected_audio_length)],
                    [sg.Text('Selected Audio to be used:')],
                    [sg.Input(), sg.FileBrowse('FileBrowse')],
                    [sg.Text('Trimmed Starting Time:'),sg.Text('00:00:00',key='-Trimmed-Starting-Time-'),sg.Slider(range=(0, total_seconds),size=(50, 10),orientation="h",enable_events=True,disable_number_display=True,key='-Trimmed-Starting-Time-Slide-',default_value=0)],
                    [sg.Text('Trimmed Ending Time: '),sg.Text(selected_audio_length,key='-Trimmed-Ending-Time-'),sg.Slider(range=(0, total_seconds),size=(50, 10),orientation="h",enable_events=True,disable_number_display=True,key='-Trimmed-Ending-Time-Slide-',default_value=total_seconds)],
                    [sg.Button('Save & Exit'),sg.Button('Discard & Exit')]
                    ]
    layout2=[[sg.Text('Error: No file is selected')],
             [sg.Button('Return')]
             ]
    if valid:
        window = sg.Window('Audio Overwriter', layout_audio_overwrite)
        while True:
            event, values = window.read()
            if event == "-Trimmed-Starting-Time-Slide-":
                startTime = values["-Trimmed-Starting-Time-Slide-"]
                window["-Trimmed-Starting-Time-"].update(seconds_to_time(startTime))
            elif event == "-Trimmed-Ending-Time-Slide-":
                endTime = values["-Trimmed-Ending-Time-Slide-"]
                window["-Trimmed-Ending-Time-"].update(seconds_to_time(endTime))

            if event == sg.WIN_CLOSED or event == 'Discard & Exit': 
                break
            if event == 'Save & Exit':
                full_path = audio_directory + '/' + selected_audio_name
                Overwrite_audio(selected_audio_name,full_path,values["-Trimmed-Starting-Time-Slide-"],values["-Trimmed-Ending-Time-Slide-"])
                break
    else:
        window= sg.Window('',layout2)
        while True:
            event,values = window.read()
            if event == 'Return' or event == sg.WIN_CLOSED:
                break
   
    window.close()
    return None  