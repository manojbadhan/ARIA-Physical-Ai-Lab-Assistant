import re
 
# Spoken once at startup, after the mic is ready.
GREETING = "Hey, it's ARIA. How can I help you?"
 
# Appended after the lab SYSTEM_PROMPT from llm/prompts.py. It makes ARIA a natural
# voice assistant and overrides the headings/bullets rule there, because text-to-speech
# would read those aloud.
VOICE_RULES = (
    "VOICE MODE - these rules override any formatting or structure instructions above. "
    "You are ARIA, a friendly voice assistant who is also a lab assistant. Talk naturally "
    "like a person: make small talk, follow the conversation and answer any topic, not "
    "only lab topics. When the user greets you or starts a chat, answer warmly and briefly, "
    "for example: Hey, it's ARIA, how can I help you? Only introduce yourself like that on "
    "a first hello, not in every reply. Your replies are spoken aloud, so use short plain "
    "sentences (1-3 unless the user asks for detail) with no headings, numbered lists, "
    "bullet points, markdown or emojis. For a long explanation or procedure, give the "
    "first few steps in flowing speech and offer to continue. You can see through a "
    "camera. If a message begins with a [Camera ...] note, use it only when the question "
    "is about something the user is showing you; otherwise ignore it."
)
 
# Words that suggest the question is about something in front of the camera.
VISUAL_WORDS = {"this", "that", "these", "those", "it", "holding", "hand", "see", "look",
                "camera", "showing", "front", "table", "desk", "bench"}
 
 
def build_message(query, objects):
    """Normal chat by default. A camera note is added only for questions about what's in view."""
    if not VISUAL_WORDS & set(re.findall(r"[a-z']+", query.lower())):
        return query
    if objects:
        note = f"[Camera sees: {', '.join(objects)}. 'this' or 'it' means these.]"
    else:
        note = ("[Camera sees nothing recognizable. If the user is asking about something they hold "
                "up, say you can't make it out and ask them to hold it closer.]")
    return f"{note}\n{query}"