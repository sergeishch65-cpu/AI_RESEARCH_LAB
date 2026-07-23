from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from .challenge_registry import ChallengeRegistry
from .config import ChallengeCostPolicy, load_challenge_config, load_cost_policy
from .hf_auth import get_hf_auth_report
from .models import (
    ChallengeConfig,
    CompetitionStudy,
    PaperCandidate,
    PublicationManifest,
    PublicationStatus,
    SelectionStatus,
    SubmissionStatus,
)
from .source_loader import sync_challenge_sources
from .submission_guard import publication_guard, submission_guard
from .trackio_adapter import run_local_trackio_smoke
from .verifier import challenge_doctor_report, secret_scan
from ..paths import validate_study_name


def challenge_config_path(root_dir: Path) -> Path:
    return root_dir / "config" / "challenge_icml_2026.yaml"


def challenge_cost_policy_path(root_dir: Path) -> Path:
    return root_dir / "config" / "challenge_cost_policy.yaml"


def load_challenge_assets(root_dir: Path) -> tuple[ChallengeConfig, ChallengeCostPolicy]:
    return load_challenge_config(challenge_config_path(root_dir)), load_cost_policy(challenge_cost_policy_path(root_dir))


def _slugify_paper_id(paper_id: str) -> str:
    cleaned = []
    for ch in paper_id.lower():
        if ch.isalnum():
            cleaned.append(ch)
        elif ch in {"/", " ", "_", "-"}:
            cleaned.append("-")
    slug = "".join(cleaned).strip("-")
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug or "paper"


def _template_root(root_dir: Path) -> Path:
    return root_dir / "research" / "_templates" / "icml_2026_reproduction"


