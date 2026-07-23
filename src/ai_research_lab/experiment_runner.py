from __future__ import annotations

import json
import platform
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .models import ExperimentPlan, ExperimentResult, WorkflowStatus
from .paths import ensure_within_root, portable_relative_path


class ExperimentRunner:
    def __init__(self) -> None:
        self._versions = self._library_versions()

    @staticmethod
    def _library_versions() -> dict[str, str]:
        versions: dict[str, str] = {"python": platform.python_version(), "platform": platform.platform()}
        for package in ["numpy", "pandas", "matplotlib", "pydantic", "pyyaml"]:
            try:
                versions[package] = metadata.version(package)
            except metadata.PackageNotFoundError:
                versions[package] = "not-installed"
        return versions

    def _validate_inputs(self, study_root: Path, plan: ExperimentPlan) -> tuple[list[int], int]:
        sample_sizes = plan.parameters["sample_sizes"]
        if not isinstance(sample_sizes, list) or not sample_sizes:
            raise ValueError("sample_sizes должен быть непустым списком.")
        if sample_sizes != sorted(sample_sizes):
            raise ValueError("sample_sizes должен быть отсортирован.")
        if any(not isinstance(size, int) or size <= 0 for size in sample_sizes):
            raise ValueError("sample_sizes должен содержать положительные целые числа.")
        replicates = int(plan.parameters["replicates"])
        project_root_dir = study_root.resolve().parents[1]
        ensure_within_root(project_root_dir / "research", study_root)
        return sample_sizes, replicates

    def run(self, study_root: Path, plan: ExperimentPlan) -> ExperimentResult:
        started_at = datetime.now(timezone.utc)
        sample_sizes, replicates = self._validate_inputs(study_root, plan)
        project_root_dir = study_root.resolve().parents[1]

        experiment_dir = study_root / "experiments" / plan.experiment_id
        results_dir = study_root / "results"
        figures_dir = study_root / "figures"
        logs_dir = study_root / "logs"
        for directory in (experiment_dir, results_dir, figures_dir, logs_dir):
            directory.mkdir(parents=True, exist_ok=True)

        rng = np.random.default_rng(plan.seed)
        max_size = max(sample_sizes)
        draws = rng.standard_normal((replicates, max_size))
        cumulative = np.cumsum(draws, axis=1)

        raw_records: list[dict[str, Any]] = []
        for replicate_index in range(replicates):
            for sample_size in sample_sizes:
                estimate = float(cumulative[replicate_index, sample_size - 1] / sample_size)
                raw_records.append(
                    {
                        "experiment_id": plan.experiment_id,
                        "replicate": replicate_index,
                        "sample_size": sample_size,
                        "estimate": estimate,
                        "abs_error": abs(estimate),
                    }
                )

        raw_df = pd.DataFrame(raw_records)
        summary_df = (
            raw_df.groupby("sample_size", as_index=False)
            .agg(
                mean_estimate=("estimate", "mean"),
                mean_abs_error=("abs_error", "mean"),
                std_abs_error=("abs_error", "std"),
                max_abs_error=("abs_error", "max"),
            )
            .sort_values("sample_size")
        )

        summary_records = summary_df.to_dict(orient="records")
        final_row = summary_records[-1]
        initial_row = summary_records[0]
        threshold = float(plan.success_criteria["final_mean_abs_error_max"])
        criterion_met = bool(
            final_row["mean_abs_error"] < initial_row["mean_abs_error"]
            and final_row["mean_abs_error"] <= threshold
        )

        raw_json_path = experiment_dir / "raw_results.json"
        raw_csv_path = results_dir / "raw_results.csv"
        metrics_path = results_dir / "metrics.json"
        figure_path = figures_dir / "convergence.png"
        result_path = experiment_dir / "experiment_result.json"
        log_path = logs_dir / f"{plan.experiment_id}.log"

        raw_json_path.write_text(
            json.dumps(raw_records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        raw_df.to_csv(raw_csv_path, index=False)
        metrics_payload = {
            "summary_by_sample_size": summary_records,
            "final_mean_abs_error": final_row["mean_abs_error"],
            "initial_mean_abs_error": initial_row["mean_abs_error"],
            "criterion_met": criterion_met,
            "sample_sizes": sample_sizes,
            "replicates": replicates,
        }
        metrics_path.write_text(
            json.dumps(metrics_payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(
            summary_df["sample_size"],
            summary_df["mean_abs_error"],
            marker="o",
            linewidth=2,
            color="#0f766e",
        )
        ax.set_xscale("log")
        ax.set_xlabel("Размер выборки")
        ax.set_ylabel("Средняя абсолютная ошибка")
        ax.set_title("Сходимость оценки среднего стандартного нормального распределения")
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.5)
        fig.tight_layout()
        fig.savefig(figure_path, dpi=160)
        plt.close(fig)

        log_path.write_text(
            "\n".join(
                [
                    f"experiment_id={plan.experiment_id}",
                    f"started_at={started_at.isoformat()}",
                    f"completed_at={datetime.now(timezone.utc).isoformat()}",
                    f"criterion_met={criterion_met}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        status = WorkflowStatus.VERIFIED if criterion_met else WorkflowStatus.NOT_REPRODUCED
        result = ExperimentResult(
            experiment_id=plan.experiment_id,
            started_at=started_at.isoformat(),
            completed_at=datetime.now(timezone.utc).isoformat(),
            status=status,
            parameters=plan.parameters,
            metrics=metrics_payload,
            artifact_paths=[
                portable_relative_path(raw_json_path, project_root_dir),
                portable_relative_path(raw_csv_path, project_root_dir),
                portable_relative_path(metrics_path, project_root_dir),
                portable_relative_path(figure_path, project_root_dir),
                portable_relative_path(result_path, project_root_dir),
                portable_relative_path(log_path, project_root_dir),
            ],
            environment=self._versions,
            error_message=None,
        )
        result_path.write_text(
            json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return result
