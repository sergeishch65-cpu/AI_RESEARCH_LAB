from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest
import yaml

from ai_research_lab.agent import ResearchAgent
from ai_research_lab.artifact_registry import register_artifacts
from ai_research_lab.challenge.verifier import secret_scan, verify_existing_demo_baseline
from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import LabConfig, SuccessCriteria
from ai_research_lab.experiment_planner import build_demo_plan
from ai_research_lab.experiment_runner import ExperimentRunner
from ai_research_lab.models import ExperimentPlan, ExperimentResult
from ai_research_lab.logbook_builder import build_logbook


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


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _demo_study_paths(root: Path) -> dict[str, Path]:
    study_root = root / "research" / "demo_study"
    return {
        "study_root": study_root,
        "claim": study_root / "claims" / "claim.json",
        "experiment_result": study_root / "experiments" / "mean_convergence_demo" / "experiment_result.json",
        "metrics": study_root / "results" / "metrics.json",
        "logbook": study_root / "logbook" / "LOGBOOK.md",
        "registry": study_root / "logs" / "artifact_registry.json",
    }


def _run_demo(root: Path):
    _write_config(root)
    return ResearchAgent(root_dir=root).run("demo_study")


def test_secret_scan_is_clean() -> None:
    root = Path(__file__).resolve().parents[1]
    findings = secret_scan(root)

    assert findings == []


def test_existing_demo_hashes_remain_valid() -> None:
    root = Path(__file__).resolve().parents[1]
    try:
        snapshot = verify_existing_demo_baseline(root)
    except FileNotFoundError:
        pytest.skip("demo baseline artifacts are not present in this clean public worktree")

    assert snapshot.claim_sha == "f382e11e9461c0a65ff332e20e6e2dc8a869e3d41a488403136e425248e93673"
    assert snapshot.experiment_result_sha == "32b23c841a4197f3c2bc6beed27705e93c31fd9deacbdbcefb50c358f80c0588"
    assert snapshot.metrics_sha == "155cdbb9cfa4ffc6dc8e2589d62b7c89c5af2e5771f99c54c3fa35bbd164a39b"
    assert snapshot.logbook_sha == "58657e82f34c77ed4c9ff0bf7f391f96a5a8912cade05edf1810c5bea4df9092"
    assert snapshot.registry_sha == "5f5ad559b8cb62ea0768eada0c6900bbb1657406268386854f0c9eddd7e4bb53"


def test_logbook_contains_expected_sections(tmp_path: Path) -> None:
    study_root = tmp_path / "research" / "demo_study"
    study_root.mkdir(parents=True, exist_ok=True)
    config = LabConfig(
        project_name="AI_RESEARCH_LAB",
        default_study="demo_study",
        safe_experiment_type="mean_convergence",
        sample_sizes=[10, 100, 1000, 10000],
        replicates=8,
        seed=20260723,
        figure_name="convergence.png",
        success_criteria=SuccessCriteria(
            final_mean_abs_error_max=0.05,
            final_error_better_than_initial=True,
        ),
    )
    claim = default_claim()
    plan = build_demo_plan(claim, config)
    result = ExperimentRunner().run(study_root, plan)
    artifacts = register_artifacts(study_root, plan.experiment_id, [Path(path) for path in result.artifact_paths])
    logbook = build_logbook(study_root, "demo_study", claim, plan, result, artifacts)

    content = logbook.read_text(encoding="utf-8")
    assert "FACT" in content
    assert "INTERPRETATION" in content
    assert "LIMITATION" in content
    assert "NEXT STEP" in content
    assert "python -m ai_research_lab.cli run demo_study" in content


