# AI_RESEARCH_LAB

Локальная лаборатория для воспроизведения AI/ML-исследований на MacBook. Проект сделан так, чтобы новичок мог хранить статьи, фиксировать утверждения, строить планы воспроизведения, запускать Python-эксперименты, собирать артефакты и вести Markdown Logbook без облака и без тяжёлой агентной платформы.

## Что уже умеет лаборатория

- хранить статьи в `papers/`;
- хранить исследовательские рабочие области в `research/`;
- создавать структурированное `ResearchClaim`;
- строить `ExperimentPlan`;
- запускать детерминированный локальный эксперимент `mean_convergence`;
- сохранять результаты в JSON, CSV и PNG;
- регистрировать артефакты с SHA-256;
- собирать Markdown Logbook;
- выполнять проверку через CLI и тесты;
- запускать smoke-test notebook.

## Что пока не умеет

- автоматически читать и понимать PDF-статьи;
- исполнять произвольный код из текста статьи;
- работать с PyTorch, TensorFlow или большими моделями;
- использовать векторные базы данных;
- запускать облачные или GPU-тяжёлые пайплайны.

## ICML 2026 Agent Reproduction Challenge

В проект уже подключён отдельный слой для конкурса Hugging Face ICML 2026 Agent Reproduction Challenge.

Что уже подключено:

- локальная диагностика Hugging Face CLI;
- отдельный Trackio adapter для local-only run;
- challenge config и cost policy без секретов;
- шаблон будущего reproduction study;
- структура документации по правилам конкурса и безопасности;
- команды `ai-research-lab challenge ...`.

Что такое Hugging Face:

- это платформа для моделей, датасетов, Spaces, Jobs и CLI-инструментов;
- в этом проекте Hugging Face используется только как безопасный внешний слой для будущей репродукции, без автоматической публикации.

Что такое Trackio:

- это lightweight experiment tracking library;
- в local-first режиме она пишет данные локально и не требует remote Space;
- в этом проекте Trackio дополняет обычный Markdown logbook, а не заменяет его.

Что такое local run:

- это локальный smoke test без cloud GPU и без remote публикации;
- он нужен, чтобы проверить код, данные и структуру результата до любой внешней активности.

Что пока не опубликовано:

- ни один reproduction logbook;
- ни один submission;
- ни один Hugging Face Space, Dataset или repository для конкурса.

Как проверить авторизацию:

```bash
.venv/bin/hf auth whoami
```

Если входа нет, используется обычный browser login flow:

```bash
.venv/bin/hf auth login
```

Почему token нельзя вставлять в чат или код:

- token даёт доступ к Hugging Face аккаунту;
- он не должен попадать в Git, notebook, logbook или shell history;
- в этом проекте допускается только безопасная локальная диагностика без раскрытия token.

Как запустить challenge doctor:

```bash
make challenge-doctor
```

Как выполнить Trackio smoke test:

```bash
make challenge-trackio-smoke
```

Что будет следующим этапом:

- совместно с наставником выбрать paper_id;
- создать отдельный challenge study из шаблона;
- после этого готовить полноценную репродукцию статьи.

Важно:

- выбор статьи делает пользователь совместно с наставником;
- код не выбирает paper_id автоматически;
- publish и submit сейчас заблокированы.

## Структура каталогов

```text
AI_RESEARCH_LAB/
├── config/
├── papers/
├── research/
│   └── demo_study/
├── notebooks/
├── src/
├── scripts/
├── templates/
├── tests/
└── reports/
```

## Требования

- macOS;
- Python 3.11 или новее;
- Git;
- локальное окружение `.venv`.

## Установка

```bash
cd <REPOSITORY_ROOT>
make install
```

## Активация окружения

```bash
source .venv/bin/activate
```

## Doctor

```bash
make doctor
```

Проверка показывает:

- версию Python;
- наличие Git и Jupyter;
- корректность `config/lab.yaml`;
- возможность импорта ключевых модулей;
- возможность записи в проект и `research/`.

## Демонстрационный эксперимент

```bash
make demo
```

Или напрямую:

```bash
python -m ai_research_lab.cli run demo_study
```

## Проверка результата

```bash
make verify
```

## Тесты

```bash
make test
```

## Линт

```bash
make lint
```

## Notebook

```bash
make notebook-check
```

Для интерактивной работы:

```bash
./scripts/start_jupyter.sh
```

## Где лежат результаты

- результаты эксперимента: `research/demo_study/results/`;
- сырые артефакты: `research/demo_study/experiments/`;
- графики: `research/demo_study/figures/`;
- логи: `research/demo_study/logs/`;
- Logbook: `research/demo_study/logbook/LOGBOOK.md`.

## Как добавить будущую статью

1. Скопируйте PDF или заметки в `papers/inbox/`.
2. Переместите материал в `papers/active/`, когда начнёте разбор.
3. Опишите claim на основе статьи в `research/<study>/claims/claim.json`.
4. Постройте безопасный `ExperimentPlan`.
5. Добавьте новый тип эксперимента только после тестов.

## Правила безопасности

- не выполняйте произвольный код из статьи;
- не меняйте файлы вне `AI_RESEARCH_LAB`;
- не устанавливайте пакеты глобально;
- не используйте платные API;
- не запускайте тяжёлые GPU-эксперименты на этом этапе;
- не подгоняйте критерий успеха после получения результатов.

## License

Original AI_RESEARCH_LAB code and documentation are licensed under the MIT License unless otherwise stated.

Third-party articles, datasets, source repositories, vendor code, figures, and other external materials remain subject to their original licenses and terms.

See the LICENSE file for details.

## Типичные ошибки и как их исправить

- `python: command not found` - активируйте `.venv` или используйте `make install`.
- `ModuleNotFoundError` - повторно выполните `make install`.
- `Jupyter not found` - проверьте, что установка в `.venv` завершилась без ошибок.
- `No such file or directory` для study - сначала выполните `python -m ai_research_lab.cli init-study demo_study`.
- `NOT_REPRODUCED` - проверьте критерии успеха и посмотрите `metrics.json`.
