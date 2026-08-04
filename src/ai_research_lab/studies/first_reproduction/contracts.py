from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .artifact_names import StudyArtifactNames
from .status import StudyStatus


class StudyClaim(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    claim_id: str
    paper: str
    dataset: str
    subset: str
    population: str
    task: str
    model: str
    conformal_method: str
    comparator: str
    metric: str
    reported_result: str
    expected_direction: str
    tolerance: str
    repetitions: int
    seed_policy: str
    source_evidence: list[str] = Field(default_factory=list)


class StudyProtocol(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    dataset: str
    subset: str
    users: str
    preprocessing: list[str] = Field(default_factory=list)
    split_strategy: list[str] = Field(default_factory=list)
    model: str
    conformal_method: str
    comparator: str
    primary_metric: str
    secondary_metric: str | None = None
    repetitions: int
    seeds: list[int] = Field(default_factory=list)


class StudyArtifacts(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    names: StudyArtifactNames = Field(default_factory=StudyArtifactNames)


class StudyResult(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    status: StudyStatus = StudyStatus.CREATED
    notes: list[str] = Field(default_factory=list)
    artifacts: StudyArtifacts = Field(default_factory=StudyArtifacts)

