import PySimpleGUI as sg
from Import_audio import Import_audio
from Record_audio import AudioRecorder
from Trim_audio import Trim_audio
from Abouts import List_about
from User_guide import List_user_guide
from List_all_audio import List_all_audio
import time
# All the stuff inside window.

sg.theme('LightBlue')

audio_directory='./audios'

# ------ Menu Definition ------ #
menu_def = [['File', ['Import Files']],['Edit', ['Trim','Overwrite']],['Help', ['User Guide','About...']]]
# ------ Frame Definition ------ #
header = ["Name","Time Length","Last Modified Date"]#["Name","Time Length","Last Modified Date"]
audio_info_list=List_all_audio(audio_directory)
frame_layout_1=[[sg.Text('Recording List:'),sg.Button('Import Files')],[sg.Table(headings=header,values=audio_info_list,key="-TABLE-")]]
frame_layout_3=[[sg.Button('🎤',font=(40),key='Record'),sg.Button('▶',font=(40),key='Play'),sg.Button('⏸',font=(40),key='Pause'),sg.Button('◼',font=(40),key='Stop'),sg.Button('⏮',font=(40),key='Fast Backward'),sg.Button('⏭',font=(40),key='Fast Forward'),sg.Text('Volume'),sg.Slider((0, 100), orientation='horizontal')]]
layout = [
    [sg.Menu(menu_def)],
    [sg.Frame('',frame_layout_1,element_justification='center'), sg.VerticalSeparator(color='black'), sg.Output(size=(40, 15))],
    [sg.HorizontalSeparator(color='LightBlue')],
    [sg.Text()],
    [sg.Text(time.strftime("%M:%S/%M:%S",time.localtime())),sg.ProgressBar(1000, key='-PROGRESS_BAR-',size=(50,10),orientation="h")],
    [sg.Frame('',frame_layout_3,element_justification='center')]
    ]


# Create the Window
window = sg.Window('Sound Recorder', layout, resizable=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    #window['-PROGRESS_BAR-'].update(count)
    event, values = window.read()
    audio_info_list=List_all_audio(audio_directory)
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Import Files':
        Import_audio()
    elif event == 'Trim':
        Trim_audio()
    elif event == 'User Guide':
        List_user_guide()
    elif event == 'About...':
        List_about()
    elif event == 'Record':
        recorder = AudioRecorder()
        recorder.run()
    elif event == 'Play':
        pass
    elif event == 'Pause':
        pass
    elif event == 'Stop':
        pass
    else:
        print(event,values)
        
window.close()
