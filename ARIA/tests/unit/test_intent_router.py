from ai_engine.orchestration.intent_router import route

def test_where_is():
    assert route("Where is the multimeter?") == ("where_is", "multimeter")
def test_vision():
    assert route("what is in my hand")[0] == "vision"
def test_general():
    assert route("explain pwm")[0] == "general"
