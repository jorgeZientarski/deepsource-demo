from __future__ import annotations

from typing import Dict, List, Tuple

from flask import current_app

from .repositories import Candidate, Job, RepositoryContainer


class ValidationError(ValueError):
    def __init__(self, errors: Dict[str, str]):
        super().__init__("Invalid payload")
        self.errors = errors


def get_repositories() -> RepositoryContainer:
    container = current_app.config.get("repositories")
    if container is None:
        raise RuntimeError("Repository container is not configured on the app")
    return container


def validate_candidate_payload(payload: Dict) -> Tuple[str, str, List[str], int]:
    errors: Dict[str, str] = {}

    name = payload.get("name")
    if not isinstance(name, str) or not name.strip():
        errors["name"] = "name must be a non-empty string"

    email = payload.get("email")
    # ensures simple format
    if not isinstance(email, str) or "@" not in email:
        errors["email"] = "email must be a valid email-like string"

    skills = payload.get("skills")
    if not isinstance(skills, list) or not all(isinstance(s, str) for s in skills):
        errors["skills"] = "skills must be a list of strings"

    years_experience = payload.get("years_experience")
    if not isinstance(years_experience, int) or years_experience < 0:
        errors["years_experience"] = "years_experience must be a non-negative integer"

    if errors:
        raise ValidationError(errors)

    return name.strip(), email.strip(), [s.strip() for s in skills], years_experience


def validate_job_payload(payload: Dict) -> Tuple[str, str, List[str]]:
    errors: Dict[str, str] = {}

    title = payload.get("title")
    if not isinstance(title, str) or not title.strip():
        errors["title"] = "title must be a non-empty string"

    location = payload.get("location")
    if not isinstance(location, str) or not location.strip():
        errors["location"] = "location must be a non-empty string"

    skills_required = payload.get("skills_required")
    if not isinstance(skills_required, list) or not all(
        isinstance(s, str) and s.strip() for s in skills_required
    ):
        errors["skills_required"] = (
            "skills_required must be a list of non-empty strings"
        )

    if errors:
        raise ValidationError(errors)

    return title.strip(), location.strip(), [s.strip() for s in skills_required]


def calculate_match_score(candidate: Candidate, job: Job) -> int:
    if not candidate.skills or not job.skills_required:
        return 0

    candidate_skills = {skill.lower() for skill in candidate.skills}
    job_skills = {skill.lower() for skill in job.skills_required}

    overlap = candidate_skills & job_skills
    if not overlap:
        return 0

    score = int((len(overlap) / len(job_skills)) * 100)
    return min(score, 100)
