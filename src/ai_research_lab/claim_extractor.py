from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import ExpectedDirection, ResearchClaim

DEFAULT_CLAIM_TEXT = (
    "При увеличении количества независимых выборок оценка среднего значения стандартного "
    "нормального распределения в среднем приближается к истинному среднему, равному нулю."
)


def default_claim() -> ResearchClaim:
    return ResearchClaim(
        claim_id="claim-standard-normal-mean",
        text=DEFAULT_CLAIM_TEXT,
        source="demo_study",
        expected_direction=ExpectedDirection.DECREASE,
        metric="absolute_error_of_mean_estimate",
        target_value=0.0,
        tolerance=0.05,
        status="PLANNED",
    )


def load_claim(path: Path) -> ResearchClaim:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload.pop("updated_at", None)
    return ResearchClaim.model_validate(payload)


def save_claim(path: Path, claim: ResearchClaim) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = claim.model_dump(mode="json")
    payload["updated_at"] = datetime.now(timezone.utc).isoformat()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_or_create_claim(path: Path) -> ResearchClaim:
    if path.exists():
        return load_claim(path)
    claim = default_claim()
    save_claim(path, claim)
    return claim


def extract_claim_from_text(text: str, source: str = "manual_note") -> ResearchClaim:
    lowered = text.lower()
    if "normal" in lowered and "mean" in lowered:
        return default_claim().model_copy(update={"source": source, "text": text})
    return ResearchClaim(
        claim_id=f"claim-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        text=text,
        source=source,
        expected_direction=ExpectedDirection.NO_CHANGE,
        metric="unspecified",
        target_value=0.0,
        tolerance=0.0,
        status="PLANNED",
    )
