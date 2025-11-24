from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..services import ValidationError, get_repositories, validate_candidate_payload

candidates_bp = Blueprint("candidates", __name__)


@candidates_bp.get("")
def list_candidates():
    repo = get_repositories().candidates
    candidates = [
        {
            "id": candidate.id,
            "name": candidate.name,
            "email": candidate.email,
            "skills": candidate.skills,
            "years_experience": candidate.years_experience,
        }
        for candidate in repo.list()
    ]
    return jsonify(candidates)


@candidates_bp.post("")
def create_candidate():
    payload = request.get_json(silent=True) or {}
    try:
        name, email, skills, years_experience = validate_candidate_payload(payload)
    except ValidationError as exc:
        return jsonify({"errors": exc.errors}), 400

    repo = get_repositories().candidates
    candidate = repo.add(name, email, skills, years_experience)
    return (
        jsonify(
            {
                "id": candidate.id,
                "name": candidate.name,
                "email": candidate.email,
                "skills": candidate.skills,
                "years_experience": candidate.years_experience,
            }
        ),
        201,
    )
