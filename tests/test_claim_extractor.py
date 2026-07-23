from pathlib import Path
import hashlib
import json

import yaml

from ai_research_lab.agent import ResearchAgent
from ai_research_lab.claim_extractor import default_claim, load_claim, save_claim


def test_default_claim_roundtrip(tmp_path: Path) -> None:
    claim = default_claim()
    claim_path = tmp_path / "claim.json"
    save_claim(claim_path, claim)

    loaded = load_claim(claim_path)
    assert loaded.claim_id == claim.claim_id
    assert loaded.text == claim.text
    assert loaded.source == claim.source


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
                "replicates": 8,
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


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_claim_bytes_remain_unchanged_after_agent_run(tmp_path: Path) -> None:
    _write_config(tmp_path)
    claim_path = tmp_path / "research" / "demo_study" / "claims" / "claim.json"
    claim_path.parent.mkdir(parents=True, exist_ok=True)
    claim = default_claim()
    save_claim(claim_path, claim)

    before_bytes = claim_path.read_bytes()
    before_sha = _sha256_bytes(before_bytes)
    before_payload = json.loads(before_bytes.decode("utf-8"))

    result = ResearchAgent(root_dir=tmp_path).run("demo_study")

    after_bytes = claim_path.read_bytes()
    after_sha = _sha256_bytes(after_bytes)
    after_payload = json.loads(after_bytes.decode("utf-8"))

    assert result.error_message is None
    assert before_bytes == after_bytes
    assert before_sha == after_sha
    assert before_payload == after_payload
