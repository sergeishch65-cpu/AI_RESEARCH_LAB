from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .hf_auth import get_hf_auth_report
from .models import TrackioRunVerification


SUSPICIOUS_PATTERNS = [
    re.compile(r"HF" + r"_TOKEN"),
    re.compile(r"HUGGINGFACE" + r"_TOKEN"),
    re.compile(r"OPENAI" + r"_API" + r"_KEY"),
    re.compile(r"\b" + r"API" + r"_KEY\b"),
    re.compile(r"\b" + r"SEC" + r"RET\b"),
    re.compile(r"\b" + r"PASS" + r"WORD\b"),
    re.compile(r"hf_" + r"[A-Za-z0-9]{10,}"),
    re.compile(r"sk-" + r"[A-Za-z0-9]{10,}"),
]


@dataclass(frozen=True)
class SecretFinding:
    path: str
    line: int
    pattern: str


@dataclass(frozen=True)
class BaselineSnapshot:
    claim_sha: str
    experiment_result_sha: str
    metrics_sha: str
    logbook_sha: str
    registry_sha: str


@dataclass(frozen=True)
class ChallengeDoctorReport:
    project_root: str
    baseline_ok: bool
    auth_report: dict
    trackio_cli_installed: bool
    hf_cli_installed: bool
    challenge_config_ok: bool
    source_docs_ok: bool
    secret_scan_ok: bool
    existing_baseline_ok: bool
    notes: list[str]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def secret_scan(root: Path, glob_excludes: Iterable[str] | None = None) -> list[SecretFinding]:
    excludes = list(glob_excludes or [])
    findings: list[SecretFinding] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if rel.startswith(".git/") or rel.startswith(".venv/") or rel.startswith(".agents/"):
            continue
        if "__pycache__" in rel or rel.endswith(".pyc") or rel.endswith(".pyo") or rel.endswith(".pyd"):
            continue
        if any(rel.startswith(pattern.rstrip("/")) for pattern in excludes):
            continue
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except Exception:
            continue
        for idx, line in enumerate(lines, start=1):
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern.search(line):
                    findings.append(SecretFinding(path=rel, line=idx, pattern=pattern.pattern))
                    break
    return findings


def verify_existing_demo_baseline(root: Path) -> BaselineSnapshot:
    study_root = root / "research" / "demo_study"
    claim_path = study_root / "claims" / "claim.json"
    experiment_result_path = study_root / "experiments" / "mean_convergence_demo" / "experiment_result.json"
    metrics_path = study_root / "results" / "metrics.json"
    logbook_path = study_root / "logbook" / "LOGBOOK.md"
    registry_path = study_root / "logs" / "artifact_registry.json"
    for path in [claim_path, experiment_result_path, metrics_path, logbook_path, registry_path]:
        if not path.exists():
            raise FileNotFoundError(f"Не найден baseline artifact: {path}")
    return BaselineSnapshot(
        claim_sha=_sha256(claim_path),
        experiment_result_sha=_sha256(experiment_result_path),
        metrics_sha=_sha256(metrics_path),
        logbook_sha=_sha256(logbook_path),
        registry_sha=_sha256(registry_path),
    )


def build_trackio_verification(adapter) -> TrackioRunVerification:
    return adapter.verify_run()


def challenge_doctor_notes(root: Path) -> list[str]:
    notes = []
    if not (root / "docs" / "challenge" / "ICML_2026_CHALLENGE_GUIDE.md").exists():
        notes.append("Challenge guide snapshot not yet synced.")
    if not (root / "config" / "challenge_icml_2026.yaml").exists():
        notes.append("Challenge config missing.")
    return notes


def challenge_doctor_report(root: Path) -> ChallengeDoctorReport:
    auth_report = get_hf_auth_report().model_dump(mode="json")
    hf_cli_installed = auth_report["auth_status"]["cli_installed"]
    trackio_cli_installed = (root / ".venv" / "bin" / "trackio").exists()
    secret_findings = secret_scan(root)
    baseline_ok = True
    existing_baseline_ok = False
    notes = challenge_doctor_notes(root)
    try:
        verify_existing_demo_baseline(root)
        existing_baseline_ok = True
    except Exception as exc:
        baseline_ok = False
        notes.append(str(exc))
    return ChallengeDoctorReport(
        project_root=str(root),
        baseline_ok=baseline_ok,
        auth_report=auth_report,
        trackio_cli_installed=trackio_cli_installed,
        hf_cli_installed=hf_cli_installed,
        challenge_config_ok=(root / "config" / "challenge_icml_2026.yaml").exists(),
        source_docs_ok=(root / "docs" / "challenge" / "ICML_2026_CHALLENGE_GUIDE.md").exists(),
        secret_scan_ok=not secret_findings,
        existing_baseline_ok=existing_baseline_ok,
        notes=notes,
    )
