from pathlib import Path

from ai_research_lab.challenge.config import load_challenge_config, load_cost_policy


def test_challenge_config_parsing_and_policy() -> None:
    root = Path(__file__).resolve().parents[1]
    config = load_challenge_config(root / "config" / "challenge_icml_2026.yaml")
    policy = load_cost_policy(root / "config" / "challenge_cost_policy.yaml")

    assert config.challenge_id == "ICML-2026-agent-repro"
    assert config.publication_enabled is False
    assert config.submission_enabled is False
    assert config.cost_limit_usd == 0.0
    assert config.source_urls
    assert policy.publication_allowed is False
    assert policy.submission_allowed is False
    assert policy.max_remote_cost_usd == 0.0
    assert all("token" not in url.lower() for url in config.source_urls)
