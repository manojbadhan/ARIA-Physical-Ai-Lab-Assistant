import os

def get_provider():
    """Groq first (fast), Gemini second, None if no keys/libs are available."""
    try:
        if os.getenv("GROQ_API_KEY"):
            from ai_engine.llm.groq_client import GroqClient
            return GroqClient()
        if os.getenv("GEMINI_API_KEY"):
            from ai_engine.llm.gemini_client import GeminiClient
            return GeminiClient()
    except ImportError:
        pass
    return None
