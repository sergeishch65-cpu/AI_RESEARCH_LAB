from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from ai_research_lab.challenge.workflows import (
    blocked_publication_payload,
    blocked_submission_payload,
    challenge_sources_sync_payload,
    create_challenge_study,
)
from ai_research_lab.cli import main


def _prepare_temp_challenge_root(tmp_path: Path) -> Path:
    root = tmp_path
    (root / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        Path("/Users/sergej/Documents/AI_RESEARCH_LAB/config/challenge_icml_2026.yaml"),
        root / "config" / "challenge_icml_2026.yaml",
    )
    shutil.copy2(
        Path("/Users/sergej/Documents/AI_RESEARCH_LAB/config/challenge_cost_policy.yaml"),
        root / "config" / "challenge_cost_policy.yaml",
    )
    shutil.copytree(
        Path("/Users/sergej/Documents/AI_RESEARCH_LAB/research/_templates/icml_2026_reproduction"),
        root / "research" / "_templates" / "icml_2026_reproduction",
    )
    return root


def test_create_challenge_study_in_temp_root(tmp_path: Path) -> None:
    root = _prepare_temp_challenge_root(tmp_path)
    study = create_challenge_study(root, paper_id="paper-123", study_id="study-one")

    assert study.study_id == "study-one"
    assert (root / "research" / "study-one" / "challenge" / "challenge_metadata.json").exists()
    assert (root / "research" / "study-one" / "challenge" / "paper_candidate.json").exists()
    metadata = json.loads(
        (root / "research" / "study-one" / "challenge" / "challenge_metadata.json").read_text(encoding="utf-8")
    )
    assert metadata["paper_id"] == "paper-123"


def test_paper_id_required_and_path_traversal_blocked(tmp_path: Path) -> None:
    _prepare_temp_challenge_root(tmp_path)

    with pytest.raises(SystemExit):
        main(["challenge", "init-study"])

    with pytest.raises(ValueError):
        create_challenge_study(tmp_path, paper_id="paper-123", study_id="../evil")


def test_publication_and_submission_are_blocked_by_default() -> None:
    root = Path("/Users/sergej/Documents/AI_RESEARCH_LAB")
    publication = blocked_publication_payload(root, "demo")
    submission = blocked_submission_payload(root, "demo")

    assert publication["guard"]["allowed"] is False
    assert submission["guard"]["allowed"] is False
    assert publication["guard"]["reasons"]
    assert submission["guard"]["reasons"]


def test_sources_sync_writes_guide_and_provenance(tmp_path: Path) -> None:
    root = _prepare_temp_challenge_root(tmp_path)
    payload = challenge_sources_sync_payload(root)
    guide_path = Path(payload["guide_path"])
    provenance_path = Path(payload["provenance_path"])
    guide_sha = hashlib.sha256(guide_path.read_bytes()).hexdigest()

    assert guide_path.exists()
    assert provenance_path.exists()
    assert payload["sources"]
    assert guide_sha == payload["sources"][1]["local_text_sha256"]
