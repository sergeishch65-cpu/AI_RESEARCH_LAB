from __future__ import annotations

import shutil
from pathlib import Path

from ai_research_lab import cli as cli_module
from ai_research_lab.cli import main


REPO_ROOT = Path(__file__).resolve().parents[1]


def _prepare_temp_challenge_root(tmp_path: Path) -> Path:
    root = tmp_path
    (root / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy2(
        REPO_ROOT / "config" / "challenge_icml_2026.yaml",
        root / "config" / "challenge_icml_2026.yaml",
    )
    shutil.copy2(
        REPO_ROOT / "config" / "challenge_cost_policy.yaml",
        root / "config" / "challenge_cost_policy.yaml",
    )
    shutil.copytree(
        REPO_ROOT / "research" / "_templates" / "icml_2026_reproduction",
        root / "research" / "_templates" / "icml_2026_reproduction",
    )
    return root


def test_challenge_cli_end_to_end_in_temp_root(tmp_path: Path, monkeypatch) -> None:
    root = _prepare_temp_challenge_root(tmp_path)
    monkeypatch.setattr(cli_module, "project_root", lambda: root)

    assert main(["challenge", "auth-status"]) == 0
    assert main(["challenge", "sources-sync"]) == 0
    assert main(["challenge", "trackio-smoke"]) == 0
    assert main(["challenge", "init-study", "--paper-id", "paper-123", "--study-id", "study-one"]) == 0
    assert main(["challenge", "publication-status", "study-one"]) == 0
    assert main(["challenge", "submission-status", "study-one"]) == 0
    assert main(["challenge", "prepare-publication", "study-one"]) == 0
    assert main(["challenge", "publish", "study-one"]) == 1
    assert main(["challenge", "submit", "study-one"]) == 1
    assert (root / "research" / "study-one" / "challenge" / "publication_manifest.json").exists()
