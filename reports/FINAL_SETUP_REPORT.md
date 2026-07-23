# FINAL_SETUP_REPORT

Дата отчёта: 2026-07-23

## 1. Executive verdict

Локальный baseline проекта `AI_RESEARCH_LAB` доведён до рабочего и воспроизводимого состояния. Ключевые дефекты устранены:

- claim больше не мутируется при чтении и повторных прогонах;
- registry и `experiment_result.json` теперь используют переносимые относительные пути;
- logbook собирается детерминированно для одного и того же результата;
- итоговый demo-run и верификация проходят успешно.

## 2. Project identity

- Проект: `AI_RESEARCH_LAB`
- Корень: `/Users/sergej/Documents/AI_RESEARCH_LAB`
- Назначение: локальная исследовательская лаборатория с CLI, агентом, runner-логикой, registry артефактов, logbook и notebook smoke-test.

## 3. Environment

- OS: macOS
- Python: 3.x в локальном `.venv`
- Основные команды запускаются через `.venv/bin/python` и `.venv/bin/jupyter`
- Git branch: `main`

## 4. Project tree

Ключевые каталоги проекта:

- `src/ai_research_lab`
- `tests`
- `research/demo_study`
- `notebooks`
- `reports`
- `templates`
- `config`
- `scripts`

## 5. Key files

- [`src/ai_research_lab/paths.py`](../src/ai_research_lab/paths.py)
- [`src/ai_research_lab/claim_extractor.py`](../src/ai_research_lab/claim_extractor.py)
- [`src/ai_research_lab/artifact_registry.py`](../src/ai_research_lab/artifact_registry.py)
- [`src/ai_research_lab/experiment_runner.py`](../src/ai_research_lab/experiment_runner.py)
- [`src/ai_research_lab/logbook_builder.py`](../src/ai_research_lab/logbook_builder.py)
- [`src/ai_research_lab/agent.py`](../src/ai_research_lab/agent.py)
- [`src/ai_research_lab/cli.py`](../src/ai_research_lab/cli.py)
- [`tests/test_portable_paths.py`](../tests/test_portable_paths.py)
- [`tests/test_claim_extractor.py`](../tests/test_claim_extractor.py)
- [`tests/test_artifact_registry.py`](../tests/test_artifact_registry.py)
- [`tests/test_logbook_builder.py`](../tests/test_logbook_builder.py)

## 6. Verification commands

Проверялись следующие команды:

- `python -m ai_research_lab.cli doctor`
- `python -m ruff check src tests`
- `python -m pytest -q`
- `python -m pytest --cov=ai_research_lab --cov-report=term-missing -q`
- `python -m ai_research_lab.cli run demo_study`
- `python -m ai_research_lab.cli verify demo_study`
- `python -m ai_research_lab.cli build-logbook demo_study`
- `jupyter nbconvert --to notebook --execute notebooks/00_lab_smoke_test.ipynb`

## 7. Test evidence

- `pytest -q`: 15 passed
- `pytest --cov=ai_research_lab --cov-report=term-missing -q`: 15 passed
- Общая покрываемость: 90%

## 8. Demo experiment evidence

Параметры demo study:

- `experiment_id`: `mean_convergence_demo`
- `seed`: `20260723`
- `sample_sizes`: `[10, 100, 1000, 10000]`
- `replicates`: `64`
- критерии успеха:
  - финальная средняя абсолютная ошибка `<= 0.05`;
  - финальная ошибка меньше начальной.

Итог:

- initial mean absolute error: `0.2476798226685518`
- final mean absolute error: `0.007766857514033455`
- criterion_met: `true`
- final status: `VERIFIED`

## 9. Reproducibility comparison

Результаты совпадают с ожидаемой тенденцией: при росте размера выборки оценка среднего стандартного нормального распределения сходится к нулю. Повторные прогоны сохраняют ту же метрику и статус `VERIFIED`.

