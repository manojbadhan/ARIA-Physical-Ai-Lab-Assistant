"""Check how often retrieval + answer is right. Run: python -m rag.evaluate

tests/questions.json holds your ~30 questions:
  {"q": "...", "file": "expected source file", "keywords": ["must", "appear"]}
  Use {"q": "...", "file": null} for questions that are NOT in the notes (expects "not in the notes").
Add --llm to also check the final answer text (uses Groq tokens); default checks retrieval only.
"""
import json
import sys
from pathlib import Path

from rag.retrieve import get_retriever, ask

QUESTIONS = Path(__file__).resolve().parent.parent / "tests" / "questions.json"


def main(use_llm=False):
    items = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    retriever, ok = get_retriever(), 0
    for item in items:
        if use_llm:
            res = ask(item["q"])
            files = [s["file"] for s in res["sources"]]
            text = res["answer"].lower()
        else:
            hits = retriever.search(item["q"])
            files = [h["file"] for h in hits]
            text = " ".join(h["text"] for h in hits).lower()
        if item["file"] is None:
            passed = not files if not use_llm else not res["found"]
        else:
            passed = item["file"] in files and all(k.lower() in text for k in item.get("keywords", []))
        ok += passed
        print(("PASS" if passed else "FAIL"), "-", item["q"], "->", files[:3])
    print(f"\n{ok}/{len(items)} correct ({100 * ok / len(items):.0f}%)")


if __name__ == "__main__":
    main("--llm" in sys.argv)
