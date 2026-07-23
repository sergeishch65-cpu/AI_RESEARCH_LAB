from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest
import yaml

from ai_research_lab.agent import ResearchAgent
from ai_research_lab.paths import portable_relative_path, resolve_portable_path


def _write_config(root: Path) -> None:
    config_path = root / "config" / "lab.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump(
            {
                "project_name": "AI_RESEARCH_LAB",
                "default_study": "demo_study",
                "safe_experiment_type": "mean_convergence",
                "sample_sizes": [10, 100, 1000, 10000],
                "replicates": 8,
                "seed": 20260723,
                "figure_name": "convergence.png",
                "success_criteria": {
                    "final_mean_abs_error_max": 0.05,
                    "final_error_better_than_initial": True,
                },
            }
        ),
        encoding="utf-8",
    )


def test_registry_and_result_store_relative_paths(tmp_path: Path) -> None:
    _write_config(tmp_path)
    result = ResearchAgent(root_dir=tmp_path).run("demo_study")
    study_root = tmp_path / "research" / "demo_study"

    assert all(not Path(path).is_absolute() for path in result.artifact_paths)

    result_payload = json.loads(
        (study_root / "experiments" / "mean_convergence_demo" / "experiment_result.json").read_text(
            encoding="utf-8"
        )
    )
    assert all(not Path(path).is_absolute() for path in result_payload["artifact_paths"])

    registry_payload = json.loads((study_root / "logs" / "artifact_registry.json").read_text(encoding="utf-8"))
    assert registry_payload
    assert all(not Path(item["path"]).is_absolute() for item in registry_payload)
    for item in registry_payload:
        assert (tmp_path / item["path"]).exists()

    copied_root = tmp_path / "copied_root"
    shutil.copytree(study_root, copied_root / "research" / "demo_study")
    (copied_root / "config").mkdir(parents=True, exist_ok=True)
    shutil.copy2(tmp_path / "config" / "lab.yaml", copied_root / "config" / "lab.yaml")
    for item in registry_payload:
        assert (copied_root / item["path"]).exists()


def test_portable_path_helpers_handle_relative_and_reject_traversal(tmp_path: Path) -> None:
    target = tmp_path / "research" / "demo_study" / "results" / "metrics.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("{}", encoding="utf-8")

    assert portable_relative_path(target, tmp_path) == "research/demo_study/results/metrics.json"
    assert portable_relative_path(Path("research/demo_study/results/metrics.json"), tmp_path) == (
        "research/demo_study/results/metrics.json"
    )
    assert resolve_portable_path("research/demo_study/results/metrics.json", tmp_path) == target.resolve()

    with pytest.raises(ValueError):
        resolve_portable_path("../outside.json", tmp_path)

    with pytest.raises(ValueError):
        portable_relative_path(tmp_path.parent / "outside.json", tmp_path)

    with pytest.raises(ValueError):
        resolve_portable_path("/absolute/path.json", tmp_path)
