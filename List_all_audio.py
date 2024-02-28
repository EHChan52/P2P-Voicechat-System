import os
import time

def List_all_audio(directory):
    audio_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            filepath = os.path.join(directory, filename)
            audio_info = []
            try:
                with open(filepath, 'rb') as wav_file:
                    wave = bytes(wav_file.read())
                    # Read the WAV file header
                    n_channels = int.from_bytes(wave[22:24], byteorder='little')
                    sample_rate = int.from_bytes(wave[24:28], byteorder='little')
                    bits_per_sample = int.from_bytes(wave[34:36], byteorder='little')

                    # Calculate duration
                    data_size = os.path.getsize(filepath) - 44
                    duration_seconds = data_size / (sample_rate * n_channels * (bits_per_sample // 8))
                    minutes, seconds = divmod(duration_seconds, 60)
                    hours, minutes = divmod(minutes, 60)
                    duration_str = "%02d:%02d:%02d" % (hours, minutes, seconds)

                    # Get modification time
                    mod_time = os.path.getmtime(filepath)
                    mod_time = time.strftime('%Y-%m-%d', time.localtime(mod_time))

                    audio_info = [filename, duration_str, mod_time]
            except Exception as e:
                print(f'Could not process file {filename}: {str(e)}')

            audio_list.append(audio_info)

    return audio_list