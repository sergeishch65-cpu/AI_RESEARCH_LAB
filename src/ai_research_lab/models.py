from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkflowStatus(str, Enum):
    PLANNED = "PLANNED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"
    NOT_REPRODUCED = "NOT_REPRODUCED"


class ExpectedDirection(str, Enum):
    INCREASE = "INCREASE"
    DECREASE = "DECREASE"
    NO_CHANGE = "NO_CHANGE"


class ArtifactType(str, Enum):
    RAW_RESULTS = "RAW_RESULTS"
    METRICS = "METRICS"
    FIGURE = "FIGURE"
    LOGBOOK = "LOGBOOK"
    CLAIM = "CLAIM"
    PLAN = "PLAN"
    LOG = "LOG"
    NOTEBOOK = "NOTEBOOK"
    OTHER = "OTHER"


class ResearchClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    claim_id: str
    text: str
    source: str
    expected_direction: ExpectedDirection
    metric: str
    target_value: float
    tolerance: float = Field(ge=0)
    status: WorkflowStatus = WorkflowStatus.PLANNED


class ExperimentPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    experiment_id: str
    claim_id: str
    hypothesis: str
    method: str
    parameters: dict[str, Any]
    seed: int
    expected_artifacts: list[str]
    success_criteria: dict[str, Any]
    status: WorkflowStatus = WorkflowStatus.PLANNED


class ExperimentResult(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    experiment_id: str
    started_at: str
    completed_at: str
    status: WorkflowStatus
    parameters: dict[str, Any]
    metrics: dict[str, Any]
    artifact_paths: list[str]
    environment: dict[str, Any]
    error_message: str | None = None


class ArtifactRecord(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    artifact_id: str
    artifact_type: ArtifactType
    path: str
    sha256: str
    created_at: str
    experiment_id: str

