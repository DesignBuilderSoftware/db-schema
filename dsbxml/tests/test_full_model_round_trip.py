"""A whole model must be identical after load -> save -> reload.

The HVAC-specific tests live in test_hvac_roundtrip_completeness.py; this one
compares the complete model, so data lost or changed anywhere (geometry,
attributes, tables, HVAC) is caught.
"""

import re
from pathlib import Path

import pytest

from dsbxml import dsbXML
from dsbxml.utils import load_model

repo_root = Path(__file__).parent.parent.parent
# Whole models are grouped into one folder per DesignBuilder version
# (samples/2026.1.0.004/ ...); other folders such as samples/fragments/ hold
# partial XML that is not a dsbXML model.
_VERSION_FOLDER = re.compile(r"\d+(\.\d+)+")
sample_files = sorted(
    path
    for path in (repo_root / "samples").glob("*/*.xml")
    if _VERSION_FOLDER.fullmatch(path.parent.name)
)


@pytest.mark.parametrize("filepath", sample_files, ids=lambda p: p.name)
def test_model_is_unchanged_after_save_and_reload(filepath):
    original = load_model(filepath, use_cache=False)
    xml = original.to_xml()
    reloaded = dsbXML.from_xml(xml)
    assert reloaded.model_dump() == original.model_dump()
