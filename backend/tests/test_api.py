from fastapi.testclient import TestClient
from app.main import api
import time

client = TestClient(api)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["ok"] is True

def test_score_happy():
    data = {"cv_text": "python developer", "jd_text": "python job"}
    r = client.post("/score", json=data)
    assert r.status_code == 200
    out = r.json()
    assert 0 <= out["score"] <= 1
    assert isinstance(out["matches"], list)
    assert isinstance(out["gaps"], list)

def test_rate_limit():
    # Lower limit for test
    for _ in range(12):
        r = client.post("/score", json={"cv_text": "a", "jd_text": "b"})
        if r.status_code == 429:
            break
    assert r.status_code == 429
