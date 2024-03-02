def List_user_guide():
    import PySimpleGUI as sg

    # Multiline text to display
    text = """
# P2P-Voicechat-System
CSCI3280 project phase I


on the top there is menu that allows import and delete files, audio trimming and overwrite and equalization AFTER selecting a wav file from the table below

GUI: Left is audio list table and with import more wav for editing

Right is a graph that can show sound wave diagram

Below the Graph is a textbox which shows the audio transcript

below audio list tableshows the name of the audio currently playing

below that a timer in form hh:mm:ss/hh:mm:ss that shows the current time in audio and total audio length then a slider that can choose time interval of audio

There are record, delete, play, pause, stop, Audio to Test and Noise Reduce Buttons. Next we have a playback speed contro; which allow choosing different playspeed BEFORE playing. Then we have a volume slider from 0 to 100 that support real time volume change.

Made by EHChan on 2/3/2024

Github:https://github.com/EHChan52/P2P-Voicechat-System/
    """

    # Define the window layout
    layout = [[sg.Multiline(text, size=(60, 20),disabled=True)],
            [sg.Button('OK')]]

    # Create the window
    window = sg.Window('User Guide', layout)

    # Event loop
    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            break

    window.close()

    return None