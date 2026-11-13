import re

WHERE = re.compile(r"where\s+(?:is|are|did i (?:put|keep)|can i find)\s+(?:the\s+|my\s+|a\s+)?(.+?)[?.!]*$", re.I)
VISION = re.compile(r"what(?:'s| is)\s+(?:this|that|in my hand)|identify|what am i holding|read (?:this|the label)", re.I)
GREET = re.compile(r"^(hi|hello|hey|good (morning|evening|afternoon))\b", re.I)

def route(text):
    """Returns (intent, argument)."""
    t = (text or "").strip()
    m = WHERE.search(t)
    if m: return "where_is", m.group(1)
    if VISION.search(t): return "vision", None
    if GREET.match(t): return "greeting", None
    return "general", None
