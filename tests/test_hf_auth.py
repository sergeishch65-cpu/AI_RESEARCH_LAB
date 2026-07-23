from ai_research_lab.challenge.hf_auth import get_hf_auth_report
from ai_research_lab.challenge.models import WriteReadiness


def test_hf_auth_report_without_login_is_safe() -> None:
    report = get_hf_auth_report()

    assert report.auth_status.cli_installed is True
    assert report.auth_status.authenticated is False
    assert report.auth_status.username is None
    assert report.auth_status.token_source_category.value == "NONE"
    assert report.auth_status.write_readiness == WriteReadiness.NOT_AUTHENTICATED
    assert report.cli_path is not None
