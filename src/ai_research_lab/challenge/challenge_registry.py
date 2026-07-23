from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import CompetitionStudy, PaperCandidate


class ChallengeRegistry:
    def __init__(self, root_dir: Path) -> None:
        self.root_dir = Path(root_dir).resolve()
        self.path = self.root_dir / "research" / "challenge_registry.json"

    def load(self) -> dict:
        if not self.path.exists():
            return {"paper_candidates": [], "studies": [], "updated_at": None}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def save(self, payload: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload["updated_at"] = datetime.now(timezone.utc).isoformat()
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def upsert_paper_candidate(self, candidate: PaperCandidate) -> None:
        payload = self.load()
        candidates = [PaperCandidate.model_validate(item) for item in payload.get("paper_candidates", [])]
        candidates = [item for item in candidates if item.paper_id != candidate.paper_id]
        candidates.append(candidate)
        payload["paper_candidates"] = [item.model_dump(mode="json") for item in candidates]
        self.save(payload)

    def register_study(self, study: CompetitionStudy) -> None:
        payload = self.load()
        studies = [CompetitionStudy.model_validate(item) for item in payload.get("studies", [])]
        studies = [item for item in studies if item.study_id != study.study_id]
        studies.append(study)
        payload["studies"] = [item.model_dump(mode="json") for item in studies]
        self.save(payload)

    def study_exists(self, study_id: str) -> bool:
        payload = self.load()
        return any(item.get("study_id") == study_id for item in payload.get("studies", []))
