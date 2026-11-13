import json

def test_json_line_roundtrip():
    msg = {"cmd": "led", "on": 1}
    assert json.loads((json.dumps(msg) + "\n").strip()) == msg
