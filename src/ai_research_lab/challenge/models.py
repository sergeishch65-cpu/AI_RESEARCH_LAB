from __future__ import annotations

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class TokenSourceCategory(str, Enum):
    NONE = "NONE"
    HF_ENV_TOKEN = "HF_ENV_TOKEN"
    HF_CACHE_TOKEN = "HF_CACHE_TOKEN"
    HF_LOCAL_CACHE = "HF_LOCAL_CACHE"
    UNKNOWN = "UNKNOWN"


class WriteReadiness(str, Enum):
    VERIFIED = "VERIFIED"
    NOT_VERIFIED = "NOT_VERIFIED"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"


class PublicationStatus(str, Enum):
    NOT_CONFIGURED = "NOT_CONFIGURED"
    LOCAL_ONLY = "LOCAL_ONLY"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED_FOR_PUBLICATION = "APPROVED_FOR_PUBLICATION"
    PUBLISHED = "PUBLISHED"
    FAILED = "FAILED"


class SubmissionStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    BLOCKED = "BLOCKED"
    READY_FOR_REVIEW = "READY_FOR_REVIEW"
    APPROVED = "APPROVED"
    SUBMITTED = "SUBMITTED"
    FAILED = "FAILED"


class SelectionStatus(str, Enum):
    NOT_SELECTED = "NOT_SELECTED"
    SHORTLISTED = "SHORTLISTED"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class ChallengeConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    challenge_id: str
    challenge_space: str
    guide_url: str
    organization: str
    starts_at: datetime
    ends_at: datetime
    publication_required: bool
    trackio_required: bool
    source_urls: list[str] = Field(default_factory=list)
    trackio_local_dir: str = ".trackio"
    default_study_dir: str = "research/_templates/icml_2026_reproduction"
    publication_enabled: bool = False
    submission_enabled: bool = False
    network_actions_requiring_approval: bool = True
    cost_limit_usd: float = Field(default=0.0, ge=0.0)


class ChallengeCostPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    max_local_cost_usd: float = Field(default=0.0, ge=0.0)
    max_remote_cost_usd: float = Field(default=0.0, ge=0.0)
    cloud_gpu_allowed: bool = False
    hf_jobs_allowed: bool = False
    paid_api_allowed: bool = False
    publication_allowed: bool = False
    submission_allowed: bool = False


class PaperCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    paper_id: str
    title: str
    authors: list[str]
    paper_url: str
    code_url: str | None = None
    dataset_urls: list[str] = Field(default_factory=list)
    claimed_result: str
    estimated_compute: str
    selected: bool = False
    selection_status: SelectionStatus = SelectionStatus.NOT_SELECTED


class CompetitionStudy(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    study_id: str
    paper_id: str
    challenge_id: str
    local_path: Path
    trackio_project: str
    trackio_run_id: str | None = None
    remote_logbook_id: str | None = None
    publication_status: PublicationStatus = PublicationStatus.NOT_CONFIGURED
    submission_status: SubmissionStatus = SubmissionStatus.NOT_STARTED


class AuthStatus(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    cli_installed: bool
    authenticated: bool
    username: str | None = None
    token_source_category: TokenSourceCategory = TokenSourceCategory.NONE
    write_readiness: WriteReadiness = WriteReadiness.NOT_AUTHENTICATED
    checked_at: datetime


class SourceProvenance(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    url: str
    accessed_at: datetime
    purpose: str
    local_text_path: str | None = None
    local_text_sha256: str | None = None
    claims: list[str] = Field(default_factory=list)


class PublicationManifest(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    manifest_id: str
    challenge_id: str
    study_id: str
    paper_id: str
    prepared_at: datetime
    trackio_project: str
    trackio_run_id: str | None = None
    local_logbook_path: str
    local_run_summary_path: str | None = None
    artifact_paths: list[str] = Field(default_factory=list)
    source_provenance_paths: list[str] = Field(default_factory=list)
    registry_integrity: bool = False
    approval_recorded: bool = False
    publication_flag: bool = False
    notes: list[str] = Field(default_factory=list)


class TrackioRunSummary(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    project: str
    run_name: str
    trackio_dir: str
    started_at: datetime
    finished_at: datetime | None = None
    parameters: dict[str, Any] = Field(default_factory=dict)
    metrics: list[dict[str, Any]] = Field(default_factory=list)
    artifact_references: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    local_db_files: list[str] = Field(default_factory=list)
    remote_side_effects: list[str] = Field(default_factory=list)


class TrackioRunVerification(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    verified: bool
    reasons: list[str] = Field(default_factory=list)
    summary_path: str | None = None


class AuthStatusReport(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    auth_status: AuthStatus
    installed_version: str | None = None
    cli_path: str | None = None
