from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check_and_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "Grocery List" in response.text
