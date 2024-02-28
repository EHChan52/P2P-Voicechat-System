import PySimpleGUI as sg

def Import_audio():
    layout = [[sg.Input(), sg.FileBrowse('FileBrowse')],
    [sg.Input(), sg.FolderBrowse('FolderBrowse')],
    [sg.Submit(), sg.Cancel()]]

    window = sg.Window('File', layout)

    while True:
        event, values = window.read()
     # if user closes window or clicks cancel
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
    window.close()
    return None
