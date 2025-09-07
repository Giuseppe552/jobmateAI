from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["ok"]

def test_score_endpoint():
    payload = {"cv_text":"Python pandas AWS", "jd_text":"We need Python and AWS experience"}
    r = client.post("/score", json=payload)
    assert r.status_code == 200 and "score" in r.json()
