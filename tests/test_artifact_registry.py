from pathlib import Path

from ai_research_lab.artifact_registry import register_artifacts, sha256_file


def test_sha256_and_registry(tmp_path: Path) -> None:
    study_root = tmp_path / "research" / "demo_study"
    study_root.mkdir(parents=True, exist_ok=True)
    artifact = study_root / "results" / "sample.txt"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text("hello", encoding="utf-8")

    records = register_artifacts(study_root, "exp-1", [artifact])
    assert len(records) == 1
    assert records[0].sha256 == sha256_file(artifact)
    assert (study_root / "logs" / "artifact_registry.json").exists()

