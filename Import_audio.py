import PySimpleGUI as sg
import os
from List_all_audio import List_all_audio

def Import_audio(audio_dirctory):
    layout = [[sg.Input(key='-FileBrowse-'), sg.FileBrowse('FileBrowse')],
    [sg.Input(key='-FolderBrowse-'), sg.FolderBrowse('FolderBrowse')],
    [sg.Submit(), sg.Cancel()]]

    window = sg.Window('File', layout)

    while True:
        event, values = window.read()
     # if user closes window or clicks cancel
        if event == 'Submit' and values['-FileBrowse-'] != '':
            input_file_path = values['-FileBrowse-']
            output_file_path = audio_dirctory + '/' + os.path.basename(input_file_path)
            with open(input_file_path, 'rb') as input_file:
                file_data = input_file.read()
            with open(output_file_path, 'wb') as output_file:
                output_file.write(file_data)
            break

        if event == 'Submit' and values['-FolderBrowse-'] != '':
            input_directory = values['-FolderBrowse-']
            audios = List_all_audio(input_directory)
            for audio_info in audios:
                file_path = input_directory + '/' + audio_info[0]
                output_path = audio_dirctory + '/' + audio_info[0]
                with open(file_path, 'rb') as input_file:
                    file_data = input_file.read()
                with open(output_path, 'wb') as output_file:
                    output_file.write(file_data)
            break

        if event == sg.WIN_CLOSED or event == 'Cancel':
            break
    window.close()
    return None
