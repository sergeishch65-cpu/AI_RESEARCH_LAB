from ai_research_lab.cli import cmd_doctor, main


def test_cli_commands_run_successfully() -> None:
    assert cmd_doctor() == 0
    assert main(["verify", "demo_study"]) == 0
    assert main(["build-logbook", "demo_study"]) == 0

