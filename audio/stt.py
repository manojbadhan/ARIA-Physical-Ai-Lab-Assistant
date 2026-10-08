from groq import Groq
from config import GROQ_API_KEY, STT_MODEL


class SpeechToText:

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = STT_MODEL

    def transcribe(self, audio_file_path):
        """
        Takes a path to a recorded audio file (wav/mp3/m4a) and returns
        the transcribed text. Returns None if transcription fails, so
        callers can handle "didn't catch that" gracefully instead of
        crashing on a bad/empty question.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                response = self.client.audio.transcriptions.create(
                    file=audio_file,
                    model=self.model,
                    response_format="text",
                    language="en",
                    temperature=0
                )
            text = response.strip() if isinstance(response, str) else response.text.strip()
            return text if text else None

        except FileNotFoundError:
            print(f"[STT ERROR] Audio file not found: {audio_file_path}")
            return None

        except Exception as error:
            print(f"[STT ERROR] {type(error).__name__}: {error}")
            return None