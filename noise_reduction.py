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
        # Open the input audio file
        with wave.open(self.input_file, 'rb') as wav_file:
            # Get the audio parameters
            sample_width = wav_file.getsampwidth()
            sample_rate = wav_file.getframerate()
            num_channels = wav_file.getnchannels()
            num_frames = wav_file.getnframes()

            # Read the audio data
            audio_data = np.frombuffer(wav_file.readframes(num_frames), dtype=np.int16)

        # Reshape the audio data based on the number of channels
        if num_channels > 1:
            audio_data = np.reshape(audio_data, (num_frames, num_channels))

        # Perform noise reduction
        reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)

        # Create a new wave file for the processed audio
        with wave.open(output_file, 'wb') as processed_wav:
            # Set the audio parameters for the processed file
            processed_wav.setsampwidth(sample_width)
            processed_wav.setframerate(sample_rate)
            processed_wav.setnchannels(num_channels)

            # Write the processed audio data to the file
            processed_wav.writeframes(reduced_noise.tobytes())