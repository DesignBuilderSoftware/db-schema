"""Run every Python example in USAGE_GUIDE.md, so the guide cannot go stale.

The blocks run in order in one namespace, as a reader would run them, with
a real sample model copied to building.xml in a temporary directory.
"""

import re
import shutil
from pathlib import Path

import pytest

repo_root = Path(__file__).parent.parent.parent
guide = repo_root / "USAGE_GUIDE.md"
sample = repo_root / "samples" / "2026.1.0.013" / "Shoebox261.xml"

_PYTHON_BLOCK = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)


def test_guide_has_examples():
    assert len(_PYTHON_BLOCK.findall(guide.read_text(encoding="utf-8"))) >= 10


def test_usage_guide_examples_run(tmp_path, monkeypatch):
    if not sample.exists():
        pytest.skip(f"{sample} not found")
    from dsbxml.utils import clear_model_cache

    shutil.copy(sample, tmp_path / "building.xml")
    monkeypatch.chdir(tmp_path)
    clear_model_cache()
    namespace: dict = {}
    try:
        for number, block in enumerate(_PYTHON_BLOCK.findall(guide.read_text("utf-8")), 1):
            try:
                exec(compile(block, f"USAGE_GUIDE.md block {number}", "exec"), namespace)
            except Exception as exc:  # pragma: no cover - reported to the reader
                pytest.fail(f"USAGE_GUIDE.md python block {number} failed: {exc!r}\n{block}")
    finally:
        clear_model_cache()
