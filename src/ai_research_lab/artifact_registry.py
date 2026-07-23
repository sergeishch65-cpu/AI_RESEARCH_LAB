from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .models import ArtifactRecord, ArtifactType
from .paths import ensure_within_root


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_artifact(path: Path) -> ArtifactType:
    name = path.name.lower()
    suffix = path.suffix.lower()
    if name == "logbook.md":
        return ArtifactType.LOGBOOK
    if suffix == ".png":
        return ArtifactType.FIGURE
    if suffix == ".csv":
        return ArtifactType.RAW_RESULTS
    if suffix == ".json" and "metrics" in name:
        return ArtifactType.METRICS
    if suffix == ".json" and "claim" in name:
        return ArtifactType.CLAIM
    if suffix == ".json" and "plan" in name:
        return ArtifactType.PLAN
    if suffix in {".md", ".txt"} and "log" in name:
        return ArtifactType.LOG
    if suffix == ".ipynb":
        return ArtifactType.NOTEBOOK
    return ArtifactType.OTHER


def register_artifacts(
    study_root: Path,
    experiment_id: str,
    artifact_paths: Iterable[Path],
) -> list[ArtifactRecord]:
    registry_path = study_root / "logs" / "artifact_registry.json"
    registry_path.parent.mkdir(parents=True, exist_ok=True)

    records: list[ArtifactRecord] = []
    for artifact_path in artifact_paths:
        resolved = artifact_path if artifact_path.is_absolute() else (study_root / artifact_path)
        resolved = ensure_within_root(study_root, resolved)
        if not resolved.exists():
            raise FileNotFoundError(f"Артефакт не найден: {resolved}")
        records.append(
            ArtifactRecord(
                artifact_id=f"{experiment_id}:{resolved.relative_to(study_root).as_posix()}",
                artifact_type=classify_artifact(resolved),
                path=str(resolved),
                sha256=sha256_file(resolved),
                created_at=datetime.now(timezone.utc).isoformat(),
                experiment_id=experiment_id,
            )
        )

    registry_path.write_text(
        json.dumps([record.model_dump(mode="json") for record in records], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    return records

