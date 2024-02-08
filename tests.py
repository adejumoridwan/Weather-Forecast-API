from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_predict():
    response = client.post(
        "/predict", data={"weather_variable": "temperature", "days": 5}
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
