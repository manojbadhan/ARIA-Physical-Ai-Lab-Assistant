import os

class GroqClient:
    def __init__(self, key=None, model=None):
        from groq import Groq
        self.client = Groq(api_key=key or os.getenv("GROQ_API_KEY"))
        self.model = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    def chat(self, messages, max_tokens=200):
        r = self.client.chat.completions.create(model=self.model, messages=messages, max_tokens=max_tokens, temperature=0.3)
        return r.choices[0].message.content.strip()
