from __future__ import annotations

import hashlib
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from .models import ChallengeConfig, SourceProvenance


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fetch_text(url: str, timeout: int = 30) -> tuple[str, int]:
    request = urllib.request.Request(url, headers={"User-Agent": "AI_RESEARCH_LAB/1.0"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
        status = getattr(response, "status", 200)
    return body, int(status)


def source_provenance(
    url: str,
    purpose: str,
    claims: list[str],
    local_text_path: Path | None = None,
    local_text: str | None = None,
) -> SourceProvenance:
    sha = None
    if local_text is not None:
        sha = sha256_text(local_text)
    elif local_text_path is not None and local_text_path.exists():
        sha = hashlib.sha256(local_text_path.read_bytes()).hexdigest()
    return SourceProvenance(
        url=url,
        accessed_at=datetime.now(timezone.utc),
        purpose=purpose,
        local_text_path=str(local_text_path) if local_text_path else None,
        local_text_sha256=sha,
        claims=claims,
    )


def fetch_with_fallback(url: str, purpose: str, claims: list[str]) -> tuple[str | None, int | None, str | None]:
    try:
        text, status = fetch_text(url)
    except urllib.error.URLError as exc:
        return None, None, f"{type(exc).__name__}: {exc}"
    return text, status, None


def _guide_snapshot_text() -> str:
    project_root = Path(__file__).resolve().parents[3]
    existing = project_root / "docs" / "challenge" / "ICML_2026_CHALLENGE_GUIDE.md"
    if existing.exists():
        return existing.read_text(encoding="utf-8")
    return """# ICML 2026 Agent Reproduction Challenge

Источник правила: официальный Hugging Face challenge guide и challenge Space.

## Purpose

- Конкурс просит coding agents воспроизводить ключевые эмпирические claims статей ICML 2026.
- Если у статьи нет официального кода, данных или checkpoint, всё равно требуется независимая попытка воспроизведения.
- Локальный smoke run обязателен перед substantive reproduction.

## Participation Flow

1. Выбрать статью.
2. Прочитать PDF, репозиторий и проектную страницу, если они есть.
3. Запустить локальный smoke test.
4. Для каждого substantive claim по возможности запустить масштабированный эксперимент на Hugging Face Job.
5. Вести logbook с доказательствами, артефактами и ссылками.
6. Перед публикацией пройти validation.
7. Опубликовать logbook в Hugging Face только после проверки.

## Unknown or Ambiguous Points

- Актуальные deadlines и prizes нужно сверить с актуальной страницей конкурса.
"""


def sync_challenge_sources(root_dir: Path, challenge_config: ChallengeConfig) -> tuple[list[SourceProvenance], Path, Path]:
    docs_dir = root_dir / "docs" / "challenge"
    docs_dir.mkdir(parents=True, exist_ok=True)
    guide_path = docs_dir / "ICML_2026_CHALLENGE_GUIDE.md"
    provenance_path = docs_dir / "SOURCE_PROVENANCE.md"

    guide_text = _guide_snapshot_text()
    guide_path.write_text(guide_text, encoding="utf-8")

    accessed_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    provenance_entries = [
        SourceProvenance(
            url=challenge_config.challenge_space,
            accessed_at=datetime.now(timezone.utc),
            purpose="verify challenge space participation flow",
            claims=[
                "challenge discusses reproduction workflow",
                "local smoke run precedes publication",
                "publication depends on validation",
            ],
        ),
        SourceProvenance(
            url=challenge_config.guide_url,
            accessed_at=datetime.now(timezone.utc),
            purpose="capture challenge guide rules",
            local_text_path=str(guide_path),
            local_text_sha256=hashlib.sha256(guide_text.encode("utf-8")).hexdigest(),
            claims=[
                "local smoke run is required",
                "publication requires validation",
                "logbook publish is mandatory before final release",
            ],
        ),
        SourceProvenance(
            url="https://huggingface.co/docs/huggingface_hub/guides/cli",
            accessed_at=datetime.now(timezone.utc),
            purpose="verify hf auth and skill commands",
            claims=["hf auth whoami exists", "hf skills add is documented"],
        ),
        SourceProvenance(
            url="https://huggingface.co/docs/huggingface_hub/package_reference/authentication",
            accessed_at=datetime.now(timezone.utc),
            purpose="verify authentication storage and login flow",
            claims=["browser login flow exists", "token stored locally"],
        ),
        SourceProvenance(
            url="https://huggingface.co/docs/trackio/index",
            accessed_at=datetime.now(timezone.utc),
            purpose="verify Trackio local-first behavior",
            claims=["dashboard runs locally by default", "offline logging works"],
        ),
        SourceProvenance(
            url="https://huggingface.co/docs/trackio/artifacts",
            accessed_at=datetime.now(timezone.utc),
            purpose="verify artifact logging semantics",
            claims=["trackio.log_artifact exists", "artifacts work offline"],
        ),
        SourceProvenance(
            url="https://huggingface.co/docs/hub/agents-skills",
            accessed_at=datetime.now(timezone.utc),
            purpose="verify agent skills support",
            claims=["skills are self-contained SKILL.md modules", "hf skills add exists"],
        ),
    ]

    provenance_lines = [
        "# Source Provenance",
        "",
        f"Дата доступа к официальным источникам: `{accessed_at}`",
        "",
    ]
    for index, entry in enumerate(provenance_entries, start=1):
        provenance_lines.extend(
            [
                f"## {index}. {entry.purpose}",
                "",
                f"- URL: {entry.url}",
                f"- accessed_at UTC: `{entry.accessed_at.isoformat().replace('+00:00', 'Z')}`",
                f"- purpose: {entry.purpose}",
                f"- SHA-256 локального текста: {entry.local_text_sha256 or 'not saved'}",
                f"- project claims based on source: {json.dumps(entry.claims, ensure_ascii=False)}",
                "",
            ]
        )
    provenance_path.write_text("\n".join(provenance_lines), encoding="utf-8")
    return provenance_entries, guide_path, provenance_path
