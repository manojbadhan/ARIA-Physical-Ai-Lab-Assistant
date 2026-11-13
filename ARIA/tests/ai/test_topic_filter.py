from ai_engine.orchestration import topic_filter

def test_keyword_fallback_rejects_offtopic():
    assert topic_filter._keyword_check("who won the cricket match")[0] == "reject"
    assert topic_filter._keyword_check("how do servos work")[0] == "allow"
