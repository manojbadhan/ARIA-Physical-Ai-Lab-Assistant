from ai_engine.speech.wake_word import WakeWord

def test_wake_and_followup():
    w = WakeWord("aria")
    assert w.process("random chatter") is None
    assert w.process("ARIA what is a servo") == "what is a servo"
    assert w.process("and a stepper?") == "and a stepper?"
