# AI Research Lab
# Итоговый публикационный отчёт по независимой репродукции статьи Colorful Pinball

**Объект проверки:** Diamond benchmark
**Тип документа:** Independent Reproduction and Reproducibility Audit
**Версия отчёта:** v1.0
**Дата:** 2026-07-25
**Итоговый статус:** `PARTIALLY_CONFIRMED`
**STATISTICAL_REPRODUCIBILITY:** `INSUFFICIENT_EVIDENCE`
**Scope:** Diamond only

## 1. Резюме
AI Research Lab проверила Diamond benchmark статьи **Colorful Pinball: Density-Weighted Quantile Regression for Conditional Guarantee of Conformal Prediction** на основе recovered primary sources, official repository, опубликованных Diamond-таблиц и полного набора аудиторских артефактов исследования.
Технический путь выполнения Diamond benchmark был восстановлен и подтверждён: официальный entrypoint запустился, завершился с `exit code 0`, дал ожидаемый файл результатов и сохранил полную provenance chain.
Часть числовых значений, победителей и рангов совпадает с публикацией, но не все пары подтверждаются на одинаковом уровне: часть совпадает точно, часть совпадает на уровне опубликованной точности, часть остаётся численно близкой, а часть даёт материальный rank shift.
Независимая статистическая проверка между внешне заданными seeds оказалась невозможной, потому что официальный entrypoint не предоставляет поддерживаемого механизма внешнего управления seed без изменения авторского кода. Поэтому статистическая воспроизводимость остаётся недостаточно доказанной.
Итоговый независимый вердикт лаборатории: `PARTIALLY_CONFIRMED`.

Что подтверждено:
- техническая воспроизводимость Diamond benchmark;
- восстановление первичных источников и provenance;
- совпадение лучших методов по всем шести общим метрикам Diamond;
- сохранение top-1 на уровне аналитического сравнения;
- подтверждение части claim audit для Diamond-scoped утверждений.

Что не подтверждено полностью:
- полное row-by-row совпадение всех опубликованных чисел;
- полное сохранение всех рангов;
- независимая межзапусковая устойчивость по внешне контролируемым seeds;
- причинность наблюдаемых расхождений;
- воспроизводимость за пределами Diamond.

## 2. Об исследуемой статье
- **Название:** Colorful Pinball: Density-Weighted Quantile Regression for Conditional Guarantee of Conformal Prediction
- **Авторы:** Qianyi Chen, Bo Li
- **Год:** 2026
- **Площадка публикации:** Machine Learning, ICML (подтверждено по recovered primary sources)
- **arXiv ID:** 2512.24139

**Заявление авторов.** Статья предлагает Colorful Pinball, density-weighted quantile regression подход для conditional guarantee of conformal prediction.
**Заявление авторов.** В статье обсуждаются stabilization strategies, включая Softplus, clipping и loss mixing, а также finite-sample guarantee для weighted objective.
**Заявление авторов.** В Diamond-части статьи сравниваются несколько baseline/method variants на dataset Naval Propulsion с метриками WSC и MSCE, а также связанными efficiency metrics.
**Интерпретация AI Research Lab.** Для Diamond этот benchmark является главным эмпирическим окном в то, насколько опубликованный алгоритм ведёт себя так, как описано в primary source и официальном репозитории.

Какие подходы рассматриваются в статье и что предложено авторами:
- **Заявление авторов:** сравниваются baseline conformal prediction family методы и CPCP-варианты.
- **Заявление авторов:** новизна связывается с density-weighted objective и соответствующей стабилизацией обучения/калибровки.
- **Интерпретация AI Research Lab:** для Diamond ключевым является не только формальное описание метода, но и совпадение официального кода, таблиц и метрик с опубликованными числами.

Какие datasets и benchmarks использованы:
- Diamond benchmark использует Naval Propulsion benchmark из статьи.
- В статье также рассматриваются другие datasets, но они не входят в scope этого отчёта.

Какую роль играет Diamond:
- Diamond является наиболее важной частью независимой проверки, потому что это восстановленный empirical benchmark с опубликованными таблицами, по которым можно сделать честное article × reproduction сравнение.
- Основные Diamond-выводы статьи касаются сравнения CPCP и baseline-методов по WSC, MSCE_10, MSCE_30, L1-ERT и L2-ERT, а также по Volume/Size как по renamed same metric.

## 3. Цель независимой проверки
Лаборатория проверяла, запускается ли официальный benchmark, доступны ли необходимые данные, воспроизводятся ли опубликованные числовые результаты, совпадают ли лучшие методы, сохраняется ли ranking, понятны ли определения метрик, можно ли независимо контролировать seeds, можно ли проверить статистическую устойчивость и достаточно ли опубликовано информации для повторения эксперимента.
Лаборатория не ставила целью доказать недобросовестность авторов, проверить всю статью, проверять Bike, менять авторский код, оптимизировать методы или получать лучший результат.

## 4. Объём исследования
**В scope:** Colorful Pinball, Diamond benchmark, официальный код, официальный dataset, опубликованные Diamond values, методы и метрики Diamond, winner analysis, ranking analysis, discrepancy analysis и statistical reproducibility feasibility.
**Вне scope:** Bike, другие datasets, полная репродукция всей статьи, GPU-matched reproduction, изменение vendor-кода, сравнение с новыми методами и оценка прикладной ценности за пределами статьи.

## 5. Источники и provenance
| Объект | Источник | Версия/идентификатор | SHA-256 | Статус |
| --- | --- | --- | --- | --- |
| Primary PDF | arXiv PDF | 2512.24139 | 20ca7db872d6d2905f5d06bad11294aa2ccdc4878506c4eadd4f803f84094187 | primary source / verified |
| Primary HTML | arXiv HTML | 2512.24139v5 | 6b027153904c4992f14f72e1a7ca3efd315e5d2e6f82ae9e1dc2fd90d68acedb | primary source / verified |
| Official repository README | https://github.com/Cqyiiii/Colorful-Pinball-Conformal-Prediction-CPCP | 98ce4fa0c851a9bfdedb609f82d4847f6e666def | 6f8102f10e3dfc8ce69cddc49f72d642833065b9f401ffa17d1abfb282907ba9 | primary source / verified |
| Official repository main | https://github.com/Cqyiiii/Colorful-Pinball-Conformal-Prediction-CPCP | 98ce4fa0c851a9bfdedb609f82d4847f6e666def | af875a6b1674df7cd79bb40d25deba26e2aa824c6f357bfd68e6f486746eaf98 | primary source / verified |
| Official repository metrics | https://github.com/Cqyiiii/Colorful-Pinball-Conformal-Prediction-CPCP | 98ce4fa0c851a9bfdedb609f82d4847f6e666def | 166e01296f2e2f3faf1e0570ea4c81a3f15a5938377cb7f6660449dfd142ad62 | primary source / verified |
| Article identity provenance | provenance/article_sources/ARTICLE_IDENTITY.json | 2512.24139 | a1db5e2a479caaaad638181b9d4f55fa4fa3a232707e57e98abf8ac571262b65 | audit provenance / verified |
| Source manifest | provenance/article_sources/SOURCE_MATERIALS_MANIFEST.json | 2512.24139 | acc2d46b5b23d493cd8491cde9e6e1c172217c8b2b4d1cd306018da84c3baa7b | audit provenance / verified |
| Diamond statistical plan | planning/DIAMOND_STATISTICAL_REPRODUCTION_PLAN.json | approved plan | 5a3dc9fd90b3dceea89e4215b2ba44af90158effeea5018447a50ad6108fd0b8 | locked plan / verified |
| Diamond control run | execution/diamond_statistical/runs/run-001-seed-42 | run-001-seed-42 | 59d9b2d6de886ca25ce911b7fc0375f0d82ad12c6c3d0df48481e971a733ae17 | immutable run bundle / verified |
| Pair-level comparison | analysis/diamond/diamond_pair_verdicts.csv | Diamond pair audit | d02d6e46173c573ce9a6463bdf173fec738e8817b4714e35650e4abc88172dc7 | audit evidence / verified |

Сведения о supplementary materials: в primary sources не найден отдельный supplementary archive URL; это зафиксировано в identity provenance как ambiguity, не как отсутствие article identity.

