import os

class GeminiClient:
    def __init__(self, key=None, model="gemini-2.5-flash"):
        import google.generativeai as genai
        genai.configure(api_key=key or os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model)

    def chat(self, messages, max_tokens=200):
        text = "\n".join(f"{m['role']}: {m['content']}" for m in messages)
        return self.model.generate_content(text, generation_config={"max_output_tokens": max_tokens}).text.strip()
