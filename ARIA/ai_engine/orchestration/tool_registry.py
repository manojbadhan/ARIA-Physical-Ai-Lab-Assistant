_TOOLS = {}

def tool(name):
    def deco(fn): _TOOLS[name] = fn; return fn
    return deco

def call(name, *a, **k): return _TOOLS[name](*a, **k)
def available(): return list(_TOOLS)

@tool("where_is")
def _where_is(arg):
    from ai_engine.vision import location_memory
    r = location_memory.find(arg)
    if not r: return {"reply": f"I don't have a location saved for {arg} yet.", "intent": "where_is"}
    return {"reply": f"{r['name']} was last placed in {r['location']}.", "intent": "where_is", "photo": r["photo"]}