## 6. Методика репродукции
| Шаг | Цель | Использованный артефакт | Результат | Ограничение |
| --- | --- | --- | --- | --- |
| 1. Идентификация primary source | Подтвердить точную статью и официальный репозиторий. | ARTICLE_IDENTITY.json, SOURCE_MATERIALS_MANIFEST.json | Идентичность восстановлена по arXiv v5 и официальному репозиторию. | Ограничение: отсутствует отдельный supplementary archive URL. |
| 2. Извлечение опубликованных Diamond results | Получить таблицы Diamond из primary sources. | article_diamond_results.csv, article_diamond_claims.csv | Таблицы Diamond извлечены и нормализованы. | Ограничение: Volume и Size требуют отдельного mapping audit. |
| 3. Подготовка официального окружения | Зафиксировать окружение и зависимости. | ENVIRONMENT_SNAPSHOT.json | Окружение документировано, CPU-only. | Ограничение: environment match authors не доказан. |
| 4. Проверка dataset | Убедиться в неизменности данных. | BASELINE_INTEGRITY_MANIFEST.json | Dataset locked и unchanged. | Ограничение: matched-environment rerun не выполнялся. |
| 5. Проверка config | Проверить конфигурацию воспроизведения. | BASELINE_INTEGRITY_MANIFEST.json | Config locked и unchanged. | Ограничение: новых reruns нет. |
| 6. Проверка wrapper | Убедиться в неизменности официального entrypoint. | official_main.py, BASELINE_INTEGRITY_MANIFEST.json | Wrapper locked and unchanged. | Ограничение: seed override не exposed. |
| 7. Запуск benchmark | Подтвердить техническое выполнение. | benchmark_diamond provenance and logs | Run completed with exit code 0. | Ограничение: no new benchmark was launched in this continuation. |
| 8. Сохранение raw result | Зафиксировать результат в неизменяемом bundle. | diamond_results.csv, RESULT_MANIFEST.json | Raw result preserved and hashed. | Ограничение: single control bundle only. |
| 9. Нормализация методов и метрик | Свести article ↔ reproduction naming. | diamond_method_mapping.csv, diamond_metric_mapping.csv | Mappings verified. | Ограничение: article-only methods exist. |
| 10. Pair-level comparison | Сравнить пары метод × метрика. | diamond_comparison.csv, diamond_pair_verdicts.csv | 115 comparison rows and 78 comparable pairs. | Ограничение: article-only/reproduction-only rows exist. |
| 11. Проверка округления | Отдельно оценить совпадение по reported precision. | diamond_comparison.csv | 11 rows match at reported precision. | Ограничение: reported precision does not imply statistical stability. |
| 12. Winner comparison | Проверить top method per metric. | diamond_winner_comparison.csv | 6 shared metrics have matching winners. | Ограничение: Cov is reproduction-only. |
| 13. Ranking comparison | Проверить rank order and shifts. | diamond_ranking_comparison.csv, diamond_rank_shift_analysis.csv | Top-1 matches; full order does not. | Ограничение: single-run control bundle. |
| 14. Discrepancy cause audit | Оценить гипотезы причин расхождений. | diamond_discrepancy_hypotheses.csv | Coverage gaps, renamed metric, and seed-control limitation dominate. | Ограничение: causality not proven. |
| 15. Claim audit | Сопоставить claims article ↔ evidence. | article_diamond_claims.csv | 4 confirmed, 1 partially confirmed. | Ограничение: claim audit is Diamond-scoped. |
| 16. Statistical execution planning | Проверить plan and sample-completion logic. | DIAMOND_STATISTICAL_REPRODUCTION_PLAN.json, PLAN_EXECUTION_REVIEW.json | Plan and execution review align on the completed control run. | Ограничение: no independent external seed reruns. |
| 17. Immutable execution packaging | Сохранить authoritative control bundle. | run-001-seed-42 bundle | Bundle validated and immutable. | Ограничение: no per-seed fan-out path. |
| 18. Проверка seed control | Убедиться, можно ли внешне управлять seeds. | official_main.py, SAMPLE_COMPLETION_REVIEW.json | Seed control blocked. | Ограничение: no supported external `--seed`. |
| 19. Итоговая классификация | Собрать verdicts по evidence base. | all audits and reports | PARTIALLY_CONFIRMED overall; statistical reproducibility insufficient. | Ограничение: no new evidence created. |

## 7. Среда выполнения
| Компонент | Значение | Соответствие среде авторов | Влияние на вывод |
| --- | --- | --- | --- |
| OS | Darwin 22.6.0 | Не доказано | Accepted with limitations |
| Architecture | x86_64 | Не доказано | Accepted with limitations |
| CPU | Intel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz | Не доказано | Accepted with limitations |
| RAM | 16 GB | Не доказано | Accepted with limitations |
| Python | 3.11.15 | Не доказано | Accepted with limitations |
| GPU | False | No GPU available | CPU-only accepted with limitations |
| BLAS/LAPACK | OpenBLAS 0.3.23.dev / LAPACK 1.26.4 | Не доказано | Accepted with limitations |
| Threads | OMP/MKL/OPENBLAS/NUMEXPR/VECLIB/PYTHONHASHSEED unset | Не доказано | Accepted with limitations |

Использованная классификация CPU-only audit: `CPU_ONLY_ACCEPTED_WITH_LIMITATIONS`.

## 8. Проверка технической воспроизводимости
- Официальный entrypoint запустился и завершился с `exit code 0`.
- Ожидаемый raw result `diamond_results.csv` был создан и имеет 13 строк.
- `VALIDATION.json` подтверждает `completed=true`, `required_files_present=true` и совпадение SHA-256 с control run provenance.
- Vendor source, dataset, config и wrapper не изменялись.
- Полная provenance chain сохранена: command, environment, stdout/stderr, result manifest, validation.

**Техническая воспроизводимость: ПОДТВЕРЖДЕНА.**
Технический успех не равен подтверждению научных выводов: он показывает, что официальный путь выполнения работоспособен, а не что все численные результаты и ранги полностью совпадают.

## 9. Результаты числового сравнения
В comparison CSV и pair-level audits есть две совместимые, но разные проекции результата. На уровне `diamond_comparison.csv` сравниваются все 115 строк article/reproduction coverage; на уровне pair-level audit сравниваются 78 пар, где сравнение осмысленно.
| Категория | Количество |
| --- | --- |
| Exact precision matches (comparison CSV) | 0 |
| Matches at reported precision (comparison CSV) | 11 |
| Numerically close without threshold | 57 |
| Material numerical discrepancy | 10 |
| Article-only rows | 24 |
| Reproduction-only rows | 13 |
| Comparable pairs (pair-level audit) | 78 |

Ниже приведена полная pair-level таблица. Она включает все строки `diamond_comparison.csv` и фиксирует, где сравнение возможно, где оно ограничено опубликованной точностью и где исходный материал присутствует только в одном источнике.

