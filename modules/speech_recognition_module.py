# modules/speech_recognition_module.py

import speech_recognition as sr

class SpeechRecognitionModule:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self, cmd=False):
        with self.microphone as source:
            print("Listening...")
            audio = self.recognizer.listen(source)
        try:
            print("Recognizing...")
            command = self.recognizer.recognize_google(audio)
            print(f"Recognized: {command}")
            if cmd:
                return command.lower()
            return command
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return ""
