import os
import PySimpleGUI as sg
def Delete_Audio(audio_directory,selected_audio_name):
    after_deletion=False
    if selected_audio_name!=[]:
        selected_audio_name=selected_audio_name[0]
    layout1=[
        [sg.Text('Are you sure to Delete? This process cannot be reverted!',key='-Deleted-')],
        [sg.Button('Yes',disabled=after_deletion),sg.Button('Cancel')]
            ]
    layout2=[[sg.Text('Error: No file is selected')],
             [sg.Button('Return')]
             ]
    if selected_audio_name!=[]:
        window= sg.Window('',layout1)

        # Construct the full path
        full_path = audio_directory + '/' + selected_audio_name

        while True:
            event,values = window.read()
            if event == 'Cancel' or event == sg.WIN_CLOSED:
                break
            elif event == 'Yes' and after_deletion== False:
                window['-Deleted-'].update('The selected audio has been deleted successfully')
                os.remove(full_path)
                after_deletion=True
            elif event == 'Yes' and after_deletion== True:
                break
        window.close()
    else:
        window= sg.Window('',layout2)
        while True:
            event,values = window.read()
            if event == 'Return' or event == sg.WIN_CLOSED:
                break
        
        window.close()
    
    
    return None