### Appendix D — Pair-Level Comparison
| method | metric | article_value | reproduced_value | absolute_difference | relative_difference_percent | matches_at_reported_precision | article_rank | reproduction_rank | rank_delta | comparison_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CPCP-Clip+Mix-0.02 | Cov |  | 0.8999 |  |  | Нет |  | 7 |  | REPRODUCTION_ONLY |
| CPCP-Clip-0.02 | Cov |  | 0.8981 |  |  | Нет |  | 13 |  | REPRODUCTION_ONLY |
| CPCP-Mix-0.02 | Cov |  | 0.9007 |  |  | Нет |  | 4 |  | REPRODUCTION_ONLY |
| CPCP-Split-0.02 | Cov |  | 0.899 |  |  | Нет |  | 12 |  | REPRODUCTION_ONLY |
| CQR-ALD | Cov |  | 0.9 |  |  | Нет |  | 6 |  | REPRODUCTION_ONLY |
| CQR-Pinball | Cov |  | 0.8996 |  |  | Нет |  | 8 |  | REPRODUCTION_ONLY |
| Gaussian-Scoring | Cov |  | 0.8994 |  |  | Нет |  | 10 |  | REPRODUCTION_ONLY |
| PLCP-Pin-G20 | Cov |  | 0.9001 |  |  | Нет |  | 5 |  | REPRODUCTION_ONLY |
| PLCP-Pin-G50 | Cov |  | 0.9009 |  |  | Нет |  | 2 |  | REPRODUCTION_ONLY |
| RCP-ALD | Cov |  | 0.9009 |  |  | Нет |  | 2 |  | REPRODUCTION_ONLY |
| RCP-MultiHead | Cov |  | 0.9018 |  |  | Нет |  | 1 |  | REPRODUCTION_ONLY |
| RCP-Pinball | Cov |  | 0.8993 |  |  | Нет |  | 11 |  | REPRODUCTION_ONLY |
| Split | Cov |  | 0.8995 |  |  | Нет |  | 9 |  | REPRODUCTION_ONLY |
| CPCP-0.01 (Clip+Mix) | L1-ERT | 0.0230 |  |  |  | Нет | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | L1-ERT | 0.0219 | 0.0223 | 0.000400000000000001 | 1.82648401826484 | Нет | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | L1-ERT | 0.0243 |  |  |  | Нет | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | L1-ERT | 0.0256 | 0.0256 | 0 | 0 | Да | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | L1-ERT | 0.0275 | 0.0302 | 0.0027 | 9.81818181818182 | Нет | 5 | 4 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | L1-ERT | 0.0394 |  |  |  | Нет | 12 |  |  | ARTICLE_ONLY |
| CPCP | L1-ERT | 0.0379 | 0.0358 | 0.0021 | 5.54089709762534 | Нет | 10 | 8 | -2 | NUMERIC_MISMATCH |
| CPCP-0.05 | L1-ERT | 0.0375 |  |  |  | Нет | 9 |  |  | ARTICLE_ONLY |
| CQR-ALD | L1-ERT | 0.0301 | 0.0263 | 0.0038 | 12.624584717608 | Нет | 6 | 3 | -3 | NUMERIC_MISMATCH |
| CQR | L1-ERT | 0.0384 | 0.0345 | 0.00389999999999999 | 10.15625 | Нет | 11 | 7 | -4 | NUMERIC_MISMATCH |
| Gaussian-Scoring | L1-ERT | 0.0330 | 0.0333 | 0.000300000000000002 | 0.909090909090914 | Нет | 7 | 5 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | L1-ERT | 0.0642 | 0.0534 | 0.0108 | 16.822429906542 | Нет | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | L1-ERT | 0.0445 | 0.0377 | 0.0068 | 15.2808988764045 | Нет | 13 | 9 | -4 | NUMERIC_MISMATCH |
| RCP-ALD | L1-ERT | 0.0373 | 0.0344 | 0.0029 | 7.77479892761394 | Нет | 8 | 6 | -2 | NUMERIC_MISMATCH |
| RCP-MultiHead | L1-ERT | 0.0484 | 0.0517 | 0.0033 | 6.81818181818183 | Нет | 15 | 11 | -4 | NUMERIC_MISMATCH |
| RCP | L1-ERT | 0.0446 | 0.0456 | 0.001 | 2.24215246636772 | Нет | 14 | 10 | -4 | NUMERIC_MISMATCH |
| Split | L1-ERT | 0.1223 | 0.123 | 0.000699999999999992 | 0.572363041700729 | Нет | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | L2-ERT | 0.0009 |  |  |  | Нет | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | L2-ERT | 0.0007 | 0.0008 | 0.0001 | 14.2857142857143 | Нет | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | L2-ERT | 0.0010 |  |  |  | Нет | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | L2-ERT | 0.0011 | 0.0011 | 0 | 0 | Да | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | L2-ERT | 0.0013 | 0.0015 | 0.0002 | 15.3846153846154 | Нет | 5 | 4 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | L2-ERT | 0.0024 |  |  |  | Нет | 10 |  |  | ARTICLE_ONLY |
| CPCP | L2-ERT | 0.0022 | 0.0021 | 0.0001 | 4.54545454545456 | Нет | 7 | 7 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 | L2-ERT | 0.0022 |  |  |  | Нет | 7 |  |  | ARTICLE_ONLY |
| CQR-ALD | L2-ERT | 0.0016 | 0.0011 | 0.0005 | 31.25 | Нет | 6 | 2 | -4 | NUMERIC_MISMATCH |
| CQR | L2-ERT | 0.0024 | 0.002 | 0.0004 | 16.6666666666667 | Нет | 10 | 6 | -4 | NUMERIC_MISMATCH |
| Gaussian-Scoring | L2-ERT | 0.0024 | 0.0026 | 0.0002 | 8.33333333333334 | Нет | 10 | 8 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | L2-ERT | 0.0076 | 0.0056 | 0.002 | 26.3157894736842 | Нет | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | L2-ERT | 0.0038 | 0.0028 | 0.001 | 26.3157894736842 | Нет | 15 | 9 | -6 | NUMERIC_MISMATCH |
| RCP-ALD | L2-ERT | 0.0022 | 0.0017 | 0.0005 | 22.7272727272727 | Нет | 7 | 5 | -2 | NUMERIC_MISMATCH |
| RCP-MultiHead | L2-ERT | 0.0036 | 0.004 | 0.0004 | 11.1111111111111 | Нет | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | L2-ERT | 0.0029 | 0.003 | 0.0001 | 3.44827586206897 | Нет | 13 | 10 | -3 | NUMERIC_MISMATCH |
| Split | L2-ERT | 0.0287 | 0.0293 | 0.0006 | 2.09059233449477 | Нет | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | MSCE_10 | 0.0004 |  |  |  | Нет | 1 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | MSCE_10 | 0.0004 | 0.0004 | 0 | 0 | Да | 1 | 1 | 0 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.05 (Clip+Mix) | MSCE_10 | 0.0005 |  |  |  | Нет | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | MSCE_10 | 0.0005 | 0.0005 | 0 | 0 | Да | 3 | 2 | -1 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | MSCE_10 | 0.0006 | 0.0006 | 0 | 0 | Да | 5 | 3 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.01 | MSCE_10 | 0.0007 |  |  |  | Нет | 7 |  |  | ARTICLE_ONLY |
| CPCP | MSCE_10 | 0.0009 | 0.0008 | 9.99999999999999e-05 | 11.1111111111111 | Нет | 10 | 6 | -4 | NUMERIC_MISMATCH |
| CPCP-0.05 | MSCE_10 | 0.0008 |  |  |  | Нет | 9 |  |  | ARTICLE_ONLY |
| CQR-ALD | MSCE_10 | 0.0007 | 0.0006 | 0.0001 | 14.2857142857143 | Нет | 7 | 3 | -4 | NUMERIC_MISMATCH |
| CQR | MSCE_10 | 0.0010 | 0.001 | 0 | 0 | Да | 11 | 8 | -3 | MATCH_AT_REPORTED_PRECISION |
| Gaussian-Scoring | MSCE_10 | 0.0006 | 0.0006 | 0 | 0 | Да | 5 | 3 | -2 | MATCH_AT_REPORTED_PRECISION |
| PLCP (G=20) | MSCE_10 | 0.0032 | 0.0023 | 0.0009 | 28.125 | Нет | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | MSCE_10 | 0.0016 | 0.0012 | 0.0004 | 25 | Нет | 15 | 9 | -6 | NUMERIC_MISMATCH |
| RCP-ALD | MSCE_10 | 0.0010 | 0.0008 | 0.0002 | 20 | Нет | 11 | 6 | -5 | NUMERIC_MISMATCH |
| RCP-MultiHead | MSCE_10 | 0.0015 | 0.0018 | 0.0003 | 20 | Нет | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | MSCE_10 | 0.0013 | 0.0015 | 0.0002 | 15.3846153846154 | Нет | 13 | 10 | -3 | NUMERIC_MISMATCH |
| Split | MSCE_10 | 0.0118 | 0.0119 | 0.000100000000000001 | 0.847457627118654 | Нет | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | MSCE_30 | 0.0011 |  |  |  | Нет | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | MSCE_30 | 0.0010 | 0.001 | 0 | 0 | Да | 1 | 1 | 0 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.05 (Clip+Mix) | MSCE_30 | 0.0010 |  |  |  | Нет | 1 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | MSCE_30 | 0.0012 | 0.0014 | 0.0002 | 16.6666666666667 | Нет | 4 | 4 | 0 | NUMERIC_MISMATCH |
| CPCP (Mix) | MSCE_30 | 0.0015 | 0.0017 | 0.0002 | 13.3333333333333 | Нет | 7 | 7 | 0 | NUMERIC_MISMATCH |
| CPCP-0.01 | MSCE_30 | 0.0020 |  |  |  | Нет | 10 |  |  | ARTICLE_ONLY |
| CPCP | MSCE_30 | 0.0020 | 0.0018 | 0.0002 | 10 | Нет | 10 | 9 | -1 | NUMERIC_MISMATCH |
| CPCP-0.05 | MSCE_30 | 0.0021 |  |  |  | Нет | 12 |  |  | ARTICLE_ONLY |
| CQR-ALD | MSCE_30 | 0.0012 | 0.0012 | 0 | 0 | Да | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CQR | MSCE_30 | 0.0016 | 0.0015 | 0.0001 | 6.25 | Нет | 8 | 6 | -2 | NUMERIC_MISMATCH |
| Gaussian-Scoring | MSCE_30 | 0.0014 | 0.0014 | 0 | 0 | Да | 6 | 4 | -2 | MATCH_AT_REPORTED_PRECISION |
| PLCP (G=20) | MSCE_30 | 0.0045 | 0.0037 | 0.000799999999999999 | 17.7777777777778 | Нет | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | MSCE_30 | 0.0025 | 0.0017 | 0.0008 | 32 | Нет | 15 | 7 | -8 | NUMERIC_MISMATCH |
| RCP-ALD | MSCE_30 | 0.0017 | 0.0013 | 0.0004 | 23.5294117647059 | Нет | 9 | 3 | -6 | NUMERIC_MISMATCH |
| RCP-MultiHead | MSCE_30 | 0.0022 | 0.0025 | 0.0003 | 13.6363636363636 | Нет | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | MSCE_30 | 0.0021 | 0.0021 | 0 | 0 | Да | 12 | 10 | -2 | MATCH_AT_REPORTED_PRECISION |
| Split | MSCE_30 | 0.0138 | 0.0144 | 0.0006 | 4.34782608695652 | Нет | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | Volume | 0.3437 |  |  |  | Нет | 10 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | Volume | 0.3381 | 0.3382 | 9.9999999999989e-05 | 0.0295770482105853 | Нет | 8 | 7 | -1 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | Volume | 0.3340 |  |  |  | Нет | 7 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | Volume | 0.3459 | 0.352 | 0.00609999999999999 | 1.76351546689795 | Нет | 11 | 10 | -1 | NUMERIC_MISMATCH |
| CPCP (Mix) | Volume | 0.3566 | 0.3796 | 0.023 | 6.44980370162648 | Нет | 13 | 13 | 0 | NUMERIC_MISMATCH |
| CPCP-0.01 | Volume | 0.3928 |  |  |  | Нет | 16 |  |  | ARTICLE_ONLY |
| CPCP | Volume | 0.3723 | 0.3643 | 0.00800000000000001 | 2.1488047273704 | Нет | 14 | 11 | -3 | NUMERIC_MISMATCH |
| CPCP-0.05 | Volume | 0.4128 |  |  |  | Нет | 17 |  |  | ARTICLE_ONLY |
| CQR-ALD | Volume | 0.3170 | 0.3191 | 0.00209999999999999 | 0.662460567823341 | Нет | 4 | 5 | 1 | NUMERIC_MISMATCH |
| CQR | Volume | 0.2990 | 0.3016 | 0.00259999999999999 | 0.869565217391301 | Нет | 2 | 2 | 0 | NUMERIC_MISMATCH |
| Gaussian-Scoring | Volume | -1.6312 | -1.6495 | 0.0183 | 1.12187346738597 | Нет | 1 | 1 | 0 | NUMERIC_MISMATCH |
| PLCP (G=20) | Volume | 0.3520 | 0.3415 | 0.0105 | 2.98295454545453 | Нет | 12 | 8 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | Volume | 0.3427 | 0.3452 | 0.0025 | 0.72950102130143 | Нет | 9 | 9 | 0 | NUMERIC_MISMATCH |
| RCP-ALD | Volume | 0.3219 | 0.3249 | 0.003 | 0.931966449207829 | Нет | 6 | 6 | 0 | NUMERIC_MISMATCH |
| RCP-MultiHead | Volume | 0.3156 | 0.3163 | 0.000700000000000034 | 0.221799746514586 | Нет | 3 | 4 | 1 | NUMERIC_MISMATCH |
| RCP | Volume | 0.3197 | 0.3155 | 0.00419999999999998 | 1.31373162339693 | Нет | 5 | 3 | -2 | NUMERIC_MISMATCH |
| Split | Volume | 0.3793 | 0.3776 | 0.00170000000000003 | 0.448194041655691 | Нет | 15 | 12 | -3 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | WSC | 0.8783 |  |  |  | Нет | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | WSC | 0.8802 | 0.8813 | 0.00109999999999999 | 0.124971597364234 | Нет | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | WSC | 0.8801 |  |  |  | Нет | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | WSC | 0.8682 | 0.8708 | 0.00260000000000005 | 0.299470168164023 | Нет | 5 | 3 | -2 | NUMERIC_MISMATCH |
| CPCP (Mix) | WSC | 0.8676 | 0.8668 | 0.000800000000000023 | 0.0922083909635803 | Нет | 6 | 5 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | WSC | 0.8571 |  |  |  | Нет | 10 |  |  | ARTICLE_ONLY |
| CPCP | WSC | 0.8589 | 0.8618 | 0.00290000000000001 | 0.337641168937014 | Нет | 9 | 7 | -2 | NUMERIC_MISMATCH |
| CPCP-0.05 | WSC | 0.8617 |  |  |  | Нет | 7 |  |  | ARTICLE_ONLY |
| CQR-ALD | WSC | 0.8735 | 0.8776 | 0.00409999999999999 | 0.469376073268459 | Нет | 4 | 2 | -2 | NUMERIC_MISMATCH |
| CQR | WSC | 0.8563 | 0.8601 | 0.00380000000000003 | 0.443769706878433 | Нет | 11 | 8 | -3 | NUMERIC_MISMATCH |
| Gaussian-Scoring | WSC | 0.8613 | 0.8652 | 0.00390000000000001 | 0.452803901079765 | Нет | 8 | 6 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | WSC | 0.8068 | 0.8261 | 0.0193 | 2.39216658403569 | Нет | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | WSC | 0.8498 | 0.8557 | 0.00590000000000002 | 0.694281007295836 | Нет | 13 | 9 | -4 | NUMERIC_MISMATCH |
| RCP-ALD | WSC | 0.8558 | 0.8679 | 0.0121 | 1.41388174807198 | Нет | 12 | 4 | -8 | NUMERIC_MISMATCH |
| RCP-MultiHead | WSC | 0.8361 | 0.8306 | 0.00549999999999995 | 0.657816050711631 | Нет | 15 | 11 | -4 | NUMERIC_MISMATCH |
| RCP | WSC | 0.8448 | 0.8422 | 0.00260000000000005 | 0.307765151515157 | Нет | 14 | 10 | -4 | NUMERIC_MISMATCH |
| Split | WSC | 0.6480 | 0.6449 | 0.00309999999999999 | 0.478395061728394 | Нет | 17 | 13 | -4 | NUMERIC_MISMATCH |

