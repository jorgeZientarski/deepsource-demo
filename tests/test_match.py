import pytest

from app import create_app


@pytest.fixture()
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client


def _create_candidate(client, **overrides):
    payload = {
        "name": "Grace Hopper",
        "email": "grace@example.com",
        "skills": ["python", "leadership"],
        "years_experience": 10,
    }
    payload.update(overrides)
    response = client.post("/candidates", json=payload)
    return response.get_json()["id"]


def _create_job(client, **overrides):
    payload = {
        "title": "Engineering Manager",
        "location": "NYC",
        "skills_required": ["leadership", "python"],
    }
    payload.update(overrides)
    response = client.post("/jobs", json=payload)
    return response.get_json()["id"]


def test_match_success(client):
    candidate_id = _create_candidate(client)
    job_id = _create_job(client)

    response = client.post(
        "/match", json={"candidate_id": candidate_id, "job_id": job_id}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["score"] == 100


def test_match_missing_entities(client):
    response = client.post("/match", json={"candidate_id": 99, "job_id": 1})
    assert response.status_code == 404
    assert "errors" in response.get_json()


def test_match_validation_errors(client):
    response = client.post("/match", json={"candidate_id": "bad", "job_id": None})
    assert response.status_code == 400
    assert "errors" in response.get_json()
