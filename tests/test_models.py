from ai_research_lab.models import (
    ArtifactRecord,
    ArtifactType,
    ExpectedDirection,
    ExperimentPlan,
    ExperimentResult,
    ResearchClaim,
    WorkflowStatus,
)


def test_models_validate_and_serialize() -> None:
    claim = ResearchClaim(
        claim_id="claim-1",
        text="Example claim",
        source="paper",
        expected_direction=ExpectedDirection.DECREASE,
        metric="error",
        target_value=0.0,
        tolerance=0.1,
    )
    plan = ExperimentPlan(
        experiment_id="exp-1",
        claim_id=claim.claim_id,
        hypothesis="Hypothesis",
        method="Method",
        parameters={"experiment_type": "mean_convergence", "sample_sizes": [10], "replicates": 1},
        seed=1,
        expected_artifacts=["result.json"],
        success_criteria={"final_mean_abs_error_max": 0.1},
    )
    result = ExperimentResult(
        experiment_id=plan.experiment_id,
        started_at="2026-07-23T00:00:00+00:00",
        completed_at="2026-07-23T00:00:01+00:00",
        status=WorkflowStatus.COMPLETED,
        parameters=plan.parameters,
        metrics={"criterion_met": True},
        artifact_paths=["/tmp/result.json"],
        environment={"python": "3.13.1"},
    )
    artifact = ArtifactRecord(
        artifact_id="exp-1:result.json",
        artifact_type=ArtifactType.RAW_RESULTS,
        path="/tmp/result.json",
        sha256="a" * 64,
        created_at="2026-07-23T00:00:00+00:00",
        experiment_id="exp-1",
    )

    assert claim.claim_id == "claim-1"
    assert plan.claim_id == claim.claim_id
    assert result.status == WorkflowStatus.COMPLETED
    assert artifact.artifact_type == ArtifactType.RAW_RESULTS