**Итог по comparison CSV:** 0 exact matches, 11 matches at reported precision, 57 numerically close rows, 10 material discrepancies, 24 article-only rows и 13 reproduction-only rows.

## 10. Победители по метрикам
Таблица ниже показывает, что top method совпадает по всем шести общим метрикам Diamond. `Cov` не сравнивается на article стороне, потому что в публикационных Diamond tables оно не табулировано численно.
| Метрика | Победитель статьи | Победитель репродукции | Совпадение | Tie | Комментарий |
| --- | --- | --- | --- | --- | --- |
| Size / Volume | Gaussian-Scoring | Gaussian-Scoring | Да | Нет | Volume/Size mapping verified as renamed same metric. |
| WSC | CPCP-Clip+Mix-0.02 | CPCP-Clip+Mix-0.02 | Да | Нет | Top winner preserved. |
| MSCE_10 | CPCP-Clip+Mix-0.02 | CPCP-Clip+Mix-0.02 | Да | Нет | Top winner preserved. |
| MSCE_30 | CPCP-Clip+Mix-0.02 | CPCP-Clip+Mix-0.02 | Да | Нет | Top winner preserved. |
| L1-ERT | CPCP-Clip+Mix-0.02 | CPCP-Clip+Mix-0.02 | Да | Нет | Top winner preserved. |
| L2-ERT | CPCP-Clip+Mix-0.02 | CPCP-Clip+Mix-0.02 | Да | Нет | Top winner preserved. |

Итог: winner comparison совпадает по всем общим метрикам; это сильный, но не статистически независимый сигнал, потому что cross-seed control не доступен.

## 11. Анализ ранжирования
| Метрика | Spearman | Kendall | Top-1 | Full order | Max rank shift | Tie influence |
| --- | --- | --- | --- | --- | --- | --- |
| Volume | 0.951 | 0.846 | Да | Нет | 2 | Нет |
| WSC | 0.945 | 0.897 | Да | Нет | 4 | Нет |
| MSCE_10 | 0.967 | 0.945 | Да | Нет | 2 | Да |
| MSCE_30 | 0.882 | 0.787 | Да | Нет | 4 | Да |
| L1-ERT | 0.989 | 0.949 | Да | Нет | 1 | Нет |
| L2-ERT | 0.953 | 0.893 | Да | Нет | 2 | Да |

Какие rankings подтверждены: top-1 ranking на шести общих метриках. Какие подтверждены частично: весь порядок методов в целом, потому что rank correlations высоки, но full order match везде false. Какие изменились: lower-ranked methods смещаются на нескольких метриках. Какие нельзя оценить статистически: межзапусковая устойчивость ranking, потому что официальный seed fan-out blocked.

