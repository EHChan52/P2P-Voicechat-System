import PySimpleGUI as sg
from Import_audio import Import_audio
from Record_audio import Record_audio
import time
import os
# All the stuff inside window.

sg.theme('Gray Gray Gray')
count = 0
playing=0
# ------ Menu Definition ------ #
menu_def = [['File', ['Import Files']],['Edit', ['Trim','Overwrite']],['9', ['oo']],['Help', ['About...']]]
# ------ Frame Definition ------ #
frame_layout_1=[[sg.Text('Recording List:'),sg.Button('Import Files')],[sg.Button('Music')]]
layout = [[sg.Menu(menu_def)],
          [sg.Frame('',frame_layout_1,element_justification='center'), sg.VerticalSeparator(color='black'), sg.Output(size=(70, 40))],
            [sg.Text(time.strftime("%M:%S/%M:%S",time.localtime())),sg.ProgressBar(1000, key='-PROGRESS_BAR-',size=(50,10))],
            [sg.Button('🎤',font=(40),key='Record'),sg.Button('▶',font=(40),key='Play'),sg.Button('⏸',font=(40),key='Pause'),sg.Button('◼',font=(40),key='Stop'),sg.Button('⏮',font=(40),key='Fast Backward'),sg.Button('⏭',font=(40),key='Fast Forward')]]

# Create the Window
window = sg.Window('Sound Recorder', layout, resizable=True)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'Import Files':
        Import_audio()
    elif event == 'Record':
        Record_audio()
    elif event == 'Play':
        playing=1  
    elif event == 'Stop':
        playing=0
        count=0
    else:
        print(event)

    if playing == 1:
        for count in range(1000):
            count+=10
            time.sleep(1)                
    window['-PROGRESS_BAR-'].update(current_count=count)
window.close()

''',[sg.Input(), sg.FileBrowse('FileBrowse')],
    [sg.Input(), sg.FolderBrowse('FolderBrowse')],
    [sg.Submit(), sg.Cancel()]'''