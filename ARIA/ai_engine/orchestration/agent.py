from ai_engine.llm.conversation import build_messages
from ai_engine.llm.prompts import RAG_SYSTEM_PROMPT, SYSTEM_PROMPT
from ai_engine.llm.provider import get_provider
from ai_engine.orchestration import intent_router, tool_registry, topic_filter

class Agent:
    def __init__(self):
        self.llm, self._rag = None, None

    def _provider(self):
        if self.llm is None: self.llm = get_provider()
        return self.llm

    def _context(self, text):
        try:
            if self._rag is None:
                from ai_engine.rag.retriever import Retriever
                self._rag = Retriever()
            return self._rag.context(text)
        except Exception:
            return ""

    def handle(self, text, history=None):
        intent, arg = intent_router.route(text)
        if intent == "where_is": return tool_registry.call("where_is", arg)
        if intent == "vision":
            return {"reply": "Hold it up to the camera and press Identify.", "intent": "vision"}
        if intent == "greeting":
            return {"reply": "Hi, I'm ARIA. Ask me about a board, a sensor, or where a tool is.", "intent": "greeting"}
        verdict, topic = topic_filter.check(text)
        if verdict == "suggest":
            return {"reply": f"Did you mean {topic}? Please say it again.", "intent": "clarify"}
        if verdict == "reject":
            return {"reply": "I only help with tech and lab questions.", "intent": "rejected"}
        llm = self._provider()
        if llm is None:
            return {"reply": "The language model is not configured. Add GROQ_API_KEY to .env.", "intent": "general"}
        ctx = self._context(text)
        system = RAG_SYSTEM_PROMPT.format(context=ctx) if ctx else SYSTEM_PROMPT
        msgs = build_messages(text, history, system)
        return {"reply": llm.chat(msgs), "intent": "general"}
