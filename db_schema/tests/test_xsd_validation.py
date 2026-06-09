import os
from pathlib import Path

import pytest
from lxml import etree


def get_filepaths(directory, extension=".xml"):
    filepaths = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                filepaths.append(os.path.join(root, file))
    return filepaths


# Get paths relative to repository root
test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
xsd_path = repo_root / "DesignBuilder.xsd"
models_folder = repo_root / "samples" / "models_dhvac"

xml_filepaths = get_filepaths(str(models_folder), extension=".xml")


@pytest.fixture(scope="module")
def xsd_schema():
    schema_doc = etree.parse(str(xsd_path))
    return etree.XMLSchema(schema_doc)


@pytest.mark.parametrize("filepath", xml_filepaths)
def test_xml_validates_against_xsd(filepath, xsd_schema):
    doc = etree.parse(filepath)
    is_valid = xsd_schema.validate(doc)

    if not is_valid:
        errors = "\n".join(
            f"  Line {error.line}: {error.message}" for error in xsd_schema.error_log
        )
        pytest.fail(f"XML validation failed for {Path(filepath).name}:\n{errors}")
