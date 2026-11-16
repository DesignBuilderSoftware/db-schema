"""Run every Python example in the user guide, so the guide cannot go stale.

The guide is the docs_src/guide/ pages. Their blocks run in the order the
pages appear in mkdocs.yml's nav, in one namespace, as a reader would run
them, with a real sample model copied to building.xml in a temporary
directory.
"""

import re
import shutil
from pathlib import Path

import pytest

repo_root = Path(__file__).parent.parent.parent
guide_dir = repo_root / "docs_src" / "guide"
mkdocs_yml = repo_root / "mkdocs.yml"
sample = repo_root / "samples" / "2026.1.0.013" / "Shoebox261.xml"

_PYTHON_BLOCK = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)
_NAV_PAGE = re.compile(r"^\s*- [^:\n]+: (guide/[\w-]+\.md)\s*$", re.MULTILINE)


def _pages_in_nav_order() -> list[Path]:
    return [
        repo_root / "docs_src" / page
        for page in _NAV_PAGE.findall(mkdocs_yml.read_text(encoding="utf-8"))
    ]


def test_every_guide_page_is_in_the_nav():
    assert set(_pages_in_nav_order()) == set(guide_dir.glob("*.md"))


def test_guide_has_examples():
    blocks = [
        block
        for page in _pages_in_nav_order()
        for block in _PYTHON_BLOCK.findall(page.read_text(encoding="utf-8"))
    ]
    assert len(blocks) >= 10


def test_usage_guide_examples_run(tmp_path, monkeypatch):
    if not sample.exists():
        pytest.skip(f"{sample} not found")
    from dsbxml.utils import clear_model_cache

    pages = _pages_in_nav_order()
    shutil.copy(sample, tmp_path / "building.xml")
    monkeypatch.chdir(tmp_path)
    clear_model_cache()
    namespace: dict = {}
    try:
        for page in pages:
            name = f"docs_src/guide/{page.name}"
            blocks = _PYTHON_BLOCK.findall(page.read_text(encoding="utf-8"))
            for number, block in enumerate(blocks, 1):
                try:
                    exec(compile(block, f"{name} block {number}", "exec"), namespace)
                except Exception as exc:  # pragma: no cover - reported to the reader
                    pytest.fail(f"{name} python block {number} failed: {exc!r}\n{block}")
    finally:
        clear_model_cache()
