import io

def test_faculty_adds_tool_then_student_finds_it(client):
    data = {"name": "Oscilloscope", "almirah": "C", "rack": "4", "box": "2", "photo": (io.BytesIO(b"x"), "o.jpg")}
    assert client.post("/api/faculty/tools", data=data, content_type="multipart/form-data").status_code == 200
    r = client.post("/api/chat", json={"message": "where is the oscilloscope"}).get_json()
    assert "Almirah C" in r["reply"]
