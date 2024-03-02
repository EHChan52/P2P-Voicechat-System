"""
This is the file for Noise reduction function`s implement
Please notice that torch and noisereduce library need to be added before using this pack
"""
import noisereduce as nr
import numpy as np
import wave

class NoiseReducer:
    def __init__(self, input_file):
        self.input_file = input_file

    def reduce_noise(self, output_file):
        with wave.open(self.input_file, 'rb') as wav_file:
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            num_channels = wav_file.getnchannels()
            num_frames = wav_file.getnframes()

            audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        if num_channels > 1:
            audio_data = np.reshape(audio_data, (num_frames, num_channels))

        reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)

        with wave.open(output_file, 'wb') as processed_wav:
            processed_wav.setsampwidth(sample_width)
            processed_wav.setframerate(sample_rate)
            processed_wav.setnchannels(num_channels)

            processed_wav.writeframes(reduced_noise.tobytes())