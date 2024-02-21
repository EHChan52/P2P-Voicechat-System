import PySimpleGUI as sg

# All the stuff inside window.

sg.theme('gray gray gray')
# ------ Menu Definition ------ #
menu_def = [['Help', ['About...']]]
# ------ Frame Definition ------ #
frame_layout_1=[[sg.Text('Recording List:'),sg.Button('Import Files')],[sg.Button('Music')]]
layout = [[sg.Menu(menu_def)],
          [sg.Frame('',frame_layout_1,element_justification='center'), sg.VerticalSeparator(color='black'), sg.Output(size=(30, 10))],
            [sg.InputText()],
            [sg.Button('Play'), sg.Button('Stop'),sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('Sound Recorder', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'About...':
        print('爻')
    else:
        print(event)

window.close()
