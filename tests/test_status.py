from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_get_status_unknown_order():
    r = client.get("/status/TEST-001")
    assert r.status_code in (200, 404)
