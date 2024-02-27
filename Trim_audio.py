import PySimpleGUI as sg
from Record_audio import AudioRecorder

def Trim_audio(input_file, start_time, end_time):
    # time in seconds
    output_file = 'trimmed_' + input_file

    layout = [[sg.Text('Audio Selected to Trim: ')]]
    window = sg.Window('Audio Trimmer', layout)

    with open(input_file, 'rb') as wave_file:
        wave = bytearray(wave_file.read())

        wave_file.seek(24)
        frame_rate_bytes = wave_file.read(4)
        frame_rate = int.from_bytes(frame_rate_bytes, byteorder='little')

        wave_file.seek(34)
        bits_per_sample_bytes = wave_file.read(2)
        bits_per_sample = int.from_bytes(bits_per_sample_bytes, byteorder='little')
    
    sample_width = bits_per_sample / 8

    start_pos = int(start_time * frame_rate * sample_width)
    end_pos = int(end_time * frame_rate * sample_width)

    trimmed_wave = wave[start_pos:end_pos]

    recorder = AudioRecorder()
    recorder.write_wav_file(output_file, trimmed_wave)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()

    return None
