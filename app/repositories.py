from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Candidate:
    id: int
    name: str
    email: str
    skills: List[str]
    years_experience: int


@dataclass
class Job:
    id: int
    title: str
    location: str
    skills_required: List[str]


class CandidateRepository:
    def __init__(self) -> None:
        self._candidates: Dict[int, Candidate] = {}
        self._next_id = 1

    def list(self) -> List[Candidate]:
        return list(self._candidates.values())

    def add(
        self, name: str, email: str, skills: List[str], years_experience: int
    ) -> Candidate:
        candidate = Candidate(
            id=self._next_id,
            name=name,
            email=email,
            skills=skills,
            years_experience=years_experience,
        )
        self._candidates[self._next_id] = candidate
        self._next_id += 1
        return candidate

    def get(self, candidate_id: int) -> Optional[Candidate]:
        return self._candidates.get(candidate_id)


class JobRepository:
    def __init__(self) -> None:
        self._jobs: Dict[int, Job] = {}
        self._next_id = 1

    def list(self) -> List[Job]:
        return list(self._jobs.values())

    def add(self, title: str, location: str, skills_required: List[str]) -> Job:
        job = Job(
            id=self._next_id,
            title=title,
            location=location,
            skills_required=skills_required,
        )
        self._jobs[self._next_id] = job
        self._next_id += 1
        return job

    def get(self, job_id: int) -> Optional[Job]:
        return self._jobs.get(job_id)


@dataclass
class RepositoryContainer:
    candidates: CandidateRepository = field(default_factory=CandidateRepository)
    jobs: JobRepository = field(default_factory=JobRepository)
