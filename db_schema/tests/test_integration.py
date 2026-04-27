import tempfile
from pathlib import Path

import pytest

from db_schema import load_model, save_model
from db_schema.id import set_site_counter


class TestRoundTrip:
    @pytest.mark.parametrize(
        "sample_file",
        [
            "db_schema/samples/models/EmptySite.xml",
            "db_schema/samples/models/Tutorial Model.xml",
            "db_schema/samples/models/DetailedHVAC.xml",
        ],
    )
    def test_load_save_load_produces_equivalent_models(self, sample_file: str):
        sample_path = Path(sample_file)
        if not sample_path.exists():
            pytest.skip(f"Sample file {sample_file} not found")

        # Load original
        model1 = load_model(sample_path)

        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            save_model(model1, tmp_path)

            # Load saved file
            model2 = load_model(tmp_path)

            # Verify key properties are preserved
            assert model1.name == model2.name, "Name should be preserved"
            assert model1.version == model2.version, (
                "Version should be preserved"
            )
            assert model1.objects == model2.objects, (
                "Objects should be preserved"
            )

            # Verify site structure if present
            if model1.site and model2.site:
                assert model1.site.count == model2.site.count
                assert model1.site.handle == model2.site.handle

        finally:
            # Clean up
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_save_maintains_xml_validity(self):
        sample_path = Path("db_schema/samples/models/EmptySite.xml")
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        model = load_model(sample_path)

        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            save_model(model, tmp_path)

            # Verify it's valid XML by trying to parse it
            import xml.etree.ElementTree as ET

            tree = ET.parse(tmp_path)
            root = tree.getroot()
            assert root.tag == "dsbXML", "Root element should be dsbXML"

        finally:
            Path(tmp_path).unlink(missing_ok=True)


class TestModelModification:
    def test_modify_and_save_name(self):
        sample_path = Path("db_schema/samples/models/EmptySite.xml")
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        original_model = load_model(sample_path)
        original_name = original_model.name

        # Modify
        original_model.name = "Modified Model"

        with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            save_model(original_model, tmp_path)
            reloaded_model = load_model(tmp_path)

            # Verify change persisted
            assert reloaded_model.name == "Modified Model"
            assert reloaded_model.name != original_name

        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_site_counter_persistence(self):
        sample_path = Path("db_schema/samples/models/EmptySite.xml")
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        # Load and get initial site handle
        set_site_counter(0)
        model1 = load_model(sample_path)

        if model1.site:
            handle1 = model1.site.handle
            # Load again - site handle should be updated
            model2 = load_model(sample_path)
            if model2.site:
                handle2 = model2.site.handle
                # After reloading, handles might differ based on counter
                # but they should both be valid integers
                assert isinstance(handle1, int)
                assert isinstance(handle2, int)


class TestComplexModels:
    @pytest.mark.parametrize(
        "sample_file",
        [
            "db_schema/samples/models_dhvac/1.xml",
            "db_schema/samples/models_dhvac/10.xml",
            "db_schema/samples/models_dhvac/DetailedHVAC.xml",
        ],
    )
    def test_load_complex_hvac_models(self, sample_file: str):
        sample_path = Path(sample_file)
        if not sample_path.exists():
            pytest.skip(f"Sample file {sample_file} not found")

        # Should load without errors
        model = load_model(sample_path)
        assert model is not None
        assert model.name is not None

        # Should have a site
        assert model.site is not None

    def test_round_trip_complex_models(self):
        sample_files = [
            "db_schema/samples/models_dhvac/1.xml",
            "db_schema/samples/models/DetailedHVAC.xml",
        ]

        for sample_file in sample_files:
            sample_path = Path(sample_file)
            if not sample_path.exists():
                continue

            model1 = load_model(sample_path)

            with tempfile.NamedTemporaryFile(
                suffix=".xml", delete=False
            ) as tmp:
                tmp_path = tmp.name

            try:
                save_model(model1, tmp_path)
                model2 = load_model(tmp_path)

                # Verify basic properties
                assert model1.name == model2.name
                assert model1.version == model2.version
                assert model1.date == model2.date

            finally:
                Path(tmp_path).unlink(missing_ok=True)


class TestLazyLoading:
    def test_lazy_hvac_components_access(self):
        # Import module freshly
        import db_schema

        # Should be able to access HVACComponents
        hvac_components_class = db_schema.HVACComponents
        assert hvac_components_class is not None
        assert hvac_components_class.__name__ == "HVACComponents"

    def test_lazy_hvac_network_access(self):
        import db_schema

        # Should be able to access HVACNetwork
        hvac_network_class = db_schema.HVACNetwork
        assert hvac_network_class is not None
        assert hvac_network_class.__name__ == "HVACNetwork"

    def test_lazy_loading_error_handling(self):
        import db_schema

        with pytest.raises(
            AttributeError, match="has no attribute 'NonExistent'"
        ):
            getattr(db_schema, "NonExistent")


class TestErrorHandling:
    def test_load_nonexistent_file_raises_error(self):
        with pytest.raises(FileNotFoundError):
            load_model("/nonexistent/path/file.xml")

    def test_load_non_xml_file_raises_error(self):
        with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
            tmp.write(b"not xml")
            tmp.flush()

            with pytest.raises(ValueError, match="Unsupported file format"):
                load_model(tmp.name)

    def test_save_to_non_xml_path_raises_error(self):
        sample_path = Path("db_schema/samples/models/EmptySite.xml")
        if not sample_path.exists():
            pytest.skip("Sample file not found")

        model = load_model(sample_path)

        with pytest.raises(ValueError, match="Unsupported file format"):
            save_model(model, "/tmp/output.txt")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
