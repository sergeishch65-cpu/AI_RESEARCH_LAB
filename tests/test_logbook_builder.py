from pathlib import Path
import hashlib
import json

from ai_research_lab.artifact_registry import register_artifacts
from ai_research_lab.agent import ResearchAgent
from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import LabConfig, SuccessCriteria
from ai_research_lab.experiment_planner import build_demo_plan
from ai_research_lab.experiment_runner import ExperimentRunner
from ai_research_lab.models import ExperimentPlan, ExperimentResult
from ai_research_lab.logbook_builder import build_logbook


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


def _write_config(root: Path) -> None:
    import yaml

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
