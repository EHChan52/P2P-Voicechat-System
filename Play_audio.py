import pyaudio

def Play_audio(audio_name):

    with open('./audios/' + audio_name, 'rb') as input_file:

        wave = bytes(input_file.read())

        input_file.seek(22)
        n_channels_bytes = input_file.read(2)
        n_channels = int.from_bytes(n_channels_bytes, byteorder='little')

        input_file.seek(24)
        frame_rate_bytes = input_file.read(4)
        frame_rate = int.from_bytes(frame_rate_bytes, byteorder='little')

        input_file.seek(34)
        bits_per_sample_bytes = input_file.read(2)
        bits_per_sample = int.from_bytes(bits_per_sample_bytes, byteorder='little')

    sample_width = bits_per_sample / 8

    audio_obj = pyaudio.PyAudio()
    stream = audio_obj.open(format=audio_obj.get_format_from_width(sample_width),
                            channels=n_channels,
                            rate=frame_rate,
                            output=True)
    stream.write(wave)
    stream.stop_stream()
    stream.close()
    audio_obj.terminate()
    return None