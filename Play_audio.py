import pyaudio
import time

class AudioPlayer:
    def __init__(self, audio_directory, audio_name):
        self.audio_directory = audio_directory
        self.audio_name = audio_name
        self.paused = False
        self.stopped = False
        self.stream = None
        self.audio_obj = None

    def play_audio(self, speed):
        with open(self.audio_directory + '/' + self.audio_name, 'rb') as input_file:
            wave = bytes(input_file.read())

        n_channels = int.from_bytes(wave[22:24], byteorder='little')
        sample_rate = int.from_bytes(wave[24:28], byteorder='little')
        bits_per_sample = int.from_bytes(wave[34:36], byteorder='little')

        sample_width = bits_per_sample // 8

        if (speed == '200%'):
            speed = 2
        if (speed == '50%'):
            speed = 0.5

        self.audio_obj = pyaudio.PyAudio()
        self.stream = self.audio_obj.open(format=self.audio_obj.get_format_from_width(sample_width),
                                channels=n_channels,
                                rate=int(sample_rate * speed),
                                output=True)
        
        with open(self.audio_directory + '/' + self.audio_name, 'rb') as input_file:
            input_file.seek(44)
            data = input_file.read(2048)

            while data != b"" and not self.stopped:
                    if self.paused:
                        time.sleep(0.1)
                    else:
                        self.stream.write(data)
                        data = input_file.read(2048)

        self.stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.audio_obj.terminate()

    def pause_audio(self):
        self.paused = True

    def resume_audio(self):
        self.paused = False

    def stop_audio(self):
        self.stopped = True