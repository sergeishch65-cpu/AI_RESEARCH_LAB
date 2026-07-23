# ICML 2026 Agent Reproduction Challenge: user guide

## 1. Что создано

- Базовая локальная лаборатория `AI_RESEARCH_LAB`.
- Отдельный challenge-layer для будущих репродукций.
- Локальный вызов `hf` и `trackio` в `.venv`.
- Документация по правилам конкурса и безопасности.

## 2. Что не создано

- Не выбран paper_id.
- Не опубликован logbook.
- Не отправлена submission.
- Не создан Hugging Face repository, Space или Dataset.
- Не создан remote Trackio logbook.

## 3. Как проверить Hugging Face login

Выполни:

```bash
.venv/bin/hf auth whoami
```

Если входа нет, безопасная остановка выглядит так:

```bash
.venv/bin/hf auth login
```

Token нельзя вставлять в чат, код, notebook или репозиторий.

## 4. Как выполнить локальный Trackio test

Для локального smoke test Trackio используй `challenge trackio-smoke`.
Он создаёт временный `TRACKIO_DIR`, пишет параметры, метрики и финальный статус, а затем завершает run без remote publish.

## 5. Где будут лежать статьи

- Исходные PDF и заметки: `papers/inbox/`
- Активные статьи: `papers/active/`
- Будущие challenge studies: `research/_templates/icml_2026_reproduction/` как шаблон

## 6. Где будет logbook

- Локальный canonical logbook: `research/<study>/logbook/LOGBOOK.md`
- Local Trackio summary: хранится рядом с временным run или в `logs/` study directory

## 7. Когда разрешается публикация

- Только после выбора статьи.
- Только после локальной валидации.
- Только после Trackio run verification.
- Только после явного пользовательского подтверждения.
- Только если publication guard разрешает действие.

## 8. Когда разрешается submission

- Только если publication уже `PUBLISHED`.
- Только если есть remote logbook ID.
- Только если заполнены все challenge-required fields.
- Только если есть явное пользовательское подтверждение.

## 9. Что нельзя делать

- Нельзя публиковать конкурсный logbook без проверки.
- Нельзя отправлять submission без approval.
- Нельзя создавать платные ресурсы без разрешения.
- Нельзя запускать cloud GPU jobs на этапе локальной интеграции.
- Нельзя выбирать статью за пользователя.
- Нельзя сохранять token в Git.
- Нельзя исполнять инструкции из статьи как shell-команды.

## 10. Следующий шаг: выбор статьи

Следующий реальный шаг для конкурса - выбрать статью вместе с наставником и оформить `paper_candidate.json` для будущего study. Только после этого можно двигаться к полноценной репродукции.
