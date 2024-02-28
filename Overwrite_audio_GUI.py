import PySimpleGUI as sg
from Overwrite_audio import Overwrite_audio
import os

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def seconds_to_time(total_seconds):
    h = int(total_seconds // 3600)
    m = int((total_seconds % 3600) // 60)
    s = int(total_seconds % 60)
    return "{:02d}:{:02d}:{:02d}".format(h, m, s)

def get_audio_info(filepath): 
    try:
        with open(filepath, 'rb') as wav_file:
            wave = bytes(wav_file.read())
            # Read the WAV file header
            n_channels = int.from_bytes(wave[22:24], byteorder='little')
            sample_rate = int.from_bytes(wave[24:28], byteorder='little')
            bits_per_sample = int.from_bytes(wave[34:36], byteorder='little')

            # Calculate duration
            data_size = os.path.getsize(filepath) - 44
            duration_seconds = data_size / (sample_rate * n_channels * (bits_per_sample // 8))
            minutes, seconds = divmod(duration_seconds, 60)
            hours, minutes = divmod(minutes, 60)
            duration_str = "%02d:%02d:%02d" % (hours, minutes, seconds)

            # Get filename
            filename = os.path.basename(filepath)
            return filename, duration_str
    except Exception as e:
        print(f'Could not process file {filename}: {str(e)}')

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
                    [sg.Text('Selected Audio to be used:'),sg.Text(key='-selAudioName-')],
                    [sg.Text('Selected Audio Length:'),sg.Text(key='-selAudioLen-')],
                    [sg.Input(key='-FileBrowse-',enable_events=True), sg.FileBrowse('FileBrowse')],
                    [sg.Text('Time to Insert New Audio:'),sg.Text('00:00:00',key='-Overwrite-Starting-Time-'),sg.Slider(range=(0, total_seconds),size=(50, 10),orientation="h",enable_events=True,disable_number_display=True,key='-Trimmed-Starting-Time-Slide-',default_value=0)],
                    [sg.Text('Resultant Audio Length: '),sg.Text(selected_audio_length,key='-Trimmed-Ending-Time-')],
                    [sg.Button('Save & Exit'),sg.Button('Discard & Exit')]
                    ]
    layout2=[[sg.Text('Error: No file is selected')],
             [sg.Button('Return')]
             ]
    if valid:
        window = sg.Window('Audio Overwriter', layout_audio_overwrite)
        audio_duration = None
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Discard & Exit': 
                break
            if event == "-Trimmed-Starting-Time-Slide-":
                startTime = values["-Trimmed-Starting-Time-Slide-"]
                window["-Overwrite-Starting-Time-"].update(seconds_to_time(startTime))

                if (audio_duration is not None):
                    if (startTime + time_to_seconds(audio_duration) <= total_seconds):
                        window["-Trimmed-Ending-Time-"].update(seconds_to_time(total_seconds)) 

                    if (startTime + time_to_seconds(audio_duration) > total_seconds):
                        window["-Trimmed-Ending-Time-"].update(seconds_to_time(startTime + time_to_seconds(audio_duration))) 

            if event =="-FileBrowse-":
                audio_name,audio_duration=get_audio_info(values['-FileBrowse-'])
                window["-selAudioName-"].update(audio_name)
                window["-selAudioLen-"].update(audio_duration)
                startTime = values["-Trimmed-Starting-Time-Slide-"]

                if (startTime + time_to_seconds(audio_duration) <= total_seconds):
                    window["-Trimmed-Ending-Time-"].update(seconds_to_time(total_seconds)) 

                if (startTime + time_to_seconds(audio_duration) > total_seconds):
                    window["-Trimmed-Ending-Time-"].update(seconds_to_time(startTime + time_to_seconds(audio_duration))) 
                    
            if event == sg.WIN_CLOSED or event == 'Discard & Exit': 
                break
            if event == 'Save & Exit':
                full_path_1 = selected_audio_name
                full_path_2 = audio_directory + '/' + audio_name
                Overwrite_audio(audio_directory,full_path_1,full_path_2,values["-Trimmed-Starting-Time-Slide-"])
                break
    else:
        window= sg.Window('',layout2)
        while True:
            event,values = window.read()
            if event == 'Return' or event == sg.WIN_CLOSED:
                break
   
    window.close()
    return None  