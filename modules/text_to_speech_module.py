# modules/text_to_speech_module.py

import pyttsx3

class TextToSpeechModule:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)  # Speech rate
        self.engine.setProperty('volume', 1)
        self.engine.setProperty('voice', self.get_female_voice)

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.startLoop(False)
            self.engine.iterate()
            self.engine.endLoop()
        except:
            pass
    
    @property
    def get_female_voice(self):
        voices = self.engine.getProperty('voices')
        return voices[1].id
