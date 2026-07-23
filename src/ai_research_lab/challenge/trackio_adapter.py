from __future__ import annotations

import json
import os
import tempfile
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import TrackioRunSummary, TrackioRunVerification


class LocalTrackioAdapter:
    def __init__(
        self,
        project: str,
        run_name: str | None = None,
        trackio_dir: Path | None = None,
    ) -> None:
        self.project = project
        self.run_name = run_name or "local-smoke"
        self.trackio_dir = Path(trackio_dir or Path.cwd() / ".trackio").resolve()
        self._trackio = None
        self._run = None
        self._started_at: datetime | None = None
        self._finished_at: datetime | None = None
        self._parameters: dict[str, Any] = {}
        self._metrics: list[dict[str, Any]] = []
        self._artifact_references: list[str] = []
        self._notes: list[str] = []
        self._summary_path = self.trackio_dir / f"{self.project}__{self.run_name}__summary.json"

    def _prepare_env(self) -> None:
        self.trackio_dir.mkdir(parents=True, exist_ok=True)
        os.environ["TRACKIO_DIR"] = str(self.trackio_dir)

    def _import_trackio(self):
        if self._trackio is None:
            self._prepare_env()
            import trackio  # local import so TRACKIO_DIR is honored

            self._trackio = trackio
            self._reset_trackio_paths()
        return self._trackio

    def _reset_trackio_paths(self) -> None:
        if self._trackio is None:
            return
        trackio_dir = self.trackio_dir
        media_dir = trackio_dir / "media"
        artifacts_dir = trackio_dir / "artifacts"
        module_names = [
            "trackio",
            "trackio.utils",
            "trackio.sqlite_storage",
            "trackio.bucket_storage",
            "trackio.logbook",
            "trackio.run",
            "trackio.artifact",
        ]
        for module_name in module_names:
            module = sys.modules.get(module_name)
            if module is None:
                continue
            if hasattr(module, "TRACKIO_DIR"):
                setattr(module, "TRACKIO_DIR", trackio_dir)
            if hasattr(module, "MEDIA_DIR"):
                setattr(module, "MEDIA_DIR", media_dir)
            if hasattr(module, "ARTIFACTS_DIR"):
                setattr(module, "ARTIFACTS_DIR", artifacts_dir)

    def start_run(self) -> object:
        trackio = self._import_trackio()
        self._started_at = datetime.now(timezone.utc)
        self._run = trackio.init(
            project=self.project,
            name=self.run_name,
            embed=False,
            auto_log_cpu=False,
            auto_log_gpu=False,
            space_id=None,
            server_url=None,
            dataset_id=None,
            bucket_id=None,
        )
        return self._run

    def log_parameters(self, parameters: dict[str, Any]) -> None:
        self._parameters.update(parameters)
        if self._run is not None:
            self._run.config.update(parameters)

    def log_metric(self, name: str, value: float | int, step: int | None = None) -> None:
        trackio = self._import_trackio()
        self._metrics.append({"name": name, "value": value, "step": step})
        trackio.log({name: value}, step=step)

    def log_artifact_reference(self, path: str | Path, name: str | None = None, type: str | None = None) -> None:
        trackio = self._import_trackio()
        reference_path = Path(path).resolve()
        reference = reference_path.as_uri()
        self._artifact_references.append(reference)
        if self._run is not None and reference_path.exists():
            artifact = trackio.Artifact(name=name or reference_path.stem, type=type or "unspecified")
            artifact.add_reference(reference)
            self._run.log_artifact(artifact)

    def log_note(self, note: str) -> None:
        self._notes.append(note)

    def finish_run(self) -> TrackioRunSummary:
        trackio = self._import_trackio()
        if self._run is not None:
            trackio.finish()
        self._finished_at = datetime.now(timezone.utc)
        summary = self.get_local_run_summary()
        self._summary_path.write_text(
            json.dumps(summary.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return summary

    def get_local_run_summary(self) -> TrackioRunSummary:
        local_db_files = sorted(
            str(path.relative_to(self.trackio_dir))
            for path in self.trackio_dir.glob("*.db")
            if path.is_file()
        )
        if self._run is not None and getattr(self._run, "id", None):
            run_id = str(self._run.id)
        else:
            run_id = self.run_name
        return TrackioRunSummary(
            project=self.project,
            run_name=run_id,
            trackio_dir=str(self.trackio_dir),
            started_at=self._started_at or datetime.now(timezone.utc),
            finished_at=self._finished_at,
            parameters=dict(self._parameters),
            metrics=list(self._metrics),
            artifact_references=list(self._artifact_references),
            notes=list(self._notes),
            local_db_files=local_db_files,
            remote_side_effects=[],
        )

    def verify_run(self) -> TrackioRunVerification:
        reasons: list[str] = []
        if self._run is None:
            reasons.append("Run не был запущен.")
        if not self.trackio_dir.exists():
            reasons.append("Локальный TRACKIO_DIR не создан.")
        db_files = sorted(self.trackio_dir.glob("*.db"))
        if not db_files:
            reasons.append("Локальная Trackio-база не найдена.")
        if self._run is not None:
            if getattr(self._run, "space_id", None):
                reasons.append("Run привязан к Space, а не к локальному режиму.")
            if getattr(self._run, "server_url", None):
                reasons.append("Run привязан к удалённому серверу.")
        verified = not reasons
        summary_path = str(self._summary_path) if self._summary_path.exists() else None
        return TrackioRunVerification(verified=verified, reasons=reasons, summary_path=summary_path)


def run_local_trackio_smoke(
    *,
    project: str,
    run_name: str,
    seed: int,
    sample_sizes: list[int],
    mean_abs_errors: list[float],
    final_status: str,
) -> TrackioRunVerification:
    with tempfile.TemporaryDirectory(prefix="ai-research-lab-trackio-") as tmp:
        adapter = LocalTrackioAdapter(project=project, run_name=run_name, trackio_dir=Path(tmp) / ".trackio")
        adapter.start_run()
        adapter.log_parameters({"seed": seed, "sample_sizes": sample_sizes})
        for step, value in enumerate(mean_abs_errors):
            adapter.log_metric("mean_abs_error", value, step=step)
        adapter.log_note(f"final_status={final_status}")
        adapter.finish_run()
        return adapter.verify_run()
