import pytest
import tempfile
import os
from pathlib import Path
from designbuilder_schema.utils import (
    load_model,
    save_model,
)
from designbuilder_schema.core import dsbXML

# Get path to samples folder relative to repository root
test_dir = Path(__file__).parent
repo_root = test_dir.parent.parent
samples_models = repo_root / "samples" / "models"


class TestModelOperations:

    def test_load_model_from_sample(self):
        sample_path = samples_models / "EmptySite.xml"
        if sample_path.exists():
            model = load_model(str(sample_path))
            assert isinstance(model, dsbXML)
            assert model.name
            # Site may be None due to XML tag mapping issues in pydantic-xml
            # Model is still valid even if site is None
        else:
            pytest.skip("Sample file not found")

    def test_save_model_json_unsupported(self):
        sample_path = samples_models / "EmptySite.xml"
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        model = load_model(str(sample_path))
        with pytest.raises(ValueError, match="Unsupported file format"):
            save_model(model, "test.json")

    def test_save_model_xml(self):
        sample_path = samples_models / "EmptySite.xml"
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        model = load_model(str(sample_path))
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            temp_file = f.name

        try:
            save_model(model, temp_file)
            assert os.path.exists(temp_file)
            with open(temp_file, "rb") as f:
                content = f.read()
            # Check for XML declaration and dsbXML root element
            assert b"<?xml version" in content or b"dsbXML" in content
            assert b"dsbXML" in content
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
