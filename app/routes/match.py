from __future__ import annotations

from flask import Blueprint, jsonify, request

from ..services import calculate_match_score, get_repositories

match_bp = Blueprint("match", __name__)


@match_bp.post("")
def match_candidate_job():
    payload = request.get_json(silent=True) or {}
    errors = {}

    candidate_id = payload.get("candidate_id")
    if not isinstance(candidate_id, int) or candidate_id <= 0:
        errors["candidate_id"] = "candidate_id must be a positive integer"

    job_id = payload.get("job_id")
    if not isinstance(job_id, int) or job_id <= 0:
        errors["job_id"] = "job_id must be a positive integer"

    if errors:
        return jsonify({"errors": errors}), 400

    repos = get_repositories()
    candidate = repos.candidates.get(candidate_id)
    job = repos.jobs.get(job_id)

    missing_errors = {}
    if candidate is None:
        missing_errors["candidate_id"] = f"candidate {candidate_id} not found"
    if job is None:
        missing_errors["job_id"] = f"job {job_id} not found"

    if missing_errors:
        return jsonify({"errors": missing_errors}), 404

    score = calculate_match_score(candidate, job)

    return jsonify(
        {
            "candidate_id": candidate.id,
            "job_id": job.id,
            "score": score,
        }
    )
