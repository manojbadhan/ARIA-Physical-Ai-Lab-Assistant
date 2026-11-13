import os, time

class WakeWord:
    """Text-level wake word with a follow-up window, so a conversation does not need 'ARIA' every turn."""
    def __init__(self, word=None, window=20.0):
        self.word = (word or os.getenv("WAKE_WORD", "aria")).lower()
        self.window, self.active_until = window, 0.0

    def extend(self): self.active_until = time.time() + self.window

    def process(self, text):
        """Returns the command text if ARIA should respond, else None."""
        t = (text or "").lower()
        if self.word in t:
            self.extend()
            return t.replace(self.word, "", 1).strip(" ,.!?") or "hello"
        if time.time() < self.active_until:
            self.extend(); return text.strip()
        return None