## 10. Artifact evidence

Текущие ключевые артефакты demo study:

- `research/demo_study/claims/claim.json`
- `research/demo_study/plans/experiment_plan.json`
- `research/demo_study/experiments/mean_convergence_demo/raw_results.json`
- `research/demo_study/results/raw_results.csv`
- `research/demo_study/results/metrics.json`
- `research/demo_study/figures/convergence.png`
- `research/demo_study/experiments/mean_convergence_demo/experiment_result.json`
- `research/demo_study/logs/mean_convergence_demo.log`
- `research/demo_study/logs/artifact_registry.json`
- `research/demo_study/logbook/LOGBOOK.md`

Проверенные SHA-256:

- `claim.json`: `f382e11e9461c0a65ff332e20e6e2dc8a869e3d41a488403136e425248e93673`
- `experiment_result.json`: `0928723f97399fc6fbbc9d90ab0108296c02a30cce25735c0d56bdb811b20051`
- `metrics.json`: `155cdbb9cfa4ffc6dc8e2589d62b7c89c5af2e5771f99c54c3fa35bbd164a39b`
- `LOGBOOK.md`: `1e39f3cbd2dadab8e587de18c541c892516f029d677806555d60ccc8f363ff6f`
- `artifact_registry.json`: `c05b86a8a54cecec71358b21e5344bcb8afd88e842daff492d3cfda99c4fc22b`

## 11. Registry integrity

Registry теперь хранит проектно-относительные пути. Это устранило проблему с абсолютными путями и сделало registry переносимым между копиями проекта. В актуальном состоянии SHA для записи logbook в registry соответствует фактическому SHA файла `LOGBOOK.md`.

## 12. Logbook audit

Logbook строится детерминированно для одного и того же результата:

- `created_at` берётся из времени завершения результата;
- дубликаты артефактов отфильтровываются;
- строки самого logbook не попадают в список его же артефактов;
- повторный `build-logbook` не меняет содержимое claim и не ломает registry integrity.

## 13. Notebook audit

Notebook smoke-test:

- `notebooks/00_lab_smoke_test.ipynb` успешно выполняется через `nbconvert`;
- output notebook создаётся без ошибок;
- проверка подтверждает, что базовый Jupyter-пайплайн живой.

## 14. Safety audit

Проверены и закреплены безопасные ограничения:

- имена исследований валидируются;
- переносимые пути должны быть относительными;
- попытки выйти за пределы project root отклоняются;
- абсолютные portable paths не принимаются;
- `claim.json` больше не переписывается при обычном чтении и повторных прогонах.

## 15. Git audit

- Рабочая ветка: `main`
- Изменения внесены только в нужные исходники, тесты и итоговый отчёт
- Устранённые дефекты покрыты регрессионными тестами

## 16. Baseline changes

Что было исправлено в baseline:

- добавлены `portable_relative_path` и `resolve_portable_path` в `paths.py`;
- `claim_extractor.py` стал идемпотентным при сохранении существующего claim;
- registry переведён на относительные пути;
- runner пишет переносимые пути в `experiment_result.json`;
- logbook builder больше не вносит сам себя в артефакты и использует время завершения результата;
- CLI `build-logbook` синхронизирован с новой схемой артефактов;
- добавлены регрессионные тесты на claim, portable paths, registry и logbook.

## 17. Known limitations

- Покрытие тестами не 100%, а 90%.
- Registry пересобирается при каждом build-logbook, поэтому его SHA может меняться вместе с обновлением timestamp-полей.
- Проект остаётся локальным baseline без удалённого репозитория в текущей среде.

## 18. Final conclusion

Проект собран в чистый и проверенный baseline: demo study выполняется, результаты воспроизводимы, артефакты переносимы, logbook и registry согласованы, а регрессии по claim mutation устранены. Это уже можно считать рабочей опорной точкой для дальнейшего развития.
