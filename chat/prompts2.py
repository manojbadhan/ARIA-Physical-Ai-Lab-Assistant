import re
# Spoken once at startup, after the mic is ready.
GREETINGS = {
    "en": "Hey, it's ARIA. How can I help you?",
    "hi": "नमस्ते! मैं आरिया हूँ। बताइए, मैं आपकी कैसे मदद कर सकती हूँ?",
}
 
# Spoken when someone says only the wake word ("ARIA").
WAKE_REPLIES = {
    "en": "Yes?",
    "hi": "जी, बताइए?",
}
 
VOICE_RULES = (
    "VOICE MODE - these rules override any formatting or structure instructions above. "
    "You are ARIA, a friendly voice assistant who is also a lab assistant. Talk naturally "
    "like a person: make small talk, follow the conversation and answer any topic, not "
    "only lab topics. When the user greets you, answer warmly and briefly and say you are "
    "ARIA. Only introduce yourself on a first hello, not in every reply. Your replies are "
    "spoken aloud, so use short plain sentences (1-3 unless the user asks for detail) with "
    "no headings, numbered lists, bullet points, markdown or emojis. For a long explanation "
    "or procedure, give the first few steps in flowing speech and offer to continue. You can "
    "see through a camera. If a message begins with a [Camera ...] note, use it only when the "
    "question is about something the user is showing you; otherwise ignore it."
)
 
# One rule per language; assistant.py picks the one matching LANGUAGE.
LANGUAGE_RULES = {
    "en": ("Always reply in English, even if the user's words look like another language. "
           "If a message is garbled or makes no sense, say you didn't catch that and ask "
           "them to repeat instead of guessing."),
    "hi": ("Always reply in simple, everyday spoken Hindi written in Devanagari script. You are "
           "female, so use feminine forms for yourself (जैसे: 'मैं बताती हूँ'). Write English "
           "technical words in Devanagari too, for example मल्टीमीटर, कैलिपर, सर्वो मोटर, "
           "because the speech engine reads Devanagari best. If a message is garbled or makes "
           "no sense, say in Hindi that you didn't catch it and ask them to repeat, instead "
           "of guessing."),
}
 
# Words that suggest the question is about something in front of the camera.
VISUAL_WORDS = {
    # English
    "this", "that", "these", "those", "it", "holding", "hand", "see", "look",
    "camera", "showing", "front", "table", "desk", "bench",
    # Hindi
    "यह", "ये", "वह", "वो", "इसे", "इसको", "इसका", "इसकी", "इसके", "उसे", "देखो", "देखिए",
    "देख", "हाथ", "कैमरा", "सामने", "मेज", "टेबल",
}
 
 
def _words(text):
    # \w alone splits Devanagari words at vowel signs, so the Devanagari block is listed too
    return set(re.sub(r"[^\w\u0900-\u097F']+", " ", text.lower()).split())
 
 
def build_message(query, objects):
    """Normal chat by default. A camera note is added only for questions about what's in view."""
    if not VISUAL_WORDS & _words(query):
        return query
    if objects:
        note = f"[Camera sees: {', '.join(objects)}. 'this' or 'it' means these.]"
    else:
        note = ("[Camera sees nothing recognizable. If the user is asking about something they hold "
                "up, say you can't make it out and ask them to hold it closer.]")
    return f"{note}\n{query}"