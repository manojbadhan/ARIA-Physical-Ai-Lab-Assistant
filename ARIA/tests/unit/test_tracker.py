from ai_engine.vision.tracker import UsageTracker

def test_fires_once_after_hold():
    t = UsageTracker(hold=2, cooldown=60)
    assert t.update(["multimeter"], now=0) == []
    assert t.update(["multimeter"], now=3) == ["multimeter"]
    assert t.update(["multimeter"], now=4) == []
