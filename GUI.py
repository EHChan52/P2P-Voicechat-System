import PySimpleGUI as sg
from Import_audio import Import_audio
from Record_audio import Record_audio
from List_all_audio import List_all_audio
import time
import os
import wave
# All the stuff inside window.

sg.theme('LightBlue')
playing=0
audio_directory='./audios'

# ------ Menu Definition ------ #
menu_def = [['File', ['Import Files']],['Edit', ['Trim','Overwrite']],['9', ['oo']],['Help', ['User Guide','About...']]]
# ------ Frame Definition ------ #
header = ["Name","Time Length","Last Modified Date"]#["Name","Time Length","Last Modified Date"]
audio_info_list=List_all_audio(audio_directory)
frame_layout_1=[[sg.Text('Recording List:'),sg.Button('Import Files')],[sg.Table(headings=header,values=audio_info_list,key="-TABLE-")]]
layout = [[sg.Menu(menu_def)],
          [sg.Frame('',frame_layout_1,element_justification='center'), sg.VerticalSeparator(color='black'), sg.Output(size=(60, 10))],
          [sg.Text('songname')],
            [sg.Text(time.strftime("%M:%S/%M:%S",time.localtime())),sg.ProgressBar(1000, key='-PROGRESS_BAR-',size=(50,10),orientation="h")],
            [sg.Button('🎤',font=(40),key='Record'),sg.Button('▶',font=(40),key='Play'),sg.Button('⏸',font=(40),key='Pause'),sg.Button('◼',font=(40),key='Stop'),sg.Button('⏮',font=(40),key='Fast Backward'),sg.Button('⏭',font=(40),key='Fast Forward'),sg.Slider((1, 100), orientation='horizontal')]]


# Create the Window
window = sg.Window('Sound Recorder', layout, resizable=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    #window['-PROGRESS_BAR-'].update(count)
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Import Files':
        Import_audio()
    elif event == 'Record':
        Record_audio()
    elif event == 'Play':
        playing=1
    elif event == 'Pause':
        playing=1  
    elif event == 'Stop':
        playing=0
        count=0
    else:
        print(event,values)
        
window.close()