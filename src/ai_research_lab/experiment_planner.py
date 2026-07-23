from __future__ import annotations

from .config import LabConfig
from .models import ExperimentPlan, ResearchClaim


def build_demo_plan(claim: ResearchClaim, config: LabConfig) -> ExperimentPlan:
    parameters = {
        "experiment_type": config.safe_experiment_type,
        "sample_sizes": config.sample_sizes,
        "replicates": config.replicates,
        "distribution": "standard_normal",
    }
    return ExperimentPlan(
        experiment_id="mean_convergence_demo",
        claim_id=claim.claim_id,
        hypothesis=(
            "Если увеличить размер выборки, средняя абсолютная ошибка оценки среднего "
            "значения стандартного нормального распределения уменьшится."
        ),
        method=(
            "Генерируем независимые выборки из стандартного нормального распределения, "
            "сравниваем среднюю абсолютную ошибку оценки среднего для нескольких размеров выборки."
        ),
        parameters=parameters,
        seed=config.seed,
        expected_artifacts=[
            "raw_results.json",
            "raw_results.csv",
            "metrics.json",
            "convergence.png",
            "experiment_result.json",
            "artifact_registry.json",
            "LOGBOOK.md",
        ],
        success_criteria=dict(config.success_criteria.model_dump()),
        status="PLANNED",
    )


def validate_plan(plan: ExperimentPlan) -> None:
    params = plan.parameters
    sample_sizes = params.get("sample_sizes")
    if not isinstance(sample_sizes, list) or not sample_sizes:
        raise ValueError("План должен содержать непустой список sample_sizes.")
    if any(not isinstance(size, int) or size <= 0 for size in sample_sizes):
        raise ValueError("sample_sizes должен содержать положительные целые числа.")
    if sample_sizes != sorted(sample_sizes):
        raise ValueError("sample_sizes должен быть отсортирован по возрастанию.")
    if plan.parameters.get("experiment_type") != "mean_convergence":
        raise ValueError("Разрешён только безопасный тип эксперимента mean_convergence.")