### Appendix F — Ranking Comparison
| method | metric | article_rank | reproduction_rank | rank_delta | comparison_status |
| --- | --- | --- | --- | --- | --- |
| CPCP-Clip+Mix-0.02 | Cov |  | 7 |  | REPRODUCTION_ONLY |
| CPCP-Clip-0.02 | Cov |  | 13 |  | REPRODUCTION_ONLY |
| CPCP-Mix-0.02 | Cov |  | 4 |  | REPRODUCTION_ONLY |
| CPCP-Split-0.02 | Cov |  | 12 |  | REPRODUCTION_ONLY |
| CQR-ALD | Cov |  | 6 |  | REPRODUCTION_ONLY |
| CQR-Pinball | Cov |  | 8 |  | REPRODUCTION_ONLY |
| Gaussian-Scoring | Cov |  | 10 |  | REPRODUCTION_ONLY |
| PLCP-Pin-G20 | Cov |  | 5 |  | REPRODUCTION_ONLY |
| PLCP-Pin-G50 | Cov |  | 2 |  | REPRODUCTION_ONLY |
| RCP-ALD | Cov |  | 2 |  | REPRODUCTION_ONLY |
| RCP-MultiHead | Cov |  | 1 |  | REPRODUCTION_ONLY |
| RCP-Pinball | Cov |  | 11 |  | REPRODUCTION_ONLY |
| Split | Cov |  | 9 |  | REPRODUCTION_ONLY |
| CPCP-0.01 (Clip+Mix) | L1-ERT | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | L1-ERT | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | L1-ERT | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | L1-ERT | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | L1-ERT | 5 | 4 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | L1-ERT | 12 |  |  | ARTICLE_ONLY |
| CPCP | L1-ERT | 10 | 8 | -2 | NUMERIC_MISMATCH |
| CPCP-0.05 | L1-ERT | 9 |  |  | ARTICLE_ONLY |
| CQR-ALD | L1-ERT | 6 | 3 | -3 | NUMERIC_MISMATCH |
| CQR | L1-ERT | 11 | 7 | -4 | NUMERIC_MISMATCH |
| Gaussian-Scoring | L1-ERT | 7 | 5 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | L1-ERT | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | L1-ERT | 13 | 9 | -4 | NUMERIC_MISMATCH |
| RCP-ALD | L1-ERT | 8 | 6 | -2 | NUMERIC_MISMATCH |
| RCP-MultiHead | L1-ERT | 15 | 11 | -4 | NUMERIC_MISMATCH |
| RCP | L1-ERT | 14 | 10 | -4 | NUMERIC_MISMATCH |
| Split | L1-ERT | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | L2-ERT | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | L2-ERT | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | L2-ERT | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | L2-ERT | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | L2-ERT | 5 | 4 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | L2-ERT | 10 |  |  | ARTICLE_ONLY |
| CPCP | L2-ERT | 7 | 7 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 | L2-ERT | 7 |  |  | ARTICLE_ONLY |
| CQR-ALD | L2-ERT | 6 | 2 | -4 | NUMERIC_MISMATCH |
| CQR | L2-ERT | 10 | 6 | -4 | NUMERIC_MISMATCH |
| Gaussian-Scoring | L2-ERT | 10 | 8 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | L2-ERT | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | L2-ERT | 15 | 9 | -6 | NUMERIC_MISMATCH |
| RCP-ALD | L2-ERT | 7 | 5 | -2 | NUMERIC_MISMATCH |
| RCP-MultiHead | L2-ERT | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | L2-ERT | 13 | 10 | -3 | NUMERIC_MISMATCH |
| Split | L2-ERT | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | MSCE_10 | 1 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | MSCE_10 | 1 | 1 | 0 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.05 (Clip+Mix) | MSCE_10 | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | MSCE_10 | 3 | 2 | -1 | MATCH_AT_REPORTED_PRECISION |
| CPCP (Mix) | MSCE_10 | 5 | 3 | -2 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.01 | MSCE_10 | 7 |  |  | ARTICLE_ONLY |
| CPCP | MSCE_10 | 10 | 6 | -4 | NUMERIC_MISMATCH |
| CPCP-0.05 | MSCE_10 | 9 |  |  | ARTICLE_ONLY |
| CQR-ALD | MSCE_10 | 7 | 3 | -4 | NUMERIC_MISMATCH |
| CQR | MSCE_10 | 11 | 8 | -3 | MATCH_AT_REPORTED_PRECISION |
| Gaussian-Scoring | MSCE_10 | 5 | 3 | -2 | MATCH_AT_REPORTED_PRECISION |
| PLCP (G=20) | MSCE_10 | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | MSCE_10 | 15 | 9 | -6 | NUMERIC_MISMATCH |
| RCP-ALD | MSCE_10 | 11 | 6 | -5 | NUMERIC_MISMATCH |
| RCP-MultiHead | MSCE_10 | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | MSCE_10 | 13 | 10 | -3 | NUMERIC_MISMATCH |
| Split | MSCE_10 | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | MSCE_30 | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | MSCE_30 | 1 | 1 | 0 | MATCH_AT_REPORTED_PRECISION |
| CPCP-0.05 (Clip+Mix) | MSCE_30 | 1 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | MSCE_30 | 4 | 4 | 0 | NUMERIC_MISMATCH |
| CPCP (Mix) | MSCE_30 | 7 | 7 | 0 | NUMERIC_MISMATCH |
| CPCP-0.01 | MSCE_30 | 10 |  |  | ARTICLE_ONLY |
| CPCP | MSCE_30 | 10 | 9 | -1 | NUMERIC_MISMATCH |
| CPCP-0.05 | MSCE_30 | 12 |  |  | ARTICLE_ONLY |
| CQR-ALD | MSCE_30 | 4 | 2 | -2 | MATCH_AT_REPORTED_PRECISION |
| CQR | MSCE_30 | 8 | 6 | -2 | NUMERIC_MISMATCH |
| Gaussian-Scoring | MSCE_30 | 6 | 4 | -2 | MATCH_AT_REPORTED_PRECISION |
| PLCP (G=20) | MSCE_30 | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | MSCE_30 | 15 | 7 | -8 | NUMERIC_MISMATCH |
| RCP-ALD | MSCE_30 | 9 | 3 | -6 | NUMERIC_MISMATCH |
| RCP-MultiHead | MSCE_30 | 14 | 11 | -3 | NUMERIC_MISMATCH |
| RCP | MSCE_30 | 12 | 10 | -2 | MATCH_AT_REPORTED_PRECISION |
| Split | MSCE_30 | 17 | 13 | -4 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | Volume | 10 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | Volume | 8 | 7 | -1 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | Volume | 7 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | Volume | 11 | 10 | -1 | NUMERIC_MISMATCH |
| CPCP (Mix) | Volume | 13 | 13 | 0 | NUMERIC_MISMATCH |
| CPCP-0.01 | Volume | 16 |  |  | ARTICLE_ONLY |
| CPCP | Volume | 14 | 11 | -3 | NUMERIC_MISMATCH |
| CPCP-0.05 | Volume | 17 |  |  | ARTICLE_ONLY |
| CQR-ALD | Volume | 4 | 5 | 1 | NUMERIC_MISMATCH |
| CQR | Volume | 2 | 2 | 0 | NUMERIC_MISMATCH |
| Gaussian-Scoring | Volume | 1 | 1 | 0 | NUMERIC_MISMATCH |
| PLCP (G=20) | Volume | 12 | 8 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | Volume | 9 | 9 | 0 | NUMERIC_MISMATCH |
| RCP-ALD | Volume | 6 | 6 | 0 | NUMERIC_MISMATCH |
| RCP-MultiHead | Volume | 3 | 4 | 1 | NUMERIC_MISMATCH |
| RCP | Volume | 5 | 3 | -2 | NUMERIC_MISMATCH |
| Split | Volume | 15 | 12 | -3 | NUMERIC_MISMATCH |
| CPCP-0.01 (Clip+Mix) | WSC | 3 |  |  | ARTICLE_ONLY |
| CPCP (Clip+Mix) | WSC | 1 | 1 | 0 | NUMERIC_MISMATCH |
| CPCP-0.05 (Clip+Mix) | WSC | 2 |  |  | ARTICLE_ONLY |
| CPCP (Clip) | WSC | 5 | 3 | -2 | NUMERIC_MISMATCH |
| CPCP (Mix) | WSC | 6 | 5 | -1 | NUMERIC_MISMATCH |
| CPCP-0.01 | WSC | 10 |  |  | ARTICLE_ONLY |
| CPCP | WSC | 9 | 7 | -2 | NUMERIC_MISMATCH |
| CPCP-0.05 | WSC | 7 |  |  | ARTICLE_ONLY |
| CQR-ALD | WSC | 4 | 2 | -2 | NUMERIC_MISMATCH |
| CQR | WSC | 11 | 8 | -3 | NUMERIC_MISMATCH |
| Gaussian-Scoring | WSC | 8 | 6 | -2 | NUMERIC_MISMATCH |
| PLCP (G=20) | WSC | 16 | 12 | -4 | NUMERIC_MISMATCH |
| PLCP (G=50) | WSC | 13 | 9 | -4 | NUMERIC_MISMATCH |
| RCP-ALD | WSC | 12 | 4 | -8 | NUMERIC_MISMATCH |
| RCP-MultiHead | WSC | 15 | 11 | -4 | NUMERIC_MISMATCH |
| RCP | WSC | 14 | 10 | -4 | NUMERIC_MISMATCH |
| Split | WSC | 17 | 13 | -4 | NUMERIC_MISMATCH |

## 12. Проверка Volume и Size
В статье для Diamond используется метка `Volume`, тогда как в официальном коде и reproduction output используется `Size`. Отдельный volume-size audit показывает `RENAMED_SAME_METRIC` с высокой уверенностью: same formula, same direction, same scale и directly comparable.
Это не просто семантическое сходство: mapping подтверждён по primary source, official repository main/metrics code и формату output столбца.
Неопределённость остаётся только в смысле именования, а не в смысле числовой сопоставимости. Для итогового вердикта это не меняет общий вывод, но важно для честного сравнения метрик.

## 13. Анализ причин расхождений
Ниже приведены гипотезы и их причинный статус. Наблюдаемое расхождение само по себе не доказывает причину; отсутствие внешнего seed override не доказывает высокую случайность; CPU-only не считается причиной без matched comparison.
| Гипотеза | Доказательства | Сила доказательств | Причинный статус | Вывод |
| --- | --- | --- | --- | --- |
| randomness | Публикация использует 20-seed control protocol; differences are small relative to reported spread in many rows. | MODERATE | PLAUSIBLE_CONTRIBUTOR | Может вносить вклад, но не объясняет всё само по себе. |
| single-run effect | The control bundle already aggregates 20 seeds; no lone-run artifact in the authoritative bundle. | STRONG | RULED_OUT | Не объясняет текущие результаты. |
| version mismatch | Fixed repo commit pinned; no evidence of post-publication code drift in recovered sources. | MODERATE | RULED_OUT | Не поддерживается recovered provenance. |
| dependency mismatch | Environment versions recorded, but no matched-environment rerun was performed. | WEAK | UNRESOLVED | Нельзя подтвердить или опровергнуть. |
| environment mismatch | CPU-only macOS x86_64 environment recorded, no matched comparison against authors. | WEAK | UNRESOLVED | Возможна, но не доказана. |
| CPU-only | CPU-only acceptable as baseline, but no evidence links CPU-only directly to the rank shifts. | WEAK | UNRESOLVED | Нельзя считать причиной без matched comparison. |
| rounding | 11 rows match at reported precision in comparison CSV, but others do not. | MODERATE | SUPPORTED_CONTRIBUTOR | Объясняет часть small differences, но не все. |
| differences in metric labels | Volume/Size mapping is explicitly renamed same metric. | STRONG | SUPPORTED_CAUSE | Это naming issue, а не scientific contradiction. |
| hidden defaults | Official main hardcodes seed loop; no supported external seed override recovered. | MODERATE | SUPPORTED_BLOCKER | Это ограничение протокола, а не доказательство расхождений. |
| seed control limitation | SAMPLE_COMPLETION_REVIEW.json and official entrypoint inspection. | STRONG | SUPPORTED_BLOCKER | Блокирует независимые reruns, но не заменяет статистическую проверку. |

## 14. Статистическая репродукция
Статистический план был создан и зафиксирован в `planning/DIAMOND_STATISTICAL_REPRODUCTION_PLAN.md` и `.json`. На доступном официальном протоколе уже существует immutable bundle `run-001-seed-42`, который представляет завершённый 20-seed control run.
Лаборатория смогла подтвердить sample completion, но не смогла превратить этот control bundle в набор независимо управляемых seed-specific reruns: официальный entrypoint не предоставляет поддерживаемого внешнего `--seed`, а менять vendor-код в рамках основной репродукции запрещено.
Поэтому разделение статусов такое: `DIAMOND_STATISTICAL_SAMPLE_COMPLETE`, `DIAMOND_STATISTICAL_REPRODUCTION_INSUFFICIENT_EVIDENCE`, `DIAMOND_SEED_CONTROL_BLOCKED`.
Простыми словами: официальный запуск уже агрегирует результаты по внутреннему протоколу, но лаборатория не может независимо задать и повторить отдельные seeds через поддерживаемый интерфейс. Следовательно, невозможно проверить, повторяется ли распределение результатов в новых независимых сериях запусков.

