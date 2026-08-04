from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class StudyArtifactNames:
    source_record: str = "source_record.json"
    claim: str = "claim.json"
    experiment_plan: str = "experiment_plan.json"
    data_manifest: str = "data_manifest.json"
    raw_results_csv: str = "raw_results.csv"
    raw_results_json: str = "raw_results.json"
    metrics: str = "metrics.json"
    experiment_result: str = "experiment_result.json"
    experiment_log: str = "experiment.log"
    logbook: str = "LOGBOOK.md"
    artifact_registry: str = "artifact_registry.json"
    reproduction_report: str = "REPRODUCTION_REPORT.md"
    verification_result: str = "verification_result.json"


FIRST_REPRODUCTION_ARTIFACTS = StudyArtifactNames()

