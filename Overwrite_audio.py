from Record_audio import AudioRecorder

def Overwrite_audio(audio_directory, target_file, source_file, overwrite_start_time):
    # time in seconds
    output_file = audio_directory + '/' + 'overwrited_' + target_file

    with open(source_file, 'rb') as wave_file:
        source_wave = bytearray(wave_file.read())

    with open(target_file, 'rb') as wave_file:
        target_wave = bytearray(wave_file.read())

        wave_file.seek(24)
        frame_rate_bytes = wave_file.read(4)
        frame_rate = int.from_bytes(frame_rate_bytes, byteorder='little')

        wave_file.seek(34)
        bits_per_sample_bytes = wave_file.read(2)
        bits_per_sample = int.from_bytes(bits_per_sample_bytes, byteorder='little')
    
    sample_width = bits_per_sample / 8

    end_pos = int(overwrite_start_time * frame_rate * sample_width)
    

    overwrited_wave = target_wave[:end_pos] + source_wave + target_wave[end_pos + len(source_wave):]

    recorder = AudioRecorder(audio_directory)
    recorder.write_wav_file(output_file, overwrited_wave)

    return None
