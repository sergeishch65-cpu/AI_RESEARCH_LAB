from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PROJECT_NAME = "AI_RESEARCH_LAB"
SAFE_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def config_path(base_root: Path | None = None) -> Path:
    root = Path(base_root).resolve() if base_root is not None else project_root()
    return root / "config" / "lab.yaml"


def research_root(base_root: Path | None = None) -> Path:
    root = Path(base_root).resolve() if base_root is not None else project_root()
    return root / "research"


def validate_study_name(study_name: str) -> str:
    if not SAFE_NAME.fullmatch(study_name):
        raise ValueError("Небезопасное имя исследования.")
    return study_name


def study_root(study_name: str, base_root: Path | None = None) -> Path:
    validate_study_name(study_name)
    return research_root(base_root) / study_name


def ensure_within_root(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve()
    try:
        candidate_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"Путь выходит за пределы разрешённого корня: {candidate_resolved}") from exc
    return candidate_resolved


@dataclass(frozen=True)
class StudyPaths:
    root: Path
    paper: Path
    claims: Path
    plans: Path
    experiments: Path
    results: Path
    figures: Path
    logs: Path
    logbook: Path


def study_paths(study_name: str, base_root: Path | None = None) -> StudyPaths:
    root = study_root(study_name, base_root=base_root)
    return StudyPaths(
        root=root,
        paper=root / "paper",
        claims=root / "claims",
        plans=root / "plans",
        experiments=root / "experiments",
        results=root / "results",
        figures=root / "figures",
        logs=root / "logs",
        logbook=root / "logbook",
    )
