from pathlib import Path

import pytest
from lxml import etree

import dsbxml
from dsbxml.errors import ModelValidationError


def _load_sample_root():
    path = Path("samples/models/Tutorial Model.xml")
    if not path.exists():
        pytest.skip("Sample file not found")
    return etree.parse(str(path)).getroot()


class TestValidationErrorContext:
    def test_surface_error_includes_building_zone_context(self):
        root = _load_sample_root()
        surface = root.find(
            "Site/Buildings/Building/BuildingBlocks/BuildingBlock/"
            "Zones/Zone/Body/Surfaces/Surface"
        )
        surface.set("area", "not-a-number")

        with pytest.raises(ModelValidationError) as exc_info:
            dsbxml.dsbXML.from_xml(etree.tostring(root))

        message = str(exc_info.value)
        assert "Building '" in message
        assert "Zone handle=" in message
        assert "Surface[0]" in message
        assert "area" in message

    def test_error_without_known_container_falls_back_to_path(self):
        root = _load_sample_root()
        dsb = root  # dsbXML root element itself
        dsb.set("date", "not-a-date")

        with pytest.raises(ModelValidationError) as exc_info:
            dsbxml.dsbXML.from_xml(etree.tostring(root))

        message = str(exc_info.value)
        assert "date" in message
