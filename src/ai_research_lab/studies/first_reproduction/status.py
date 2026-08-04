from __future__ import annotations

from enum import Enum


class StudyStatus(str, Enum):
    CREATED = "CREATED"
    SPECIFIED = "SPECIFIED"
    DATA_PENDING = "DATA_PENDING"
    READY = "READY"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    FAILED = "FAILED"
    VERIFIED = "VERIFIED"

