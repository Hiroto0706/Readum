from fastapi.testclient import TestClient

from src.api.handler import router

client = TestClient(router)


def test_create_question():
    response = client.post("/create_question")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World from FastAPI"}