## 15. Аудит утверждений статьи
| ID | Утверждение статьи | Доказательство статьи | Доказательство репродукции | Вердикт AI Research Lab |
| --- | --- | --- | --- | --- |
| C1 | Proposition 3.4 establishes the approximation relationship that motivates the Diamond metric choice. | Primary article text and proof appendix. | Recovered article text states Proposition 3.4 and its proof pathway in Appendix B.2. | CONFIRMED |
| C2 | CPCP uses a three-stage scheme with staged calibration/fine-tuning. | Primary article text and official repository implementation. | Recovered article describes the three-stage workflow and the official repo implements the same staged structure. | CONFIRMED |
| C3 | Theorem 5.2 provides the stated finite-sample guarantee for the weighted objective. | Primary article text and proof appendix. | Recovered article states Theorem 5.2 and its proof in Appendix B.3. | CONFIRMED |
| C4 | Softplus, clipping, and loss mixing are stabilization strategies used by CPCP. | Primary article text and recovered code paths. | Recovered article discusses clipping and loss mixing; the fixed repo exposes corresponding implementation behavior. | CONFIRMED |
| C5 | On Diamond, CPCP and related baselines show a top-method comparison on WSC and MSCE metrics for Naval Propulsion. | Diamond appendix tables and the reproduction table for shared metrics. | The shared metrics preserve the top winner, but the article-only delta ablation means the full winner set is not identical across sources. | PARTIALLY_CONFIRMED |

Подтверждены: C1–C4. Подтверждены частично: C5. Не подтверждены: нет.

## 16. Что лаборатория подтвердила
- официальный benchmark технически исполним;
- исходные Diamond tables найдены и извлечены;
- published values сопоставимы с reproduction values;
- часть pair-level results воспроизводится точно или на уровне published precision;
- часть winners совпадает, а именно все шесть shared metrics;
- часть rankings сохраняется на уровне top-1;
- provenance восстановлена и проверяема;
- официальный протокол имеет ограничение внешнего seed control.

## 17. Что лаборатория не смогла подтвердить
- полное совпадение всех numerical values;
- полное сохранение всех rankings;
- причинность CPU-only;
- причинность randomness как единственной причины;
- независимую межзапусковую seed stability;
- statistical confidence across separately controlled reruns;
- результаты за пределами Diamond;
- полную воспроизводимость всей статьи.

## 18. Ограничения исследования
- Diamond-only scope: выводы не распространяются на Bike или остальные datasets.
- No environment-matched hardware run: matched comparison with authors was not performed.
- CPU-only execution: baseline accepted with limitations.
- Version and dependency uncertainty: no exact matched rerun across all dependency states.
- Limited statistical protocol detail in the article: external seed override absent.
- Impossible to independently replay individual seeds through supported interface.
- Only one official aggregated control protocol bundle is available in the workspace.
- Potential ambiguity in Volume/Size naming: resolved as renamed same metric for Diamond only.
- Published precision limits some cells to reported rounding rather than exact lexical equality.
- No new reruns were performed during publication packaging.
- No causal claim can be asserted for observed discrepancies without matched experiments.

## 19. Итоговый независимый вердикт AI Research Lab
**AI Research Lab Independent Verdict: `PARTIALLY_CONFIRMED`**
**Technical Reproducibility: `CONFIRMED`**
**Statistical Reproducibility: `INSUFFICIENT_EVIDENCE`**
**External Seed Control: `BLOCKED`**

Уверенность в общем вердикте: средняя. Её повышают восстановленный primary source, стабильный top-1 на общих метриках, корректная provenance chain и независимое восстановление технического пути. Её снижают наличие article-only / reproduction-only rows, неполное сохранение full order, отсутствие external seed override и невозможность независимого межзапускового анализа.

## 20. Рекомендации авторам статьи
| Priority | Recommendation | Problem | Scientific benefit |
| --- | --- | --- | --- |
| Critical | Добавить официальный внешний параметр `--seed` | Проблема: external reproducibility blocked. Предлагаемое изменение: CLI seed override. | Польза: enables independent reruns and seed audit. |
| Critical | Добавить официальный список seeds | Проблема: seed schedule hidden inside entrypoint. Предлагаемое изменение: explicit published seed list. | Польза: makes repeatability auditable. |
| Critical | Разрешить запуск одного seed отдельно | Проблема: cannot isolate one run. Предлагаемое изменение: single-seed mode. | Польза: improves debugging and variance estimation. |
| High | Публиковать raw result для каждого seed | Проблема: only aggregate output is published. Предлагаемое изменение: per-seed raw results. | Польза: enables inter-run statistics. |
| High | Публиковать mean, std и confidence intervals | Проблема: incomplete statistical disclosure. Предлагаемое изменение: report mean/std/CI. | Польза: enables stronger replication claims. |
| High | Указать точное число repeats | Проблема: repeated-seed semantics are implicit. Предлагаемое изменение: explicit repeat count. | Польза: prevents ambiguity in audit. |
| High | Описать метод aggregation | Проблема: aggregation path not explicit enough for external audit. Предлагаемое изменение: specify aggregation protocol. | Польза: makes result reproduction transparent. |
| High | Зафиксировать hardware | Проблема: hardware sensitivity unresolved. Предлагаемое изменение: publish CPU/GPU and model details. | Польза: aids matched-environment comparison. |
| High | Зафиксировать OS | Проблема: OS-dependent behavior may vary. Предлагаемое изменение: publish OS version and build. | Польза: improves environment matching. |
| High | Зафиксировать Python version | Проблема: runtime drift. Предлагаемое изменение: exact Python version. | Польза: reduces dependency ambiguity. |
| High | Зафиксировать dependency versions | Проблема: package drift. Предлагаемое изменение: lock dependency versions. | Польза: reproducible environment. |
| High | Публиковать lock-file | Проблема: hidden dependency state. Предлагаемое изменение: include lock-file. | Польза: supports exact recreation. |
| Medium | Указать thread count | Проблема: multithreading can affect numerical order. Предлагаемое изменение: record thread settings. | Польза: more deterministic execution. |
| Medium | Указать BLAS/LAPACK backend | Проблема: linear algebra backend may differ. Предлагаемое изменение: backend disclosure. | Польза: better numeric comparability. |
| Medium | Уточнить CPU/GPU equivalence | Проблема: equivalence is assumed, not proven. Предлагаемое изменение: explicit equivalence note or benchmark. | Польза: clarifies interpretation of hardware results. |
| Medium | Документировать hidden defaults | Проблема: defaults can alter outcomes. Предлагаемое изменение: publish all defaults. | Польза: avoids hidden-state surprises. |
| Medium | Добавить deterministic execution mode | Проблема: stochastic drift. Предлагаемое изменение: deterministic mode flag. | Польза: supports regression testing. |
| Medium | Уточнить mapping Volume/Size | Проблема: naming ambiguity. Предлагаемое изменение: explicit metric mapping note. | Польза: avoids miscomparison. |
| Medium | Публиковать machine-readable tables | Проблема: manual extraction is error-prone. Предлагаемое изменение: CSV/JSON tables. | Польза: easier auditing. |
| Medium | Добавить reproducibility script | Проблема: procedural reconstruction is verbose. Предлагаемое изменение: one-command bundle generator. | Польза: lowers replication barrier. |
| Medium | Публиковать checksum datasets and results | Проблема: provenance validation requires hashes. Предлагаемое изменение: explicit checksums. | Польза: integrity verification. |
| Low | Добавить CI smoke test benchmark | Проблема: regressions may go unnoticed. Предлагаемое изменение: CI smoke test. | Польза: early warning for breakages. |
| Low | Документировать expected runtime and memory | Проблема: planning is difficult without resource info. Предлагаемое изменение: runtime/memory estimates. | Польза: operational readiness. |
| Low | Указать rules for rounding | Проблема: precision interpretation can differ. Предлагаемое изменение: rounding rules. | Польза: fewer false disagreements. |
| High | Публиковать полный statistical protocol | Проблема: statistical reproducibility remains insufficiently evidenced. Предлагаемое изменение: complete protocol. | Польза: stronger and more auditable claims. |

## 21. Рекомендации другим исследователям
- Использовать exact commit, а не только repo name.
- Фиксировать SHA-256 для primary PDF, raw outputs и manifests.
- Не ограничиваться exit code.
- Проверять direction of metric before interpreting winners.
- Явно проверять ties и tie-breaking rules.
- Отличать execution reproducibility от result reproducibility.
- Не считать один run статистической проверкой.
- Не менять vendor-код без отдельного experimental branch.
- Документировать environment differences честно и полностью.
- Хранить immutable run bundles и read-only provenance snapshots.

## 22. Рекомендации AI Research Lab
- Считать Diamond-проверку завершённой.
- Сохранить verdict `PARTIALLY_CONFIRMED`.
- Не выполнять новые Diamond runs без нового утверждённого протокола.
- Не изменять vendor ради seed control в рамках основной репродукции.
- При необходимости создать отдельное последующее исследование `DIAMOND_INSTRUMENTED_SEED_CONTROL_EXTENSION`.
- Ясно обозначать, что такое исследование будет модифицированной репродукцией, а не чистым повтором.
- Перейти к следующему benchmark только отдельным решением.
- Подготовить публичную презентацию на основе финального отчёта.

