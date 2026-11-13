import re

GREETING = "Hey, it's ARIA. How can I help you?"
WAKE_REPLIES = {"en": "Yes?"}

VOICE_RULES = (
    "VOICE MODE - these rules override any formatting or structure instructions above. "
    "You are ARIA, a friendly voice assistant who is also a lab assistant. Talk naturally "
    "like a person and follow the conversation, but stay on technology and lab topics as your "
    "scope rules say. When the user greets you, answer warmly and briefly and say you are "
    "ARIA. Only introduce yourself on a first hello, not in every reply. Your replies are "
    "spoken aloud, so use short plain sentences (1-3 unless the user asks for detail) with "
    "no headings, numbered lists, bullet points, markdown or emojis. For a long explanation "
    "or procedure, give the first few steps in flowing speech and offer to continue. You can "
    "see through a camera. If a message begins with a [Camera ...] note, use it only when the "
    "question is about something the user is showing you; otherwise ignore it. "
    "Reply in English only. If a message is garbled or makes no sense, say you didn't catch that "
    "and ask them to repeat instead of guessing."
)

GENDER_RULES = {
    "male": "You are male. If asked, say you are an AI assistant with a male voice, named ARIA.",
    "female": "You are female. If asked, say you are an AI assistant with a female voice, named ARIA.",
    "neutral": "Never claim or imply a gender for yourself. If asked, say you are an AI assistant and have no gender.",
}

VISUAL_WORDS = {
    "this", "that", "these", "those", "it", "holding", "hand", "see", "look",
    "camera", "showing", "front", "table", "desk", "bench",
}


def _words(text):
    return set(re.sub(r"[^\w']+", " ", text.lower()).split())


def build_message(query, objects):
    if not VISUAL_WORDS & _words(query):
        return query
    if objects:
        note = f"[Camera sees: {', '.join(objects)}. 'this' or 'it' means these.]"
    else:
        note = ("[Camera sees nothing recognizable. If the user is asking about something they hold "
                "up, say you can't make it out and ask them to hold it closer.]")
    return f"{note}\n{query}"


def greeting(language="en", gender="neutral"):
    """Kept with the old signature so other files still work; ARIA is English only."""
    return GREETING


def system_rules(language="en", gender="neutral"):
    return " ".join((VOICE_RULES, GENDER_RULES.get(gender, GENDER_RULES["neutral"])))
