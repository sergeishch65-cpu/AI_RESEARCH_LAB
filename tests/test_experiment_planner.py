from pathlib import Path

import yaml

from ai_research_lab.claim_extractor import default_claim
from ai_research_lab.config import load_lab_config
from ai_research_lab.experiment_planner import build_demo_plan, validate_plan


def test_build_and_validate_plan(tmp_path: Path) -> None:
    config_path = tmp_path / "config" / "lab.yaml"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        yaml.safe_dump(
            {
                "project_name": "AI_RESEARCH_LAB",
                "default_study": "demo_study",
                "safe_experiment_type": "mean_convergence",
                "sample_sizes": [10, 100, 1000, 10000],
                "replicates": 8,
                "seed": 123,
                "figure_name": "convergence.png",
                "success_criteria": {
                    "final_mean_abs_error_max": 0.2,
                    "final_error_better_than_initial": True,
                },
            }
        ),
        encoding="utf-8",
    )
    config = load_lab_config(root_dir=tmp_path)
    plan = build_demo_plan(default_claim(), config)
    validate_plan(plan)
    assert plan.parameters["sample_sizes"] == [10, 100, 1000, 10000]
    assert plan.parameters["experiment_type"] == "mean_convergence"

