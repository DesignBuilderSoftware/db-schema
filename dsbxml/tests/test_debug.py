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


# Get model filepaths from folder
# Use Path to find samples folder relative to repository root
test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
debug_folder = repo_root / "samples" / "debug"
xml_filepaths = get_filepaths(str(debug_folder), extension=".xml")


@pytest.mark.skipif(not xml_filepaths, reason="No debug XML files in samples/debug/")
@pytest.mark.parametrize("filepath", xml_filepaths or ["placeholder"])
def test_validate_dbxml(filepath):
    if filepath == "placeholder":
        pytest.skip("No debug XML files in samples/debug/")
    assert load_model(filepath)
