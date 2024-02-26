import wave
import PySimpleGUI as sg

def Trim_audio(input_file, start_time, end_time):
    # time in seconds
    output_file = 'trimmed_' + input_file
    layout = [[sg.Text('Audio Selected to Trim: ')]]
    window = sg.Window('Audio Trimmer', layout)

    with wave.open(input_file, 'rb') as input_wave:
        
        params = input_wave.getparams()

        start_frame = int(start_time * params.framerate)
        end_frame = int(end_time * params.framerate)

        input_wave.setpos(start_frame)

        frames = input_wave.readframes(end_frame - start_frame)

    with wave.open(output_file, 'wb') as output_wave:
        
        output_wave.setparams(params)

        output_wave.writeframes(frames)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
    return None
