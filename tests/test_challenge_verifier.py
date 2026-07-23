from pathlib import Path

from ai_research_lab.challenge.verifier import secret_scan, verify_existing_demo_baseline


def test_secret_scan_is_clean() -> None:
    root = Path("/Users/sergej/Documents/AI_RESEARCH_LAB")
    findings = secret_scan(root)

    assert findings == []


def test_existing_demo_hashes_remain_valid() -> None:
    root = Path("/Users/sergej/Documents/AI_RESEARCH_LAB")
    snapshot = verify_existing_demo_baseline(root)

    assert snapshot.claim_sha == "f382e11e9461c0a65ff332e20e6e2dc8a869e3d41a488403136e425248e93673"
    assert snapshot.logbook_sha == "1e39f3cbd2dadab8e587de18c541c892516f029d677806555d60ccc8f363ff6f"
