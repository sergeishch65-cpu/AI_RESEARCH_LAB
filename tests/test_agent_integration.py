from pathlib import Path

import yaml

from ai_research_lab.agent import ResearchAgent


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
                "replicates": 16,
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


def test_agent_runs_end_to_end_in_temp_root(tmp_path: Path) -> None:
    _write_config(tmp_path)
    agent = ResearchAgent(root_dir=tmp_path)
    result = agent.run("demo_study")

    assert result.status.value in {"VERIFIED", "NOT_REPRODUCED"}
    assert (tmp_path / "research" / "demo_study" / "logbook" / "LOGBOOK.md").exists()
    assert (tmp_path / "research" / "demo_study" / "logs" / "artifact_registry.json").exists()

