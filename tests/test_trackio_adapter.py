from pathlib import Path

from ai_research_lab.challenge.trackio_adapter import LocalTrackioAdapter


def test_local_trackio_adapter_smoke(tmp_path: Path) -> None:
    adapter = LocalTrackioAdapter(project="trackio-smoke-test", run_name="smoke", trackio_dir=tmp_path / ".trackio")
    run = adapter.start_run()
    adapter.log_parameters({"seed": 20260723, "sample_sizes": [10, 100, 1000, 10000]})
    for step, value in enumerate([0.25, 0.08, 0.02, 0.008]):
        adapter.log_metric("mean_abs_error", value, step=step)
    artifact = tmp_path / "artifact.txt"
    artifact.write_text("hello", encoding="utf-8")
    adapter.log_artifact_reference(artifact, name="artifact", type="text")
    adapter.log_note("final_status=VERIFIED")
    summary = adapter.finish_run()
    verification = adapter.verify_run()

    assert run is not None
    assert getattr(run, "space_id", None) is None
    assert getattr(run, "server_url", None) is None
    assert summary.project == "trackio-smoke-test"
    assert len(summary.metrics) == 4
    assert summary.notes[-1] == "final_status=VERIFIED"
    assert verification.verified is True
    assert verification.summary_path is not None
    assert Path(verification.summary_path).exists()
