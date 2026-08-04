"""First reproduction study skeleton."""

from .artifact_names import FIRST_REPRODUCTION_ARTIFACTS, StudyArtifactNames
from .contracts import StudyArtifacts, StudyClaim, StudyProtocol, StudyResult
from .metadata import STUDY_ID, STUDY_VERSION, SPECIFICATION_VERSION, StudyMetadata
from .status import StudyStatus

__all__ = [
    "FIRST_REPRODUCTION_ARTIFACTS",
    "SPECIFICATION_VERSION",
    "STUDY_ID",
    "STUDY_VERSION",
    "StudyArtifactNames",
    "StudyArtifacts",
    "StudyClaim",
    "StudyMetadata",
    "StudyProtocol",
    "StudyResult",
    "StudyStatus",
]
