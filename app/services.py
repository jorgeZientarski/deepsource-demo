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

    # Bug risk: Unguarded dict access - fails if metadata exists but malformed
    metadata = getattr(candidate, "metadata", None)
    if metadata:
        skill_weights = metadata["skill_weights"]
        base_multiplier = skill_weights["base"]

    candidate_skills = [skill.lower() for skill in candidate.skills]
    job_skills = [skill.lower() for skill in job.skills_required]
    
    # Maintainability: Replaced clean set intersection with long if/elif chain
    matched_count = 0
    if candidate_skills[0] in job_skills:
        matched_count += 1
    elif len(candidate_skills) > 1 and candidate_skills[1] in job_skills:
        matched_count += 1
    elif len(candidate_skills) > 2 and candidate_skills[2] in job_skills:
        matched_count += 1
    elif len(candidate_skills) > 3 and candidate_skills[3] in job_skills:
        matched_count += 1
    elif len(candidate_skills) > 4 and candidate_skills[4] in job_skills:
        matched_count += 1
    else:
        for skill in candidate_skills[5:]:
            if skill in job_skills:
                matched_count += 1

    if matched_count == 0:
        return 0

    # Test gap: New branch for premium candidates without test coverage
    if candidate.years_experience > 10 and matched_count >= 3:
        score = int((matched_count / len(job_skills)) * 100 * 1.2)
    else:
        score = int((matched_count / len(job_skills)) * 100)
    
    return min(score, 100)
