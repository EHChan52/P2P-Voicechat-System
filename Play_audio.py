import pyaudio

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

        if speed == 0.5:
            adjusted_wave = bytearray()
            for i in range(44, len(wave), sample_width):
                adjusted_wave.extend(wave[i:i+sample_width])
                adjusted_wave.extend(wave[i:i+sample_width])
        elif speed == 2:
            adjusted_wave = bytearray()
            for i in range(44, len(wave), sample_width*2):
                adjusted_wave.extend(wave[i:i+sample_width])

        self.audio_obj = pyaudio.PyAudio()
        self.stream = self.audio_obj.open(format=self.audio_obj.get_format_from_width(sample_width),
                                channels=n_channels,
                                rate=sample_rate,
                                output=True)

        if speed == 0.5 or speed == 2:
            self.stream.write(bytes(adjusted_wave))
        else:
            self.stream.write(wave)

        self.stream.stop_stream()
        self.stream.close()
        self.audio_obj.terminate()

    def pause_audio(self):
        self.paused = True

    def resume_audio(self):
        self.paused = False

    def stop_audio(self):
        self.stopped = True
        self.stream.stop_stream()
        self.stream.close()
        self.audio_obj.terminate()