## 23. Заключение
1. **Запустился ли официальный эксперимент?** Да, официальный Diamond entrypoint запустился и завершился успешно.
2. **Совпали ли опубликованные числа?** Частично: 11 rows match at reported precision, многие пары close, 10 пар material discrepancy.
3. **Совпали ли победители?** Да, top winner совпал по всем шести общим метрикам.
4. **Сохранилось ли ранжирование?** Частично: top-1 preserved, full order not preserved.
5. **Доказаны ли причины расхождений?** Нет, causal attribution не доказана.
6. **Проверена ли статистическая воспроизводимость?** Нет в строгом межзапусковом смысле; sample completion есть, но seed control blocked и evidence insufficient.
7. **Каков итоговый вердикт?** `PARTIALLY_CONFIRMED`.

**AI Research Lab Independent Verdict: `PARTIALLY_CONFIRMED`**
**Statistical Reproducibility: `INSUFFICIENT_EVIDENCE`**

## 24. Техническое приложение
### Appendix A — Artifact Index
| Artifact | Path | SHA-256 | Purpose |
| --- | --- | --- | --- |
| publication/COLORFUL_PINBALL_DIAMOND_FINAL_REPRODUCTION_REPORT.md | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/COLORFUL_PINBALL_DIAMOND_FINAL_REPRODUCTION_REPORT.md | N/A | Main Russian report |
| publication/COLORFUL_PINBALL_DIAMOND_PUBLIC_SUMMARY_RU.md | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/COLORFUL_PINBALL_DIAMOND_PUBLIC_SUMMARY_RU.md | 6cc00e4c9c8a237e8c2da8769182d21a645b258fe0d777b078a3893c1545a932 | Short public Russian summary |
| publication/COLORFUL_PINBALL_DIAMOND_EXECUTIVE_SUMMARY_EN.md | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/COLORFUL_PINBALL_DIAMOND_EXECUTIVE_SUMMARY_EN.md | 6d30103878a394ef421bca5e2cefc1999facc7a8992df93608846783471b31be | English executive summary |
| publication/COLORFUL_PINBALL_DIAMOND_FINAL_VERDICT.json | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/COLORFUL_PINBALL_DIAMOND_FINAL_VERDICT.json | 0371503c0c63512b764de08d36f5d93c7988309db8f01eaf95bd28c4e1fcfc84 | Machine-readable verdict |
| publication/COLORFUL_PINBALL_DIAMOND_CITATION_MAP.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/COLORFUL_PINBALL_DIAMOND_CITATION_MAP.csv | 7363bf4ee73f6c57faad1368113d72135bc0d925ddf67c65ae992e5cacf45d14 | Claim-to-evidence citation map |
| publication/PUBLICATION_MANIFEST.json | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/PUBLICATION_MANIFEST.json | N/A | Manifest for the publication bundle |
| publication/FINAL_REPORT_EVIDENCE_VALIDATION.json | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/publication/FINAL_REPORT_EVIDENCE_VALIDATION.json | 1e74bb90d2972c1614f44795aa6a1d37ecf261f0a0bbda25cd5ade08c8adb584 | Validation gate |
| analysis/diamond/diamond_pair_verdicts.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/diamond_pair_verdicts.csv | d02d6e46173c573ce9a6463bdf173fec738e8817b4714e35650e4abc88172dc7 | Pair-level audit |
| analysis/diamond/diamond_comparison.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/diamond_comparison.csv | 07c702106805b238b31d4b559bebdc102fbb34dc389a5ac195855a00dd8c9c3f | Comparison table |
| analysis/diamond/diamond_winner_comparison.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/diamond_winner_comparison.csv | f34fd40169e97514c7ad568b24b75e9b418903d502dc2ccb57c5af6e65102850 | Winner comparison |
| analysis/diamond/diamond_ranking_comparison.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/diamond_ranking_comparison.csv | 344e56d5d40c32a6ce204005b6259863d9d2803d13cf22b70d0e6f332d85357d | Ranking comparison |
| analysis/diamond/diamond_discrepancy_hypotheses.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/diamond_discrepancy_hypotheses.csv | 5a288b1bba021234585466a4b627105e59b9b7810eef1d622ceffa239f4a027c | Discrepancy audit |
| analysis/diamond/article_diamond_claims.csv | /Users/sergej/Documents/AI_RESEARCH_LAB/research/repro-colorful-pinball-targeted/analysis/diamond/article_diamond_claims.csv | d52e3e460068c13304478883231a7d887bd2ff3ad4dcbec4e27db6a661697110 | Claim audit |

### Appendix B — Method Mapping
| article_method | reproduction_method | mapping_status | mapping_basis | confidence | notes |
| --- | --- | --- | --- | --- | --- |
| Split | Split | EXACT_MATCH | Identical label in paper and reproduction. | HIGH | Direct label match. |
| PLCP (G=20) | PLCP-Pin-G20 | OFFICIAL_ALIAS_MATCH | Paper abbreviation maps to the repo alias used for the pinball PLCP-G20 implementation. | HIGH | Supported by main.py and README. |
| PLCP (G=50) | PLCP-Pin-G50 | OFFICIAL_ALIAS_MATCH | Paper abbreviation maps to the repo alias used for the pinball PLCP-G50 implementation. | HIGH | Supported by main.py and README. |
| Gaussian-Scoring | Gaussian-Scoring | EXACT_MATCH | Identical label in paper and reproduction. | HIGH | Direct label match. |
| CQR | CQR-Pinball | OFFICIAL_ALIAS_MATCH | Paper uses the method family name; the repo specifies the pinball variant. | HIGH | README and main.py identify the pinball variant. |
| CQR-ALD | CQR-ALD | EXACT_MATCH | Identical label in paper and reproduction. | HIGH | Direct label match. |
| RCP | RCP-Pinball | OFFICIAL_ALIAS_MATCH | Paper uses the family name; the repo uses the pinball alias. | HIGH | README and main.py identify the pinball variant. |
| RCP-ALD | RCP-ALD | EXACT_MATCH | Identical label in paper and reproduction. | HIGH | Direct label match. |
| RCP-MultiHead | RCP-MultiHead | EXACT_MATCH | Identical label in paper and reproduction. | HIGH | Direct label match. |
| CPCP | CPCP-Split-0.02 | OFFICIAL_ALIAS_MATCH | Paper default CPCP corresponds to the vanilla / split CPCP implementation with delta 0.02 in the repo. | HIGH | Supported by README and main.py. |
| CPCP (Clip) | CPCP-Clip-0.02 | OFFICIAL_ALIAS_MATCH | Paper variant name maps to the repo clipping variant with delta 0.02. | HIGH | Supported by README and main.py. |
| CPCP (Mix) | CPCP-Mix-0.02 | OFFICIAL_ALIAS_MATCH | Paper variant name maps to the repo mixing variant with delta 0.02. | HIGH | Supported by README and main.py. |
| CPCP (Clip+Mix) | CPCP-Clip+Mix-0.02 | OFFICIAL_ALIAS_MATCH | Paper variant name maps to the repo combined clipping-plus-mixing variant with delta 0.02. | HIGH | Supported by README and main.py. |
| CPCP-0.01 | CPCP-Split-0.01 | ARTICLE_ONLY | Paper publishes delta 0.01 ablations but the reproduction file does not contain them. | HIGH | No counterpart in reproduced_diamond_results.csv. |
| CPCP-0.01 (Clip+Mix) | CPCP-Clip+Mix-0.01 | ARTICLE_ONLY | Paper publishes delta 0.01 ablations but the reproduction file does not contain them. | HIGH | No counterpart in reproduced_diamond_results.csv. |
| CPCP-0.05 | CPCP-Split-0.05 | ARTICLE_ONLY | Paper publishes delta 0.05 ablations but the reproduction file does not contain them. | HIGH | No counterpart in reproduced_diamond_results.csv. |
| CPCP-0.05 (Clip+Mix) | CPCP-Clip+Mix-0.05 | ARTICLE_ONLY | Paper publishes delta 0.05 ablations but the reproduction file does not contain them. | HIGH | No counterpart in reproduced_diamond_results.csv. |

### Appendix C — Metric Mapping
| article_metric | reproduction_metric | mapping_status | mapping_basis | confidence | notes |
| --- | --- | --- | --- | --- | --- |
| Cov | Cov | REPRODUCTION_ONLY | Empirical marginal coverage exists in the reproduction outputs but is not numerically tabulated in the appendix Diamond tables. | MEDIUM | Unpublished metric for Diamond; no direct article row was extracted. |
| Volume | Size | RENAMED_SAME_METRIC | The paper uses the Volume label while the repo writes Size; the scalar Diamond benchmark uses the same quantity in the published numbers. | HIGH | See the dedicated volume-size mapping audit. |
| WSC | WSC | EXACT_MATCH | Same metric name. | HIGH | Direct label and implementation match. |
| MSCE_10 | MSCE_10 | EXACT_MATCH | Same metric name and K=10 setting. | HIGH | Direct label and implementation match. |
| MSCE_30 | MSCE_30 | EXACT_MATCH | Same metric name and K=30 setting. | HIGH | Direct label and implementation match. |
| L1-ERT | L1-ERT | EXACT_MATCH | Same metric name. | HIGH | Direct label and implementation match. |
| L2-ERT | L2-ERT | EXACT_MATCH | Same metric name. | HIGH | Direct label and implementation match. |

