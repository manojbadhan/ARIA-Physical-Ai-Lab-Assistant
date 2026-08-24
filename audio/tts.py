import pyttsx3   # This imports the Python library that performs text-to-speech

class TextToSpeech:

    def __init__(self, rate=170, volume=1.0):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", rate)      # words per minute — 170 is a natural pace, default is often too fast
        self.engine.setProperty("volume", volume)

    def speak(self, text):
    
        if not text:
            return

        try:
            self.engine.say(text)
            self.engine.runAndWait()

        except Exception as error:
            print(f"[TTS ERROR] {type(error).__name__}: {error}")

    def set_voice(self, voice_index=0):
        
        voices = self.engine.getProperty("voices")
        if 0 <= voice_index < len(voices):
            self.engine.setProperty("voice", voices[voice_index].id)

    def list_voices(self):
        voices = self.engine.getProperty("voices")
        for i, v in enumerate(voices):
            print(f"[{i}] {v.name} ({v.languages})")