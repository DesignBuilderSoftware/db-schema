import os
from pathlib import Path

import pytest

from dsbxml.utils import load_model


def get_filepaths(directory, extension=".xml"):
    filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                filepaths.append(os.path.join(root, file))
    return filepaths


# Get model filepaths from the per-version sample folders, except the
# detailed HVAC sets (2026.1.0.004, 2025.1.0.095), which other tests load
test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
model_folders = [
    repo_root / "samples" / version
    for version in ("7.3.1.003", "8.0.0.057", "8.0.0.058", "2026.1.0.013")
]

xml_filepaths = [
    path for folder in model_folders for path in get_filepaths(str(folder), extension=".xml")
]


@pytest.mark.parametrize("filepath", xml_filepaths)
def test_validate_dsbxml(filepath):
    assert load_model(filepath)


"""
json_filepaths = get_filepaths(models_folder, extension=".json")

@pytest.mark.parametrize("filepath", json_filepaths)
def test_validate_dsbjson(filepath):
    assert load_model(filepath)"""