### Appendix E — Winner Comparison
| metric | article_metric | article_best_method | article_best_value | article_best_rank | reproduction_best_method | reproduction_best_value | reproduction_best_rank | shared_methods_count | full_order_match | top_method_match | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | Volume | Gaussian-Scoring | -1.6312 |  | Gaussian-Scoring | -1.6495 |  |  |  |  | Volume/Size mapping normalized to compare the same scalar quantity. |
|  | WSC | CPCP-Clip+Mix-0.02 | 0.8802 |  | CPCP-Clip+Mix-0.02 | 0.8813 |  |  |  |  |  |
|  | MSCE_10 | CPCP-Clip+Mix-0.02 | 0.0004 |  | CPCP-Clip+Mix-0.02 | 0.0004 |  |  |  |  |  |
|  | MSCE_30 | CPCP-Clip+Mix-0.02 | 0.0010 |  | CPCP-Clip+Mix-0.02 | 0.0010 |  |  |  |  |  |
|  | L1-ERT | CPCP-Clip+Mix-0.02 | 0.0219 |  | CPCP-Clip+Mix-0.02 | 0.0223 |  |  |  |  |  |
|  | L2-ERT | CPCP-Clip+Mix-0.02 | 0.0007 |  | CPCP-Clip+Mix-0.02 | 0.0008 |  |  |  |  |  |

### Appendix G — Statistical Execution Record
| run_id | seed | metric | winner_method | winner_value | tie_count | winner_frequency_estimable | notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| run-001-seed-42 | 42 | Cov | CPCP-Clip-0.02 | 0.8981 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | Size | Gaussian-Scoring | -1.6495 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | WSC | CPCP-Clip+Mix-0.02 | 0.8813 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | MSCE_10 | CPCP-Clip+Mix-0.02 | 0.0004 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | MSCE_30 | CPCP-Clip+Mix-0.02 | 0.001 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | L1-ERT | CPCP-Clip+Mix-0.02 | 0.0223 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |
| run-001-seed-42 | 42 | L2-ERT | CPCP-Clip+Mix-0.02 | 0.0008 | 1 | false | Single run bundle only; no cross-seed winner frequency can be estimated. |

### Appendix H — Environment Snapshot
| Компонент | Значение | Соответствие среде авторов | Влияние на вывод |
| --- | --- | --- | --- |
| OS | Darwin 22.6.0 | Не доказано | Accepted with limitations |
| Architecture | x86_64 | Не доказано | Accepted with limitations |
| CPU | Intel(R) Core(TM) i7-4870HQ CPU @ 2.50GHz | Не доказано | Accepted with limitations |
| RAM | 16 GB | Не доказано | Accepted with limitations |
| Python | 3.11.15 | Не доказано | Accepted with limitations |
| GPU | False | No GPU available | CPU-only accepted with limitations |
| BLAS/LAPACK | OpenBLAS 0.3.23.dev / LAPACK 1.26.4 | Не доказано | Accepted with limitations |
| Threads | OMP/MKL/OPENBLAS/NUMEXPR/VECLIB/PYTHONHASHSEED unset | Не доказано | Accepted with limitations |

### Appendix I — Limitations Matrix
| Ограничение | Что ограничено | Какой вывод нельзя сделать | Влияние |
| --- | --- | --- | --- |
| Diamond-only scope | Analysis does not extend to Bike or the full article. | Cannot generalize to the entire paper. | High |
| No environment-matched hardware | No matched rerun against authors' exact stack. | Cannot attribute differences to hardware. | Medium |
| CPU-only execution | Current execution baseline is CPU-only. | Cannot claim CPU causes discrepancies. | Medium |
| Version and dependency uncertainty | No exact matched rerun across all dependency states. | Cannot fully rule out environment drift. | Medium |
| External seed control absent | No supported external `--seed` path. | Cannot estimate inter-run variance. | High |
| Single aggregate control protocol | Only one official immutable bundle is available. | Cannot derive multi-run variance. | High |

### Appendix J — Claim Verdict Matrix
| ID | Утверждение | Вердикт | Basis | Limitations |
| --- | --- | --- | --- | --- |
| C1 | Proposition 3.4 establishes the approximation relationship that motivates the Diamond metric choice. | CONFIRMED | The proposition is explicitly present in the recovered primary source and is textually supported by the surrounding derivation. | This is a paper-level theoretical claim and does not depend on the Diamond benchmark table. |
| C2 | CPCP uses a three-stage scheme with staged calibration/fine-tuning. | CONFIRMED | The workflow is directly described in the article and aligned with the recovered official code paths. | Implementation alignment is supported at the recovered commit only. |
| C3 | Theorem 5.2 provides the stated finite-sample guarantee for the weighted objective. | CONFIRMED | The theorem is explicitly stated in the recovered primary source and its proof structure is present. | Theory claims are verified textually, not via benchmark rerun. |
| C4 | Softplus, clipping, and loss mixing are stabilization strategies used by CPCP. | CONFIRMED | The claim is directly supported by primary-source text and the recovered repository implementation. | No new experiment is needed to verify this claim. |
| C5 | On Diamond, CPCP and related baselines show a top-method comparison on WSC and MSCE metrics for Naval Propulsion. | PARTIALLY_CONFIRMED | The headline winner on the shared metrics is reproduced, but the article/reproduction method coverage differs and prevents full row-by-row confirmation. | This claim is restricted to Diamond only and should not be generalized to the full article. |

### Appendix K — Reproducibility Recommendations
| Priority | Recommendation | Problem | Scientific benefit |
| --- | --- | --- | --- |
| Critical | Добавить официальный внешний параметр `--seed` | Проблема: external reproducibility blocked. Предлагаемое изменение: CLI seed override. | Польза: enables independent reruns and seed audit. |
| Critical | Добавить официальный список seeds | Проблема: seed schedule hidden inside entrypoint. Предлагаемое изменение: explicit published seed list. | Польза: makes repeatability auditable. |
| Critical | Разрешить запуск одного seed отдельно | Проблема: cannot isolate one run. Предлагаемое изменение: single-seed mode. | Польза: improves debugging and variance estimation. |
| High | Публиковать raw result для каждого seed | Проблема: only aggregate output is published. Предлагаемое изменение: per-seed raw results. | Польза: enables inter-run statistics. |
| High | Публиковать mean, std и confidence intervals | Проблема: incomplete statistical disclosure. Предлагаемое изменение: report mean/std/CI. | Польза: enables stronger replication claims. |
| High | Указать точное число repeats | Проблема: repeated-seed semantics are implicit. Предлагаемое изменение: explicit repeat count. | Польза: prevents ambiguity in audit. |
| High | Описать метод aggregation | Проблема: aggregation path not explicit enough for external audit. Предлагаемое изменение: specify aggregation protocol. | Польза: makes result reproduction transparent. |
| High | Зафиксировать hardware | Проблема: hardware sensitivity unresolved. Предлагаемое изменение: publish CPU/GPU and model details. | Польза: aids matched-environment comparison. |
| High | Зафиксировать OS | Проблема: OS-dependent behavior may vary. Предлагаемое изменение: publish OS version and build. | Польза: improves environment matching. |
| High | Зафиксировать Python version | Проблема: runtime drift. Предлагаемое изменение: exact Python version. | Польза: reduces dependency ambiguity. |
| High | Зафиксировать dependency versions | Проблема: package drift. Предлагаемое изменение: lock dependency versions. | Польза: reproducible environment. |
| High | Публиковать lock-file | Проблема: hidden dependency state. Предлагаемое изменение: include lock-file. | Польза: supports exact recreation. |
| Medium | Указать thread count | Проблема: multithreading can affect numerical order. Предлагаемое изменение: record thread settings. | Польза: more deterministic execution. |
| Medium | Указать BLAS/LAPACK backend | Проблема: linear algebra backend may differ. Предлагаемое изменение: backend disclosure. | Польза: better numeric comparability. |
| Medium | Уточнить CPU/GPU equivalence | Проблема: equivalence is assumed, not proven. Предлагаемое изменение: explicit equivalence note or benchmark. | Польза: clarifies interpretation of hardware results. |
| Medium | Документировать hidden defaults | Проблема: defaults can alter outcomes. Предлагаемое изменение: publish all defaults. | Польза: avoids hidden-state surprises. |
| Medium | Добавить deterministic execution mode | Проблема: stochastic drift. Предлагаемое изменение: deterministic mode flag. | Польза: supports regression testing. |
| Medium | Уточнить mapping Volume/Size | Проблема: naming ambiguity. Предлагаемое изменение: explicit metric mapping note. | Польза: avoids miscomparison. |
| Medium | Публиковать machine-readable tables | Проблема: manual extraction is error-prone. Предлагаемое изменение: CSV/JSON tables. | Польза: easier auditing. |
| Medium | Добавить reproducibility script | Проблема: procedural reconstruction is verbose. Предлагаемое изменение: one-command bundle generator. | Польза: lowers replication barrier. |
| Medium | Публиковать checksum datasets and results | Проблема: provenance validation requires hashes. Предлагаемое изменение: explicit checksums. | Польза: integrity verification. |
| Low | Добавить CI smoke test benchmark | Проблема: regressions may go unnoticed. Предлагаемое изменение: CI smoke test. | Польза: early warning for breakages. |
| Low | Документировать expected runtime and memory | Проблема: planning is difficult without resource info. Предлагаемое изменение: runtime/memory estimates. | Польза: operational readiness. |
| Low | Указать rules for rounding | Проблема: precision interpretation can differ. Предлагаемое изменение: rounding rules. | Польза: fewer false disagreements. |
| High | Публиковать полный statistical protocol | Проблема: statistical reproducibility remains insufficiently evidenced. Предлагаемое изменение: complete protocol. | Польза: stronger and more auditable claims. |
