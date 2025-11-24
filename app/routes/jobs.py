from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..services import ValidationError, get_repositories, validate_job_payload

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.get("")
def list_jobs():
    repo = get_repositories().jobs
    jobs = [
        {
            "id": job.id,
            "title": job.title,
            "location": job.location,
            "skills_required": job.skills_required,
        }
        for job in repo.list()
    ]
    return jsonify(jobs)


@jobs_bp.post("")
def create_job():
    payload = request.get_json(silent=True) or {}
    try:
        title, location, skills_required = validate_job_payload(payload)
    except ValidationError as exc:
        return jsonify({"errors": exc.errors}), 400

    repo = get_repositories().jobs
    job = repo.add(title, location, skills_required)
    return (
        jsonify(
            {
                "id": job.id,
                "title": job.title,
                "location": job.location,
                "skills_required": job.skills_required,
            }
        ),
        201,
    )
