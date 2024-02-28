import speech_recognition as sr
import os

class TextConverter:
    def __init__(self, audio_folder):
        self.audio_folder = audio_folder
        self.r = sr.Recognizer()

    def process_audio_files(self):
        wav_files = [file for file in os.listdir(self.audio_folder) if file.endswith('.wav')]

        for wav_file in wav_files:
            wav_path = os.path.join(self.audio_folder, wav_file)
            print("Processing:", wav_path)

            audio_file = sr.AudioFile(wav_path)

            try:
                with audio_file as source:
                    audio = self.r.record(source)
                text = self.r.recognize_google(audio)
                segments = text.split(".")
                for segment in segments:
                    print(segment.strip())
                print("\n--- End of File ---\n")
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from the speech recognition service; {0}".format(e))
                
'''
from Text_converter import TextConverter 

audio_folder = "./audios" # we will convert all the wav file under this path

text_converter = tc(audio_folder)
text_converter.process_audio_files()
'''