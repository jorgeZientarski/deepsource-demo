import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def test_list_candidates_initially_empty(client):
    response = client.get("/candidates")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_candidate_success(client):
    payload = {
        "name": "Ada Lovelace",
        "email": "ada@example.com",
        "skills": ["python", "math"],
        "years_experience": 5,
    }
    response = client.post("/candidates", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["name"] == payload["name"]

    list_response = client.get("/candidates")
    assert len(list_response.get_json()) == 1


def test_create_candidate_validation_error(client):
    response = client.post("/candidates", json={"name": ""})
    assert response.status_code == 400
    assert "errors" in response.get_json()
