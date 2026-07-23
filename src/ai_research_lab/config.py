from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

from .paths import config_path


class SuccessCriteria(BaseModel):
    model_config = ConfigDict(extra="forbid")

    final_mean_abs_error_max: float = Field(gt=0)
    final_error_better_than_initial: bool = True


class LabConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    project_name: str
    default_study: str
    safe_experiment_type: str
    sample_sizes: list[int]
    replicates: int = Field(gt=0)
    seed: int
    figure_name: str
    success_criteria: SuccessCriteria


def load_lab_config(path: Path | None = None, root_dir: Path | None = None) -> LabConfig:
    config_file = path or config_path(root_dir)
    data: dict[str, Any]
    with config_file.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return LabConfig.model_validate(data)
