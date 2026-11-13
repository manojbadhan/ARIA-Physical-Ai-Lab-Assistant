from ai_engine.llm.prompts import SYSTEM_PROMPT

def build_messages(user_text, history=None, system=SYSTEM_PROMPT, keep=6):
    msgs = [{"role": "system", "content": system}]
    msgs += [m for m in (history or [])[-keep:] if m["role"] in ("user", "assistant")]
    msgs.append({"role": "user", "content": user_text})
    return msgs
