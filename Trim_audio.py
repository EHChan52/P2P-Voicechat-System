import PySimpleGUI as sg

def Trim_audio():
    layout = [[sg.Text('Audio Selected to Trim: ')]]
    window = sg.Window('Audio Trimmer', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
    return None
