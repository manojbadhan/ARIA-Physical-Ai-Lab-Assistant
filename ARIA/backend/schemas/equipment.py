from backend.core.exceptions import AppError

def validate_tool(form):
    loc = ", ".join(f"{k.capitalize()} {form.get(k).strip()}" for k in ("almirah", "rack", "box") if (form.get(k) or "").strip())
    if not loc: raise AppError("Give at least one of almirah, rack or box")
    return {"name": (form.get("name") or "").strip(), "location": loc}
