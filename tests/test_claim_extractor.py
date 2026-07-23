from pathlib import Path

from ai_research_lab.claim_extractor import default_claim, load_claim, save_claim


def test_default_claim_roundtrip(tmp_path: Path) -> None:
    claim = default_claim()
    claim_path = tmp_path / "claim.json"
    save_claim(claim_path, claim)

    loaded = load_claim(claim_path)
    assert loaded.claim_id == claim.claim_id
    assert loaded.text == claim.text
    assert loaded.source == claim.source

