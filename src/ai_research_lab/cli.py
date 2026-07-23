from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from .agent import ResearchAgent
from .artifact_registry import register_artifacts
from .claim_extractor import load_claim
from .config import load_lab_config
from .models import ExperimentPlan, ExperimentResult
from .logbook_builder import build_logbook
from .paths import config_path, project_root, research_root, study_paths, validate_study_name


def _print(msg: str) -> None:
    print(msg)


def cmd_doctor() -> int:
    problems: list[str] = []
    root = project_root()
    python_bin = Path(sys.executable)
    jupyter_bin = python_bin.with_name("jupyter")
    _print(f"Проект: {root}")
    _print(f"Python: {sys.version.split()[0]}")
    _print(f"Git: {shutil.which('git') or 'не найден'}")
    if jupyter_bin.exists():
        try:
            version_output = subprocess.run(
                [str(jupyter_bin), "--version"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            _print(f"Jupyter: {jupyter_bin} ({version_output})")
        except Exception as exc:
            problems.append(f"Не удалось запустить Jupyter: {exc}")
    else:
        problems.append(f"Jupyter не найден рядом с интерпретатором: {jupyter_bin}")

    try:
        config = load_lab_config()
        _print(f"Конфиг: {config_path()}")
        _print(f"Config OK: {config.project_name}")
    except Exception as exc:
        problems.append(f"Ошибка конфигурации: {exc}")

    required_modules = [
        "numpy",
        "pandas",
        "matplotlib",
        "yaml",
        "pydantic",
        "pytest",
        "jupyterlab",
    ]
    for module in required_modules:
        try:
            __import__(module)
        except Exception as exc:
            problems.append(f"Не удалось импортировать {module}: {exc}")

    for directory in [project_root(), research_root(), research_root() / "demo_study"]:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            marker = directory / ".write_test"
            marker.write_text("ok", encoding="utf-8")
            marker.unlink()
        except Exception as exc:
            problems.append(f"Нет доступа на запись в {directory}: {exc}")

    if problems:
        for problem in problems:
            _print(f"ОШИБКА: {problem}")
        return 1

    _print("Doctor: все базовые проверки пройдены.")
    return 0


def cmd_init_study(study_name: str) -> int:
    validate_study_name(study_name)
    paths = study_paths(study_name)
    for directory in [
        paths.root,
        paths.paper,
        paths.claims,
        paths.plans,
        paths.experiments,
        paths.results,
        paths.figures,
        paths.logs,
        paths.logbook,
    ]:
        directory.mkdir(parents=True, exist_ok=True)
    (paths.root / "README.md").write_text(
        f"# {study_name}\n\nИсследовательская папка для AI_RESEARCH_LAB.\n",
        encoding="utf-8",
    )
    _print(f"Инициализировано исследование: {paths.root}")
    return 0


def cmd_run(study_name: str) -> int:
    validate_study_name(study_name)
    agent = ResearchAgent()
    result = agent.run(study_name)
    _print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0 if result.error_message is None else 1


def cmd_verify(study_name: str) -> int:
    validate_study_name(study_name)
    agent = ResearchAgent()
    result = agent.verify(study_name)
    _print(json.dumps(result.model_dump(mode="json"), ensure_ascii=False, indent=2))
    return 0 if result.status.value in {"VERIFIED", "NOT_REPRODUCED"} else 1


def cmd_build_logbook(study_name: str) -> int:
    validate_study_name(study_name)
    paths = study_paths(study_name)
    claim_path = paths.claims / "claim.json"
    plan_path = paths.plans / "experiment_plan.json"
    result_files = sorted((paths.experiments).glob("*/experiment_result.json"))
    if not (claim_path.exists() and plan_path.exists() and result_files):
        _print("Невозможно построить logbook: не хватает claim, plan или result.")
        return 1
    claim = load_claim(claim_path)
    plan = ExperimentPlan.model_validate_json(plan_path.read_text(encoding="utf-8"))
    result = ExperimentResult.model_validate_json(result_files[-1].read_text(encoding="utf-8"))
    artifact_paths = [claim_path, plan_path, *[Path(path) for path in result.artifact_paths]]
    artifacts = register_artifacts(paths.root, result.experiment_id, artifact_paths)
    logbook_path = build_logbook(paths.root, study_name, claim, plan, result, artifacts)
    _print(f"Logbook построен: {logbook_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ai_research_lab")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("doctor")

    init_parser = subparsers.add_parser("init-study")
    init_parser.add_argument("study_name")

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("study_name")

    verify_parser = subparsers.add_parser("verify")
    verify_parser.add_argument("study_name")

    build_parser = subparsers.add_parser("build-logbook")
    build_parser.add_argument("study_name")

    args = parser.parse_args(argv)

    if args.command == "doctor":
        return cmd_doctor()
    if args.command == "init-study":
        return cmd_init_study(args.study_name)
    if args.command == "run":
        return cmd_run(args.study_name)
    if args.command == "verify":
        return cmd_verify(args.study_name)
    if args.command == "build-logbook":
        return cmd_build_logbook(args.study_name)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
