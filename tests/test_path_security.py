from pathlib import Path

import pytest

from ai_research_lab.paths import ensure_within_root, validate_study_name


def test_rejects_traversal_and_invalid_names(tmp_path: Path) -> None:
    root = tmp_path / "research"
    root.mkdir(parents=True, exist_ok=True)

    with pytest.raises(ValueError):
        validate_study_name("../evil")

    with pytest.raises(ValueError):
        ensure_within_root(root, root.parent / "outside")

