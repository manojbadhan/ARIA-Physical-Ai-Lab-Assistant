from backend.repositories import chat_repository as chats
from ai_engine.orchestration.agent import Agent

_agent = Agent()

def reply(user_id, text):
    chats.add(user_id, "user", text)
    out = _agent.handle(text, chats.history(user_id))
    chats.add(user_id, "assistant", out["reply"])
    return out
