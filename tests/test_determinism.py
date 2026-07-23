from pathlib import Path

from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import LabConfig, SuccessCriteria
from ai_research_lab.experiment_planner import build_demo_plan
from ai_research_lab.experiment_runner import ExperimentRunner


def _plan(seed: int) -> tuple[Path, object]:
    config = LabConfig(
        project_name="AI_RESEARCH_LAB",
        default_study="demo_study",
        safe_experiment_type="mean_convergence",
        sample_sizes=[10, 100, 1000, 10000],
        replicates=8,
        seed=seed,
        figure_name="convergence.png",
        success_criteria=SuccessCriteria(
            final_mean_abs_error_max=0.05,
            final_error_better_than_initial=True,
        ),
    )
    return Path("/tmp"), build_demo_plan(default_claim(), config)


def test_same_seed_produces_same_metrics(tmp_path: Path) -> None:
    study_one = tmp_path / "research" / "one"
    study_two = tmp_path / "research" / "two"
    study_one.mkdir(parents=True, exist_ok=True)
    study_two.mkdir(parents=True, exist_ok=True)
    _, plan = _plan(20260723)
    runner = ExperimentRunner()

    result_one = runner.run(study_one, plan)
    result_two = runner.run(study_two, plan)

    assert result_one.metrics == result_two.metrics