def create_challenge_study(root_dir: Path, paper_id: str, study_id: str | None = None) -> CompetitionStudy:
    challenge_config, _ = load_challenge_assets(root_dir)
    study_id = study_id or f"repro-{_slugify_paper_id(paper_id)}"
    validate_study_name(study_id)
    template_root = _template_root(root_dir)
    study_root = root_dir / "research" / study_id
    if study_root.exists():
        raise FileExistsError(f"Study already exists: {study_root}")
    shutil.copytree(template_root, study_root)

    paper_candidate = PaperCandidate(
        paper_id=paper_id,
        title="TBD",
        authors=[],
        paper_url="",
        claimed_result="TBD",
        estimated_compute="TBD",
        selected=False,
        selection_status=SelectionStatus.NOT_SELECTED,
    )
    metadata = {
        "challenge_id": challenge_config.challenge_id,
        "challenge_space": challenge_config.challenge_space,
        "paper_id": paper_id,
        "study_id": study_id,
        "publication_status": PublicationStatus.LOCAL_ONLY.value,
        "submission_status": SubmissionStatus.NOT_STARTED.value,
        "trackio_project": study_id,
    }
    challenge_dir = study_root / "challenge"
    challenge_dir.mkdir(parents=True, exist_ok=True)
    (challenge_dir / "challenge_metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (challenge_dir / "paper_candidate.json").write_text(
        json.dumps(paper_candidate.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    registry = ChallengeRegistry(root_dir)
    study = CompetitionStudy(
        study_id=study_id,
        paper_id=paper_id,
        challenge_id=challenge_config.challenge_id,
        local_path=study_root,
        trackio_project=study_id,
    )
    registry.register_study(study)
    registry.upsert_paper_candidate(paper_candidate)
    return study


def challenge_doctor_payload(root_dir: Path) -> dict:
    report = challenge_doctor_report(root_dir)
    return {
        "project_root": report.project_root,
        "baseline_ok": report.baseline_ok,
        "auth_report": report.auth_report,
        "trackio_cli_installed": report.trackio_cli_installed,
        "hf_cli_installed": report.hf_cli_installed,
        "challenge_config_ok": report.challenge_config_ok,
        "source_docs_ok": report.source_docs_ok,
        "secret_scan_ok": report.secret_scan_ok,
        "existing_baseline_ok": report.existing_baseline_ok,
        "notes": report.notes,
    }


def challenge_auth_payload(root_dir: Path) -> dict:
    return get_hf_auth_report().model_dump(mode="json")


def challenge_sources_sync_payload(root_dir: Path) -> dict:
    challenge_config, _ = load_challenge_assets(root_dir)
    provenance, guide_path, provenance_path = sync_challenge_sources(root_dir, challenge_config)
    return {
        "guide_path": str(guide_path),
        "provenance_path": str(provenance_path),
        "sources": [entry.model_dump(mode="json") for entry in provenance],
    }


def challenge_trackio_smoke_payload(root_dir: Path) -> dict:
    challenge_config, _ = load_challenge_assets(root_dir)
    smoke = run_local_trackio_smoke(
        project=challenge_config.challenge_id,
        run_name="trackio-smoke",
        seed=20260723,
        sample_sizes=[10, 100, 1000, 10000],
        mean_abs_errors=[
            0.2476798226685518,
            0.0764609097232232,
            0.02348242357601119,
            0.007766857514033455,
        ],
        final_status="VERIFIED",
    )
    return smoke.model_dump(mode="json")


def verify_challenge_study(root_dir: Path, study_id: str) -> dict:
    study_root = root_dir / "research" / study_id
    challenge_dir = study_root / "challenge"
    logbook = study_root / "logbook" / "LOGBOOK.md"
    registry = ChallengeRegistry(root_dir)
    findings = secret_scan(root_dir)
    study_entry = next(
        (item for item in registry.load().get("studies", []) if item.get("study_id") == study_id),
        None,
    )
    return {
        "study_id": study_id,
        "exists": study_root.exists(),
        "challenge_metadata": (challenge_dir / "challenge_metadata.json").exists(),
        "paper_candidate": (challenge_dir / "paper_candidate.json").exists(),
        "logbook_exists": logbook.exists(),
        "registry_entry": study_entry is not None,
        "secret_scan_ok": not findings,
        "status": "VERIFIED" if study_root.exists() and logbook.exists() and not findings else "BLOCKED",
    }


def publication_status_payload(root_dir: Path, study_id: str) -> dict:
    study_root = root_dir / "research" / study_id
    metadata_path = study_root / "challenge" / "challenge_metadata.json"
    if not metadata_path.exists():
        return {"study_id": study_id, "publication_status": PublicationStatus.NOT_CONFIGURED.value}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    return {"study_id": study_id, **metadata}


def submission_status_payload(root_dir: Path, study_id: str) -> dict:
    payload = publication_status_payload(root_dir, study_id)
    if payload.get("publication_status") != PublicationStatus.PUBLISHED.value:
        payload["submission_status"] = SubmissionStatus.BLOCKED.value
    return payload


def prepare_publication_manifest(root_dir: Path, study_id: str, *, user_approval_recorded: bool = False, publication_flag: bool = False) -> dict:
    study_root = root_dir / "research" / study_id
    metadata_path = study_root / "challenge" / "challenge_metadata.json"
    logbook_path = study_root / "logbook" / "LOGBOOK.md"
    if not metadata_path.exists():
        raise FileNotFoundError(f"Не найдено challenge metadata для study: {study_id}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    manifest = PublicationManifest(
        manifest_id=f"{study_id}-manifest",
        challenge_id=metadata["challenge_id"],
        study_id=study_id,
        paper_id=metadata["paper_id"],
        prepared_at=datetime.now(timezone.utc),
        trackio_project=metadata.get("trackio_project", study_id),
        local_logbook_path=str(logbook_path),
        artifact_paths=[],
        source_provenance_paths=[],
        registry_integrity=logbook_path.exists(),
        approval_recorded=user_approval_recorded,
        publication_flag=publication_flag,
        notes=[],
    )
    manifest_path = study_root / "challenge" / "publication_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return manifest.model_dump(mode="json")


def blocked_publication_payload(root_dir: Path, study_id: str) -> dict:
    challenge_config, cost_policy = load_challenge_assets(root_dir)
    auth_status = get_hf_auth_report().auth_status
    guard = publication_guard(
        auth_status=auth_status,
        challenge_config=challenge_config,
        paper_selected=False,
        study_verified=False,
        trackio_run_verified=False,
        registry_integrity=False,
        logbook_exists=False,
        manifest_complete=False,
        secret_scan_clean=not secret_scan(root_dir),
        user_approval_recorded=False,
        publication_flag=False,
        cost_policy=cost_policy,
    )
    return {"study_id": study_id, "guard": guard.model_dump(mode="json")}


def blocked_submission_payload(root_dir: Path, study_id: str) -> dict:
    challenge_config, cost_policy = load_challenge_assets(root_dir)
    guard = submission_guard(
        publication_status=PublicationStatus.LOCAL_ONLY,
        remote_logbook_id=None,
        challenge_required_fields_complete=False,
        user_approval_recorded=False,
        submission_flag=False,
        challenge_config=challenge_config,
        cost_policy=cost_policy,
    )
    return {"study_id": study_id, "guard": guard.model_dump(mode="json")}
