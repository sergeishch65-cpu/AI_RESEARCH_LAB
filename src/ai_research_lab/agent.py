from __future__ import annotations

import json
from pathlib import Path

from .artifact_registry import register_artifacts
from .claim_extractor import load_or_create_claim, save_claim
from .config import load_lab_config
from .experiment_planner import build_demo_plan, validate_plan
from .experiment_runner import ExperimentRunner
from .logbook_builder import build_logbook
from .models import ExperimentResult, WorkflowStatus
from .paths import ensure_within_root, project_root, study_paths


class ResearchAgent:
    def __init__(self, root_dir: Path | None = None) -> None:
        self.root_dir = Path(root_dir or project_root()).resolve()
        self.config = load_lab_config(root_dir=self.root_dir)
        self.runner = ExperimentRunner()

    def _ensure_study_root(self, study_name: str) -> Path:
        paths = study_paths(study_name, base_root=self.root_dir)
        ensure_within_root(self.root_dir / "research", paths.root)
        for directory in [
            paths.root,
            paths.paper,
            paths.claims,
            paths.plans,
            paths.experiments,
            paths.results,
            paths.figures,
            paths.logs,
            paths.logbook,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
        return paths.root

    def _result_path(self, study_root: Path, experiment_id: str) -> Path:
        return study_root / "experiments" / experiment_id / "experiment_result.json"

    def _evaluate_result(self, result: ExperimentResult) -> WorkflowStatus:
        metrics = result.metrics
        final_ok = (
            bool(metrics.get("criterion_met"))
            and float(metrics["final_mean_abs_error"]) <= float(self.config.success_criteria.final_mean_abs_error_max)
        )
        return WorkflowStatus.VERIFIED if final_ok else WorkflowStatus.NOT_REPRODUCED

    def run(self, study_name: str) -> ExperimentResult:
        study_root = self._ensure_study_root(study_name)
        claim_path = study_root / "claims" / "claim.json"
        plan_path = study_root / "plans" / "experiment_plan.json"

        claim = load_or_create_claim(claim_path)
        save_claim(claim_path, claim)
        plan = build_demo_plan(claim, self.config)
        validate_plan(plan)
        plan_path.write_text(
            json.dumps(plan.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        try:
            result = self.runner.run(study_root, plan)
            artifact_paths = [
                claim_path,
                plan_path,
                *[Path(path) for path in result.artifact_paths],
            ]
            final_status = self._evaluate_result(result)
            result = result.model_copy(update={"status": final_status, "artifact_paths": [str(p) for p in artifact_paths]})
            self._result_path(study_root, plan.experiment_id).write_text(
                json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            artifacts = register_artifacts(study_root, plan.experiment_id, artifact_paths)
            logbook_path = build_logbook(study_root, study_name, claim, plan, result, artifacts)
            artifacts = register_artifacts(study_root, plan.experiment_id, artifact_paths + [logbook_path])
            result = result.model_copy(update={"artifact_paths": [str(p) for p in artifact_paths + [logbook_path]]})
            self._result_path(study_root, plan.experiment_id).write_text(
                json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return result
        except Exception as exc:
            failed_result = ExperimentResult(
                experiment_id=plan.experiment_id,
                started_at="",
                completed_at="",
                status=WorkflowStatus.FAILED,
                parameters=plan.parameters,
                metrics={"criterion_met": False},
                artifact_paths=[],
                environment={},
                error_message=str(exc),
            )
            self._result_path(study_root, plan.experiment_id).parent.mkdir(parents=True, exist_ok=True)
            self._result_path(study_root, plan.experiment_id).write_text(
                json.dumps(failed_result.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            return failed_result

    def verify(self, study_name: str) -> ExperimentResult:
        study_root = self._ensure_study_root(study_name)
        result_files = sorted((study_root / "experiments").glob("*/experiment_result.json"))
        if not result_files:
            raise FileNotFoundError("Не найден experiment_result.json.")
        result = ExperimentResult.model_validate_json(result_files[-1].read_text(encoding="utf-8"))
        status = self._evaluate_result(result)
        updated = result.model_copy(update={"status": status})
        result_files[-1].write_text(
            json.dumps(updated.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return updated
