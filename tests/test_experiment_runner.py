from pathlib import Path

from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import LabConfig, SuccessCriteria
from ai_research_lab.experiment_planner import build_demo_plan
from ai_research_lab.experiment_runner import ExperimentRunner


def _config() -> LabConfig:
    return LabConfig(
        project_name="AI_RESEARCH_LAB",
        default_study="demo_study",
        safe_experiment_type="mean_convergence",
        sample_sizes=[10, 100, 1000, 10000],
        replicates=16,
        seed=20260723,
        figure_name="convergence.png",
        success_criteria=SuccessCriteria(
            final_mean_abs_error_max=0.05,
            final_error_better_than_initial=True,
        ),
    )


def test_runner_creates_artifacts_and_is_deterministic(tmp_path: Path) -> None:
    study_root = tmp_path / "research" / "demo_study"
    study_root.mkdir(parents=True, exist_ok=True)
    plan = build_demo_plan(default_claim(), _config())
    runner = ExperimentRunner()

    result_one = runner.run(study_root, plan)
    result_two = runner.run(study_root, plan)

    assert result_one.status in {result_one.status.VERIFIED, result_one.status.NOT_REPRODUCED}
    assert result_one.metrics == result_two.metrics
    assert (study_root / "figures" / "convergence.png").exists()
    assert (study_root / "results" / "metrics.json").exists()
    assert (study_root / "experiments" / plan.experiment_id / "raw_results.json").exists()

