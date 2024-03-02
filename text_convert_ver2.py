import speech_recognition as sr


class TextConverter:
    def __init__(self, audio_path):
        self.audio_path = audio_path
        self.r = sr.Recognizer()

    def process_audio_files(self):
        audio_file = sr.AudioFile(self.audio_path)

        try:
            with audio_file as source:
                audio = self.r.record(source)
            text = self.r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(
                "Could not request results from the speech recognition service; {0}".format(
                    e
                )
            )
