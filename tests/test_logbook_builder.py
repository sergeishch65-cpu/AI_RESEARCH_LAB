from pathlib import Path

from ai_research_lab.artifact_registry import register_artifacts
from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import LabConfig, SuccessCriteria
from ai_research_lab.experiment_planner import build_demo_plan
from ai_research_lab.experiment_runner import ExperimentRunner
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

