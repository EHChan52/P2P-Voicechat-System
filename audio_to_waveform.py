import numpy as np
import matplotlib.pyplot as plt
import wave
from PIL import Image
import io

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)

def array_to_data(array):
    im = Image.fromarray(array)
    with io.BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data


def Generate_waveform(filename):
    with wave.open(filename, 'rb') as audio_file:
        sample_rate = audio_file.getframerate()
        num_samples = audio_file.getnframes()
        plt.clf()
        # Read the audio samples as a numpy array
        audio_samples = np.frombuffer(audio_file.readframes(num_samples), dtype=np.int16)

        # Create a time array based on the sample rate and number of samples
        time = np.arange(0, num_samples) * (1.0 / sample_rate)

        # Plot the audio waveform
        plt.plot(time, audio_samples)
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.title('Audio Waveform')
        plt.grid(False)

        # Save the waveform plot as an image file
        plt.savefig('temp_plot.png')
        resize_image('temp_plot.png', 'temp_plot.png', (400, 200))
        im = Image.open("temp_plot.png")
        array_image = np.array(im, dtype=np.uint8)
        image_data = array_to_data(array_image)
    return image_data

            