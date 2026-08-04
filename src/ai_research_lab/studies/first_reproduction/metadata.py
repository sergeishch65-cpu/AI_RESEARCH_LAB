from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

from .status import StudyStatus

STUDY_ID = "repro-wisdm-ucm-rf"
SPECIFICATION_VERSION = "1.0"
STUDY_VERSION = "0.1"


class StudyMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    study_id: str = STUDY_ID
    paper: str = "Conformal Prediction in Multi-User Settings: An Evaluation"
    dataset: str = "WISDM Activity Prediction v1.1 transformed dataset"
    claim_id: str = "wisdm-ucm-rf-coverage-v1"
    specification_version: str = SPECIFICATION_VERSION
    study_version: str = STUDY_VERSION
    status: StudyStatus = Field(default=StudyStatus.CREATED)

