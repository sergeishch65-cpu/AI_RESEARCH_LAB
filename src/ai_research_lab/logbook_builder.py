from __future__ import annotations

from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path

from .models import ArtifactRecord, ExperimentPlan, ExperimentResult, ResearchClaim


def _version(name: str) -> str:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def build_logbook(
    study_root: Path,
    study_name: str,
    claim: ResearchClaim,
    plan: ExperimentPlan,
    result: ExperimentResult,
    artifacts: list[ArtifactRecord],
) -> Path:
    logbook_dir = study_root / "logbook"
    logbook_dir.mkdir(parents=True, exist_ok=True)
    logbook_path = logbook_dir / "LOGBOOK.md"
    created_at = datetime.now(timezone.utc).isoformat()

    artifact_lines = "\n".join(
        f"| {artifact.artifact_id} | {artifact.artifact_type.value} | {artifact.path} | {artifact.sha256} |"
        for artifact in artifacts
    )

    summary_rows = result.metrics["summary_by_sample_size"]
    metric_lines = "\n".join(
        f"| {row['sample_size']} | {row['mean_estimate']:.6f} | {row['mean_abs_error']:.6f} | {row['std_abs_error']:.6f} |"
        for row in summary_rows
    )

    rerun_command = f"python -m ai_research_lab.cli run {study_name}"

    body = f"""# Logbook: {study_name}

Дата и время создания: {created_at}

## Исследование
- Утверждение: {claim.text}
- Источник: {claim.source}
- Гипотеза: {plan.hypothesis}

## План эксперимента
- experiment_id: {plan.experiment_id}
- claim_id: {plan.claim_id}
- seed: {plan.seed}
- method: {plan.method}
- parameters: {plan.parameters}
- success_criteria: {plan.success_criteria}

## Окружение
- python: {result.environment.get("python", "unknown")}
- platform: {result.environment.get("platform", "unknown")}
- numpy: {_version("numpy")}
- pandas: {_version("pandas")}
- matplotlib: {_version("matplotlib")}
- pydantic: {_version("pydantic")}
- pyyaml: {_version("PyYAML")}

## FACT
- Результат проверки: {result.status.value}
- Criterion met: {result.metrics["criterion_met"]}
- Initial mean abs error: {result.metrics["initial_mean_abs_error"]:.6f}
- Final mean abs error: {result.metrics["final_mean_abs_error"]:.6f}

### Метрики по размерам выборки
| sample_size | mean_estimate | mean_abs_error | std_abs_error |
|---:|---:|---:|---:|
{metric_lines}

### Артефакты
| artifact_id | artifact_type | path | sha256 |
|---|---|---|---|
{artifact_lines}

## INTERPRETATION
Экспериментальная инфраструктура демонстрационно подтвердила, что средняя абсолютная ошибка оценки среднего уменьшается на большем размере выборки для выбранного фиксированного seed.

## LIMITATION
- Это не воспроизведение статьи, а проверка локальной инфраструктуры лаборатории.
- Проверяется только один простой детерминированный эксперимент.
- Результат зависит от фиксированного seed и выбранных параметров.

## NEXT STEP
- Загрузить первую реальную статью в `papers/inbox`.
- Сформулировать claim из статьи и добавить новый безопасный экспериментальный тип.
- Подготовить более строгий протокол воспроизведения с несколькими прогоном и сравнением метрик.

## Команда повторного запуска
```bash
{rerun_command}
```
"""
    logbook_path.write_text(body, encoding="utf-8")
    return logbook_path

