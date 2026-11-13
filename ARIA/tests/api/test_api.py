def test_pages(client):
    for p in ["/", "/login", "/signup", "/dashboard", "/chat", "/inventory", "/faculty"]:
        assert client.get(p).status_code == 200

def test_inventory(client):
    items = client.get("/api/inventory").get_json()["items"]
    assert any(i["name"] == "Multimeter" for i in items)

def test_where_is_chat(client):
    r = client.post("/api/chat", json={"message": "where is the multimeter?"}).get_json()
    assert "Rack 2, Box 3" in r["reply"]

def test_signup_login(client):
    d = {"name": "A", "email": "a@x.com", "password": "password1", "role": "student"}
    assert client.post("/api/auth/signup", json=d).status_code == 200
    assert client.post("/api/auth/login", json={"email": "a@x.com", "password": "password1"}).status_code == 200
    assert client.post("/api/auth/login", json={"email": "a@x.com", "password": "bad"}).status_code == 401
