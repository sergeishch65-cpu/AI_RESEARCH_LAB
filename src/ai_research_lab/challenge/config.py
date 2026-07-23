from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .models import ChallengeConfig, ChallengeCostPolicy


def _load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Ожидался YAML-объект в {path}")
    return data


def load_challenge_config(path: Path) -> ChallengeConfig:
    return ChallengeConfig.model_validate(_load_yaml(path))


def load_cost_policy(path: Path) -> ChallengeCostPolicy:
    return ChallengeCostPolicy.model_validate(_load_yaml(path))
