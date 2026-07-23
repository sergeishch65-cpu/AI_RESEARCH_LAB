from pathlib import Path

import yaml

from ai_research_lab.agent import ResearchAgent
from ai_research_lab.experiment_runner import ExperimentRunner


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
                "replicates": 4,
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


def test_agent_returns_failed_result_on_exception(tmp_path: Path, monkeypatch) -> None:
    _write_config(tmp_path)

    def boom(self, study_root, plan):  # type: ignore[no-untyped-def]
        raise RuntimeError("boom")

    monkeypatch.setattr(ExperimentRunner, "run", boom)

    agent = ResearchAgent(root_dir=tmp_path)
    result = agent.run("demo_study")

    assert result.status.value == "FAILED"
    assert "boom" in (result.error_message or "")