def test_logbook_registry_hash_is_stable_across_rebuilds(tmp_path: Path) -> None:
    _write_config(tmp_path)
    agent = ResearchAgent(root_dir=tmp_path)
    agent.run("demo_study")
    study_root = tmp_path / "research" / "demo_study"
    claim_path = study_root / "claims" / "claim.json"
    plan_path = study_root / "plans" / "experiment_plan.json"
    result_path = study_root / "experiments" / "mean_convergence_demo" / "experiment_result.json"

    claim = default_claim()
    plan = ExperimentPlan.model_validate_json(plan_path.read_text(encoding="utf-8"))
    result = ExperimentResult.model_validate_json(result_path.read_text(encoding="utf-8"))
    artifact_paths = [claim_path, plan_path, *[Path(path) for path in result.artifact_paths if Path(path).name != "LOGBOOK.md"]]

    artifacts_first = register_artifacts(study_root, plan.experiment_id, artifact_paths)
    logbook_first = build_logbook(study_root, "demo_study", claim, plan, result, artifacts_first)
    final_artifacts_first = register_artifacts(study_root, plan.experiment_id, artifact_paths + [logbook_first])
    registry_first = json.loads((study_root / "logs" / "artifact_registry.json").read_text(encoding="utf-8"))
    stored_first = next(item["sha256"] for item in registry_first if item["path"] == logbook_first.relative_to(tmp_path).as_posix())
    actual_first = _sha256(logbook_first)

    artifacts_second = register_artifacts(study_root, plan.experiment_id, artifact_paths)
    logbook_second = build_logbook(study_root, "demo_study", claim, plan, result, artifacts_second)
    final_artifacts_second = register_artifacts(study_root, plan.experiment_id, artifact_paths + [logbook_second])
    registry_second = json.loads((study_root / "logs" / "artifact_registry.json").read_text(encoding="utf-8"))
    stored_second = next(item["sha256"] for item in registry_second if item["path"] == logbook_second.relative_to(tmp_path).as_posix())
    actual_second = _sha256(logbook_second)

    assert logbook_first.read_text(encoding="utf-8") == logbook_second.read_text(encoding="utf-8")
    assert stored_first == actual_first
    assert stored_second == actual_second
    assert final_artifacts_first[-1].sha256 == actual_first
    assert final_artifacts_second[-1].sha256 == actual_second


def test_baseline_normalization_ignores_wall_clock_drift(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    snapshot_root_a = tmp_path / "snapshot_a"
    snapshot_root_b = tmp_path / "snapshot_b"

    _run_demo(project_root)
    snapshot_root_a.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        project_root / "research" / "demo_study",
        snapshot_root_a / "research" / "demo_study",
    )
    _run_demo(project_root)
    snapshot_root_b.mkdir(parents=True, exist_ok=True)
    shutil.copytree(
        project_root / "research" / "demo_study",
        snapshot_root_b / "research" / "demo_study",
    )

    snapshot_a = verify_existing_demo_baseline(snapshot_root_a)
    snapshot_b = verify_existing_demo_baseline(snapshot_root_b)

    assert snapshot_a == snapshot_b


def test_baseline_verifier_does_not_rewrite_real_files(tmp_path: Path) -> None:
    _run_demo(tmp_path)
    paths = _demo_study_paths(tmp_path)
    before = {name: _sha256(path) for name, path in paths.items() if name != "study_root"}

    verify_existing_demo_baseline(tmp_path)

    after = {name: _sha256(path) for name, path in paths.items() if name != "study_root"}
    assert before == after


def test_baseline_detects_scientific_changes(tmp_path: Path) -> None:
    _run_demo(tmp_path)
    paths = _demo_study_paths(tmp_path)
    baseline = verify_existing_demo_baseline(tmp_path)

    payload = json.loads(paths["experiment_result"].read_text(encoding="utf-8"))
    payload["metrics"]["final_mean_abs_error"] = payload["metrics"]["final_mean_abs_error"] + 0.001
    paths["experiment_result"].write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    changed = verify_existing_demo_baseline(tmp_path)
    assert changed.experiment_result_sha != baseline.experiment_result_sha


def test_full_demo_regression_verifies_twice(tmp_path: Path) -> None:
    first_result = _run_demo(tmp_path)
    paths = _demo_study_paths(tmp_path)
    raw_first = {name: _sha256(path) for name, path in paths.items() if name != "study_root"}
    snapshot_first = verify_existing_demo_baseline(tmp_path)

    second_result = _run_demo(tmp_path)
    raw_second = {name: _sha256(path) for name, path in paths.items() if name != "study_root"}
    snapshot_second = verify_existing_demo_baseline(tmp_path)

    assert first_result.metrics == second_result.metrics
    assert raw_first["claim"] == raw_second["claim"]
    assert raw_first["metrics"] == raw_second["metrics"]
    assert raw_first["experiment_result"] != raw_second["experiment_result"]
    assert raw_first["registry"] != raw_second["registry"]
    assert raw_first["logbook"] != raw_second["logbook"]
    assert snapshot_first == snapshot_second
