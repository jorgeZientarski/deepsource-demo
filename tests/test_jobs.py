import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def test_list_jobs_initially_empty(client):
    response = client.get("/jobs")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_job_success(client):
    payload = {
        "title": "Backend Engineer",
        "location": "Remote",
        "skills_required": ["python", "flask"],
    }
    response = client.post("/jobs", json=payload)
    data = response.get_json()

    assert response.status_code == 201
    assert data["id"] == 1
    assert data["title"] == payload["title"]

    list_response = client.get("/jobs")
    assert len(list_response.get_json()) == 1


def test_create_job_validation_error(client):
    response = client.post("/jobs", json={"title": ""})
    assert response.status_code == 400
    assert "errors" in response.get_json()
