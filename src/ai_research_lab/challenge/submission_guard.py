from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .models import AuthStatus, ChallengeConfig, ChallengeCostPolicy, PublicationStatus


class GuardDecision(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    allowed: bool
    status: str
    reasons: list[str] = Field(default_factory=list)


def publication_guard(
    *,
    auth_status: AuthStatus,
    challenge_config: ChallengeConfig,
    paper_selected: bool,
    study_verified: bool,
    trackio_run_verified: bool,
    registry_integrity: bool,
    logbook_exists: bool,
    manifest_complete: bool,
    secret_scan_clean: bool,
    user_approval_recorded: bool,
    publication_flag: bool,
    cost_policy: ChallengeCostPolicy,
) -> GuardDecision:
    reasons: list[str] = []
    if not auth_status.authenticated:
        reasons.append("Пользователь не авторизован в Hugging Face.")
    if auth_status.write_readiness.name != "VERIFIED":
        reasons.append("Write readiness не подтверждена безопасным способом.")
    if not paper_selected:
        reasons.append("Статья не выбрана явно.")
    if not study_verified:
        reasons.append("Study не verified.")
    if not trackio_run_verified:
        reasons.append("Trackio run не verified.")
    if not registry_integrity:
        reasons.append("Registry integrity = false.")
    if not logbook_exists:
        reasons.append("Logbook отсутствует.")
    if not manifest_complete:
        reasons.append("Publication manifest неполный.")
    if not secret_scan_clean:
        reasons.append("Secret scan нашёл проблемы.")
    if not user_approval_recorded:
        reasons.append("Подтверждение пользователя не записано.")
    if not publication_flag:
        reasons.append("Флаг публикации явно не передан.")
    if not challenge_config.publication_enabled:
        reasons.append("Публикация отключена в challenge config.")
    if not cost_policy.publication_allowed:
        reasons.append("Политика затрат запрещает публикацию.")
    return GuardDecision(allowed=not reasons, status="PUBLISHED" if not reasons else "BLOCKED", reasons=reasons)


def submission_guard(
    *,
    publication_status: PublicationStatus,
    remote_logbook_id: str | None,
    challenge_required_fields_complete: bool,
    user_approval_recorded: bool,
    submission_flag: bool,
    challenge_config: ChallengeConfig,
    cost_policy: ChallengeCostPolicy,
) -> GuardDecision:
    reasons: list[str] = []
    if publication_status != PublicationStatus.PUBLISHED:
        reasons.append("Publication status не PUBLISHED.")
    if not remote_logbook_id:
        reasons.append("Remote logbook ID отсутствует.")
    if not challenge_required_fields_complete:
        reasons.append("Challenge-required fields неполны.")
    if not user_approval_recorded:
        reasons.append("Подтверждение пользователя не записано.")
    if not submission_flag:
        reasons.append("Флаг submission явно не передан.")
    if not challenge_config.submission_enabled:
        reasons.append("Submission отключён в challenge config.")
    if not cost_policy.submission_allowed:
        reasons.append("Политика затрат запрещает submission.")
    return GuardDecision(allowed=not reasons, status="SUBMITTED" if not reasons else "BLOCKED", reasons=reasons)
